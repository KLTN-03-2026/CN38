from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "e7f8a9b0c1d2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    userrole = postgresql.ENUM("admin", "member", name="userrole")
    userrole.create(bind, checkfirst=True)
    orderstatus = postgresql.ENUM("pending", "paid", "cancelled", "expired", name="orderstatus")
    orderstatus.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=True),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("role", userrole, nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "membership_packages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("duration_days", sa.Integer(), nullable=False),
        sa.Column("max_workouts_per_week", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_membership_packages_id"), "membership_packages", ["id"], unique=False)

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("package_id", sa.Integer(), nullable=False),
        sa.Column("total_amount", sa.Float(), nullable=False),
        sa.Column("status", orderstatus, nullable=True),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["package_id"], ["membership_packages.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_orders_id"), "orders", ["id"], unique=False)

    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("payment_method", sa.String(length=50), nullable=True),
        sa.Column("transaction_id", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("transaction_id"),
    )
    op.create_index(op.f("ix_payments_id"), "payments", ["id"], unique=False)

    op.create_table(
        "ai_chat_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("response", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_chat_logs_id"), "ai_chat_logs", ["id"], unique=False)

    op.create_table(
        "workout_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("calories_burned", sa.Float(), nullable=True),
        sa.Column("intensity_score", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_workout_sessions_id"), "workout_sessions", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_workout_sessions_id"), table_name="workout_sessions")
    op.drop_table("workout_sessions")
    op.drop_index(op.f("ix_ai_chat_logs_id"), table_name="ai_chat_logs")
    op.drop_table("ai_chat_logs")
    op.drop_index(op.f("ix_payments_id"), table_name="payments")
    op.drop_table("payments")
    op.drop_index(op.f("ix_orders_id"), table_name="orders")
    op.drop_table("orders")
    op.drop_index(op.f("ix_membership_packages_id"), table_name="membership_packages")
    op.drop_table("membership_packages")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
    bind = op.get_bind()
    postgresql.ENUM("pending", "paid", "cancelled", "expired", name="orderstatus").drop(bind, checkfirst=True)
    postgresql.ENUM("admin", "member", name="userrole").drop(bind, checkfirst=True)
