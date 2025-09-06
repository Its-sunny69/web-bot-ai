"""
FastAPI entrypoint for AI Service
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import uvicorn

from routes.ai import router as ai_router

# Initialize FastAPI app
app = FastAPI(
    title="AI Service",
    description="AI-powered chat and embeddings service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(ai_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Service is running", "status": "healthy"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": "ai-service",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    # Get configuration from environment
    host = config("HOST", default="0.0.0.0")
    port = config("PORT", default=8000, cast=int)
    debug = config("DEBUG", default=False, cast=bool)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug"
    )
