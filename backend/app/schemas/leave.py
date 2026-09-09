from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class LeaveCreate(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: str


class LeaveUpdate(BaseModel):
    status: str


class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    status: str
    applied_at: datetime
    reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True