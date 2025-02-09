from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from rhystic.api.routers import auth, users, pods, rtc

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