from fastapi import APIRouter, Depends
from fastapi_versioning import version

from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import RoomParams, SRoomInfo

router = APIRouter(prefix="/hotels", tags=["Hotels & Rooms"])


@router.get("/{hotel_id}/rooms")
@version(1)
async def get_rooms(params: RoomParams = Depends()) -> list[SRoomInfo]:
    return await RoomDAO.find_all(params)
