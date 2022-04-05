from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field
from sqlalchemy.dialects.mysql import LONGTEXT


class MandateBase(BaseModel):
    mandate_id: Optional[str] = None
    token: Optional[str] = None
    metadata: str
    created_date: datetime = Field(default_factory=datetime.now)


class MandateMetaData(BaseModel):
    key1: Optional[str] = None
    key2: Optional[str] = None
    key3: Optional[str] = None


class MandateCancelCreate(BaseModel):
    cancel_reason: Optional[str] = None


class MandateCreate(BaseModel):
    metadata: MandateMetaData


class MandateDB(MandateBase):
    id: int


mandate_metadata = sqlalchemy.MetaData()


mandates = sqlalchemy.Table(
    "mandates",
    mandate_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("mandate_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("metadata", LONGTEXT, nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True),
    # sqlalchemy.Column("created_date_time",sqlalchemy.DateTime, default=datetime.datetime.utcnow)
)


mandates_cancel = sqlalchemy.Table(
    "mandates_cancel",
    mandate_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("mandate_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True),
    # sqlalchemy.Column("created_date_time",sqlalchemy.DateTime, default=datetime.datetime.utcnow)
)