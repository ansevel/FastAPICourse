"""unique user

Revision ID: f10a57f36af4
Revises: 86f43c6f0253
Create Date: 2024-10-16 10:37:03.506525

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f10a57f36af4"
down_revision: Union[str, None] = "86f43c6f0253"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_unique_constraint(None, "users", ["username"])
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:

    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "users", type_="unique")
