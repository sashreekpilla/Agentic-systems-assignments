import os
import re
from pathlib import Path

import chromadb
from openai import OpenAI
from pypdf import PdfReader


# 1. CONFIGURATION

PDF_FOLDER = "policy_documents"
CHROMA_PATH = "campus_policy_chroma_db"
COLLECTION_NAME = "campus_policies"

EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = 'gpt-4.1-mini'

client = OpenAI()


# 1.1 INNER POLCIY TYPE

def infer_policy_type(filename):
    name = filename.lower()

    if "hostel" in name:
        return "hostel"
    elif "refund" in name:
        return "refund"
    elif 'library' in name:
        return "library"
    else:
        return "general"

# 1.2 LOAD ALL PDF FILES

def load_all_pdfs(folder_path):
    documents = []

    pdf_files = Path(folder_path).glob("*.pdf")

    for pdf_file in pdf_files:
        reader = PdfReader(str(pdf_file))

        policy_type = infer_policy_type(pdf_file.name)

        for page_number, page in enumerate(reader.pages):
            text = page.extract_text()

            if text:
                documents.append({
                    # EXTRACTED TEXT
                    "text": text,
                    # METADATA
                    "source": pdf_file.name,
                    "page": page_number + 1,
                    "policy_type": policy_type
                })

        return documents


# 1.3 CLEAN TEXT
def clean_text(text):
    # \s+ matches one or more whitespace characters
    text = re.sub(r"\s+", " ", text)
    # ...
    return text.strip()

# 2 SPLIT INTO CHUNKS
def split_text_into_chunks(text, chunk_size = 150, overlap = 20):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words)

        chunks.append(chunk_text)

        start += (chunk_size - overlap)

    return chunks

# 3. GENERATE EMBEDDINGS
def generate_embeddings(text):

    response = client.embeddings.create(model=EMBED_MODEL, input=text)

    embedding = response.data[0].embedding

    return embedding

# 4. BUILD CHROMADB (Vector Store)
def build_knowledge_base():

    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
    documents = load_all_pdfs(PDF_FOLDER)

    doc_id = 0

    for doc in documents:
        cleaned_text = clean_text(doc['text'])
        chunks = split_text_into_chunks(cleaned_text)

        for chunk in chunks:
            embedding = generate_embeddings(chunk)
            collection.add(
                ids = [str(doc_id)],
                document = [chunk],
                embeddings = [embedding],
                metadata=[{
                    "source": doc['source'],
                    "page" : doc['page'],
                    "policy_type" : doc['policy_type']
                }]
            )

            doc_id += 1

    print("Knowlege base created successfully!!!")

    return collection

# 5. RETREIVER
def retrieve_relevant_chunks(query, collection, top_k = 3):
    query_embedding = generate_embeddings(query)

    results = collection.query(query_embeddings = [query_embedding],
                               n_results = top_k)

    return results

# 6. BUILD PROMPT
def build_prompt(query, retrieved_chunks):

    context = "\n\n".join(retrieve_relevant_chunks)

    prompt = f"""
    You are a campus policy assistant. Answer ONLY from the retrieved policy context.

    If the answer is not available in the context, say: "I don't have that information."

    Keep the response simple and student-friendly.

    Retrieved Policy Context:
    {context}

    Student Question:
    {query}
    """

    return prompt

# 7. GENERATE FINAL ANSWER
def answer_question(query, collection):

    results = retrieve_relevant_chunks(query, collection)

    retrieved_chunks = results['documents'][0]

    prompt = build_prompt(query, retrieved_chunks)

    response = client.chat.completions.create(
        model = CHAT_MODEL,
        message = [
            {
                "role": "system",
                "content" : "You are a helpful campus polciy assistant."
            },
            {
                "role" : "user",
                "content" : prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return answer

# ------------------------------------------------------------
## MAIN BLOCK
# ------------------------------------------------------------

if __name__ == "__main__":

    # 1. Build Knowledge Base
    collection = build_knowledge_base()

    # 2. Test Student Queries
    test_queries = [
        "Can I get a refund after dropping a course?",
        "What is the deadline for returning a library book?",
        "Are hostel visitors allowed on weekends?"
    ]

    print("\n=================== CAMPUS POLICY RAG =======================\n")

    # 3. Generate Answers
    for query in test_queries:
        print(f"Question: {query}")

        answer = answer_question(query, collection)

        print(f"Answer: {answer}")

        print("-"*50)





