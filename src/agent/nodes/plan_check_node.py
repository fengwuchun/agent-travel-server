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

            出发地：{request.departure}
            目的地：{request.destination}
            开始日期：{request.start_date}
            结束日期：{request.end_date}
            人数：{request.travelers}
            预算：{request.budget}
            偏好：{request.preferences}

            ====================
            【已收集的旅游信息】
            ====================

            天气：{collection_info.weather}
            景点：{collection_info.attractions}
            酒店：{collection_info.hotels}
            交通：{collection_info.transportation}
            路线：{collection_info.rotues}

            ====================
            【当前旅行方案】
            ====================

            {itinerary}

            ====================
            【检查建议】
            ====================

             1. 日期
             2. 景点数量
             3. 路线
             4. 行程强度
             5. 用户偏好
             6. 预算

            【原始用户偏好】
             {effective_preferences}

            【最新人工修改意见】
             {user_feedback}


            【优先级规则】

                原始用户需求只是初始需求。

                如果用户后续通过人工审批提出了修改意见，
                则最新人工修改意见优先级高于原始用户需求。

                例如：

                原始偏好：
                ["自然风光", "大熊猫"]

                最新人工修改意见：
                "我不想去看大熊猫了"

                那么最终有效偏好应该理解为：

                ["自然风光"]

                此时：

                - 不得因为没有大熊猫而判定方案不合理
                - 不得要求重新加入大熊猫基地
                - 不得要求加入卧龙熊猫相关景点
                - 不得因为没有满足“大熊猫”原始偏好而产生问题

            """

    llm_struct = llm.with_structured_output(
        TravelPlanCheckResult
    )

    result = llm_struct.invoke(prompt)

    return {"check_plan_result" : result}
