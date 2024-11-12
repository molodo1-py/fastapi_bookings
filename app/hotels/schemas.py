from datetime import date
from typing import Optional

from fastapi import Query
from pydantic import BaseModel


class HotelParams:

    def __init__(
        self, 
        location: str,
        date_from: date = Query(..., description="For example '2020-02-20'"),
        date_to: date = Query(..., description="For example '2020-03-15'")
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to


class SHotel(BaseModel):

    id: int
    name: str
    location: str
    services: Optional[list[str]]
    rooms_quantity: int
    image_id: Optional[int]

    class Config:
        from_attributes = True


class SHotelInfo(SHotel):

    left_rooms: int
