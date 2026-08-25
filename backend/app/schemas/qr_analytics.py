from pydantic import BaseModel
from datetime import date


class QRAnalyticsResponse(BaseModel):

    total_scans: int

    present_scans: int

    other_status_scans: int

    attendance_percentage: float

    unique_employees: int

    average_scans_per_employee: float


class QRDailyAnalyticsResponse(BaseModel):

    scan_date: date

    total_scans: int

    present_scans: int

    other_status_scans: int


class QREmployeeAnalyticsResponse(BaseModel):

    employee_id: int

    total_scans: int

    present_scans: int

    other_status_scans: int