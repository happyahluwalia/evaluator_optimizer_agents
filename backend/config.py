SUPPORTED_PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "models": ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"],
        "api_key_env_var": "OPENAI_API_KEY",
    },
    "anthropic": {
        "name": "Anthropic",
        "models": ["claude-v1", "claude-v1.3", "claude-v2"],
        "api_key_env_var": "ANTHROPIC_API_KEY",
    },
    "cohere": {
        "name": "Cohere",
        "models": ["command-xlarge", "command-medium", "command-light"],
        "api_key_env_var": "COHERE_API_KEY",
    },
}
