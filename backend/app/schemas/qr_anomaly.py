from pydantic import BaseModel


class QRAnomalyResponse(BaseModel):
    employee_id: int
    total_scans: int
    anomaly: bool
    reason: str