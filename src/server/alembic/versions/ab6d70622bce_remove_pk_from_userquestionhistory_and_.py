"""Remove PK from UserQuestionHistory and add ID

Revision ID: ab6d70622bce
Revises: 6f511624e294
Create Date: 2025-04-14 22:45:42.413646

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "ab6d70622bce"
down_revision: Union[str, None] = "6f511624e294"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint(
        "user_question_history_pkey", "user_question_history", type_="primary"
    )
    op.add_column(
        "user_question_history",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
    )
    op.create_primary_key("user_question_history_pkey", "user_question_history", ["id"])


def downgrade():
    op.drop_constraint(
        "user_question_history_pkey", "user_question_history", type_="primary"
    )
    op.drop_column("user_question_history", "id")
    op.create_primary_key(
        "user_question_history_pkey",
        "user_question_history",
        ["user_id", "question_id"],
    )
