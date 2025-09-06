from ninja_extra import NinjaExtraAPI

from llmhub.api import router as ai_router

api = NinjaExtraAPI(
    title="Web Bot AI API",
    version="1.0.0",
)

api.add_router("/ai", ai_router)