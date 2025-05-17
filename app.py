from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Get API key from environment variable
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable is not set")

# Define API key header
api_key_header = APIKeyHeader(name="X-API-Key")

# API key authentication dependency
def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """
    Validate API key from request header
    """
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key"
    )

@app.get("/", dependencies=[Security(get_api_key)])
def root():
    return {"message": "Hello World"}
