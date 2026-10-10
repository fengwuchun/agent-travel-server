
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from agent.database.models.travel_state_model import TravelStateModel
def add_travel_state(
         thread_id: str,
         state: str,
         db: Session,
)->TravelStateModel:

    model = TravelStateModel(
        thread_id = thread_id,
        state = state
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def update_travel_state(
         thread_id: str,
         state: str,
         db: Session,
):
   travel_state = get_travel_state_by_thead_id(thread_id,db)
   if travel_state is None: 
       return None
   travel_state.state = state
   db.commit()
   db.refresh(travel_state)
   return travel_state

def get_travel_state_by_thead_id(
      thread_id: str,  
       db: Session, 
):
      stmt = select(TravelStateModel).where(
        TravelStateModel.thread_id == thread_id
      )

      return db.execute(stmt).scalar_one_or_none()

def delete_travel_state_by_thread_id(
        thread_id: str,
        db: Session,
):
    travel_state = get_travel_state_by_thead_id(thread_id, db)

    if travel_state is None:
        return None

    db.delete(travel_state)
    db.commit()
    return travel_state

    
    
    


    