from agent.states.travel_state import TravelState
from agent.nodes.llm_node import llm
from agent.models.travel_itinerary import TravelItinerary
import time
from openai import LengthFinishReasonError

def plan_itinerary_node(state:TravelState) -> TravelState:
      print("========State========")
      print(state)
      request = state["travel_request"]  # TravelRequest 对象
      collection_info = state["travel_collection_info"] # TravelCollectionInfo 对象
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
               3. 严格按照结构化数据中的Field 中description 要求进行生成，每个活动的 description 不超过 20 个汉字。
               4. 每天安排 2~3 个主要行程，行程不包括吃饭。
               5. 每个行程说明开始时间，结束时间，使用简短描述，避免长篇介绍 
               6. 每个活动只填写必要信息，避免长篇介绍。
       """
      # 5. daily_plans 的数量必须等于 {request.duration},不能多一天，也不能少一天
      # 6. daily_plans 必须恰好包含 {expected_days} 天。

      # struct_llm = llm.with_structured_output(
      #    TravelItinerary,
      # )
      # print("========struct_llm========\n")
      # print(struct_llm)

      

      # print("========== Prompt 长度 ==========")
      # print(len(prompt))
      # result = struct_llm.invoke(prompt)

      
      # print("========Plan Itinerary reusult========\n")
      # print(result)

      # print("======== 每日计划数量 ========")
      # print(len(result.daily_plans))


      print("======= 测试普通模型 =======", flush=True)

      try:
         start = time.time()
         normal_result = llm.invoke(prompt)
         print("普通模型成功", flush=True)
         print("耗时:", round(time.time() - start, 2), "秒")
         print("输出字符数:", len(normal_result.content), flush=True)
      except Exception as e:
         print("普通模型失败:", repr(e), flush=True)

         print("======= 测试结构化模型 =======", flush=True)

      try:
         struct_llm = llm.with_structured_output(TravelItinerary)
         start = time.time()
         struct_result = struct_llm.invoke(prompt)
         print("结构化模型成功", flush=True)
         print("耗时:", round(time.time() - start, 2), "秒")
         return {"itinerary":struct_result}

      except LengthFinishReasonError as e:
         print("结构化模型达到输出长度上限:", repr(e), flush=True)
         raise
      except Exception as e:
         print("结构化模型失败:", repr(e), flush=True)
         raise


      # print("======== 普通模型调用开始 ========", flush=True)

      # result = llm.invoke(prompt)

      # print("======== 普通模型调用结束 ========", flush=True)
      # print("返回类型：", type(result), flush=True)
      # print("返回内容：", result.content, flush=True)
      # print("响应元数据：", result.response_metadata, flush=True)

      return {"itinerary":result}
