from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import Ollama

def get_answer(question, retriever, st_session):
    """
    Generate contextual answers using Ollama + RAG + Memory.
    Keeps previous conversation context for continuity.
    """

    if retriever is None:
        return "⚠️ Please upload and process a document first."

    # Initialize LLM
    llm = Ollama(model="llama3.2")

    # Initialize memory in session state if not already
    if "memory" not in st_session:
        st_session.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    # Create conversational chain with memory
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=st_session.memory,
        return_source_documents=False
    )

    # Run query
    result = qa_chain.invoke({"question": question})
    base_answer = result.get("answer", "").strip()

    if not base_answer:
        return "No relevant information found in the uploaded documents."

    # Paraphrase for polish
    paraphrase_prompt = f"""
    Reword the following answer naturally while preserving meaning and correctness.
    Avoid phrases like "Here's a paraphrase" or commentary.

    Original Answer:
    {base_answer}

    Paraphrased Answer:
    """
    paraphrased = llm.invoke(paraphrase_prompt).strip()
    return paraphrased
