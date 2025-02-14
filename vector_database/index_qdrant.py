# Standard library imports
import uuid
from typing import Any
from dotenv import load_dotenv
_ = load_dotenv()
# Vector store imports
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Langchain imports
from langchain_core.documents import Document
from langchain_qdrant.qdrant import QdrantVectorStore


def create_collection(
    collection_name: str, embedding_model: Any, vector_size: int = 768
) -> QdrantVectorStore:
    """
    Create a new collection in Qdrant or return existing one if it already exists

    Args:
        collection_name (str): Name of the collection
        vector_size (int): Size of the embedding vector (default 768)
    """
    # Initialize Qdrant client
    client = QdrantClient(host="localhost", port=6333, timeout=10.0)

    # try:
    # Check if collection exists
    collections = client.get_collections()
    if collection_name in [col.name for col in collections.collections]:
        print(f"Collection {collection_name} already exists")
        vector_store = QdrantVectorStore.from_existing_collection(
            host="localhost",
            port=6333,
            collection_name=collection_name,
            embedding=embedding_model,
        )
        return vector_store
    # Create new collection if it doesn't exist
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        on_disk_payload=True,
    )
    vector_store = QdrantVectorStore(
        client=client, collection_name=collection_name, embedding=embedding_model
    )
    print(f"Collection {collection_name} created successfully")
    return vector_store
    # except Exception as e:
    #     print(f"Error creating/accessing collection: {e}")

def add_to_qdrant(
    documents: list[Document],
    collection_name: str,
    embedding_model: Any,
    vector_size: int = 768,
):
    """
    Add text to Qdrant with a specified embedding model

    Args:
        text (str): Text to be added
        collection_name (str): Name of the Qdrant collection
        embedding_model: The embedding model to use
        vector_size (int): Size of the embedding vector (default 384)
    """
    # Initialize Qdrant client
    vector_store = create_collection(collection_name, embedding_model, vector_size)
    uuids = [str(uuid.uuid4()) for _ in range(len(documents))]
    # Generate a unique ID for the point
    vector_store.add_documents(documents=documents, ids=uuids)
    print(f"Added {len(documents)} documents to collection: {collection_name}")
    return uuids

def search_qdrant(
    query: str,
    vector_store: QdrantVectorStore,
    top_k: int = 5,
    score_threshold = 0.5
):
    """
    Search for similar documents in Qdrant using a query
    """
    retriever = vector_store.as_retriever(search_type = "mmr", search_kwargs={"k": top_k}, )
    docs = retriever.invoke(query)
    # docs = vector_store.similarity_search_with_score(query, k=top_k)
    return docs

async def asearch_qdrant(
    query: str,
    vector_store: QdrantVectorStore,
    top_k: int = 5,
    score_threshold = 0.5
):
    """
    Search for similar documents in Qdrant using a query
    """
    retriever = vector_store.as_retriever(search_type = "mmr", search_kwargs={"k": top_k})
    docs = await retriever.ainvoke(query)
    return docs
