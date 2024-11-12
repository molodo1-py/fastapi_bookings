from sqlalchemy.exc import SQLAlchemyError
from typing import Any
from app.logger import logger


def log_sql_or_unknwn_error(
    error: SQLAlchemyError|Exception, 
    msg: str,
    extra: dict[Any]
):
    if isinstance(error, SQLAlchemyError):
        base_msg = "Database Exc: "
    elif isinstance(error, Exception):
        base_msg = "Unknown Exc: "
    msg = base_msg + msg
    logger.error(msg, extra=extra, exc_info=True)