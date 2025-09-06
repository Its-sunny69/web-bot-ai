from ninja import Router, Schema
from openai import OpenAI
from django.conf import settings

router = Router(tags=["AI"])


# Schemas
class PromptIn(Schema):
    prompt: str


class PromptOut(Schema):
    response: str


# OpenAI-compatible client (points to vLLM)
client = OpenAI(
    base_url=settings.OPENAI_API_BASE,
    api_key=settings.OPENAI_API_KEY,
)


@router.post("/chat", response=PromptOut)
def chat_with_ai(request, data: PromptIn):
    """Send a prompt to vLLM (Mistral) and return response"""
    resp = client.chat.completions.create(
        model="openai/gpt-oss-120b:cerebras",
        messages=[{"role": "user", "content": data.prompt}],
    )

    return PromptOut(response=resp.choices[0].message.content)
