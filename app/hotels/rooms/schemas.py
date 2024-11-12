from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class RoomParams:

    def __init__(self, hotel_id: int, date_from: date, date_to: date):
        self.hotel_id = hotel_id
        self.date_from = date_from
        self.date_to = date_to


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: Optional[str]
    services: List[str]
    price: int
    quantity: int
    image_id: int


class SRoomInfo(SRoom):
    total_cost: int
    rooms_left: int

    class Config:
        from_attributes = True
