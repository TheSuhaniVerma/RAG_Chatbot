import os
import streamlit as st
import pickle
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from pypdf import PdfReader
from pypdf.errors import PdfReadError

# -------------------- PATHS --------------------
VECTORSTORE_PATH = "vectorstore_data/vectorstore.faiss"
EMBEDDINGS_PATH = "vectorstore_data/embeddings.pkl"



class CustomEmbeddings:
    """Wrapper around OllamaEmbeddings for FAISS compatibility."""
    def __init__(self, model_name="nomic-embed-text"):
        self.embedder = OllamaEmbeddings(model=model_name)

    def embed_documents(self, texts):
        return self.embedder.embed_documents(texts)

    def embed_query(self, query):
        return self.embedder.embed_query(query)

    def __call__(self, text):
        if isinstance(text, list):
            return self.embed_documents(text)
        return self.embed_query(text)
    
# -------------------- MAIN DOCUMENT PROCESSOR --------------------
def process_documents(uploaded_files):
    os.makedirs("vectorstore_data", exist_ok=True)
    os.makedirs("temp_files", exist_ok=True)

    # If vectorstore exists → load it directly (no need to reload embeddings)
    if os.path.exists(VECTORSTORE_PATH):
        st.info("Loading existing vectorstore from disk...")
        vectorstore = FAISS.load_local(
            "vectorstore_data",
            CustomEmbeddings(),  # recreate embedding class
            allow_dangerous_deserialization=True
        )
        return vectorstore

    all_docs = []

    with st.spinner("Extracting and processing uploaded documents..."):
        for uploaded_file in uploaded_files:
            temp_path = os.path.join("temp_files", uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            ext = os.path.splitext(uploaded_file.name)[1].lower()

            try:
                if ext == ".pdf":
                    with open(temp_path, "rb") as f:
                        reader = PdfReader(f, strict=False)
                        if len(reader.pages) == 0:
                            raise ValueError("Empty or unreadable PDF")
                    loader = PyPDFLoader(temp_path)

                elif ext == ".txt":
                    loader = TextLoader(temp_path, encoding="utf-8")

                else:
                    st.warning(f"⚠ Unsupported file type: {uploaded_file.name}")
                    continue

                docs = loader.load()
                all_docs.extend(docs)

            except Exception as e:
                st.warning(f"⚠ Skipped {uploaded_file.name}: {e}")
                continue

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300,
        length_function=len
    )
    split_docs = text_splitter.split_documents(all_docs)

    embeddings = CustomEmbeddings()

    vectorstore = FAISS.from_documents(split_docs, embeddings)
    vectorstore.save_local("vectorstore_data")

    return vectorstore