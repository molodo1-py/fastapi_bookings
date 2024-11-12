from datetime import datetime

from app.bookings.dao import BookingDAO
from app.bookings.models import Bookings


async def test_add_and_get_booking():
    new_booking: Bookings = await BookingDAO.add(
        room_id=2,
        user_id=2,
        date_from=datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking: Bookings = await BookingDAO.find_by_id(new_booking.id)
    assert new_booking
