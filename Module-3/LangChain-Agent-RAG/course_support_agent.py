from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_core.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

raw_documents= [
    Document(
        page_content="""
        Refund policy: Full refund within 7 days of enrollment if no live class attended.
        Partial refund within 30 days per program rules
        """,
        metadata= {"source":"refund_policy.md"}

    ),
    Document(
        page_content="""
        Attendance policy: Minimum 75% attendance is required for certification and placement support.
        """,
        metadata= {"source":"attendance_policy.md"}

    ),
    Document(
        page_content="""
        Batch change policy: Students may request one batch change per cohort. Missing more than three classes without approved leave may delay batch change.        """,
        metadata= {"source":"batch_change_policy.md"}

    ),
]


text_splitter= RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=60
)

split_documents = text_splitter.split_documents(raw_documents)

embeddings= OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma.from_documents(
    documents = split_documents,
    embedding = embeddings,
    collection_name = "helpdesk_policy_docs"
)

retriever = vector_store.as_retriever(
    search_type = "similarity"
    search_kwargs = {"k":2}
)

course_policy_tool = create_retriever_tool(
    retriever= retriever,
    name = "course_policy_tool"
    description= (
        "Searches official course policy documents for refund rules, attendance requirements,"
        "batch change policy, project submission deadlines, placement eligibility, and extension rules."
        "Use this tool only for questions about course policies or learner program rules."

    )
)

@tool
def get_ticket_status (ticket_id: str):
    """
    Returns support ticket status for a given ticket id.
    Use this tool when the user asks about ticket status, refund request status,
    support request status, escalation status, or ticket tracking.
    """

    FAKE_TICKET_DATABASE = {
        "TKT-2001": "Refund request under review. Expected response in 2 working days.",
        "TKT-2002": "Batch change request approved. New batch starts next Monday.",
    }

    ticket_status = FAKE_TICKET_DATABASE.get (ticket_id)

    if not ticket_status :
        return f"Ticket status not found for the given ticket id: {ticket_id}"
    return ticket_status

tools =[get_ticket_status, course_policy_tool]

llm = ChatOpenAI(
    model= "gpt-5.2",
    temperature= 0
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful course assistant.

            You have access to two tools:

            1. course_policy_search:
            Use this for questions about refund policy, atendance rules, batch change,
            project submission, extension, certificate, and career services eligibilty.

            2. get_ticket_status:
            Use this when the user gives a ticket id or asks about support ticket status.

            Rules:
            - If the question is abouit official course policy, use course_policy_search.
            - If the question is about ticket status, use get_ticket_status.
            - If the question needs both policy and ticket status, use both tools.
            - If the question is outside the course suppport, politely say that you can only help with course policies and support tickets.
            - Do not invent policy details.
            - When answering from documents, mention that the answer is based on  the available policy documents.
            - Keep answers clear and student friendly.
            """
        ),
        
        MessagesPlaceholder(variable_name="chat_history", optional= True),

        ("human","{input}"),

        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = create_tool_calling_agent(
    llm = llm,
    tools = tools,
    prompt = prompt
)

agent_executor = AgentExecutor(
    agent= agent,
    tools = tools,
    verbose= True,
    max_iterations= 3
)

chat_history = []

def ask_agent(user_query: str) -> str:
    """
    Sends the user query to the agent and stores conversation history in chat history manually.
    """

    response = agent_executor.invoke(
        {
            "input": user_query,
            "chat_history": chat_history
        }
    )

    answer = response["output"]

    chat_history.append (HumanMessage(content= user_query))
    chat_history.append (AIMessage(content= answer))

    return answer

def main ():
    DemoA="What is the refund policy in the first week?"
    print ("Demo A user input:", DemoA)
    output1= ask_agent(DemoA)
    print ("output of Demo A:", output1)
    print ("=\n"*100)

    DemoB="What is the status of ticket TKT-2001?"
    print ("Demo B user input:", DemoB)
    output2= ask_agent(DemoB)
    print ("output of Demo B:", output2)
    print ("=\n"*100)

    DemoC1="My support ticket is TKT-2002."
    print ("Demo C1 user input:", DemoC1)
    output3= ask_agent(DemoC1)
    print ("output of Demo C1:", output3)
    print ("=\n"*100)

    DemoC2="What is the status of it?"    
    print ("Demo C2 user input:", DemoC2)
    output4= ask_agent(DemoC2)
    print ("output of Demo C2:", output4)
    print ("=\n"*100)

    DemoD="Who won IPL 2025?"
    print ("Demo D user input:", DemoD)
    output5= ask_agent(DemoD)
    print ("output of Demo D:", output5)



