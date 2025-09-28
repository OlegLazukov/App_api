from alembic import op
import sqlalchemy as sa

revision = "20240925_0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "answers",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("question_id", sa.Integer(), sa.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("user_id", sa.String(), nullable=False, index=True),
        sa.Column("text", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

def downgrade() -> None:
    op.drop_table("answers")
    op.drop_table("questions")
