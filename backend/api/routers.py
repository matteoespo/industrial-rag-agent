# Contains endpoints

from fastapi import HTTPException, APIRouter
from .models import QueryRequest
from ai.rag_engine import get_rag_chain

router = APIRouter()

@router.post("/upload")
async def upload_pdf():
    return {"message": "PDF received and sent to chunking"}

@router.post("/chat")
async def chat_with_agent(query: QueryRequest):
    chain = get_rag_chain()
    response = chain.invoke({"input": query})
    return {"answer": response["answer"]}