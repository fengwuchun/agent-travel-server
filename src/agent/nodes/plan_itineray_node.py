from agent.states.travel_state import TravelState
from agent.nodes.llm_node import llm
from agent.models.travel_itinerary import TravelItinerary

def plan_itinerary_node(state:TravelState) -> TravelState:
    print("========State========")
    print(state)
    request = state["travel_request"]  # TravelRequest 对象
    collection_info = state["travel_collection_info"] # TravelCollectionInfo 对象

    prompt = f""" 
     你是一名专业的旅游规划师。

请根据用户的旅行需求以及已经收集到的旅游信息，生成一份完整但简洁的旅行计划。

【用户需求】
出发地：{request.departure}
目的地：{request.destination}
开始日期：{request.start_date}
结束日期：{request.end_date}
人数：{request.travelers}
预算：{request.budget}
偏好：{request.preferences}

【已收集的旅游信息】
天气：{collection_info.weather}
景点：{collection_info.attractions}
酒店：{collection_info.hotels}
交通：{collection_info.transportation}
路线：{collection_info.rotues}

【生成要求】

      1. 严格按照 TravelItinerary 结构生成结果。
      2. 只返回结构化数据，不要输出任何额外解释。
      3. 严格按照结构化数据中的Field 中description 要求进行生成
      3. 每天安排 2~3 个主要行程。
      4. 每个行程说明开始时间，结束时间，使用简短描述，避免长篇介绍 
   """

    struct_llm = llm.with_structured_output(
       TravelItinerary

    )
   #  print("========struct_llm========\n")
    print(struct_llm)

    result = struct_llm.invoke(prompt)
   #  print("========Plan Itinerary reusult========\n")
   #  print(result)

    return {"itinerary":result}
