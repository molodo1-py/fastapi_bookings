from fastapi import Depends
from sqlalchemy import and_, func, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session
from app.exc.utils import log_sql_or_unknwn_error
from app.hotels.rooms.models import Rooms
from app.hotels.rooms.schemas import RoomParams


class RoomDAO(BaseDAO):

    model = Rooms

    @classmethod
    async def find_all(cls, params: RoomParams = Depends()):
        """
        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked FROM bookings
            WHERE (date_from <= '2023-05-15' AND date_to >= '2023-06-20')
            OR (date_from >= '2023-05-15' AND date_from <= '2023-06-20')
            GROUP BY room_id
        )
        SELECT rooms.*, (rooms.quantity - COALESCE(booked_rooms.rooms_booked, 0)) AS left_rooms
        FROM rooms LEFT JOIN booked_rooms ON rooms.id=booked_rooms.room_id
        WHERE rooms.hotel_id=1;
        """
        try:
            booked_rooms = (
                select(
                    Bookings.room_id, (func.count(Bookings.room_id)).label("rooms_booked")
                )
                .select_from(Bookings)
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
            get_rooms = (
                select(
                    Rooms.__table__.columns,
                    (Rooms.price * (params.date_to - params.date_from).days).label(
                        "total_cost"
                    ),
                    (Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label(
                        "rooms_left"
                    ),
                )
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.hotel_id == params.hotel_id)
            )
            async with async_session() as session:
                rooms = await session.execute(get_rooms)
                return rooms.mappings().all()
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