"""add is_safe_to_go_out enum column

Revision ID: a314a67e30a0
Revises: 564f568e3df6
Create Date: 2025-06-14 23:39:20.812187

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

# revision identifiers, used by Alembic.
revision: str = 'a314a67e30a0'
down_revision: Union[str, None] = '564f568e3df6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

safetylevel_enum = pg.ENUM('yes', 'no', name='safetylevel')

def upgrade() -> None:
    # Створити ENUM тип
    safetylevel_enum.create(op.get_bind(), checkfirst=True)

    # Якщо колонка існувала раніше — видалити
    with op.batch_alter_table("astronomy_info") as batch_op:
        batch_op.drop_column("is_safe_to_go_out")

    # Додати нову колонку з ENUM типом
    op.add_column('astronomy_info', sa.Column('is_safe_to_go_out', safetylevel_enum, nullable=True))

def downgrade() -> None:
    op.drop_column('astronomy_info', 'is_safe_to_go_out')
    safetylevel_enum.drop(op.get_bind(), checkfirst=True)

