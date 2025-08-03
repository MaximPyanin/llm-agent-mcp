import streamlit as st
import asyncio
from app.agents.weather_agent import WeatherAgent
from app.services.settings import Settings


class WeatherUI:
    def __init__(self, weather_agent: WeatherAgent, settings: Settings):
        self.weather_agent = weather_agent
        self.settings = settings

    def run(self) -> None:
        st.set_page_config(
            page_title=self.settings.app_title, page_icon="🌤️", layout="centered"
        )
        st.title(self.settings.app_title)

        if user_input := st.chat_input(self.settings.input_placeholder):
            st.chat_message("user").write(user_input)

            with st.spinner("thinking…"):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    response = loop.run_until_complete(
                        self.weather_agent.process_message(user_input)
                    )
                finally:
                    loop.close()

            st.chat_message("assistant").write(response)
