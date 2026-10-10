
import json
from agent.database.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from agent.database.models.travel_request_model import TravelRequestModel
from agent.models.travel_request import  TravelRequest


def add_travel_request(
        # id:int,
        # thread_id : str,
        # departure:str,
        # destination: str,
        # start_date: str,
        # end_date:str,
        # duration:int,
        # travelers:int,
        # budget:float,
        # preferences:str,
        thread_id : str,
        travel_request:TravelRequest,
         db: Session,

) -> TravelRequestModel:

   model  = TravelRequestModel(
             thread_id = thread_id,
             departure = travel_request.departure,
             destination = travel_request.destination,
             start_date = travel_request.start_date,
             end_date = travel_request.end_date,
             duration = travel_request.duration,
             travelers = travel_request.travelers,
             budget = travel_request.budget,
             preferences = json.dumps( travel_request.preferences, ensure_ascii=False ),
             service_requirements = json.dumps( travel_request.service_requirements, ensure_ascii=False ),
   )

   db.add(model)
   db.commit()
   db.refresh(model)

   return model

def update_travel_request(
         thread_id: str, 
         travel_request:TravelRequest,
          db: Session,
   ):

    travel_request_model = get_travel_request_by_thread_id(thread_id,db) 
    if travel_request_model is None: return None 
    travel_request_model.departure = travel_request.departure
    travel_request_model.destination = travel_request.destination 
    travel_request_model.start_date = travel_request.start_date 
    travel_request_model.end_date = travel_request.end_date 
    travel_request_model.duration = travel_request.duration 
    travel_request_model.travelers = travel_request.travelers 
    travel_request_model.budget = travel_request.budget 
    travel_request_model.preferences = json.dumps( travel_request.preferences, ensure_ascii=False ) 
    travel_request_model.service_requirements = json.dumps( travel_request.service_requirements, ensure_ascii=False ) 
    db.commit() 
    db.refresh(travel_request_model)
    return travel_request_model

    
def get_travel_request_by_thread_id( 
        thread_id: str,
        db: Session, 
      
        ):
     """ 根据 thread_id 获取旅行需求 """ 
     stmt = select(TravelRequestModel).where( TravelRequestModel.thread_id == thread_id ) 
     return db.scalar(stmt)

def delete_travel_request_by_thread_id(
        thread_id: str,
        db: Session, 
):

    travel_request_model = get_travel_request_by_thread_id(thread_id,db) 
    if travel_request_model is None: return None 

    db.delete(travel_request_model)
    db.commit()
    return travel_request_model


    

    