import csv
import codecs
from typing import Literal, Any

from fastapi import APIRouter, status, Depends, UploadFile
from app.dao.base import BaseDAO
from app.exc.exceptions import CannotAddDataToDatabase, CannotProcessCSV
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.importer.utils import TABLE_MODEL_MAP, convert_csv_to_postgres_format


router = APIRouter(
    prefix="/import",
    tags=["Importer"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def import_data_to_table(
    table_name: Literal["hotels", "rooms", "bookings"],
    file: UploadFile,
    user: Users = Depends(get_current_user)
) -> None:
    
    ModelDAO: BaseDAO = TABLE_MODEL_MAP[table_name]
    csvReader = csv.DictReader(codecs.iterdecode(file.file, encoding="utf-8"), delimiter=";")
    data: list[dict[Any]] = convert_csv_to_postgres_format(csvReader)
    file.file.close()
    if not data:
        raise CannotProcessCSV
    added_data = await ModelDAO.add_bulk(*data)
    if not added_data:
        raise CannotAddDataToDatabase