from agent.database.database import get_db
from sqlalchemy.orm import Session
from agent.database.models.conversation import Conversation
from sqlalchemy import select
def create_conversation(
        user_id: int,
        thread_id: str,
        title: str,
         db: Session,
       
)-> Conversation:
    conversation = Conversation(
        user_id = user_id,
        thread_id = thread_id,
        title = title
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation
   

def get_conversation_by_user_id(
        user_id: int,
        db: Session,
)-> list[Conversation]:
    conversations = db.execute(
        
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
    ).scalars().all()
    
    return conversations