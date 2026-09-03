from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from supabase import create_client
from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase_auth import User
from src.models import (
    SignUpRequest,
    LoginRequest,
    SignUpResponse,
    LoginResponse,
    UserProfileResponse,
)
import os
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL if SUPABASE_URL is not None else "",
    SUPABASE_KEY if SUPABASE_KEY is not None else "",
)

app = FastAPI()

security = HTTPBearer()


def datetime_to_string(dt):  # type: ignore
    """Convert datetime object to ISO format string, or return as-is if already string."""
    if dt is None:
        return None
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt  # type: ignore


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        return user_response.user  # type: ignore
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )


@app.get("/")
def read_root():
    return {"message": "FastAPI with Supabase Auth is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/auth/signup", status_code=status.HTTP_201_CREATED, response_model=SignUpResponse
)
def signup(request: SignUpRequest):
    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )

    try:
        response = supabase.auth.sign_up(
            {
                "email": request.email,
                "password": request.password,
            }
        )
        user_data = response.user
        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed"
            )
        return SignUpResponse(
            id=user_data.id,
            email=user_data.email if user_data.email is not None else "",
            email_confirmed_at=datetime_to_string(user_data.email_confirmed_at),
            created_at=(
                datetime_to_string(user_data.created_at)
                if user_data.created_at is not None  # type: ignore
                else ""
            ),  # pyright: ignore[reportArgumentType]
            updated_at=datetime_to_string(user_data.updated_at),
            last_sign_in_at=datetime_to_string(user_data.last_sign_in_at),
            phone=user_data.phone,
            is_email_verified=user_data.email_confirmed_at is not None,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest):
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
        )
        user_data = response.user
        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid login credentials",
            )
        user_response = SignUpResponse(
            id=user_data.id,
            email=user_data.email if user_data.email is not None else "",
            email_confirmed_at=datetime_to_string(user_data.email_confirmed_at),
            created_at=datetime_to_string(user_data.created_at),  # type: ignore
            updated_at=datetime_to_string(user_data.updated_at),
            last_sign_in_at=datetime_to_string(user_data.last_sign_in_at),
            phone=user_data.phone,
            is_email_verified=user_data.email_confirmed_at is not None,
        )
        return LoginResponse(
            access_token=response.session.access_token,  # type: ignore
            refresh_token=response.session.refresh_token,  # type: ignore
            expires_in=response.session.expires_in,  # type: ignore
            token_type="bearer",
            user=user_response,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login credentials"
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Invalid body or missing title"},
    )


@app.get("/public/info")
def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile", response_model=UserProfileResponse)
def protected_profile(user: User = Depends(get_current_user)):
    return UserProfileResponse(
        id=user.id,
        email=user.email if user.email is not None else "",
        email_confirmed_at=datetime_to_string(user.email_confirmed_at),
        created_at=datetime_to_string(user.created_at),  # type: ignore
        updated_at=datetime_to_string(user.updated_at),
        last_sign_in_at=datetime_to_string(user.last_sign_in_at),
        phone=user.phone,
        is_email_verified=user.email_confirmed_at is not None,
    )


@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(user: User = Depends(get_current_user)):
    try:
        supabase.auth.sign_out()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Logout failed"
        )
