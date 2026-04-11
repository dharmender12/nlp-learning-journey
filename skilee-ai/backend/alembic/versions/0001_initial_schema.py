"""initial schema

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-03-08
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "contracts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("company_name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("required_trainers", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_contracts_id", "contracts", ["id"])

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("tier", sa.String(), nullable=False, server_default="free"),
        sa.Column("start_date", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_subscriptions_id", "subscriptions", ["id"])

    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("contract_id", sa.Integer(), sa.ForeignKey("contracts.id"), nullable=False),
        sa.Column("trainer_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("cover_letter", sa.Text(), nullable=True),
        sa.Column("cv_url", sa.String(), nullable=False),
        sa.Column("cv_path", sa.String(), nullable=False),
        sa.Column("skills", sa.String(), nullable=True),
        sa.Column("years_experience", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("relevance_score", sa.Float(), nullable=True, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_applications_id", "applications", ["id"])


def downgrade() -> None:
    op.drop_index("ix_applications_id", table_name="applications")
    op.drop_table("applications")

    op.drop_index("ix_subscriptions_id", table_name="subscriptions")
    op.drop_table("subscriptions")

    op.drop_index("ix_contracts_id", table_name="contracts")
    op.drop_table("contracts")

    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
