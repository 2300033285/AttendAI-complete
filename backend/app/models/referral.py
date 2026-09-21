from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.sql import func

from app.database import Base


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Employee who submitted the referral
    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    # Job opening for which the candidate is referred
    opening_id = Column(
        Integer,
        ForeignKey("openings.id"),
        nullable=False
    )

    # Candidate details
    candidate_name = Column(
        String(100),
        nullable=False
    )

    candidate_email = Column(
        String(100),
        nullable=False
    )

    candidate_phone = Column(
        String(15),
        nullable=False
    )

    # Optional resume link
    resume_url = Column(
        String(500),
        nullable=True
    )

    # Optional message from referring employee
    referral_message = Column(
        Text,
        nullable=True
    )

    # Referral processing status
    status = Column(
        String(20),
        nullable=False,
        default="Pending"
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        nullable=True,
        onupdate=func.now()
    )