from datetime import date

from sqlalchemy import and_, delete, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session
from app.hotels.rooms.models import Rooms
from app.exc.utils import log_sql_or_unknwn_error


class BookingDAO(BaseDAO):

    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """
        WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id=1 AND
            (date_from <= '2023-05-15' AND date_to >= '2023-06-20') OR
            (date_from >= '2023-05-15' AND date_from <= '2023-06-20')
        )

        SELECT rooms.quantity - COUNT(booked_rooms.room_id) rooms_left FROM rooms
        LEFT JOIN booked_rooms ON rooms.id=booked_rooms.room_id
        WHERE rooms.id=1
        GROUP BY rooms.quantity, booked_rooms.room_id;
        """
        try:
            async with async_session() as session:
                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to >= date_to,
                                ),
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )
                get_rooms_left = (
                    select(
                        (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                            "rooms_left"
                        )
                    )
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )
                rooms_left = await session.execute(get_rooms_left)
                rooms_left: int = rooms_left.scalar()
                if rooms_left > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )
                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            log_sql_or_unknwn_error(
                error=e,
                msg="Cannot add data into table",
                extra={
                    "table": cls.model.__tablename__,
                    "inserted_data": {
                        "user_id": user_id,
                        "room_id": room_id,
                        "date_from": date_from,
                        "date_to": date_to
                    }
                }
            )
            return None

    @classmethod
    async def delete(cls, booking_id: int, user_id: int) -> None:
        try:    
            async with async_session() as session:
                query = delete(Bookings).where(
                    Bookings.id == booking_id, Bookings.user_id == user_id
                )
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            log_sql_or_unknwn_error(
                error=e,
                msg="Cannot delete data from table",
                extra={
                    "table": cls.model.__tablename__,
                    "filter_by": {
                        "booking_id": booking_id,
                        "user_id": user_id
                    }
                }
            )
            return None