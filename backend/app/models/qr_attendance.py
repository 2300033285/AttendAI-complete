from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.database import Base


class QRAttendance(Base):

    __tablename__ = "qr_attendance"

    # ==========================================
    # PRIMARY KEY
    # ==========================================

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # ==========================================
    # EMPLOYEE REFERENCE
    # ==========================================

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
        index=True
    )

    # ==========================================
    # QR TOKEN
    # ==========================================

    qr_token = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    # ==========================================
    # SCAN TIME
    # ==========================================

    scanned_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # ==========================================
    # ATTENDANCE STATUS
    # ==========================================

    status = Column(
        String(50),
        default="Present",
        nullable=False
    )