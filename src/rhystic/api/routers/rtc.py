from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class ICEServer(BaseModel):
    urls: List[str]
    username: Optional[str] = None
    credential: Optional[str] = None

class PodConnection(BaseModel):
    ice_servers: List[ICEServer]
    offer: Optional[str] = None
    answer: Optional[str] = None
    candidates: Optional[List[dict]] = None 