from pydantic import BaseModel
from datetime import time, datetime
from typing import Optional


class ShiftCreate(BaseModel):
    shift_name: str
    start_time: time
    end_time: time
    status: bool = True


class ShiftUpdate(BaseModel):
    shift_name: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[bool] = None


class ShiftResponse(BaseModel):
    id: int
    shift_name: str
    start_time: time
    end_time: time
    status: bool
    created_at: datetime

    class Config:
        from_attributes = True