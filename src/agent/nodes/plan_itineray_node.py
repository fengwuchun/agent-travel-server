import json
import time

from openai import LengthFinishReasonError

from agent.models.travel_itinerary import TravelItinerary
from agent.nodes.llm_node import llm
from agent.states.travel_state import TravelState


def _fallback_itinerary(destination: str) -> TravelItinerary:
    return TravelItinerary(destination=destination, daily_plans=[])


def plan_itinerary_node(state: TravelState) -> TravelState:
    print("========State========")
    print(state)
    request = state["travel_request"]
    expected_days = request.duration
    prompt = f""" 
         你是一名专业的旅游规划师。

         请根据用户的旅行需求以及已经收集到的旅游信息，生成一份完整但简洁的旅行计划。

         【用户需求】
         出发地：{request.departure}
         目的地：{request.destination}
         开始日期：{request.start_date}
         结束日期：{request.end_date}
         旅行天数：{request.duration}
         人数：{request.travelers}
         预算：{request.budget}
         偏好：{request.preferences}

         【生成要求】

               1. 严格按照 TravelItinerary 结构生成结果。
               2. 只返回结构化数据，不要输出任何额外解释。
               3. 严格按照结构化数据中的Field 中description 要求进行生成。
               4. 每天安排 2~3 个主要行程。
               5. 每个行程说明开始时间，结束时间，使用简短描述，避免长篇介绍 
               6. 行程之间必须按照时间顺序排列，例如：
                  不能出现第一个行程时间12：00，第二行程是9：00
               7. 每个活动只填写必要信息，避免长篇介绍。
               8. 只允许输出 JSON，不要输出 markdown 或说明文字。
               9. daily_plans 的数量必须恰好为 {expected_days}，不能多也不能少。
       """

    try:
        struct_llm = llm.with_structured_output(TravelItinerary)
        start = time.time()
        struct_result = struct_llm.invoke(prompt)
        print("结构化模型成功", flush=True)
        print("耗时:", round(time.time() - start, 2), "秒")
        return {"itinerary": struct_result}
    except LengthFinishReasonError as e:
        print("结构化模型达到输出长度上限:", repr(e), flush=True)
        retry_llm = llm.bind(max_tokens=1024)
        try:
            retry_result = retry_llm.with_structured_output(TravelItinerary).invoke(prompt)
            print("结构化模型重试成功", flush=True)
            return {"itinerary": retry_result}
        except LengthFinishReasonError as retry_error:
            print("结构化模型重试仍达到输出长度上限:", repr(retry_error), flush=True)
    except Exception as e:
        print("结构化模型失败:", repr(e), flush=True)

    print("结构化输出失败，返回安全的空旅行计划，避免 500 错误", flush=True)
    return {"itinerary": _fallback_itinerary(request.destination)}
