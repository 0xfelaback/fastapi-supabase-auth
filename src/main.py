from dotenv import load_dotenv
from supabase import create_client
from fastapi import FastAPI
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "FastAPI with Supabase Auth is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
