"""fix_is_deleted_type_to_boolean

Revision ID: 445bf9eeeab8
Revises: 2c637652be17
Create Date: 2025-10-18 06:49:48.445009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '445bf9eeeab8'
down_revision: Union[str, Sequence[str], None] = '2c637652be17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
