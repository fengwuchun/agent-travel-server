from pydantic import BaseModel

class TravelHumanApproval(BaseModel):
       approval:bool 
       feedback:str = ""