"""init users

Revision ID: fc2a6f407de5
Revises: 
Create Date: 2023-10-30 14:31:15.824688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc2a6f407de5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column(name='id', type_=sa.UUID(as_uuid=True) ),
        sa.Column(name="username", type_=sa.String(20), unique=True),
        sa.Column(name="password", type_=sa.Text),
        sa.Column(name='created_at', type_=sa.DateTime(timezone=True)),
        sa.Column(name='updated_at', type_=sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )


def downgrade() -> None:
    op.drop_table('users')
