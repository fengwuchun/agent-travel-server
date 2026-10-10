from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class TravelCreateRequest(BaseModel):
    content:str
    thread_id: Optional[str] = None

class TravelAddRequest(BaseModel):
    content:str
    thread_id: str



class TravelHumanApproval(BaseModel):
    approved:bool
    feedback:str = "" 
    thread_id: str


class ConversationResponse(BaseModel):
    id: int
    thread_id: str
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class MessageResponse(BaseModel):
    id: int
    thread_id: str
    role: str
    content: str
    created_at: datetime
    state: str
    model_config = {
            "from_attributes": True
        }

class MessagePageResponse(BaseModel):
    msgList: list[MessageResponse] 
    page: int
    page_size: int
    total: int
    total_pages: int
    has_more: bool

class SwitchConversationRequest(BaseModel):
    thread_id: str     


    

