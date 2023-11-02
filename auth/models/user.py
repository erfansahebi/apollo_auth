import typing
from datetime import datetime
from uuid import UUID
from dataclasses import dataclass, field
from apollo_shared.alembic import models as common_models
from sqlalchemy import Table, Column, String, Text
from sqlalchemy.orm import registry


@dataclass
class UserEntity:
    username: str
    password: str

    id: typing.Optional[UUID] = None
    created_at: typing.Optional[datetime] = field(
        default_factory=datetime.utcnow
    )
    updated_at: typing.Optional[datetime] = field(
        default_factory=datetime.utcnow
    )


user = Table(
    'users', common_models.metadata,
    common_models.uuid_primary_key_column(),
    Column(name="username", type_=String(20), unique=True),
    Column(name="password", type_=Text),
    common_models.created_at_column(),
    common_models.updated_at_column(),
)

common_models.mapper_registry.map_imperatively(UserEntity, user)
