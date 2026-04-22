import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration
DB_DIR = "chroma_db"
MANUAL_PATH = "data/manual.pdf"
EMBEDDING_MODEL = "nomic-embed-text"

def ingest_manual():
    """
    Loads a PDF, splits it into chunks, and stores embeddings in a local ChromaDB.
    """
    print(f"--- Starting Ingestion Process for: {MANUAL_PATH} ---")
    
    # Load the PDF document
    if not os.path.exists(MANUAL_PATH):
        print(f"Error: {MANUAL_PATH} not found.")
        return

    loader = PyPDFLoader(MANUAL_PATH)
    documents = loader.load()
    print(f"Successfully loaded {len(documents)} pages.")

    # Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # using 1000 chars to keep the context
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Document split into {len(chunks)} chunks.")

    # Initialize Local Embeddings (Ollama)
    print(f"Initializing local embeddings using model: {EMBEDDING_MODEL}...")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)

    # Create and persist the Vector Store
    print("Generating embeddings and saving to local vector database...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    
    print(f"Database created successfully in folder: '{DB_DIR}'")

if __name__ == "__main__":
    ingest_manual()