"""lowercase enum for safety

Revision ID: 2b0ad3862b1c
Revises: 959c6847df5d
Create Date: 2025-06-15 12:24:52.431775

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = 'fix_enum_lowercase'
down_revision: Union[str, None] = '959c6847df5d'
branch_labels = None
depends_on = None

def upgrade() -> None:
    with op.batch_alter_table("astronomy_info") as batch_op:
        batch_op.drop_column("is_safe_to_go_out")

    enum_type = sa.Enum("yes", "no", name="safetylevel_lower")
    enum_type.create(op.get_bind(), checkfirst=True)

    with op.batch_alter_table("astronomy_info") as batch_op:
        batch_op.add_column(sa.Column("is_safe_to_go_out", enum_type, nullable=True))

def downgrade() -> None:
    with op.batch_alter_table("astronomy_info") as batch_op:
        batch_op.drop_column("is_safe_to_go_out")

    sa.Enum(name="safetylevel_lower").drop(op.get_bind(), checkfirst=True)
