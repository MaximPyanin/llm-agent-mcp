from mcp.server.fastmcp import FastMCP
from app.tools.location_search_tool import LocationSearchTool
from app.tools.weather_data_tool import WeatherDataTool

mcp = FastMCP("Weather-MCP Server")


@mcp.tool()
async def search_location(city: str) -> dict:
    return await LocationSearchTool.search_location_func(city)


@mcp.tool()
async def get_weather(
    lat: float,
    lon: float,
    include_current: bool = False,
    forecast_days: int = None,
    start_date: str = None,
    end_date: str = None,
) -> dict:
    return await WeatherDataTool.get_weather_func(
        lat=lat,
        lon=lon,
        include_current=include_current,
        forecast_days=forecast_days,
        start_date=start_date,
        end_date=end_date,
    )


def main():
    mcp.run(transport="streamable-http", mount_path="/mcp")


if __name__ == "__main__":
    main()
