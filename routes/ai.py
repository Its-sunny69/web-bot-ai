from fastapi import APIRouter
from schemas import PromptIn, PromptOut
from utils import generate_chat_response

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat", response_model=PromptOut)
async def chat_with_ai(data: PromptIn):
    """
    Send a prompt to vLLM (Mistral) and return response
    """
    response = generate_chat_response(data.prompt)
    return PromptOut(response=response)
