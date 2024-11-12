from sqlalchemy import delete, insert, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session, Base
from app.exc.utils import log_sql_or_unknwn_error


class BaseDAO:

    model: Base = None

    @classmethod
    async def find_all(cls, **filter_by):
        try:
            async with async_session() as session:
                query = select(cls.model.__table__.columns).filter_by(**filter_by)
                session: Session
                result = await session.execute(query)
                return result.mappings().all()
        except (SQLAlchemyError, Exception) as e:
            log_sql_or_unknwn_error(
                error=e,
                msg="Cannot find all data in table",
                extra={
                    "table": cls.model.__tablename__,
                    "filter_by": filter_by
                }
            )
            return None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        try:
            async with async_session() as session:
                query = select(cls.model.__table__.columns).filter_by(**filter_by)
                session: Session
                result = await session.execute(query)
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            log_sql_or_unknwn_error(
                error=e,
                msg="Cannot find one or none in table",
                extra={
                    "table": cls.model.__tablename__,
                    "filter_by": filter_by
                }
            )
            return None

    @classmethod
    async def find_by_id(cls, model_id: int):
        try:
            async with async_session() as session:
                query = select(cls.model.__table__.columns).filter_by(id=model_id)
                session: Session
                result = await session.execute(query)
                return result.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            log_sql_or_unknwn_error(
                error=e,
                msg="Cannot find by id in table",
                extra={
                    "table": cls.model.__tablename__
                }
            )
            return None

    @classmethod
    async def add(cls, **data):
        try:
            async with async_session() as session:
                query = insert(cls.model).values(**data)
                session: Session
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            log_sql_or_unknwn_error(
                error=e,
                msg="Cannot add data into table",
                extra={
                    "table": cls.model.__tablename__,
                    "inserted_data": data
                }
            )
            return None

    @classmethod
    async def delete(cls, **filter_by):
        try:
            async with async_session() as session:
                query = delete(cls.model).where(**filter_by)
                session: Session
                await session.execute(query)
                await session.commit()
        except (SQLAlchemyError, Exception) as e:
            log_sql_or_unknwn_error(
                error=e,
                msg="Cannot delete data from table",
                extra={
                    "table": cls.model.__tablename__,
                    "filter_by": filter_by
                }
            )
            return None
            
    @classmethod
    async def add_bulk(cls, *data):
        try:
            query = insert(cls.model).values(data).returning(cls.model.id)
            async with async_session() as session:
                session: Session
                result = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (Exception, SQLAlchemyError) as e:
            log_sql_or_unknwn_error(
                error=e,
                msg="Cannot bulk insert data into table",
                extra={
                    "table": cls.model.__tablename__       
                }
            )
            return None