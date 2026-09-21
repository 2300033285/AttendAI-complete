from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class OpeningCreate(BaseModel):
    job_title: str
    department: str
    location: str
    employment_type: str
    description: str
    requirements: str
    experience: str
    status: str = "Open"


class OpeningUpdate(BaseModel):
    job_title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    experience: Optional[str] = None
    status: Optional[str] = None


class OpeningResponse(BaseModel):
    id: int
    job_title: str
    department: str
    location: str
    employment_type: str
    description: str
    requirements: str
    experience: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)