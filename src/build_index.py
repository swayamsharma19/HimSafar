"""
build_index.py
----------------
Step 1 of the RAG pipeline: load raw text documents, split them into chunks,
embed them, and store them in a local ChromaDB vector database.

Run this ONCE (or whenever you add new source documents) to (re)build the index.
"""

import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "chroma_db")


def load_documents():
    """Load all .txt files from the raw data directory."""
    loader = DirectoryLoader(RAW_DATA_DIR, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    print(f"Loaded {len(documents)} source documents.")
    return documents


def split_documents(documents):
    """
    Split documents into overlapping chunks.

    Why chunk_size=500 and overlap=100:
    - Government/travel-rule text has dense, standalone facts (e.g. permit
      rejection reasons) that don't need huge context windows to make sense.
    - Overlap ensures a fact split across a chunk boundary still has enough
      surrounding context to be retrieved correctly.
    These are starting values — worth tuning later using Phase 4 evaluation.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    return chunks


def build_vector_store(chunks):
    """Embed chunks and persist them to a local Chroma vector database."""
    # all-MiniLM-L6-v2 is a small, free, fast sentence-embedding model.
    # It runs locally (no API cost) and is a common, defensible choice
    # for a resume project of this size.
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )
    print(f"Vector store built and persisted to: {PERSIST_DIR}")
    return vector_store


if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)
    build_vector_store(chunks)
    print("\nDone. Run src/query.py to test retrieval, or src/app.py for the chat UI.")
