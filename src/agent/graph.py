from langgraph.graph import StateGraph,START,END
from agent.states.travel_state import TravelState
from langgraph.checkpoint.memory import MemorySaver
from agent.nodes.parse_request_node import parse_request_node
from agent.nodes.collect_infomation_node import collection_info_node
from agent.nodes.plan_itineray_node import plan_itinerary_node
from agent.utils.json_util import JsonUtil
from agent.nodes.optimize_itinerary_node import optimize_itinerary_node
from agent.nodes.plan_check_node import plan_check_node

from agent.nodes.human_approval_node import human_approval_node
from agent.nodes.analyze_human_feedback_node import analyze_human_feedback_node
from agent.nodes.update_travel_request_node import update_travel_request_node

# plan_check检测轮数
check_plan_total_numbers = 1


memory_saver = MemorySaver()
def parse_request(state:TravelState):

    result = parse_request_node(state)
    print("=======Parse Request========")
    print(result)
    return result


def collect_infomation(state:TravelState):
    result = collection_info_node(state)
    print("=======收集的 Infomation========")
    print(result)
    return result


def plan_itinerary(state:TravelState):
   
    result = plan_itinerary_node(state)
    print("=======plan Itinerary 旅游指南========")
    JsonUtil.print_json(result["itinerary"])
    return result


def optimize_itinerary(state:TravelState):
    result = optimize_itinerary_node(state)
    print("=======optimize_itinerary 优化旅游指南========")
    JsonUtil.print_json(result["itinerary"])
    return result


def check_plan(state:TravelState):
     result = plan_check_node(state)
     auto_optimization_count = state.get("auto_optimization_count",0)
     print("=======Check Plan 检测方案========")
     JsonUtil.print_json(result["check_plan_result"])
     print("=====检测计划不合理执行次数========")
     print(auto_optimization_count)
     return result

def human_approval(state:TravelState):
     result = human_approval_node(state)
     return result

def analyze_human_feedback(state:TravelState):
    analyze =  analyze_human_feedback_node(state)
    return analyze
   

def update_travel_request(state:TravelState):
    result = update_travel_request_node(state)
    return result

def finalize(state:TravelState):
    itinerary = state["itinerary"]
    print("=====最终行程========")
    JsonUtil.print_json(itinerary)
    return {"finalize" : itinerary}


def is_approval_continue(state:TravelState):
    user_approval = state["user_approved"]
    print("=====用户审批========")
    print(user_approval)
    isApproval = user_approval.approval
    print("=====用户是否通过审批========")
    JsonUtil.print_json(isApproval)
    if isApproval:
         return "finalize"
    else:
        # return "optimize_itinerary"
        return  "analyze_human_feedback"

def is_check_plan_continue(state:TravelState):
    check_plan_result = state.get("check_plan_result")
    auto_optimization_count = state.get("auto_optimization_count",0)
    print(check_plan_result.is_valid)
    if check_plan_result.is_valid:
        return "human_approval"

    if auto_optimization_count >= check_plan_total_numbers:
        return "human_approval"
    else:
        return "optimize_itinerary"

def is_update_travel_request_continue(state:TravelState):
       is_request_changed = state["is_request_changed"]
       print("=======Analyze Human Feedback 分析用户反馈是否发生改变========")
       print(is_request_changed)
       if is_request_changed == True:
           return "update_travel_request"
       else:
           return "optimize_itinerary"    

builder = StateGraph(TravelState)

builder.add_node(
    "parse_request" , parse_request
)

builder.add_node(
    "travel_collection_info" , collect_infomation
)

builder.add_node(
    "plan_itinerary" , plan_itinerary
)

builder.add_node(
    "optimize_itinerary" , optimize_itinerary
)

builder.add_node(
   "check_plan"  , check_plan
)

builder.add_node(
    "human_approval" , human_approval
)

builder.add_node(
    "analyze_human_feedback" , analyze_human_feedback
)

builder.add_node(
    "update_travel_request" , update_travel_request
)


builder.add_node(
    "finalize" , finalize
)


builder.add_edge(START,"parse_request")
builder.add_edge("parse_request","travel_collection_info")
builder.add_edge("travel_collection_info","plan_itinerary")
builder.add_edge("plan_itinerary","optimize_itinerary")
builder.add_edge("optimize_itinerary","check_plan")
builder.add_conditional_edges(
    "check_plan",
    is_check_plan_continue,
    {"human_approval": "human_approval", "optimize_itinerary": "optimize_itinerary"},
)
builder.add_conditional_edges(
    "human_approval",
    is_approval_continue,
    {"finalize": "finalize", "analyze_human_feedback": "analyze_human_feedback"},
)

builder.add_conditional_edges(
    "analyze_human_feedback",
    is_update_travel_request_continue,
    {"update_travel_request": "update_travel_request", "optimize_itinerary": "optimize_itinerary"},

)

builder.add_edge(
    "update_travel_request", "plan_itinerary"
)


builder.add_edge("finalize",END)

graph = builder.compile(checkpointer=memory_saver)
