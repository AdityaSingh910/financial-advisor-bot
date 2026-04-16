"""
Agent 1: Data Retrieval Agent
Searches the FAISS vector store for relevant financial information
based on the user's query.
"""

import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


VECTOR_STORE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_store")


def get_vector_store():
    """Load the FAISS vector store."""
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    return FAISS.load_local(
        VECTOR_STORE_DIR, embeddings, allow_dangerous_deserialization=True
    )


def retrieve(query: str, k: int = 5) -> dict:
    """
    Retrieve relevant documents from the vector store.
    
    Args:
        query: User's financial question
        k: Number of documents to retrieve
        
    Returns:
        Dictionary with retrieved context and source metadata
    """
    vector_store = get_vector_store()
    
    # Similarity search with scores
    results_with_scores = vector_store.similarity_search_with_score(query, k=k)
    
    retrieved_chunks = []
    sources = set()
    
    for doc, score in results_with_scores:
        source_file = os.path.basename(doc.metadata.get("source", "unknown"))
        source_name = source_file.replace(".md", "").replace("_", " ").title()
        sources.add(source_name)
        
        retrieved_chunks.append({
            "content": doc.page_content,
            "source": source_name,
            "relevance_score": round(float(1 / (1 + score)), 3),  # Convert distance to similarity
        })
    
    # Combine context for downstream agents
    combined_context = "\n\n---\n\n".join(
        [f"[Source: {chunk['source']}]\n{chunk['content']}" for chunk in retrieved_chunks]
    )
    
    return {
        "agent": "Data Retriever",
        "status": "completed",
        "chunks_retrieved": len(retrieved_chunks),
        "sources": list(sources),
        "context": combined_context,
        "details": retrieved_chunks,
    }
