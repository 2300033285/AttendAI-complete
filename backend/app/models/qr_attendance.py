from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
import uuid

from app.database import Base


class QRAttendance(Base):

    __tablename__ = "qr_attendance"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
        index=True
    )

    qr_token = Column(
    String(255),
    index=True,
    nullable=False,
    default=lambda: str(uuid.uuid4())
)

    scanned_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    status = Column(
        String(50),
        default="Present",
        nullable=False
    )