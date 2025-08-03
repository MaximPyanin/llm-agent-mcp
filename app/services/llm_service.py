from langchain_groq.chat_models import ChatGroq
from app.services.settings import Settings


class LLMService:
    def __init__(self, settings: Settings):
        self._llm = ChatGroq(
            model=settings.groq_model,
            temperature=settings.groq_temperature,
        )

    @property
    def get_llm(self) -> ChatGroq:
        return self._llm
