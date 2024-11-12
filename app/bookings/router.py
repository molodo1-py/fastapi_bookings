from datetime import date

from fastapi import APIRouter, Depends, status
from fastapi_versioning import version
from pydantic import parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exc.exceptions import CannotBookHotelForLongPeriod, RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
@version(1)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
) -> None:
    if date_from >= date_to:
            raise RoomCannotBeBooked
    if (date_to - date_from).days > 30:
        raise CannotBookHotelForLongPeriod
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@version(1)
async def delete_booking(
    booking_id: int, user: Users = Depends(get_current_user)
) -> None:
    await BookingDAO.delete(booking_id=booking_id, user_id=user.id)
