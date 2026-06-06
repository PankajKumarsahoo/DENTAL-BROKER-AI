import json
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ==========================
# CONFIG
# ==========================

DATA_FOLDER = "categorized_data"
CHROMA_DB_DIR = "chroma_db"

# ==========================
# LOAD DOCUMENTS
# ==========================

def load_documents():
    documents = []

    for file in os.listdir(DATA_FOLDER):

        if not file.endswith(".json"):
            continue

        filepath = os.path.join(DATA_FOLDER, file)

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            if not isinstance(data, list):
                continue

            category = file.replace(".json", "")

            for item in data:

                url = item.get("url", "")
                title = item.get("title", "")
                content = item.get("content", "")

                if not content.strip():
                    continue

                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "url": url,
                            "title": title,
                            "category": category
                        }
                    )
                )

        except Exception as e:
            print(f"Error reading {file}: {e}")

    return documents


# ==========================
# SPLIT DOCUMENTS
# ==========================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=150
    )

    return splitter.split_documents(documents)


# ==========================
# CREATE CHROMA DB
# ==========================

def create_vector_db():

    print("Loading documents...")

    docs = load_documents()

    print(f"Documents loaded: {len(docs)}")

    chunks = split_documents(docs)

    print(f"Chunks created: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )

    vectordb.persist()

    print("\nVector Database Created Successfully!")
    print(f"Saved to: {CHROMA_DB_DIR}")


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":
    create_vector_db()