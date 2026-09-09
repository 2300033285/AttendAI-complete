from sqlalchemy import Column, Integer, String, Date, DateTime, Text
from sqlalchemy.sql import func

from app.database import Base


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(Integer, nullable=False, index=True)

    leave_type = Column(String(50), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    reason = Column(Text, nullable=False)

    status = Column(
        String(20),
        nullable=False,
        default="Pending",
    )

    applied_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    reviewed_at = Column(
        DateTime,
        nullable=True,
    )