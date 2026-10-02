from agent.database.database import SessionLocal
from agent.database.models.conversation import Conversation
from sqlalchemy import select

db = SessionLocal()

#添加
# conversation = Conversation(
#     user_id = 10004,
#     thread_id = 'thread_005',
#     title = '北京5日游'
# )

# db.add(conversation)
# db.commit()
# db.refresh(conversation)
# db.close()

#查询
conversations = db.query(Conversation).all()
print("查询结果")
for conversation in conversations:
    print("---------------------------")
    print(conversation.id, conversation.user_id, conversation.thread_id, conversation.title)

#修改
conversation = db.execute(
    select(Conversation).where(
        Conversation.thread_id == 'thread_005'
    )
).scalar_one_or_none()

if conversation:
    conversation.title = '西安5日游'
    db.commit()

print("修改结果")
conversations = db.query(Conversation).all()
for conversation in conversations:
    print("---------------------------")
    print(conversation.id, conversation.user_id, conversation.thread_id, conversation.title)

    #删除

    # conversation = db.execute(
    #     select(Conversation).where(
    #         Conversation.thread_id == 'thread_005'
    #     )
    # ).scalar_one_or_none()

    # db.delete(conversation)
    # db.commit()

    # print("删除结果")
    # conversations = db.query(Conversation).all()
    # for conversation in conversations:
    #     print("---------------------------")
    #     print(conversation.id, conversation.user_id, conversation.thread_id, conversation.title)
    
