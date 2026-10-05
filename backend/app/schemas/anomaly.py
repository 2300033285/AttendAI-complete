from pydantic import BaseModel
from typing import List


class Anomaly(BaseModel):
    attendance_id: int
    user_id: int
    status: str
    anomaly_type: str
    severity: str
    description: str
    source: str


class AnomalyResponse(BaseModel):
    total_anomalies: int
    anomalies: List[Anomaly]


class EmployeeAnomalyResponse(BaseModel):
    employee_id: int
    total_anomalies: int
    attendance_anomalies: List[Anomaly]
    leave_anomalies: dict
    referral_anomalies: dict