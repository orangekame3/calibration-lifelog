from fastapi import FastAPI, Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv
import os
from .db import initialize
from .dbmodel.chip import ChipDocument
from .dbmodel.chip_history import ChipHistoryDocument
# Load environment variables from .env file
load_dotenv()

app = FastAPI()
initialize()
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

@app.get("/health", dependencies=[Security(get_api_key)])
def health():
    """
    Health check endpoint
    """
    return {"status": "ok"}

@app.get("/chip/user/{username}/latest", dependencies=[Security(get_api_key)])
def get_current_chip(username: str):
    """
    Get the latest chip information by chip_id
    """
    chip = ChipDocument.get_current_chip(username=username)
    if not chip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chip with ID {username} not found"
        )
    return  chip.model_dump()


@app.get("/chip/{chip_id}/user/{username}/history", dependencies=[Security(get_api_key)])
def get_chip_history(username: str, chip_id: str, start_date: str, end_date: str):
    """
    Get the history of a chip by chip_id
    """
    chip_history = ChipHistoryDocument.find({
    "chip_id": chip_id,
    "username": username,
    "recorded_date": {
        "$gte": start_date,
        "$lte": end_date
    }
}).run()
    if not chip_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chip with ID {chip_id} not found"
        )
    return [history.model_dump() for history in chip_history]
