from fastapi import APIRouter
from agent.graph import graph
from agent.api.schemas import TravelCreateRequest,TravelHumanApproval,TravelAddRequest
from uuid import uuid4
from langgraph.types import Command

travel_router = APIRouter()


@travel_router.post("/travel/create")
def create_travel(request: TravelCreateRequest):
    thread_id = str(uuid4())
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
    return {"result" : result, "thread_id" : thread_id, "status" : "success"}

@travel_router.post("/travel/add_request")

def add_request(request: TravelAddRequest):
    thread_id = request.thread_id
    content = request.content
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
def human_approval(request: TravelHumanApproval):
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
    result = graph.invoke(  
        Command(
               resume={
               "approved" : approval,
               "feedback" : request.feedback,
           }),
    config=config
    )
    return {"result" : result, "thread_id" : thread_id, "status" : "success"}