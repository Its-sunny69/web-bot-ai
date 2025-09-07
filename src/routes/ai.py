from fastapi import APIRouter
from src.schemas import PromptIn, PromptOut
from sqlalchemy.orm import Session
from src.utils import generate_chat_response
from fastapi import APIRouter, Depends
from sqlalchemy import select
from src.db.session import get_db
from src.db.models import repos

router = APIRouter(prefix="/test", tags=["Test"])


router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat", response_model=PromptOut)
async def chat_with_ai(data: PromptIn):
    """
    Send a prompt to vLLM (Mistral) and return response
    """
    response = generate_chat_response(data.prompt)
    return PromptOut(response=response)

@router.get("/{repo_id}")
async def get_repo(repo_id: int, db: Session = Depends(get_db)):
    query = select(repos).where(repos.c.id == repo_id)
    result = db.execute(query).mappings().first()
    return result
