from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
from uuid import UUID

router = APIRouter()

class PodCreate(BaseModel):
    name: str

class PodParticipant(BaseModel):
    id: UUID
    user_id: UUID
    joined_at: datetime
    left_at: datetime

class Pod(BaseModel):
    id: UUID
    name: str
    owner_id: UUID
    created_at: datetime
    participants: List[PodParticipant]

@router.get("")
async def list_pods():
    # Implementation here
    pass

@router.post("", status_code=201)
async def create_pod(pod: PodCreate):
    # Implementation here
    pass

@router.get("/{pod_id}")
async def get_pod(pod_id: UUID):
    # Implementation here
    pass

@router.post("/{pod_id}/join")
async def join_pod(pod_id: UUID):
    # Implementation here
    pass 