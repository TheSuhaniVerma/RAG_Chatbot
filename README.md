
<p align="center">
  <img src="assets/logo.png" alt="DocuMind Logo" width="170">
</p>

<h1 align="center">DocuMind – RAG-Based Local Document Assistant</h1>

<p align="center">
A lightweight, private, local Retrieval-Augmented Generation chatbot that answers questions from your PDF and TXT documents — powered by FAISS, LangChain, and Ollama.
</p>

---

## Features

- Upload PDFs or TXT files  
- Intelligent retrieval using **FAISS**  
- Embedding powered by **Ollama (nomic-embed-text)** – No PyTorch required  
- LLM responses with **Ollama llama3.2**  
- Local, fast, and private  
- Clean **Streamlit UI**  
- Fully containerized using **Docker**  

---

##  Project Structure



RAG_Chatbot/
├── app.py                     # Main Streamlit UI
├── module/
│   ├── document_processor.py  # Document loading, splitting, embeddings
│   ├── retriever.py           # Semantic retrieval + re-ranking
│   ├── generator.py           # Answer generation with Ollama
│   ├── utilities.py           # Helper utilities
├── assets/
│   └── logo.png               # Your DocuMind logo
├── Dockerfile                 # Docker configuration
├── requirements.txt           # Lightweight dependency list
└── README.md                  # Project documentation

`

---

##  Prerequisites

You must install:

- **Docker** → https://www.docker.com/get-started  
- **Ollama** → https://ollama.ai  

After installing Ollama, pull the required models:

bash
ollama pull nomic-embed-text
ollama pull llama3.2
`

---

##  Running DocuMind With a Single Command

From inside the project folder:

###  Build

bash
docker build -t documind .


###  Run the app

bash
docker run -p 8501:8501 documind


Open your browser at:


http://localhost:8501


---

##  How It Works

### 1️⃣ Document Upload

The user uploads one or multiple **PDF/TXT** files.

### 2️⃣ Preprocessing

Documents are:

* Loaded using PyPDFLoader / TextLoader
* Cleaned & validated
* Split into chunks with RecursiveCharacterTextSplitter

### 3️⃣ Embedding (Ollama)

Text chunks → **OllamaEmbeddings ("nomic-embed-text")**
✔ No PyTorch
✔ No Transformers
✔ Low memory + fast

### 4️⃣ Indexing

Chunks stored inside **FAISS** (local semantic vector search).

### 5️⃣ Retrieval

Best chunks are selected using:

* base_retriever (FAISS)
* contextual re-ranking (LLMChainExtractor + llama3.2)

### 6️⃣ Answer Generation

The final context is fed into **llama3.2**:

You get a grounded, non-hallucinated answer.

---

##  Example Prompt

Ask something like:


What does this document say about neural networks?


DocuMind will fetch relevant chunks and generate an answer.

---

##  Technologies Used

* **LangChain** – Retrieval + processing
* **FAISS** – Fast vector search
* **Ollama** – Local LLM + Embeddings
* **Streamlit** – User interface
* **Docker** – Containerized deployment

---

##  Contributors

###  Developers

* **Suhani Verma** – RAG pipeline, embeddings, retrieval, LLM generation
* **Arya Jha** – Interface design & Docker workflow
* **Ria Kumari** – Documentation & repository structure

---

##  License

This project is licensed under the **MIT License**.

---

##  If you like this project…

Consider giving the repo a **star** ⭐ on GitHub!


gitHub.com/TheSuhaniVerma/RAG_Chatbot
```

