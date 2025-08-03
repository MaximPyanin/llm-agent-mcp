from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mcp_server_url: str = "http://127.0.0.1:8000/mcp"

    groq_model: str = "llama3-8b-8192"
    groq_temperature: float = 0.1
    groq_api_key: str

    app_title: str = "🌤️ Weather Assistant"
    input_placeholder: str = "Ask me about the weather…"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
