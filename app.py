import streamlit as st
import base64, os, time
from module.document_processor import process_documents
from module.retriever import get_retriever
from module.generator import get_answer

# -------------------- LOGO ENCODING --------------------
def get_base64_image(image_path):
    """Encode an image to base64 for embedding"""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

LOGO_PATH = "assets/no_text.png"
LOGO_BASE64 = get_base64_image(LOGO_PATH)
ICON_PATH = "assets/logo.png"
ICON_BASE64 = get_base64_image(ICON_PATH)

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="DocuMind",
    page_icon=LOGO_PATH,
    layout="wide"
)

# -------------------- GLOBAL STYLE --------------------
st.markdown("""
<style>
header[data-testid="stHeader"] {display: none;}

.stApp {
    background: #F7F1E8;
    color: #1A1A1A;
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2px !important;
    max-width: 950px;
    margin: 2px;
}

/* ---- HEADINGS ---- */
h1, h2 {
    color: #2B2B2B !important;
    font-weight: 800 !important;
    text-align: center !important;
}
h3, h4 {
    color: #2B2B2B !important;
    font-weight: 700 !important;
    text-align: left !important;
}

/* ---- PARAGRAPHS ---- */
p { color: #3a3a3a !important; }

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: #1A1A1A;
    color: #F7F1E8;
    padding-top: 15px;
}
[data-testid="stSidebar"] h2 {
    color: #F7F1E8 !important;
    text-align: center !important;
}

/* ---- FILE UPLOAD BUTTON ---- */
section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] div div div div button {
    background-color: #F7F1E8 !important;
    color: #1A1A1A !important;
    border: 1px solid #F7F1E8 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 6px 16px !important;
    transition: all 0.25s ease-in-out !important;
}
section[data-testid="stFileUploader"] div[data-testid="stFileUploaderDropzone"] div div div div button:hover {
    background-color: #F7F1E8 !important;
    color: black !important;
    border: 1px solid white !important;
}

/* ---- SIDEBAR BUTTONS ---- */
[data-testid="stSidebar"] div.stButton > button {
    all: unset !important;
    display: inline-block !important;
    background-color: #F7F1E8 !important;
    color: #1A1A1A !important;
    padding: 0.5em 1.2em !important;
    border-radius: 10px !important;
    border: 1px solid #F7F1E8 !important;
    text-align: center !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    cursor: pointer !important;
    transition: all 0.25s ease-in-out !important;
}
[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: gray !important;
    color: #F7F1E8 !important;
    border: 1px solid #1A1A1A !important;
}

/* ---- CHAT INPUT ---- */
[data-testid="stChatInput"] textarea {
    border: 2px solid #1A1A1A !important;
    border-radius: 10px !important;
    background: white !important;
    color: #1A1A1A !important;
    font-size: 16px !important;
    padding: 0.6em 1em !important;
}
[data-testid="stChatInput"] button {
    background: #1A1A1A !important;
    color: white !important;
    border-radius: 8px !important;
    margin-bottom: 10px;
}
[data-testid="stChatInput"] button:hover {
    background: #1A1A1A !important;
    color: white !important;
}

/* ---- CHAT MESSAGES ---- */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] pre,
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] ol {
    text-align: left !important;
    line-height: 1.6 !important;
    color: #1A1A1A !important;
    font-size: 16px !important;
    margin-left: 8px !important;
}

/* ---- GLOBAL ALIGNMENT FIX ---- */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] pre,
[data-testid="stMarkdownContainer"] code,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    text-align: left !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------- NAVBAR --------------------
def render_navbar():
    pages = ["home", "about", "developer", "documentation"]
    labels = ["Home", "About", "Developer", "Documentation"]

    if "page" not in st.session_state:
        st.session_state.page = "home"

    st.markdown("""
    <style>
    .nav-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        position: absolute;
        top: 1px;
        left: 0;
        right: 0;
        z-index: 9999;
        border-bottom: 1px solid black !important;
    }
    div[data-testid="stVerticalBlock"] button {
        background: none !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 17px !important;
        color: #1A1A1A !important;
        cursor: pointer !important;
        padding: 0px 3px !important;
    }
    div[data-testid="stVerticalBlock"] button:hover {
        color: #F382C6 !important;
    }
    div[data-testid="stVerticalBlock"].active button {
        color: #F382C6 !important;
        border-bottom: 1px solid #F382C6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    cols = st.columns(len(pages))
    for i, page in enumerate(pages):
        active = (st.session_state.page == page)
        with cols[i]:
            container_class = "active" if active else ""
            st.markdown(f'<div class="{container_class}">', unsafe_allow_html=True)
            if st.button(labels[i], key=f"nav_{page}") or st.session_state.page == page:
                st.session_state.page = page
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

render_navbar()
page = st.session_state.page

# -------------------- SIDEBAR (ONLY ON HOME) --------------------
if page == "home":
    if ICON_BASE64:
        st.sidebar.markdown(
            f"""
            <div style='text-align:center; margin-bottom:15px;'>
                <img src='data:image/png;base64,{ICON_BASE64}' alt='DocuMind Logo' width='120'>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.sidebar.markdown("<h2 style='color:#F7F1E8;text-align:center;'>Upload Documents Here</h2>", unsafe_allow_html=True)
    uploaded_files = st.sidebar.file_uploader("", type=["pdf", "txt"], accept_multiple_files=True)

    if st.sidebar.button("Reset Chat"):
        st.session_state.chat_history = []
        msg = st.empty()
        msg.markdown("<p style='text-align:center;'>Chat has been reset</p>", unsafe_allow_html=True)
        time.sleep(2)
        msg.empty()
else:
    uploaded_files = None

# -------------------- SESSION STATE --------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- PAGE LOGIC --------------------
if page == "home":
    st.title("DocuMind - Your RAG-Based Chatbot")
    st.markdown(
        "<div style='text-align:center; font-size:18px; color:#3a3a3a;'>Chat intelligently with your documents using LLM-powered retrieval and reasoning.</div>",
        unsafe_allow_html=True
    )

    if uploaded_files and st.session_state.vectorstore is None:
        with st.spinner("Processing your document..."):
            vectorstore = process_documents(uploaded_files)
            retriever = get_retriever(vectorstore)
            st.session_state.vectorstore = vectorstore
            st.session_state.retriever = retriever
        placeholder = st.empty()
        placeholder.markdown("<p style='text-align:center;'>Documents processed successfully</p>", unsafe_allow_html=True)
        time.sleep(2)
        placeholder.empty()

    user_query = st.chat_input("Type your question here...")
    if user_query:
        retriever = st.session_state.retriever
        if not retriever:
            bot_reply = "Please upload and process a document first."
        else:
            with st.spinner("Thinking..."):
                bot_reply = get_answer(user_query, retriever, st.session_state)
        st.session_state.chat_history.append({"user": user_query, "bot": bot_reply})

    for chat in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(chat["user"])
        with st.chat_message("assistant"):
            st.write(chat["bot"])

# -------------------- ABOUT --------------------
elif page == "about":
    st.title("About DocuMind")
    st.markdown("""
    <div style='text-align:left; font-size:16px; color:#1A1A1A; line-height:1.8; padding:20px 40px;'>
    <h3>What is DocuMind?</h3>
    <p><b>DocuMind</b> is an intelligent Retrieval-Augmented chatbot that helps you interact with your documents conversationally.
    Instead of manually searching for information, DocuMind lets you ask natural questions and get grounded, context-aware answers.</p>

    <h3>How It Works</h3>
    <p>It uses <b>Retrieval-Augmented Generation (RAG)</b>, combining the reasoning ability of large language models with document retrieval.
    Relevant content is fetched, then summarized or explained via a language model.</p>

    <h3>The RAG Story</h3>
    <p>Developed by <b>Facebook AI Research (FAIR)</b> in 2020, RAG introduced a retriever–generator hybrid to eliminate AI hallucinations.
    <b>DocuMind</b> extends this idea locally using <b>LangChain</b>, <b>FAISS</b>, and <b>Ollama</b> within a <b>Streamlit</b> interface.</p>

    <h3>Why Choose DocuMind?</h3>
    <ul>
        <li><b>Factual Accuracy</b> – Answers are based on your documents.</li>
        <li><b>Privacy</b> – Everything runs locally with Ollama & Docker.</li>
        <li><b>Instant Learning</b> – Each upload expands your knowledge base.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------- DEVELOPER --------------------
elif page == "developer":
    st.title("Meet the Developers")
    st.markdown("""
    <div style='text-align:left; font-size:16px; color:#1A1A1A; line-height:1.8; padding:20px 40px;'>
    <p><b>DocuMind</b> was built through a collaborative effort uniting AI design, robust backend engineering, and clear documentation.</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    with cols[0]:
        st.markdown("""
        <div style='text-align:left; background:#fff; padding:15px; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.1);'>
        <h3>Suhani Verma</h3>
        <p>Developed and implemented the <b>RAG pipeline</b> — document processing, embeddings, retrieval, and response generation using <b>LangChain</b>, <b>FAISS</b>, and <b>Ollama</b>.</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown("""
        <div style='text-align:left; background:#fff; padding:15px; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.1);'>
        <h3>Arya Jha</h3>
        <p>Designed the <b>Streamlit interface</b> to make user-friendly frontend and handled <b>Docker containerization</b>, ensuring smooth deployment and UI experience.</p>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown("""
        <div style='text-align:left; background:#fff; padding:15px; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.1);'>
        <h3>Ria Kumari</h3>
        <p>Created the <b>project documentation, User Manual to help in DocuMind setup </b> and structured the <b>GitHub repository</b>, ensuring clarity and organization.</p>
        </div>
        """, unsafe_allow_html=True)

# -------------------- DOCUMENTATION --------------------
elif page == "documentation":
    st.title("Documentation")
    st.markdown("""
    <div style='text-align:left; font-size:16px; color:#1A1A1A; line-height:1.8; padding:20px 40px;'>
    
    <h3 style='color:#1A1A1A;'>Setup Guide</h3>
    <p><b>DocuMind</b> is powered by <b>Ollama</b>, <b>FAISS</b>, and <b>LangChain</b>, all within a streamlined <b>Streamlit</b> interface.
    Using <b>Docker</b>, the project runs locally with all dependencies packaged automatically.</p>

    <h4 style='color:#1A1A1A;'>1. Prerequisites</h4>
    <ul>
        <li>Install <a href='https://www.docker.com/get-started' target='_blank'>Docker</a></li>
        <li>Install <a href='https://ollama.ai' target='_blank'>Ollama</a></li>
        <li>Ensure an internet connection for initial dependency and model downloads</li>
    </ul>

    <h4 style='color:#1A1A1A;'>2. Clone the Repository</h4>
    <pre><code class='language-bash'>
    git clone https://github.com/TheSuhaniVerma/RAG_Chatbot.git
    cd RAG_Chatbot
    </code></pre>

    <h4 style='color:#1A1A1A;'>3. Build the Docker Image</h4>
    <p>All dependencies (LangChain, FAISS, Sentence-Transformers, Streamlit, etc.) are listed in
    <code>requirements.txt</code>. Docker will install them automatically during build.</p>
    <pre><code class='language-bash'>
    docker build -t documind .
    </code></pre>

    <h4 style='color:#1A1A1A;'>4. Run the Application</h4>
    <pre><code class='language-bash'>
    docker run -p 8501:8501 documind
    </code></pre>
    <p>Once running, open your browser at:</p>
    <pre><code class='language-bash'>
    http://localhost:8501
    </code></pre>

    <h4 style='color:#1A1A1A;'>5. How DocuMind Works</h4>
    <ul>
        <li><b>Document Upload:</b> PDFs are uploaded and parsed via PyPDF & LangChain loaders.</li>
        <li><b>Embeddings:</b> Text chunks are vectorized using Sentence-Transformers.</li>
        <li><b>Storage:</b> Embeddings are saved locally in a <b>FAISS</b> index.</li>
        <li><b>Retrieval:</b> Relevant chunks are fetched by semantic similarity.</li>
        <li><b>Response Generation:</b> <b>Ollama</b> uses the context to produce grounded, precise answers.</li>
    </ul>

    <h4 style='color:#1A1A1A;'>6. Project Structure</h4>
    <pre><code class='language-bash'>
    RAG_Chatbot/
    ├── app.py                 # Main Streamlit interface
    ├── module/
    │   ├── document_processor.py   # PDF loader + embedding
    │   ├── retriever.py            # FAISS retrieval logic
    │   ├── generator.py            # Query response via Ollama
    │   ├── utilities.py            # Helper tools
    ├── requirements.txt       # Dependency list
    ├── Dockerfile             # Docker configuration
    ├── assets/                # Logos and icons
    └── vectorstore_data/      # FAISS database
    </code></pre>

    <h4 style='color:#1A1A1A;'>7. Usage</h4>
    <ol>
        <li>Run via Docker or use <code>streamlit run app.py</code>.</li>
        <li>Upload documents in the sidebar.</li>
        <li>Wait for processing confirmation.</li>
        <li>Ask your question and receive intelligent responses.</li>
    </ol>

    <h4 style='color:#1A1A1A;'>8. Technologies Used</h4>
    <ul>
        <li><b>LangChain</b> – Retrieval orchestration</li>
        <li><b>FAISS</b> – Vector search</li>
        <li><b>Ollama</b> – LLM inference</li>
        <li><b>Sentence-Transformers</b> – Embeddings</li>
        <li><b>Streamlit</b> – User interface</li>
        <li><b>Docker</b> – Deployment</li>
    </ul>

    <h4 style='color:#1A1A1A;'>9. References</h4>
    <ul>
        <li><a href='https://www.langchain.com' target='_blank'>LangChain Docs</a></li>
        <li><a href='https://github.com/facebookresearch/faiss' target='_blank'>FAISS GitHub</a></li>
        <li><a href='https://ollama.ai' target='_blank'>Ollama</a></li>
        <li><a href='https://docs.streamlit.io' target='_blank'>Streamlit Docs</a></li>
        <li><a href='https://github.com/TheSuhaniVerma/RAG_Chatbot' target='_blank'>Project Repository</a></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)