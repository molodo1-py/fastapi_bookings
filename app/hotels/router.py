from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from app.cache import request_key_builder
from app.exc.exceptions import (
    CannotBookHotelForLongPeriod,
    DateFromCannotBeAfterDateTo,
    HotelNotFound,
)
from app.hotels.dao import HotelDAO
from app.hotels.schemas import HotelParams, SHotel, SHotelInfo

router = APIRouter(prefix="/hotels", tags=["Hotels & Rooms"])

@router.get("/{location}")
@cache(expire=30, key_builder=request_key_builder)
@version(1)
async def get_hotels(params: HotelParams = Depends())-> list[SHotelInfo]:
    if params.date_from > params.date_to:
        raise DateFromCannotBeAfterDateTo
    if (params.date_to - params.date_from).days > 31:
        raise CannotBookHotelForLongPeriod
    hotels = await HotelDAO.find_all(params)
    if not hotels:
        raise HotelNotFound
    return hotels


@router.get("/id/{hotel_id}")
@version(1)
async def get_hotel_by_id(hotel_id: int) -> SHotel:
    hotel = await HotelDAO.find_by_id(hotel_id)
    if not hotel:
        raise HotelNotFound
    return hotel
