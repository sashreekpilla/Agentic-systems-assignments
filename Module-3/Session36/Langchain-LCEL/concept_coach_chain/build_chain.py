from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

MODEL_NAME="qwen:1.8b"
OLLAMA_BASE_URL="http://localhost:11434"
API_PATH="http://localhost:11434/api/chat"


def build_chain():
    prompt= ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are a beginner-friendly programming instructor.

Rules:
- Explain the concept clearly.
- Use exactly 3 bullet points.
- Each bullet point should be short.
- Do not add an introduction.
- Do not add a conclusion.
                """

            ),
            (
                "human",
                "Explain {topic} using a simple analogy from {analogy_domain}"

            ),
        ]
    )

    llm= ChatOllama(
        model= MODEL_NAME,
        base_url= OLLAMA_BASE_URL,
        temperature= 1
    )

    parser = StrOutputParser()

    chain = prompt | llm | parser

    return chain

chain= build_chain()



