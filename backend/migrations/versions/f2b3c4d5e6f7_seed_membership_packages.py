from alembic import op
import sqlalchemy as sa

revision = "f2b3c4d5e6f7"
down_revision = "e7f8a9b0c1d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    row = conn.execute(sa.text("SELECT COUNT(*) FROM membership_packages")).fetchone()
    if row is not None and row[0] > 0:
        return
    stmt = sa.text(
        """
            INSERT INTO membership_packages
                (name, description, price, duration_days, max_workouts_per_week, is_active)
            VALUES
                (:n1, :d1, :p1, :day1, :mw1, true),
                (:n2, :d2, :p2, :day2, :mw2, true),
                (:n3, :d3, :p3, :day3, :mw3, true),
                (:n4, :d4, :p4, :day4, :mw4, true)
        """
    ).bindparams(
        n1="Basic",
        d1="Gói 30 ngày cơ bản, phù hợp người mới",
        p1=299000.0,
        day1=30,
        mw1=3,
        n2="Standard",
        d2="Gói 90 ngày linh hoạt",
        p2=749000.0,
        day2=90,
        mw2=5,
        n3="Premium",
        d3="180 ngày, không giới hạn buổi/tuần",
        p3=1299000.0,
        day3=180,
        mw3=None,
        n4="VIP",
        d4="365 ngày đầy đủ tiện ích",
        p4=2499000.0,
        day4=365,
        mw4=None,
    )
    conn.execute(stmt)


def downgrade() -> None:
    pass
