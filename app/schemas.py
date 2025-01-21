from pydantic import BaseModel
from typing import Optional, List

class ExcursionBase(BaseModel):
    excursion_name: str
    excursion_description: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    max_participants: Optional[int]
    price: Optional[float]
    location: Optional[str]
    weather_sensitive: Optional[bool]

    class Config:
        orm_mode = True

class ExcursionDetail(ExcursionBase):
    excursion_id: int  
    city_name: str
    category_name: str
    organizer_name: str


class BookingRequest(BaseModel):
    customer_name: str
    customer_phone: str
    excursion_id: int