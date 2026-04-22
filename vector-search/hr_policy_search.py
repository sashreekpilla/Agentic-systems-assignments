#python version -- v3.14.2
#py -m pip install chromadb
#py -m pip install sentence-transformers
#py -m hr_policy_search.py

import chromadb
from sentence_transformers import SentenceTransformer

#create a persistent chroma client with path "./hr_chroma_store"
client = chromadb.PersistentClient(path="./hr_chroma_store")

#Load model for embedding
model = SentenceTransformer('all-MiniLM-L6-v2')


#create records for hr policies.
records = [
     {
        "id": "doc1",
        "text": "Separate, paid mental health days in addition to sick leave",
        "metadata": {"category": "leave", "version": "1"}
    },
    {
        "id": "doc2",
        "text": "Provides 24/7 medical advisor access, unlimited doctor consultations, and annual health checkups",
        "metadata": {"category": "benefit", "version": "2"}
    },
    {
        "id": "doc3",
        "text": "Mandatory compliance for 26 weeks of paid leave for female employees",
        "metadata": {"category": "leave", "version": "1"}
    },
    {
        "id": "doc4",
        "text": "a zero-tolerance policy for sexual harassment",
        "metadata": {"category": "conduct", "version": "3"}
    },
    {
        "id": "doc5",
        "text": "mandatory annual POSH training and an Internal Complaints Committee (ICC) for compliance",
        "metadata": {"category": "conduct", "version": "2"}
    }

]


#extracting each component from all the records.
doc_id= [record["id"] for record in records]
doc_text= [record["text"] for record in records]
doc_metadata= [record["metadata"] for record in records]

doc_embeddings= model.encode(doc_text, convert_to_numpy=True).tolist()

collection = client.get_or_create_collection(
    name="hr_policy_vector_db",
    embedding_function=None
)

#the document details along with the embeddings are inserted or updated in vectordb
collection.upsert(
    ids= doc_id,
    documents= doc_text,
    metadatas= doc_metadata,
    embeddings= doc_embeddings
)

print("Number of records in collection", collection.count())
print ("Records in the collection",collection.peek())

#user query to make the search on basis of
user_query= "My colleagues keep irritationg me"

user_query_embedding= model.encode(user_query, convert_to_numpy=True).tolist()

result= collection.query(
    query_embeddings= user_query_embedding,
    n_results=3
)

print("first query result",result)

#second user query
user_query_2="I dont feel very well, can i take a day off"

user_query_embedding_2= model.encode(user_query_2,convert_to_numpy=True).tolist()

result2= collection.query(
    query_embeddings= user_query_embedding_2,
    n_results=2,
    where= {"category":"leave"}
)

print("second query result",result2)


#new document in the collection
#adding new record instead of changing/updating the already existing document.
new_record= {
        "id": "doc6",
        "text": "reimbursement for home setup and guidelines for core working hours to ensure productivity",
        "metadata": {"category": "benefit", "version": "3"}
    }

new_record_embedding= model.encode(new_record["text"],convert_to_numpy=True).tolist()

collection.upsert(
    ids= [new_record["id"]],
    documents=[new_record["text"]],
    metadatas=[new_record["metadata"]],
    embeddings= new_record_embedding
)

print("Number of records in collection", collection.count())
print ("Records in the collection",collection.peek())

#third user query

user_query_3="what are being provided for me to function at a high rate"

user_query_embedding_3= model.encode(user_query_3,convert_to_numpy=True).tolist()

result3= collection.query(
    query_embeddings= user_query_embedding_3,
    n_results=3,
    where={"category":"benefit"}
)


print("third query result",result3)