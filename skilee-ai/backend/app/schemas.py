from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ContractCreate(BaseModel):
    company_name: str
    description: str
    title: str


class ContractOut(BaseModel):
    id: int
    company_name: str
    description: str
    title: str
    subject: str
    required_trainers: int
    created_by: int
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationOut(BaseModel):
    id: int
    contract_id: int
    trainer_id: int
    cover_letter: str
    cv_url: str
    skills: str
    years_experience: int
    relevance_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationsTierResponse(BaseModel):
    tier: str
    applicant_count: int
    applicants: Optional[List[ApplicationOut]] = None


class SubscriptionUpdate(BaseModel):
    tier: str


class SubscriptionOut(BaseModel):
    tier: str
    start_date: datetime
    end_date: Optional[datetime]

    class Config:
        from_attributes = True


class AdminStats(BaseModel):
    total_users: int
    total_contracts: int
    total_applications: int
    revenue_inr: int
