from pydantic import BaseModel

# Chat endpoint
class PromptIn(BaseModel):
    prompt: str

class PromptOut(BaseModel):
    response: str

# Embeddings endpoint (optional, if you add later)
class EmbeddingIn(BaseModel):
    text: str

class EmbeddingOut(BaseModel):
    vector: list[float]
