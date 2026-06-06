from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DB_DIR = "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectordb = Chroma(
    persist_directory=CHROMA_DB_DIR,
    embedding_function=embeddings
)

retriever = vectordb.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 10,
        "fetch_k": 20
    }
)

def search_documents(query):

    docs = retriever.invoke(query)

    print("\nRESULTS:\n")

    for i, doc in enumerate(docs, 1):

        print("=" * 60)
        print(f"Result {i}")

        print("\nTitle:")
        print(doc.metadata.get("title", ""))

        print("\nURL:")
        print(doc.metadata.get("url", ""))

        print("\nContent:")
        print(doc.page_content[:500])

if __name__ == "__main__":

    while True:

        q = input("\nAsk a question: ")

        if q.lower() == "exit":
            break

        search_documents(q)