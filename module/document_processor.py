import os
import streamlit as st
import pickle
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import torch

# -------------------- PATHS --------------------
VECTORSTORE_PATH = "vectorstore_data/vectorstore.faiss"
EMBEDDINGS_PATH = "vectorstore_data/embeddings.pkl"

# -------------------- CUSTOM EMBEDDINGS --------------------
class CustomEmbeddings:
    """Safe, CPU-only alternative to HuggingFaceEmbeddings."""
    def __init__(self, model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"):
        os.environ["TORCH_DISABLE_META_DEVICE"] = "1"
        torch.set_default_device("cpu")
        self.model = SentenceTransformer(model_name, device="cpu")

    def embed_documents(self, texts):
        return [self.model.encode(text, convert_to_numpy=True).tolist() for text in texts]

    def embed_query(self, query):
        return self.model.encode(query, convert_to_numpy=True).tolist()

    def __call__(self, text):
        if isinstance(text, list):
            return self.embed_documents(text)
        else:
            return self.embed_query(text)

# -------------------- MAIN DOCUMENT PROCESSOR --------------------
def process_documents(uploaded_files):
    """Load, split, embed, and store uploaded documents in a FAISS vectorstore."""
    os.makedirs("vectorstore_data", exist_ok=True)
    os.makedirs("temp_files", exist_ok=True)

    # Reuse existing vectorstore if available
    if os.path.exists(VECTORSTORE_PATH) and os.path.exists(EMBEDDINGS_PATH):
        st.info("Loading existing vectorstore from disk...")
        with open(EMBEDDINGS_PATH, "rb") as f:
            embeddings = pickle.load(f)
        vectorstore = FAISS.load_local(
            "vectorstore_data", embeddings, allow_dangerous_deserialization=True
        )
        return vectorstore

    all_docs = []
    with st.spinner("Extracting and processing uploaded documents..."):
        for uploaded_file in uploaded_files:
            temp_path = os.path.join("temp_files", uploaded_file.name)
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            file_ext = os.path.splitext(uploaded_file.name)[1].lower()

            try:
                if file_ext == ".pdf":
                    with open(temp_path, "rb") as f:
                        reader = PdfReader(f, strict=False)
                        if len(reader.pages) == 0:
                            raise ValueError("Empty or unreadable PDF")
                    loader = PyPDFLoader(temp_path)
                elif file_ext == ".txt":
                    loader = TextLoader(temp_path, encoding="utf-8")
                else:
                    st.warning(f"⚠️ Unsupported file type: {uploaded_file.name}")
                    continue

                docs = loader.load()
                all_docs.extend(docs)

            except (PdfReadError, ValueError, Exception) as e:
                st.warning(f"⚠️ Skipped {uploaded_file.name}: {e}")
                continue

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=300, length_function=len
    )
    split_docs = text_splitter.split_documents(all_docs)

    embeddings = CustomEmbeddings()
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    vectorstore.save_local("vectorstore_data")

    with open(EMBEDDINGS_PATH, "wb") as f:
        pickle.dump(embeddings, f)

    return vectorstore
