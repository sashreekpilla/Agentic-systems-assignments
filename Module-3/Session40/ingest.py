from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, Textloader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import shutil

DATA_DIR= Path("documents")
CHROMA_DIR= Path("chroma_db")
COLLECTION_NAME= "hostel_policy_docs"

documents={
    "quiet_hours.md": """
# Quiet Hours Policy

Quiet hours are from 10:00 PM to 6:00 AM on all weekdays.
During quiet hours, loud music, group calls, and hallway gatherings are not allowed.
Violations may lead to a written warning.

""",
"guest_policy.md":"""
# Guest Policy

Day guests are allowed only between 9:00 AM and 8:00 PM.
Overnight guests require prior warden approval at least 24 hours in advance.
Maximum two guests per room at any time.

"""
}

for filename, content in documents.items():
    file_path= DATA_DIR/filename
    file_path.write_text(content.strip(), encoding="utf-8")


loader = DirectoryLoader(
    path=str(DATA_DIR),
    glob="**/*.md",
    loader_cls=Textloader,
    loader_kwargs={"encoding": "utf-8"}
)

docs = loader.load()

text_splitter= RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=60,
    add_start_index=True
)

chunks=text_splitter.split_documents(docs)

if CHROMA_DIR.exists():
    shutil.rmtree(CHROMA_DIR)

embeddings= OpenAIEmbeddings(model="text-embedding-3-small")

vector_store= Chroma(
    collection_name= COLLECTION_NAME,
    embedding_function= embeddings,
    persist_directory=str(CHROMA_DIR)
)

ids= vector_store.add_documents(documents=chunks)



