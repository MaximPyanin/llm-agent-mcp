from typing import Any
from httpx import AsyncClient, Timeout, HTTPError
from app.schemas.weather_data_schema import WeatherData


class WeatherDataTool:
    name = "get_weather"
    description = "Get weather data from Open-Meteo API"
    args_schema = WeatherData

    def __init__(self) -> None:
        self._client = AsyncClient(timeout=Timeout(10.0))

    async def run(self, args: WeatherData) -> dict[str, Any]:
        try:
            self._validate_coords(args)
            url = self._select_url(args)
            params = self._build_params(args)
            result = await self._fetch(url, params)
            return result

        except HTTPError as e:
            return {"error": f"API error: {e}"}
        except Exception as e:
            return {"error": f"Error: {e}"}

    def _validate_coords(self, args: WeatherData) -> None:
        if not (-90 <= args.lat <= 90) or not (-180 <= args.lon <= 180):
            raise ValueError(f"Invalid coordinates: {args.lat}, {args.lon}")

    def _select_url(self, args: WeatherData) -> str:
        if args.start_date and args.end_date:
            return "https://api.open-meteo.com/v1/historical"
        return "https://api.open-meteo.com/v1/forecast"

    def _build_params(self, args: WeatherData) -> dict[str, Any]:
        params: dict[str, Any] = {
            "latitude": args.lat,
            "longitude": args.lon,
            "timezone": "auto",
        }
        if args.include_current:
            params["current"] = (
                "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m"
            )
        if args.forecast_days:
            days = min(max(args.forecast_days, 1), 16)
            params["forecast_days"] = days
            params.setdefault(
                "daily",
                "temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum",
            )
        if args.start_date and args.end_date:
            params.update({"start_date": args.start_date, "end_date": args.end_date})
            params["daily"] = (
                "temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum"
            )
        return params

    async def _fetch(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        response = await self._client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        await self._client.aclose()

    @staticmethod
    async def get_weather_func(lat: float, lon: float, **kwargs) -> dict:
        tool = WeatherDataTool()
        try:
            args = WeatherData(lat=lat, lon=lon, **kwargs)
            return await tool.run(args)
        finally:
            await tool.close()
