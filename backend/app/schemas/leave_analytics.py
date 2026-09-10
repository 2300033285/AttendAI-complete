from datetime import date
from typing import List

from pydantic import BaseModel


class LeaveSummaryResponse(BaseModel):

    total_leaves: int

    approved_leaves: int

    rejected_leaves: int

    pending_leaves: int


class LeaveTypeSummary(BaseModel):

    leave_type: str

    count: int


class EmployeeLeaveSummary(BaseModel):

    employee_id: int

    leave_count: int


class MonthlyLeaveSummary(BaseModel):

    month: date

    leave_count: int