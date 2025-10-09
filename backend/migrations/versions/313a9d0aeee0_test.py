"""test

Revision ID: 313a9d0aeee0
Revises: 341705bffcec
Create Date: 2025-10-09 22:21:05.189284

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '313a9d0aeee0'
down_revision: Union[str, Sequence[str], None] = '341705bffcec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute('ALTER TABLE students DROP CONSTRAINT IF EXISTS check_education_type;')
    op.execute("""
        ALTER TABLE students
        ADD CONSTRAINT check_education_type
        CHECK (education_type IS NULL OR education_type IN ('Đại học chính quy', 'Liên thông', 'Cao đẳng'));
    """)

def downgrade():
    op.execute('ALTER TABLE students DROP CONSTRAINT IF EXISTS check_education_type;')
    op.execute("""
        ALTER TABLE students
        ADD CONSTRAINT check_education_type
        CHECK (education_type IN ('Đại học chính quy', 'Liên thông', 'Cao đẳng'));
    """)