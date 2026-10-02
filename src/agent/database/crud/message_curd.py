from agent.database.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import select,func
from agent.database.models.message_model import MessageModel
def add_message(
        thread_id: str,
        role: str,
        content: str,
        state: str,
        db: Session,
)-> MessageModel:
    message = MessageModel(
        thread_id = thread_id,
        role = role,
        content = content,
        state = state
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message




def get_message_by_thread_id(
thread_id: str,
db: Session,
page: int = 1,   #第几页
page_size: int = 5,  #每页多少条
):
    offset = (page - 1) * page_size

    # 查询总数量
    total = db.scalar(
        select(func.count())
        .select_from(MessageModel)
        .where(MessageModel.thread_id == thread_id)
    )

    # 查询当前页数据
    messages = db.execute(
        select(MessageModel)
        .where(MessageModel.thread_id == thread_id)
        .order_by(MessageModel.created_at.desc())
        .offset(offset)
        .limit(page_size)
    ).scalars().all()

        #假设有12条数据，得到的是5条数据，  12, 11, 10, 9, 8
    #返回给前端需要倒转一下
    messages.reverse()

    # 计算总页数
    total_pages = (total + page_size - 1) // page_size

    return {
        "items": messages,
        "page": page, #第几页
        "page_size": page_size,  #每页多少条
        "total": total,    #总计多少条
        "total_pages": total_pages, #多少页
        "has_more": page < total_pages,  #是否还有数据
    }



    