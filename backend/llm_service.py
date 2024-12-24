import os
from dotenv.main import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from config import SUPPORTED_PROVIDERS


class LLMService:
    def __init__(self, provider: str, model: str):
        # Load the .env file
        load_dotenv()
        self.provider = provider
        self.model = model

        if provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            self.client = ChatOpenAI(model_name=model, temperature = 0, openai_api_key=api_key)
        elif provider == "anthropic":
            if not os.environ.get("ANTHROPIC_API_KEY"):
                api_key = os.environ["ANTHROPIC_API_KEY"]
            self.client = ChatAnthropic(model=model, anthropic_api_key=api_key)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_response(self, prompt: str) -> str:
        response =  self.client.invoke([{"role": "user", "content": prompt}])
        return response.content

    @staticmethod
    def get_supported_models():
        """Dynamically fetch supported models and providers."""
        return [
            {
                "provider": key,
                "name": value["name"],
                "models": value["models"],
            }
            for key, value in SUPPORTED_PROVIDERS.items()
        ]