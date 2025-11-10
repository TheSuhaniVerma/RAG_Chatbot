import streamlit as st
from module.document_processor import process_documents
from module.retriever import get_retriever
from module.generator import get_answer
from module.utilities import clear_temp_folder

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="RAG Chatbot", page_icon="💬", layout="wide")

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #fff8f0, #ffe9e3, #ffd7d0);
    background-attachment: fixed;
    color: #2a2a2a;
    font-family: 'Inter', sans-serif;
}

/* HEADINGS */
h1, h2, h3 {
    color: #444444 !important;
    font-weight: 800 !important;
    text-align: center;
}
p {
    color: #4a4a4a !important;
    text-align: center;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #083b3b, #0d4d4d);
    color: #f2f2f2;
    border-right: 2px solid rgba(255,255,255,0.1);
}

/* SIDEBAR HEADER */
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #f9f9f9 !important;
}

/* FILE UPLOADER */
section[data-testid="stFileUploader"] > div > div {
    background: rgba(255,255,255,0.08);
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.15);
}
section[data-testid="stFileUploader"] > div > div:hover {
    background: rgba(255,255,255,0.15);
    border-color: #b3fff0;
}

/* BUTTONS */
div.stButton > button {
    background: linear-gradient(90deg, #74d4b3, #ffbfa9);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6em 1.4em;
    font-weight: 600;
    box-shadow: 0 4px 8px rgba(100, 150, 150, 0.3);
    transition: 0.3s ease;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #62c6a5, #ffa98f);
    box-shadow: 0 6px 14px rgba(100, 150, 150, 0.4);
    transform: translateY(-2px);
}

/* CLEAR BUTTON IN SIDEBAR */
[data-testid="stSidebar"] div.stButton > button {
    background: linear-gradient(90deg, #ff8c8c, #ffb199);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    box-shadow: 0 3px 6px rgba(255, 120, 150, 0.3);
}
[data-testid="stSidebar"] div.stButton > button:hover {
    background: linear-gradient(90deg, #ff6b6b, #ff9a85);
}

/* INPUT BOX */
input[type="text"] {
    border: 2px solid #f5c2b0 !important;
    border-radius: 10px !important;
    background: rgba(255, 255, 255, 0.8) !important;
    color: #222 !important;
    font-size: 16px !important;
    padding: 0.6em 1em !important;
    box-shadow: 0 2px 8px rgba(255, 180, 160, 0.15);
}

/* ALERT / SUCCESS BOXES */
.stSuccess {
    background-color: #f0fffa;
    border-left: 5px solid #79d2b4;
    color: #084a3d;
    border-radius: 8px;
}
.stWarning {
    background-color: #fff6e0;
    border-left: 5px solid #ffb400;
    color: #5a4500;
    border-radius: 8px;
}

/* CENTER CONTAINER WIDTH */
.block-container {
    max-width: 950px;
    margin: auto;
}

/* FILE UPLOAD SUCCESS TEXT */
.stSidebar .stSuccess {
    background-color: rgba(255,255,255,0.1);
    border-left: 4px solid #9ef0d1;
    color: #d0fff0;
}
</style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.title("💬 RAG-Based Chatbot for Document Q&A")
st.markdown("Upload your documents and ask intelligent questions — powered by *Retrieval-Augmented Generation* 🔍✨")

# -------------------- SIDEBAR --------------------
st.sidebar.header("📂 Upload Documents")
uploaded_files = st.sidebar.file_uploader(
    "Upload PDF or TXT files", type=["pdf", "txt"], accept_multiple_files=True
)

# -------------------- SESSION STATE INITIALIZATION --------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- DOCUMENT PROCESSING --------------------
if uploaded_files and st.session_state.vectorstore is None:
    st.sidebar.info("⚙️ Processing uploaded documents (only once)...")
    vectorstore = process_documents(uploaded_files)
    retriever = get_retriever(vectorstore)

    st.session_state.vectorstore = vectorstore
    st.session_state.retriever = retriever
    st.sidebar.success("✅ Documents processed and stored for this session.")
elif st.session_state.vectorstore is not None:
    st.sidebar.success("📚 Using existing stored documents.")
else:
    st.sidebar.info("📤 Upload documents to begin.")

# -------------------- CLEAR STORED DATA --------------------
if st.sidebar.button("🧹 Clear All Documents"):
    clear_temp_folder("vectorstore_data")
    st.session_state.vectorstore = None
    st.session_state.retriever = None
    st.session_state.chat_history = []
    st.sidebar.success("🗑️ Cleared all stored data successfully ✅")

# -------------------- CHAT AREA --------------------
st.subheader("💭 Ask a question about your documents:")
user_query = st.chat_input("Type your question here...")

if user_query:
    retriever = st.session_state.retriever
    if not retriever:
        st.warning("⚠ Please upload and process a document first.")
    else:
        with st.spinner("⏳ Generating your intelligent answer..."):
            answer = get_answer(user_query, retriever, st.session_state)
            st.session_state.chat_history.append({"user": user_query, "bot": answer})

# -------------------- DISPLAY CHAT HISTORY --------------------
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant"):
        st.write(chat["bot"])
