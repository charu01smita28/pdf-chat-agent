from fastapi import FastAPI
from dependencies import get_chat_agent 
from agents.api.endpoints import router as api_router

# Create FastAPI app
app = FastAPI()

# Include router with dependencies
app.include_router(api_router)
