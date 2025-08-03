# LLM Agent for Weather Determination

LLM agent for weather information retrieval through interaction with two APIs via unified MCP interface.

## Description

The agent uses:
- **Nominatim API** for determining coordinates by city name
- **Open-Meteo API** for retrieving weather data by coordinates
- **Groq LLM** for natural language processing
- **MCP protocol** for unified tool access

Supports current weather, forecasts, and historical data in multiple languages.

## Installation and Setup

### Requirements
- Python 3.11+
- UV package manager

### Setup
1. Install dependencies:
   ```bash
   uv sync
   ```

2. Create `.env` file with API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

### Running
Requires 2 terminals:

**Terminal 1 - MCP Server:**
```bash
uv run python -m app.mcp_server
```

**Terminal 2 - UI:**
```bash
uv run streamlit run app/streamlit_app.py
```

## Usage Examples

```
"What's the weather in London today?"
"Weather forecast for next 3 days in Paris"
"What was the weather in Tokyo yesterday?"
```

## Project Structure

```
app/
├── agents/weather_agent.py      # Main agent logic
├── prompts/system_prompt.py     # System prompt
├── schemas/                     # Pydantic schemas
├── services/                    # LLM service and settings
├── tools/                       # API tools
├── ui/weather_ui.py            # Streamlit interface
├── mcp_server.py               # MCP server
└── streamlit_app.py            # Entry point
```

## Technical Details

- **LLM**: Groq (llama3-8b-8192)
- **Framework**: LangChain + LangGraph
- **Pattern**: ReAct (Reasoning + Acting)
- **UI**: Streamlit
- **APIs**: Nominatim (OpenStreetMap) + Open-Meteo