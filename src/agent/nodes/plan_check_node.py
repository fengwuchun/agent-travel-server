from agent.states.travel_state import TravelState
from agent.models.travel_plan_check_result import TravelPlanCheckResult
from agent.nodes.llm_node import llm

def plan_check_node(state:TravelState) -> TravelState:
    request = state["travel_request"]  
    collection_info = state["travel_collection_info"] 
    itinerary = state["itinerary"]

    user_approval = state.get("user_approved")

    user_feedback = ""
    effective_preferences = request.preferences.copy()

    if user_approval and not user_approval.approval:
        user_feedback = user_approval.feedback
        if "大熊猫" in user_feedback:
              effective_preferences.remove("大熊猫")

  
    prompt = f"""
            你是一名专业的旅游规划师。

            你的任务不是重新生成一个旅行方案，而是：
            **基于当前旅行方案进行检查，并在发现问题时提出优化建议。**

            ====================
            【用户需求】
            ====================

            目的地：{request.destination}
            旅行天数{request.duration}
          
            ====================
            【当前旅行方案】
            ====================

            {itinerary}

            ====================
            【检查建议】
            ====================    

             1. 检查目的地是不是{request.destination}
             2. 检查旅行天数{request.duration} 
             
            """

    llm_struct = llm.with_structured_output(
        TravelPlanCheckResult
    )

    result = llm_struct.invoke(prompt)

    return {"check_plan_result" : result}
