# RAG Chatbot (Ollama + ChromaDB)

This Streamlit app:
- Accepts a PDF upload (processed **once**),
- Builds embeddings and stores them in **ChromaDB**,
- Uses **Ollama** (local) to answer queries,
- Keeps conversation memory for follow-up questions.

# My Project

## Setup
1. Create a virtual environment  
   `python -m venv env`

2. Activate it  
   - Windows: `env\Scripts\activate`
   - Linux/Mac: `source env/bin/activate`

3. Install dependencies  
   `pip install -r requirements.txt`

4. Run the app  
   `python app.py`


