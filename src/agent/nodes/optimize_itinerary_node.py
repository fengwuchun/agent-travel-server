from agent.states.travel_state import TravelState
from agent.nodes.llm_node import llm
from agent.models.travel_itinerary import TravelItinerary
from agent.models.travel_plan_check_result import TravelPlanCheckResult
from agent.models.travel_human_approval import TravelHumanApproval


def optimize_itinerary_node(state:TravelState) -> TravelState:
    request = state["travel_request"]  # TravelRequest 对象
    collection_info = state["travel_collection_info"] # TravelCollectionInfo 对象
    itinerary = state["itinerary"]

    # 判断自动化执行次数
    count = state.get("auto_optimization_count", 0)

    # 判断是否有check_plan_result
    plan_check_result = state.get("check_plan_result")

    if plan_check_result:
        problems = plan_check_result.problems
        suggestions = plan_check_result.suggestions
        is_valid = plan_check_result.is_valid
        if not plan_check_result.is_valid:
            count += 1
    else:
        is_valid = True
        problems = []
        suggestions = []

    user_approval= state.get("user_approved")
    user_suggestions = ""
    if user_approval:
        if not user_approval.approval:
            user_suggestions = user_approval.feedback

    prompt = f"""
            你是一名专业的旅游规划师。

            你的任务不是重新生成一个旅行方案，而是：
            **基于当前旅行方案进行检查，并在发现问题时进行优化。**

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

         ====================
        【上一轮方案检查结果】
        ====================

        上一轮检查是否通过：
        {is_valid}

        发现的问题：
        {problems}

        优化建议：
        {suggestions}

         如果上一轮检查未通过，请优先解决上述问题。

        不要忽略这些问题，也不要仅仅重复当前旅行方案。

         ==================== 

        ====================
        【用户最新修改意见】
        ====================

        {user_suggestions}

        这是用户在人工审批阶段提出的最新修改要求。

        【最高优先级规则】

        如果用户最新修改意见与原始旅行偏好、当前旅行方案或之前的优化建议发生冲突：

        必须以用户最新修改意见为准。

        例如：

        如果用户说：
        “我不想去看大熊猫了”

        则必须：
        1. 删除所有大熊猫相关景点和活动。
        2. 不得安排熊猫基地。
        3. 不得安排卧龙熊猫相关活动。
        4. 不得为了满足原始“大熊猫”偏好而重新加入熊猫相关内容。
        5. 可以使用其他自然风光景点替代。
        6. 后续优化过程中也必须遵守这一修改。

        如果用户最新意见为空，则不需要进行人工修改。

        ====================
            【优化要求】
        ====================

            请逐项检查当前旅行方案：

            1. 检查每天行程是否过于紧凑。
            2. 检查景点之间的路线是否合理。
            3. 检查是否存在不必要的往返。
            4. 检查每天安排的景点数量是否合理。
            5. 检查是否符合用户的旅行偏好。
            6. 检查是否存在重复景点或重复活动。
            7. 检查景点顺序是否需要调整。
            8. 检查是否需要为交通、用餐和休息预留时间。
            9. 检查是否存在明显不合理的行程安排。
            10. 检查行程是否符合用户的预算和旅行日期。
            
            

            ====================
            【必须执行优化】
            ====================

            请不要简单复制当前旅行方案。

            如果发现任何不合理的地方，必须直接修改旅行方案。

            例如：

            - 如果存在重复景点，应删除或替换。
            - 如果一天安排过于紧凑，应减少或调整活动。
            - 如果景点顺序不合理，应重新排序。
            - 如果存在明显的往返路线，应调整景点安排。
            - 如果某些活动与用户偏好不符，应优先替换为更符合用户偏好的活动。

            请尽量保留用户喜欢的核心景点。

            不要改变：
            - 目的地
            - 开始日期
            - 结束日期

            不要凭空编造旅游信息。

            即使当前方案整体合理，也请检查是否存在可以进行的小幅优化。

            最终只输出**完整的优化后的旅行方案**，
            并严格按照 TravelItinerary 的结构输出。
            """

    llm_sructurd = llm.with_structured_output(TravelItinerary)

    result = llm_sructurd.invoke(prompt)

    return {"itinerary": result,"auto_optimization_count" : count}
