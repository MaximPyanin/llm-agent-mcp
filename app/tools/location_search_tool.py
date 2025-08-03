from typing import Any
from httpx import AsyncClient, Timeout, HTTPError
from app.schemas.location_search_schema import LocationSearch


class LocationSearchTool:
    name = "search_location"
    description = "Search for city coordinates by name using OpenStreetMap Nominatim"
    args_schema = LocationSearch

    def __init__(self) -> None:
        self._client = AsyncClient(
            timeout=Timeout(10.0),
        )

    async def run(self, args: LocationSearch) -> dict[str, Any]:
        try:
            resp = await self._client.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": args.city_name,
                    "format": "json",
                    "limit": 1,
                    "addressdetails": 1,
                },
            )
            resp.raise_for_status()
            data = resp.json()

            loc = data[0]
            return {
                "city": loc.get("display_name", args.city_name),
                "latitude": float(loc["lat"]),
                "longitude": float(loc["lon"]),
                "country": loc.get("address", {}).get("country", "Unknown"),
            }
        except HTTPError as e:
            return {"error": f"Nominatim API error: {e}"}
        except Exception as e:
            return {"error": f"Unexpected error: {e}"}

    async def close(self) -> None:
        await self._client.aclose()

    @staticmethod
    async def search_location_func(city: str) -> dict:
        tool = LocationSearchTool()
        try:
            args = LocationSearch(city_name=city)
            result = await tool.run(args)
            return result
        finally:
            await tool.close()
