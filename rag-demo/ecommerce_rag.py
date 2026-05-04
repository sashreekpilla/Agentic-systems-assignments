

# from openai import OpenAI
from google import genai
from typing import List, Dict
import chromadb

#1. creating client 
#this is for openai client
# openai_client= OpenAI() 

#this is for google client
google_client= genai.Client() 

#2. Defining global variables embedding and llm models

#the bottom embedding model and llm model are for openai
# EMBEDDING_MODEL= "text-embedding-3-small"
# LLM_MODEL= "gpt-5.4"

#the bottom embedding model and llm model are for gemini ai
EMBEDDING_MODEL="gemini-embedding-2"
LLM_MODEL="gemini-2.0-flash"

#3. Sample Policy documents
POLICY_DOCUMENTS = [
    {
        "id": "return_policy_1",
        "text": (
            "Customers can return eligible products within 30 days of delivery. "
            "Products must be unused, undamaged, and in original packaging. "
            "Digital products, opened personal care items, and perishable goods "
            "are not eligible for return."
        ),
        "metadata": {
            "category": "returns",
            "source": "return_policy"
        }
    },
    {
        "id": "refund_policy_1",
        "text": (
            "Refunds are processed after the returned product passes quality check. "
            "Refunds to cards, UPI, and net banking usually take 5 to 7 business days. "
            "COD refunds require bank details and may take 7 to 10 business days."
        ),
        "metadata": {
            "category": "refunds",
            "source": "refund_policy"
        }
    },
    {
        "id": "shipping_policy_1",
        "text": (
            "Standard shipping takes 3 to 5 business days. "
            "Express shipping takes 1 to 2 business days and may include additional charges. "
            "Orders above ₹999 are eligible for free standard shipping. "
            "Remote pin codes may take 5 to 8 business days."
        ),
        "metadata": {
            "category": "shipping",
            "source": "shipping_policy"
        }
    },
    {
        "id": "warranty_policy_1",
        "text": (
            "Electronics come with a 1-year manufacturer warranty. "
            "Warranty covers manufacturing defects only. "
            "Accidental damage, liquid damage, and physical breakage are not covered. "
            "Dead-on-arrival products must be reported within 7 days of delivery."
        ),
        "metadata": {
            "category": "warranty",
            "source": "warranty_policy"
        }
    },
    {
        "id": "cancellation_policy_1",
        "text": (
            "Customers can cancel an order before it is shipped. "
            "Once the order has been shipped, cancellation is not allowed. "
            "Customers may refuse delivery or request a return after delivery "
            "if the product is eligible under the return policy."
        ),
        "metadata": {
            "category": "cancellation",
            "source": "cancellation_policy"
        }
    }
]

#4. Create embeddings
def create_embeddings (text: List[str]) -> List[List[float]]:
    
    # the bottom code is to create embedding using openai client.
    # responses= openai_client.embeddings.create(
    #     model=EMBEDDING_MODEL,
    #     input = text
    # )


    # the bottom code is to create embeddings using google ai client.
    embeddings=[]
    ind = 0
    for t in text:
        responses= google_client.models.embed_content(
            model= EMBEDDING_MODEL,
            contents = t
        )
        embeddings.append(responses.embeddings[0].values) 
        # ind+=1
        # if (ind > 1):
        #     break


    # embeddings= [item.embedding for item in responses.data]

    # embeddings= responses.embeddings[0].values
    # embeddings = [item.values for item in responses.embeddings]

    return embeddings


#5. Setup VectorDB (chromaDB)
def setup_vector_db():
    chroma_client= chromadb.PersistentClient(path="./chroma_policy_document_db")

    collection= chroma_client.get_or_create_collection(
        name= "ecommerce_policy_collection",
        embedding_function= None
    )

    return collection


#6.Store policy document embeddings
def store_documents_in_vector_db(collection):
    ids= [document["id"] for document in POLICY_DOCUMENTS]
    documents= [document["text"] for document in POLICY_DOCUMENTS]
    metadatas= [document["metadata"] for document in POLICY_DOCUMENTS]

    embeddings= create_embeddings(documents)

    collection.upsert(
        ids=ids,
        metadatas=metadatas,
        documents=documents,
        embeddings=embeddings
    )



#7. Retriever component
def retrieve_policy_content(query:str, collection, top_k: int = 3):
    print("Reached to get embedding for query string")
    query_embedding = create_embeddings([query])[0]
    print("get embedding successfully: " , len(query_embedding))

    result= collection.query(
        query_embeddings=[query_embedding],
        n_results= top_k
    )
    print(result)
    print(len(result))
    print(len(result["documents"][0]))

    return result["documents"][0]

#8. Building prompt for LLM
def build_prompt(query:str, retreived_documents):
    context=""
    number_of_retrieved_documents= len(retreived_documents)
    for index in range (0, number_of_retrieved_documents):
        document= retreived_documents[index]

        context += f"Policy document {index}| {document}\n"
    
    prompt = """ Hi """
#   prompt = f"""
# You are a helpful customer support assistant for an e-commerce company.

# Answer the customer's question using ONLY the policy context provided below.

# Rules:
# 1. Do not make up policy details.
# 2. If the answer is not present in the context, say:
#    "I do not have enough information in the provided policy documents."
# 3. Keep the answer simple, clear, and customer-friendly.
# 4. Mention important conditions or exceptions if they are present in the context.

# Policy Context:
# {context}

# Customer Question:
# {query}

# Final Answer:
# """
    return prompt

#9. Generate final answer using the context
def generate_answer(query: str, retreived_documents):
    prompt= build_prompt(query, retreived_documents)

    # response=openai_client.responses.create(
    #     model= LLM_MODEL,
    #     input=prompt
    # )
    #return response.output_text

    response= google_client.models.generate_content(
        model= LLM_MODEL,
        contents= prompt
    )
    return response.text


#10. Resolve the query using RAG
def answer_with_rag(query: str, collection, top_k: int= 3):
    retreived_documents= retrieve_policy_content(query, collection, top_k)
    answer= generate_answer(query, retreived_documents)
    return answer


#11. Resolve the query without using RAG
def answer_without_rag(query: str):
    # response= openai_client.responses.create(
    #     model=LLM_MODEL,
    #     input= query
    # )
    # return response.output_text

    response= google_client.models.generate_content(
        model= LLM_MODEL,
        contents= query
    )
    return response.text


def main():

    print("entered main")
    # "RAG", "WO_RAG", "EMBED", "CHECK_COLL", "QUERY"
    Testing_Mode="QUERY"

    match Testing_Mode: 
        case "EMBED":
            print("in switch case")
            embeddings = create_embeddings(["Text","Book"])
            print(len(embeddings))
            # print(embeddings)

        case "CHECK_COLL":
            collection = setup_vector_db()
            print("Previous Size: " , collection.count())
            if(collection.count() == 0): 
                print ("entered if loop")
                store_documents_in_vector_db(collection)
                print(collection.count())

        case "QUERY":
            print ("in query switch case")
            collection = setup_vector_db()
            print("Previous Size: " , collection.count())
            user_query= "When will i get my refund?"

            norag_answer= answer_without_rag(user_query)
            print("Answer without RAG", norag_answer)

            rag_answer= answer_with_rag(user_query, collection)
            print("Answer with RAG", rag_answer)

main()
