from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_chroma import Chroma
from pathlib import Path

CHROMA_DIR= Path("chroma_db")
COLLECTION_NAME="hostel_policy_docs"

llm= ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
embeddings= OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    collection_name= COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR)
)

retriever= vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k":2}
)

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful customer support assitant for a college hostel office.

Use only the retrieved context to answer the user's question.

Rules:
1. If the answer is present in the context, answer clearly.
2. If the answer is not present in the context, say "I dont know based on the provided documents"
3. Do not use outside knowledge.
4. Mention the source file name wherever possible.

<context>
{context}
</context>

Question:
{question}

Answer:
    """
)

rag_chain= (
    {
        "context": retriever,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

def main():
    q1= "What are the quiet hours on weekdays?"
    ans1 = rag_chain.invoke(q1)
    print (f"user query: {q1}")
    print (f"Assistant answer: {ans1}")

    q2= "What is the scholarship amount for hostel residents?"
    ans2 = rag_chain.invoke(q2)
    print (f"user query: {q2}")
    print (f"Assistant answer: {ans2}")
