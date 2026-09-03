from pydantic import BaseModel
from typing import Optional


class SignUpRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class SignUpResponse(BaseModel):
    id: str
    email: str
    email_confirmed_at: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None
    last_sign_in_at: Optional[str] = None
    phone: Optional[str] = None
    is_email_verified: bool = False


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    user: SignUpResponse


class UserProfileResponse(BaseModel):
    id: str
    email: str
    email_confirmed_at: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None
    last_sign_in_at: Optional[str] = None
    phone: Optional[str] = None
    is_email_verified: bool = False
