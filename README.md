

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