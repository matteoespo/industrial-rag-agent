from fastapi import FastAPI
from api.routers import router
from ai.rag_engine import get_rag_chain

app = FastAPI(
    title="DocuQuery RAG Agent",
    description="Local RAG system for technical manuals using Llama3 and Ollama.",
    version="1.0.0"
)

app.include_router(router, prefix="/api", tags=["Agentic RAG"])

@app.get("/health")
async def health_check():
    """Status check for docker"""
    return {"status": "running", "model": "llama3", "db": "chromadb"}

# Load the RAG chain into memory at startup
try:
    print("Loading AI Model and Vector DB...")
    rag_chain = get_rag_chain()
    print("AI Engine ready.")
except Exception as e:
    print(f"Error loading RAG Engine: {e}")
    rag_chain = None

