from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm= ChatOpenAI(
    model="gpt-5.2"
)

prompt= PromptTemplate.from_template(
    """
    explain {topic} to {audience} in {tone} tone.
    Requirements:
    -include one real-life analogy
    -stay within {limit} words
    """
)

output_parser= StrOutputParser()

chain = prompt | llm | output_parser

LESSON_BRIEFS= ({
    "topic": "SQL indexes",
    "audience":"beginners",
    "tone":"simple",
    "limit": 120
},
{
    "topic": "FastAPI dependency injection",
    "audience":"intermediate developers",
    "tone":"technical",
    "limit": 180
},
{
    "topic": "LangChain PromptTemplate",
    "audience":"product managers",
    "tone":"friendly",
    "limit": 100
})


def validate_brief(brief):
    for b in brief:
        if not (b["topic"] or b["audience"] or b["tone"]):
            raise ValueError("Missing information")
        if not str(b["limit"]).isdigit() :
            raise ValueError("limit must be a digit")
        
        response= chain.invoke(brief)

validate_brief(LESSON_BRIEFS)