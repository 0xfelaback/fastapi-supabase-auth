from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from supabase import create_client
from fastapi import FastAPI, HTTPException, Request, status
from src.models import SignUpRequest, LoginRequest
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL if SUPABASE_URL is not None else "",
    SUPABASE_KEY if SUPABASE_KEY is not None else "",
)

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "FastAPI with Supabase Auth is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(request: SignUpRequest):
    if not request.email or not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )

    try:
        response = supabase.auth.sign_up(
            {"email": request.email, "password": request.password}
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/auth/login")
def login(request: LoginRequest):
    try:
        response = supabase.auth.sign_in_with_password(
            {"email": request.email, "password": request.password}
        )
        return response
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
