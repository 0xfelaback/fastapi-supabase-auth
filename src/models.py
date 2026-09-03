from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


class SignUpRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class SignUpResponse(BaseModel):
    id: str
    email: str
    email_confirmed_at: Optional[Union[str, datetime]] = None
    created_at: Union[str, datetime]
    updated_at: Optional[Union[str, datetime]] = None
    last_sign_in_at: Optional[Union[str, datetime]] = None
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
    email_confirmed_at: Optional[Union[str, datetime]] = None
    created_at: Union[str, datetime]
    updated_at: Optional[Union[str, datetime]] = None
    last_sign_in_at: Optional[Union[str, datetime]] = None
    phone: Optional[str] = None
    is_email_verified: bool = False
