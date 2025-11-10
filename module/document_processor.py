import os
import streamlit as st
import pickle
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


VECTORSTORE_PATH = "vectorstore_data/vectorstore.faiss"
EMBEDDINGS_PATH = "vectorstore_data/embeddings.pkl"


def process_documents(uploaded_files):
    """
    Load, split, embed, and store uploaded PDF documents in a FAISS vectorstore.
    If an existing vectorstore is found, it is reused for faster startup.
    """
    os.makedirs("vectorstore_data", exist_ok=True)

    # Step 0: Load existing vectorstore if available
    if os.path.exists(VECTORSTORE_PATH) and os.path.exists(EMBEDDINGS_PATH):
        st.info("📚 Loading existing vectorstore from disk...")
        with open(EMBEDDINGS_PATH, "rb") as f:
            embeddings = pickle.load(f)
        vectorstore = FAISS.load_local("vectorstore_data", embeddings, allow_dangerous_deserialization=True)
        return vectorstore

    all_docs = []
    with st.spinner("⏳ Extracting and processing uploaded documents..."):
        os.makedirs("temp_files", exist_ok=True)

        for uploaded_file in uploaded_files:
            temp_path = os.path.join("temp_files", uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            loader = PyPDFLoader(temp_path)
            docs = loader.load()
            all_docs.extend(docs)

        # Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        split_docs = text_splitter.split_documents(all_docs)

        # Create embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )

        # Create vectorstore
        vectorstore = FAISS.from_documents(split_docs, embeddings)

        # Save both vectorstore and embeddings for reuse
        vectorstore.save_local("vectorstore_data")
        with open(EMBEDDINGS_PATH, "wb") as f:
            pickle.dump(embeddings, f)

    st.success("✅ Document processing complete and saved for reuse!")
    return vectorstore
