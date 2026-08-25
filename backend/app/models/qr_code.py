from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database import Base


class QRCode(Base):

    __tablename__ = "qr_codes"

    id = Column(Integer, primary_key=True, index=True)

    token = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )