from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.backend.database.database import init_db, SessionLocal

from app.backend.routers.llms import router as llms_router
from app.backend.llm_service import LLMService




@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup the database
    startup()
    db = SessionLocal()
    yield
    # Close the database
    db.close()
    
def startup():
    init_db()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend is running"}

@app.get("/llms/models")
def get_llm_models():
    """Return available LLM providers and models."""
    return {"providers": LLMService.get_supported_models()}

@app.get("/generate")
def generate_text(provider: str, model: str, prompt: str):
    handler = LLMService(provider=provider, model=model)
    response = handler.get_response(prompt)
    return {"response": response}

app.include_router(llms_router, prefix="/api")
