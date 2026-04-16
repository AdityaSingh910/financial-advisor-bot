"""
Ingestion script for the Financial Advisory RAG system.
Loads knowledge base documents, chunks them, generates embeddings,
and stores them in a FAISS vector store.

Usage: python ingest.py
"""

import os
import sys
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


KNOWLEDGE_BASE_DIR = os.path.join(os.path.dirname(__file__), "knowledge_base")
VECTOR_STORE_DIR = os.path.join(os.path.dirname(__file__), "vector_store")


def load_documents():
    """Load all markdown documents from the knowledge base directory."""
    print(f"📂 Loading documents from: {KNOWLEDGE_BASE_DIR}")
    
    loader = DirectoryLoader(
        KNOWLEDGE_BASE_DIR,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=True,
    )
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} documents")
    return documents


def split_documents(documents):
    """Split documents into chunks for embedding."""
    print("✂️  Splitting documents into chunks...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
        separators=["\n## ", "\n### ", "\n#### ", "\n\n", "\n", " ", ""],
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    return chunks


def create_vector_store(chunks):
    """Generate embeddings and create FAISS vector store."""
    print("🧠 Generating embeddings (this may take a minute on first run)...")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Save the vector store
    os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
    vector_store.save_local(VECTOR_STORE_DIR)
    print(f"✅ Vector store saved to: {VECTOR_STORE_DIR}")
    
    return vector_store


def main():
    print("=" * 60)
    print("🏦 Financial Advisory RAG — Knowledge Base Ingestion")
    print("=" * 60)
    
    # Check knowledge base exists
    if not os.path.exists(KNOWLEDGE_BASE_DIR):
        print(f"❌ Knowledge base directory not found: {KNOWLEDGE_BASE_DIR}")
        sys.exit(1)
    
    # Load, split, embed, store
    documents = load_documents()
    
    if not documents:
        print("❌ No documents found in knowledge base!")
        sys.exit(1)
    
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks)
    
    # Quick test
    print("\n🔍 Quick test — searching for 'home loan interest rate'...")
    results = vector_store.similarity_search("home loan interest rate", k=3)
    for i, doc in enumerate(results):
        source = os.path.basename(doc.metadata.get("source", "unknown"))
        print(f"  Result {i+1} [{source}]: {doc.page_content[:100]}...")
    
    print("\n" + "=" * 60)
    print("✅ Ingestion complete! Vector store is ready.")
    print("=" * 60)


if __name__ == "__main__":
    main()
