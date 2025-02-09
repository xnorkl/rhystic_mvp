from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from rhystic.api.routers import auth, users, pods, rtc
from rhystic.database import engine
from rhystic.api.models import user
import logging
import traceback

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rhystic API",
    description="REST API for Rhystic - A platform for remote table top gaming sessions.",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/v1/users", tags=["users"])
app.include_router(pods.router, prefix="/v1/pods", tags=["pods"])
app.include_router(rtc.router, prefix="/v1/rtc", tags=["rtc"])

load_dotenv()  # Load environment variables from .env file

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"Error processing request: {request.url}")
        logger.error(f"Error details: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise 