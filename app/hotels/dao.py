from fastapi import Depends
from sqlalchemy import and_, func, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session
from app.exc.utils import log_sql_or_unknwn_error
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.hotels.schemas import HotelParams


class HotelDAO(BaseDAO):

    model = Hotels

    @classmethod
    async def find_all(cls, params: HotelParams = Depends()):
        """

        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked FROM bookings

            WHERE (date_from <= '2023-05-15' AND date_to >= '2023-06-20')
            OR (date_from >= '2023-05-15' AND date_to <= '2023-06-20')
            GROUP BY room_id
        ),
        booked_hotels AS (
            SELECT rooms.hotel_id, SUM(rooms.quantity - COALESCE(booked_rooms.rooms_booked, 0))
            AS left_rooms FROM rooms LEFT JOIN booked_rooms ON rooms.id=booked_rooms.room_id
            GROUP BY rooms.hotel_id
        )

        SELECT hotels.*, booked_hotels.hotel_id FROM hotels
        LEFT JOIN booked_hotels ON hotels.id=booked_hotels.hotel_id
        WHERE booked_hotels.left_rooms > 0 AND hotels.location LIKE '%Алтай%';
        """
        try:
            booked_rooms = (
                select(
                    Bookings.room_id, (func.count(Bookings.room_id)).label("rooms_booked")
                )
                .where(
                    or_(
                        and_(
                            Bookings.date_from <= params.date_from,
                            Bookings.date_to >= params.date_to,
                        ),
                        and_(
                            Bookings.date_from >= params.date_from,
                            Bookings.date_from <= params.date_to,
                        ),
                    )
                )
                .group_by(Bookings.room_id)
                .cte("booked_rooms")
            )
            booked_hotels = (
                select(
                    Rooms.hotel_id,
                    (
                        func.sum(
                            Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
                        )
                    ).label("left_rooms"),
                )
                .select_from(Rooms)
                .join(booked_rooms, Rooms.id == booked_rooms.c.room_id, isouter=True)
                .group_by(Rooms.hotel_id)
                .cte("booked_hotels")
            )
            get_left_hotels = (
                select(Hotels.__table__.columns, booked_hotels.c.left_rooms)
                .join(booked_hotels, Hotels.id == booked_hotels.c.hotel_id, isouter=True)
                .where(
                    and_(
                        booked_hotels.c.left_rooms > 0,
                        Hotels.location.like(f"%{params.location}%"),
                    )
                )
            )
            async with async_session() as session:
                left_hotels = await session.execute(get_left_hotels)
                return left_hotels.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            log_sql_or_unknwn_error(
                error=e,
                msg="Cannot find all data in table",
                extra={
                    "table": cls.model.__tablename__,
                    "filter_by": params.__dict__
                }
            )
            return None