from pydantic import BaseModel, Field
from typing import Optional


class WeatherData(BaseModel):
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")
    include_current: bool = Field(False, description="Include current weather")
    forecast_days: Optional[int] = Field(
        None, description="Number of forecast days (1-16)"
    )
    start_date: Optional[str] = Field(
        None, description="Historical start date (YYYY-MM-DD)"
    )
    end_date: Optional[str] = Field(
        None, description="Historical end date (YYYY-MM-DD)"
    )
