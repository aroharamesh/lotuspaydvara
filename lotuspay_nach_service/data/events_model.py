from datetime import datetime
from typing import Optional

import sqlalchemy


events_metadata = sqlalchemy.MetaData()


events = sqlalchemy.Table(
    "events",
    events_metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("event_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("event_object", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("event_created", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("event_livemode", sqlalchemy.Boolean, nullable=True),
    sqlalchemy.Column("resource_id", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("resource_object", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("resource_object", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("resource_created", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("resource_status", sqlalchemy.String(length=255), nullable=True),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime(), nullable=True),
)

# {'id': 'EV0044332211AA', 'object': 'event', 'created': 1530224170, 'livemode': False, 'data': {'id': 'MD0044332211AA', 'object': 'mandate', 'created': 1530224170},
# 'type': 'mandate.active'}