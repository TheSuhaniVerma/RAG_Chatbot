from langchain_community.vectorstores import FAISS
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_community.llms import Ollama


def get_retriever(vectorstore):
    """
    Returns a retriever with semantic re-ranking (contextual compression)
    so only the most relevant chunks are passed to the LLM.
    """
    base_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    llm = Ollama(model="llama3.2", temperature=0)
    compressor = LLMChainExtractor.from_llm(llm)

    return ContextualCompressionRetriever(
        base_retriever=base_retriever,
        base_compressor=compressor
    )
