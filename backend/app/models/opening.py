from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Opening(Base):
    __tablename__ = "openings"

    id = Column(Integer, primary_key=True, index=True)

    job_title = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    employment_type = Column(String(50), nullable=False)

    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    experience = Column(String(50), nullable=False)

    status = Column(String(20), nullable=False, default="Open")

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