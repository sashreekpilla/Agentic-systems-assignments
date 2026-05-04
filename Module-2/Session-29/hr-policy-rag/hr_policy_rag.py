from google import genai
from typing import List, Dict
import chromadb

# 1. Creating google client.
google_client= genai.Client() 

# 2. Embedding model and llm model global variables.
EMBEDDING_MODEL="gemini-embedding-2"
LLM_MODEL="gemini-2.0-flash"

# 3. HR-Policy Documents.
HR_POLICY_DOCUMENTS = [
    {
        "id": "leave_policy_1",
        "text": (
            "Employees are entitled to 18 working days of Earned Leave per calendar year, "
            "accrued at a rate of 1.5 days per month of service."
            "Earned Leave is credited monthly but can only be availed after completion of the 3-month probation period."
            "10 days of paid Sick Leave per calendar year."
            "For absences exceeding 2 consecutive days, a medical certificate from a registered practitioner must be submitted."
        ),
        "metadata": {
            "category": "leave",
            "source": "leave_policy"
        }
    },
    {
        "id": "work_from_home_policy_1",
        "text": (
            "Employees must have completed their probation period."
            "Must demonstrate consistent performance, low absenteeism, and "
            "possess the necessary IT infrastructure (stable internet, private workspace)."
        ),
        "metadata": {
            "category": "WFH",
            "source": "work_from_home_policy"
        }
    },
    {
        "id": "appraisal_policy_1",
        "text": (
            "Increments and bonuses are directly linked to the final rating."
            "Employees with a rating of 3 or higher are eligible for increments."
            "Employees with a 2 or 1 rating will be placed on a Performance Improvement Plan (PIP) "
            "and are ineligible for increments until performance improves."
        ),
        "metadata": {
            "category": "appraisal",
            "source": "appraisal_policy"
        }
    },
    {
        "id": "code_of_conduct_policy_1",
        "text": (
            "Discrimination based on gender, religion, caste, disability, or age is strictly prohibited."
            "The company has a zero-tolerance policy toward sexual harassment (POSH) and bullying."
            "Employees must maintain punctuality, appropriate attire, and respectful communication with colleagues and clients."
        ),
        "metadata": {
            "category": "conduct",
            "source": "conduct_policy"
        }
    }
]

# 4. create embeddings function.
def create_embeddings(texts: List[str])-> List[List[float]]:
    embeddings =[]
    for t in texts:
        responses=google_client.models.embed_content(
            model= EMBEDDING_MODEL,
            contents=t
        )
        embeddings.append(responses.embeddings[0].values)
    return embeddings

# 5. Setup Vector Database.
def setup_vector_database():
    chroma_client= chromadb.PersistentClient(path="./hr_policy_document_db")
    collection= chroma_client.get_or_create_collection(
        name="hr_policy_collection",
        embedding_function=None
    )
    return collection

# 6. Store and Index HR policy documents
def index_hr_documents(collection):
    ids= [policy["id"]for policy in HR_POLICY_DOCUMENTS]
    documents= [policy["text"] for policy in HR_POLICY_DOCUMENTS]
    metadatas= [policy["metadata"] for policy in HR_POLICY_DOCUMENTS]

    embeddings= create_embeddings(documents)

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

# 7. extract context for the system prompt
def retrieve_hr_content(collection, query, top_k: int=3):
    query_embedding= create_embeddings([query])[0]
    result= collection.query(
        query_embedding= [query_embedding],
        n_results= top_k
    )
    return result["documents"][0]

# 8. build a prompt for the LLM along with the context from the hr policy documents.
def build_grounded_prompt(query: str, chunks):
    context=""
    number_of_chunks= len(chunks)
    for index in range (0, number_of_chunks):
        document= chunks[index]
        context+= f"hr_policy_context:{index}|{document}\n"

    prompt = f"""
    You are a helpful HR Policy assistant for the company InnoTech Solutions.

    Answer the employee's question using ONLY the HR policy context provided below.

    Rules:
    1. Do not make up HR policy details.
    2. If the answer is not present in the context, say:
    "I do not have enough information in the provided HR policy documents."
    3. Mention important conditions or exceptions if they are present in the context.

    HR Policy Context:
    {context}

    Employee Question:
    {query}

    Final Answer:
    """
    return prompt


# 9. Generate response with the prompt, context using the user query
def generate_answer(query: str, chunks):
    prompt = build_grounded_prompt(query, chunks)
    response=google_client.models.generate_content(
        model= LLM_MODEL,
        contents= prompt
    )
    return response.text

# 10. Generate a response using the context (RAG)
def answer_with_rag(collection, query: str, top_k: int=3):
    chunks= retrieve_hr_content(collection,query,top_k)
    response= generate_answer(query, chunks)
    return response

#11. Generate a response using LLM model without the context
def generate_answer_without_retrieval(query: str):
    response= google_client.models.generate_content(
        model=LLM_MODEL,
        contents=query
    )
    return response.text

def main ():

    # These can be done once and don't need to create a embeddings of the policy every run.
    # Increases the number of tokens consumed.
    embeddings= create_embeddings(HR_POLICY_DOCUMENTS)
    hr_policy_collection= setup_vector_database()
    index_hr_documents(hr_policy_collection)

    # "How many days of annual leave am I entitled to per year?"
    # "Do I need manager approval before working from home?"
    # "When is the appraisal cycle conducted and how is the increment decided?"

    query = "How many days of annual leave am I entitled to per year?"
    response_with_rag= answer_with_rag(hr_policy_collection, query)
    print (f"Answer using context from policy documents,{response_with_rag}\n")

    response_without_rag= generate_answer_without_retrieval(query)
    print(f"Answer without using context from policy documents,{response_without_rag}\n")






