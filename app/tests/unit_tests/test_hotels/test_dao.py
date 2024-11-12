import pytest

from app.hotels.dao import HotelDAO
from app.hotels.models import Hotels


@pytest.mark.parametrize(
    "hotel_id,name,rooms_quantity,image_id,exists",
    [
        (1, "Cosmos Collection Altay Resort", 15, 1, True),
        (2, "Skala", 23, 2, True),
        (3, "Ару-Кёль", 30, 3, True),
        (1488, "Joker", 0, 0, False),
    ],
)
async def test_find_by_id(
    hotel_id: int, name: str, rooms_quantity: int, image_id: int, exists: bool
):

    hotel: Hotels = await HotelDAO.find_by_id(hotel_id)
    if exists:
        assert hotel.name == name
        assert hotel.rooms_quantity == rooms_quantity
        assert hotel.image_id == image_id
    else:
        assert not hotel
