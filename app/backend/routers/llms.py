from fastapi import APIRouter
from app.backend.llm_service import LLMService

router = APIRouter()

@router.get("/llms/models")
def get_llm_models():
    """Return available LLM providers and models."""
    return {"providers": LLMService.get_supported_models()}

@router.get("/generate")
def generate_text(provider: str, model: str, prompt: str):
    handler = LLMService(provider=provider, model=model)
    response = handler.get_response(prompt)
    return {"response": response}