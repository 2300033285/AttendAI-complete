from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class ReferralCreate(BaseModel):
    opening_id: int
    candidate_name: str
    candidate_email: EmailStr
    candidate_phone: str
    resume_url: Optional[str] = None
    referral_message: Optional[str] = None


class ReferralUpdate(BaseModel):
    candidate_name: Optional[str] = None
    candidate_email: Optional[EmailStr] = None
    candidate_phone: Optional[str] = None
    resume_url: Optional[str] = None
    referral_message: Optional[str] = None
    status: Optional[str] = None


class ReferralResponse(BaseModel):
    id: int
    employee_id: int
    opening_id: int
    candidate_name: str
    candidate_email: EmailStr
    candidate_phone: str
    resume_url: Optional[str] = None
    referral_message: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)