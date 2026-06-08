from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.tools import tool
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

ORDERS_DB ={
    "ORD101":{
        "status": "shipped",
        "city": "Delhi",
        "amount": 2500,
        "delivery_days": 2
    },
    "ORD102":{
        "status":"cancelled",
        "city":"Bangalore",
        "amount":4000,
        "delivery_days":0
    },
    "ORD103":{
        "status":"delivered",
        "city":"Mumbai",
        "amount":1500,
        "delivery_days":0
    }
}

@tool
def get_order_status(order_id:str) -> str:
    order= ORDERS_DB.get(order_id)
    if not order:
        return f"Order with order_id: {order_id} not found"
    return f"Order status: {order["status"]}"


tools= [get_order_status]

llm= ChatOpenAI(
    model="gpt-5.2",
    temperature= 0
)

prompt= ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a helpful customer support agent.
Rules:
- If the user gives an order id, remember it for this conversation.
- If the user asks a follow up like "track it" or "where is it", use the order id from the chat history.
- Use tools when order status is required.
- If no order id is available, politely ask the user for the order id.
        """
    ),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    (
        "human",
        "{input}"
    ),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

agent = create_tool_calling_agent(
    prompt= prompt,
    llm= llm,
    tools= tools
)

agent_executor= AgentExecutor(
    agent= agent,
    tools= tools,
    verbose= True
)

chat_history=[]

def ask_agent(user_input:str) -> str:
    response= agent_executor.invoke(
        {
            "input":user_input,
            "chat_history": chat_history
        }
    )

    chat_history.append (HumanMessage(content=user_input))
    chat_history.append (AIMessage(content=response["output"]))

    return response["output"]

print ("Turn-1")
user_input= "Hi, my order ID is ORD102"
print("user_input:", user_input)
print ("AI response:", ask_agent(user_input))

print("="*100)

print ("Turn-2")
user_input="What is the status of it?"
print ("user_input:",user_input)
print ("AI response:", ask_agent(user_input))

print("="* 100)

print(len(chat_history))