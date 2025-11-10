from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def get_retriever(vectorstore):
    """Return retriever from vectorstore."""
    if vectorstore is None:
        return None

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever
