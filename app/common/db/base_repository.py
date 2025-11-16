from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Result, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.base import ExecutableOption

from app.common.db.core_model import CoreModel

ModelType = TypeVar("ModelType", bound=CoreModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=PydanticBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=PydanticBaseModel)


class CrudRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType], db: Session):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db

    def get_one(
        self, sid: Any, custom_options: tuple[ExecutableOption, ...] | None = None
    ) -> ModelType | None:
        query = select(self.model).where(self.model.sid == sid)

        if custom_options is not None:
            query = query.options(*custom_options)

        result: Result = self.db.execute(query)
        return result.scalars().first()

    def get_all(
        self, custom_options: tuple[ExecutableOption, ...] | None = None
    ) -> Sequence[ModelType]:
        query = select(self.model)

        if isinstance(custom_options, tuple):
            query = query.options(*custom_options)

        result: Result = self.db.execute(query)
        return result.scalars().all()

    def get_all_paginated(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        custom_options: tuple[ExecutableOption] | None = None,
    ) -> Sequence[ModelType]:
        query = select(self.model).offset(offset).limit(limit)

        if isinstance(custom_options, tuple):
            query = query.options(*custom_options)

        result: Result = self.db.execute(query)
        return result.scalars().all()

    def create(
        self, *, obj_in: CreateSchemaType, with_commit: bool = True
    ) -> ModelType:
        try:
            db_obj = self.model(**obj_in.model_dump())

            self.db.add(db_obj)

            if with_commit:
                self.db.commit()
                self.db.refresh(db_obj)
            else:
                self.db.flush()

            return db_obj
        except IntegrityError as e:
            raise IntegrityError from e

    def update(
        self,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        try:
            obj_data = jsonable_encoder(db_obj)

            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            self.db.add(db_obj)

            self.db.commit()
            self.db.refresh(db_obj)

            return db_obj
        except IntegrityError as e:
            raise IntegrityError from e

    def delete(self, *, sid: Any, with_commit: bool = True) -> ModelType | None:
        query = select(self.model).where(self.model.sid == sid)
        result: Result = self.db.execute(query)
        obj = result.scalars().first()

        self.db.delete(obj)

        if with_commit:
            self.db.commit()
        else:
            self.db.flush()

        return obj

    def get_multi(
        self,
        *,
        offset: int = 0,
        limit: int = 100,
        custom_options: tuple[ExecutableOption, ...] | None = None,
    ) -> Sequence[ModelType]:
        query = select(self.model).offset(offset).limit(limit)

        if isinstance(custom_options, tuple):
            query = query.options(*custom_options)

        result: Result = self.db.execute(query)
        return result.scalars().all()
