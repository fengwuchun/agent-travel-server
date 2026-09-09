from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
from agent.models.travel_request import TravelRequest
from agent.models.travel_request_patch import TravelRequestPatch

from agent.models.travel_collection_info import TravelCollectionInfo
from agent.models.travel_plan_check_result import TravelPlanCheckResult
from agent.models.travel_human_approval import TravelHumanApproval

class TravelState(TypedDict):
    messages: Annotated[list,add_messages]

    # departure:str   #开始行程
    # destination:str  #结束行程

    # start_date:str
    # end_date:str

    # travelers:int
    # budget:float
    # preferences:list[str]   #喜好

    travel_request:TravelRequest

    # 外部信息
    # weather:list
    # attractions:list  #吸引
    # hotels:list
    # transportation:list
    # rotues:list
    travel_request_patch: TravelRequestPatch | None

    travel_collection_info:TravelCollectionInfo

    itinerary: list  # 规划结果
    total_cost: float
    auto_optimization_count: int  # 自动优化次数
    user_revision_count: int  # 用户拒绝方案后重新要求优化了多少次
    check_plan_result: TravelPlanCheckResult

    user_approved:TravelHumanApproval

    is_request_changed:bool # 用户是否修改了当前的 TravelRequest
    
