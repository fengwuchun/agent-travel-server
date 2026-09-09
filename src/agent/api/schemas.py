from pydantic import BaseModel

class TravelCreateRequest(BaseModel):
    content:str

class TravelAddRequest(BaseModel):
    content:str
    thread_id: str



class TravelHumanApproval(BaseModel):
    approved:bool
    feedback:str = "" 
    thread_id: str
