from agent.states.travel_state import TravelState
from langgraph.types import interrupt
from agent.utils.json_util import JsonUtil
from agent.models.travel_human_approval import TravelHumanApproval

def human_approval_node(state:TravelState) -> TravelState:
    print("==========进入 human_approval_node==========")
    itinerary = state["itinerary"]
    approval = interrupt({
           "type" : "human_approval",
           "message" : "行程已规划完毕，是否批准？",
           "itinerary" : itinerary,
         })

    print("=====用户审批结果========")
    JsonUtil.print_json(approval)

    user_approved = TravelHumanApproval(
        approval=approval["approved"], feedback=approval.get("feedback", "")
    )

    
     #人工审批的时候是将自动优化计数重置为0
    return {"user_approved": user_approved,"auto_optimization_count" : 0}
