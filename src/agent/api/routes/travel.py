from fastapi import APIRouter
from agent.graph import graph
from agent.api.schemas import TravelCreateRequest,TravelHumanApproval,TravelAddRequest,ConversationResponse,MessageResponse,MessagePageResponse,SwitchConversationRequest
from uuid import uuid4
from langgraph.types import Command
from fastapi import Depends
from agent.api.auth import get_current_user
from typing import Optional 
from agent.database.crud.conversation_crud import create_conversation, get_conversation_by_user_id,delete_conversation_by_user_id
from agent.database.database import get_db
from sqlalchemy.orm import Session
from agent.database.crud.message_curd import add_message,get_message_by_thread_id,delete_message_by_thead_id
from agent.database.crud.travel_request_curd import get_travel_request_by_thread_id,update_travel_request,add_travel_request,delete_travel_request_by_thread_id
from agent.utils.json_util import json_str
from agent.database.models.travel_request_model import TravelRequestModel
from agent.models.travel_request import TravelRequest
from agent.database.crud.travel_state_curd import add_travel_state,update_travel_state,get_travel_state_by_thead_id,delete_travel_state_by_thread_id
import json



travel_router = APIRouter()

@travel_router.post(
 "/travel/history/delete/thread_id"
)
def delete_conversaton(
     thread_id:str,
     db: Session = Depends(get_db)
):
     delete_travel_state_by_thread_id(thread_id = thread_id, db = db)
     delete_travel_request_by_thread_id(thread_id = thread_id, db = db)
     delete_message_by_thead_id(thread_id = thread_id, db = db)
     isSuccess = delete_conversation_by_user_id(thread_id = thread_id, db = db)
     return isSuccess

@travel_router.get(
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

@travel_router.post("/travel/history/switch")
def switch_history(
    request: SwitchConversationRequest,
    db: Session = Depends(get_db)
):
    thread_id = request.thread_id

    travel_request_model = get_travel_request_by_thread_id(
        thread_id=thread_id,
        db=db
    )

    if travel_request_model is None:
        return {
            "thread_id": thread_id,
            "travel_request": None
        }

    travel_request = TravelRequest(
        departure=travel_request_model.departure,
        destination=travel_request_model.destination,
        start_date=travel_request_model.start_date,
        end_date=travel_request_model.end_date,
        duration=travel_request_model.duration,
        travelers=travel_request_model.travelers,
        budget=travel_request_model.budget,
        preferences=json.loads(
            travel_request_model.preferences
        ) if travel_request_model.preferences else [],
        service_requirements=json.loads(
            travel_request_model.service_requirements
        ) if travel_request_model.service_requirements else [],
    )

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    #查询节点状态
    travel_state =  get_travel_state_by_thead_id(thread_id = thread_id, db = db)
    if travel_state is None:   return None
    print("=======节点===========")
    print(travel_state.state)
         
    if travel_state.state == "finalize":
        result =  graph.update_state(
            config,
            {
                "travel_request": travel_request
            },
            as_node= "parse_request"
         )
        print("========回复节点数据==============")
        print(result)

    # 重新读取当前 thread_id 对应的 State
    print("=======更新后节点数据=========")
    state_snapshot = graph.get_state(config)

    print("========更新后的 travel_request========")
    print(state_snapshot.values.get("travel_request"))

    print("========更新后的 next========")
    print(state_snapshot.next)    

    return {
        "thread_id": thread_id,
        "travel_request": travel_request
    }
     
    
    


@travel_router.post("/travel/create")
def create_travel(
    request: TravelCreateRequest,
    current_user: dict = Depends(get_current_user),
    #  thread_id: Optional[str] = None,  
      db: Session = Depends(get_db)     
      ):
    thread_id = request.thread_id
    print("=========收到用户参数==========")
    print("=======用户id==========")
    print(current_user["user_id"])
    print("=========用户名==========")
    print(current_user["username"])
    print("=========用户参数==========")
    print(request.content)
    print("======传入的thread_id======")
    print(thread_id)
   

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

    #保存状态
    travel_state = get_travel_state_by_thead_id(thread_id = thread_id,db = db)
    if travel_state is None:
        add_travel_state(
            thread_id = thread_id,
            state = "parse_request",
            db = db
        )
    else:
        update_travel_state(
             thread_id = thread_id,
             state = "parse_request",
             db = db
        )

   
    config = {
        "configurable" : {
            "thread_id" : thread_id
        }
    }

    snapshot = graph.get_state(config)

    print("======= invoke 前的 checkpoint =======")
    print("thread_id:", thread_id)
    print("travel_request:", snapshot.values.get("travel_request"))
    print("next:", snapshot.next)


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

    is_exist_travel_request_key = result.get("travel_request")
    if is_exist_travel_request_key is None:
         return {"result" : result, "thread_id" : thread_id, "status" : "success"}

   
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

     #数据库保存 travel_request 
    query_model = get_travel_request_by_thread_id(thread_id,db=db)
    param_travel_request = result["travel_request"]
    print("=====  request_dict =========")
    print(param_travel_request)
    
    if query_model is None:
        add_travel_request(thread_id, param_travel_request, db=db)
    else:
        
        update_travel_request(thread_id,param_travel_request,db = db)

    #数据库状态更新 
    update_travel_state(
                thread_id = thread_id,
                state = "human_approval",
                db = db
            ) 
    
    return {"result" : result, "thread_id" : thread_id, "status" : "success"}

@travel_router.post("/travel/add_request")

def add_request(request: TravelAddRequest,db: Session = Depends(get_db)    ):
    thread_id = request.thread_id
    content = request.content
    print("=====收到用户添加的请求参数内容========")
    print(f"用户添加的请求参数内容是：{content}")
    print("=====用户thread_id==========")
    print(thread_id)

     #数据库保存发送的消息
    add_message(
        thread_id=thread_id,
        role="user",
        content=request.content,
        state="parse_request",
        db=db
    )

    #保存状态
    travel_state = get_travel_state_by_thead_id(thread_id = thread_id,db = db)
    if travel_state is None:
        add_travel_state(
            thread_id = thread_id,
            state = "parse_request",
            db = db
        )
    else:
        update_travel_state(
                thread_id = thread_id,
                state = "parse_request",
                db = db
        )

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
    is_exist_travel_request_key = result.get("travel_request")
    if is_exist_travel_request_key is None:
        return {"result" : result, "thread_id" : thread_id, "status" : "success"}

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

        #数据库保存 travel_request 
    query_model = get_travel_request_by_thread_id(thread_id,db=db)
    param_travel_request = result["travel_request"]
    print("===== 补充需求 request_dict =========")
    print(param_travel_request)
    
    if query_model is None:
        add_travel_request(thread_id, param_travel_request, db=db)
    else:
        
        update_travel_request(thread_id,param_travel_request,db = db)

    #数据库状态更新 
    update_travel_state(
                thread_id = thread_id,
                state = "human_approval",
                db = db
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

    #数据库状态更新
    trave_state = ""
    if not approval:
       trave_state = "human_approval"
    else:
       trave_state = "finalize"

    #数据库状态更新 
    update_travel_state(
                     thread_id = thread_id,
                     state = trave_state,
                     db = db
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