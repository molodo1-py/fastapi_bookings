from datetime import datetime
from typing import Iterator, Any
import json

from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.bookings.dao import BookingDAO
from app.logger import logger

TABLE_MODEL_MAP = {
    "hotels": HotelDAO,
    "rooms": RoomDAO,
    "bookings": BookingDAO
}

def convert_csv_to_postgres_format(csv_iterable: Iterator) -> list[dict[Any]]:
    
    try:
        data = []
        for row in csv_iterable:
            row: dict
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
                elif key == "services":
                    row[key] = json.loads(value.replace("'", '"'))
                elif "date" in key:
                    row[key] = datetime.strptime(value, "%Y-%m-%d")
            data.append(row)
        return data
    except Exception:
        logger.error("Cannot convert CSV into DB format", exc_info=True)