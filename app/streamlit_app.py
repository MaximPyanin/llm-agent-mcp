from dotenv import load_dotenv
from app.services.settings import Settings
from app.services.llm_service import LLMService
from app.agents.weather_agent import WeatherAgent
from app.ui.weather_ui import WeatherUI


def main():
    load_dotenv()

    settings = Settings()
    llm_service = LLMService(settings)
    weather_agent = WeatherAgent(llm_service=llm_service, settings=settings)

    weather_ui = WeatherUI(weather_agent=weather_agent, settings=settings)
    weather_ui.run()


if __name__ == "__main__":
    main()
