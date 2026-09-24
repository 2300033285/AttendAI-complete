from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Float,
    Boolean,
    ForeignKey,
)
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    # Primary key
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Employee code
    employee_id = Column(
        String(20),
        unique=True,
        nullable=False
    )

    # Employee details
    first_name = Column(
        String(50),
        nullable=False
    )

    last_name = Column(
        String(50),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    phone = Column(
        String(15),
        nullable=False
    )

    department = Column(
        String(50),
        nullable=False
    )

    designation = Column(
        String(50),
        nullable=False
    )

    # Joining date
    joining_date = Column(
        Date,
        nullable=False
    )

    # Salary
    salary = Column(
        Float,
        nullable=False
    )

    # Employee active/inactive status
    status = Column(
        Boolean,
        default=True,
        nullable=False
    )

    # Shift assigned to employee
    shift_id = Column(
        Integer,
        ForeignKey("shifts.id"),
        nullable=True
    )

    # Record creation timestamp
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )