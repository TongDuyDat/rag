from langchain.tools import BaseTool
from langchain_qdrant import QdrantVectorStore

from vector_database.index_qdrant import asearch_qdrant, search_qdrant

class RAG_search(BaseTool):
    name:str = "rag_search"
    description:str = """
        You use this tool when you want to find information related to research.
    """
    __vector_store: QdrantVectorStore = None
    def add_vector_store(self, vector_store: QdrantVectorStore):
        self.__vector_store = vector_store
        
    def _run(self, question:str):
        documents = search_qdrant(question, self.__vector_store, top_k = 5)
        context = ""
        if not documents:
            return 
        for i, doc in  enumerate(documents):
            text = doc.page_content.replace("\n", " ")
            metadata = " ".join([f"{k}: {v}" for k, v in doc.metadata.items()])
            # metadata = ""
            context += f"Context:\n context {i}: {text}\nmetadata: {metadata}\n"
        return context
    async def _arun(self, question:str):
        documents = await asearch_qdrant(question, self.__vector_store, top_k = 5)
        context = ""
        if not documents:
            return 
        for i, doc in  enumerate(documents):
            text = doc.page_content.replace("\n", " ")
            metadata = " ".join([f"{k}: {v}" for k, v in doc.metadata.items()])
            # metadata = ""
            context += f"Context:\n context {i}: {text}\nmetadata: {metadata}\n"
        return context
