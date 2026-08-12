from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional


class EmployeeCreate(BaseModel):
    employee_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    department: str
    designation: str
    joining_date: date
    salary: float
    shift_id: Optional[int] = None


class EmployeeUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    department: str
    designation: str
    joining_date: date
    salary: float
    status: bool
    shift_id: Optional[int] = None


class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    department: str
    designation: str
    joining_date: date
    salary: float
    status: bool
    shift_id: Optional[int] = None

    class Config:
        from_attributes = True