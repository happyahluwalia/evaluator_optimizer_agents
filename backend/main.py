from fastapi import FastAPI
from routers.llms import router as llms_router
from llm_service import LLMService


app = FastAPI()

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
