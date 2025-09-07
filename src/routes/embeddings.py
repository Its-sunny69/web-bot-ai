from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.session import get_db
from src.services.embeddings import generate_embeddings_for_repo

router = APIRouter(prefix="/embeddings", tags=["Embeddings"])

@router.post("/generate/{repo_id}")
async def generate_repo_embeddings(repo_id: int, db: Session = Depends(get_db)):
    result = generate_embeddings_for_repo(repo_id, db)
    return result
