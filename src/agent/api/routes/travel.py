from fastapi import APIRouter
from agent.graph import graph
from agent.api.schemas import TravelCreateRequest,TravelHumanApproval,TravelAddRequest,ConversationResponse,MessageResponse,MessagePageResponse
from uuid import uuid4
from langgraph.types import Command
from fastapi import Depends
from agent.api.auth import get_current_user
from typing import Optional 
from agent.database.crud.conversation_crud import create_conversation, get_conversation_by_user_id
from agent.database.database import get_db
from sqlalchemy.orm import Session
from agent.database.crud.message_curd import add_message,get_message_by_thread_id
from agent.utils.json_util import json_str


travel_router = APIRouter()

@travel_router.post(
 "/travel/history/list",
 response_model = list[ConversationResponse]
                    )
def travel_history_list(
   current_user: dict = Depends(get_current_user),
   db: Session = Depends(get_db)
):
   conversations = get_conversation_by_user_id(
        user_id=current_user["user_id"],
        db=db
    )
   return conversations

@travel_router.post(
 "/travel/history/message",
 response_model = MessagePageResponse
)

def travel_history_message_list(
      thread_id:str,
      page:int,
      page_size:int,
      db: Session = Depends(get_db)
    ):
    result = get_message_by_thread_id(
         thread_id = thread_id,
         db = db,
         page = page,
         page_size = page_size,
         ) 
    return MessagePageResponse(
        msgList=result["items"],
        page=result["page"],
        page_size=result["page_size"],
        total=result["total"],
        total_pages=result["total_pages"],
        has_more=result["has_more"],
    )
     
    
    


@travel_router.post("/travel/create")
def create_travel(
    request: TravelCreateRequest,
    current_user: dict = Depends(get_current_user),
     thread_id: Optional[str] = None,  
      db: Session = Depends(get_db)     
      ):
    print("=========收到用户参数==========")
    print("=======用户id==========")
    print(current_user["user_id"])
    print("=========用户名==========")
    print(current_user["username"])
    print("=========用户参数==========")
    print(request.content)
   

    if thread_id is None:
        thread_id = str(uuid4())

        #插入数据库
        create_conversation(
            thread_id=thread_id,
            title=request.content,
            user_id=current_user["user_id"],
            db=db,
        )

       #数据库保存发送的消息
        add_message(
            thread_id=thread_id,
            role="user",
            content=request.content,
            state="parse_request",
            db=db
      )

   
    config = {
        "configurable" : {
            "thread_id" : thread_id
        }
    }
    result = graph.invoke({
        "messages" : [
            {
                "role" : "user",
                "content" : request.content
        }
      ]
    },
    config=config
    )

    print("=====行程规划结果======")
    print(result)
    #数据库保存结果
    msg = result["__interrupt__"]
    data = {
    "__interrupt__": [
        {
            "value": item.value
        }
        for item in msg
    ]
    }
    
    json_msg = json_str(data)

    add_message(
        thread_id=thread_id,
        role="assistant",
        content=json_msg,
        state="human_approval",
        db=db
    )
    return {"result" : result, "thread_id" : thread_id, "status" : "success"}

@travel_router.post("/travel/add_request")

def add_request(request: TravelAddRequest):
    thread_id = request.thread_id
    content = request.content
    print("=====收到用户添加的请求参数内容========")
    print(f"用户添加的请求参数内容是：{content}")
    print("=====用户thread_id==========")
    print(thread_id)

    config = {
        "configurable" : {
            "thread_id" : thread_id,
        }
    }
    result =  graph.invoke(
                 Command(resume={ 
                     "approved": True,
                     "travel_request_other": content
                     }),
                 config
                 )
    return {"result" : result, "thread_id" : thread_id, "status" : "success"}



@travel_router.post("/travel/approval")
def human_approval(
    request: TravelHumanApproval,
     db: Session = Depends(get_db) 

    ):
    thread_id = request.thread_id
    approval = request.approved
    config = {
        "configurable" : {
            "thread_id" : thread_id,
        }
    }
    print("=====收到用户审批参数========")
    print("=======thread_id==========")
    print(thread_id)
    print("=======approval==========")
    print(approval)
    print("=========审批内容==========")
    print(request.feedback)

    #数据库保存审批结果
    sql_content = request.feedback
    if approval:
     sql_content = "审批通过"
    add_message(
            thread_id=thread_id,
            role="user",
            content=sql_content,
            state="human_approval",
            db= db
              )
    
    result = graph.invoke(  
        Command(
               resume={
               "approved" : approval,
               "feedback" : request.feedback,
           }),
    config=config
    )

   
    print("=====审批后的回答======")
    print(result)
    if not approval:
      #数据库保存结果
        msg = result["__interrupt__"]
        data = {
            "__interrupt__": [
                {
                    "value": item.value
                }
                for item in msg
            ]
            }
            
        json_msg = json_str(data)
        
        add_message(
                thread_id=thread_id,
                role="assistant",
                content=json_msg,
                state="human_approval",
                db=db
            )

    return {"result" : result, "thread_id" : thread_id, "status" : "success"}