from pydantic import BaseModel, Field


class LocationSearch(BaseModel):
    city_name: str = Field(..., description="Name of the city to search for")
