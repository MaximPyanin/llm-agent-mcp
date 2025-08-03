from langchain.schema import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from app.services.llm_service import LLMService
from app.services.settings import Settings
from app.prompts.system_prompt import SYSTEM_PROMPT


class WeatherAgent:
    def __init__(self, llm_service: LLMService, settings: Settings):
        self.llm = llm_service.get_llm
        self.agent = None
        self.settings = settings

    async def initialize(self) -> None:
        mcp_client = MultiServerMCPClient(
            {
                "search_location": {
                    "url": self.settings.mcp_server_url,
                    "transport": "streamable_http",
                },
                "get_weather": {
                    "url": self.settings.mcp_server_url,
                    "transport": "streamable_http",
                },
            }
        )

        tools = await mcp_client.get_tools()

        self.agent = create_react_agent(
            model=self.llm, tools=tools, system_message=SYSTEM_PROMPT
        )

    async def process_message(self, message: str) -> str:
        if self.agent is None:
            await self.initialize()

        payload = {"messages": [HumanMessage(content=message)]}
        result = await self.agent.ainvoke(payload)
        return result["messages"][-1].content
