"""add hash_password to user

Revision ID: 5a73dea086cc
Revises: e9f0f3f5dfd3
Create Date: 2024-01-21 17:12:26.783441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5a73dea086cc"
down_revision: Union[str, None] = "e9f0f3f5dfd3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("hashed_password", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "hashed_password")
    # ### end Alembic commands ###