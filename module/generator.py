from langchain_community.llms import Ollama


def get_answer(user_query, retriever, session_state):
    # Step 1: Retrieve relevant docs
    docs = retriever.get_relevant_documents(user_query)

    if not docs:
        return "I couldn’t find any relevant information in the uploaded documents."

    # Step 2: Format context
    context = "\n\n".join(
        [f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)]
    )
    context = context.replace("\n", " ").replace("  ", " ")

    # Step 3: Construct prompt
    prompt = f"""
You are DocuMind — an intelligent assistant that answers based only on the provided documents.

Your task:
- Carefully read the context below.
- Use relevant information to answer clearly and concisely.
- If you don't find the direct answer to a question, then just give answer in the general context of the document that you've retrieved.
- Don't say the Document numbers in your answer.
- If you cannot find the answer, say "I couldn’t find that information in the uploaded documents."

Context:
{context}

Question:
{user_query}

Answer:
"""

    # Step 4: Generate answer
    llm = Ollama(model="llama3.2", temperature=0.3)
    answer = llm(prompt)

    return answer
