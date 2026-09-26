from agent.states.travel_state import TravelState
from agent.nodes.llm_node import llm
from agent.models.travel_request import TravelRequest
from agent.models.travel_request_patch import TravelRequestPatch
from agent.utils.json_util import JsonUtil
def analyze_human_feedback_node(state: TravelState):
      user_approved =  state["user_approved"]
      content = user_approved.feedback
      print("=======用户反馈内容：=======")
      print(content)
      request = state["travel_request"]

      prompt = f"""
                    你是一名旅游需求分析助手。

            请根据【用户反馈】，判断用户是否修改了当前的 TravelRequest，并提取明确修改的字段。

            【用户反馈】
            {content}

            【当前需求】
            出发地：{request.departure}
            目的地：{request.destination}
            开始日期：{request.start_date}
            结束日期：{request.end_date}
            天数：{request.duration}
            人数：{request.travelers}
            预算：{request.budget}
            偏好：{request.preferences}
            服务需求：{request.service_requirements}

          【service_requirements】
           - service_requirements：用户需要的旅游服务，例如 hotel、restaurant、weather、transportation
           - 如果用户明确提出酒店、住宿、入住酒店、推荐酒店、帮我找酒店、酒店推荐等需求，必须返回 ["hotel"]
           - 如果用户明确提出餐厅、美食、吃饭、推荐餐厅等需求，返回 ["restaurant"]
           - 如果同时提出酒店和餐厅，返回 ["hotel", "restaurant"]
           - 如果没有提出住宿或餐饮需求，返回 null
    
            【规则】

            1. 只有用户明确修改的内容才进行映射。
            2. 未提及或无法确定的字段返回 None。
            3. 不要根据常识或上下文猜测用户意图。
            4. 仅修改具体景点、酒店、交通、行程顺序等内容，不属于 TravelRequest 修改。
            5. 用户明确修改“天数”时，只返回新的 duration，日期计算由程序处理。
            6. 例如：“改成3天” → duration=3。
            7. 例如：“第二天不要去熊猫基地，换成青城山” → 不修改 TravelRequest 字段。

            请返回结构化结果。

    """
      struct_llm = llm.with_structured_output(
        TravelRequestPatch
      )

      patch = struct_llm.invoke(prompt)
      print("=======用户反馈分析转换成json格式：=======")
      print(patch)
      JsonUtil.print_json(patch)

      request_changed = just_requst_change(request,patch)
      is_request_changed:bool | None
      is_service_requirements_change = False

      if  isinstance(request_changed,dict):
           is_request_changed = request_changed.get("change",None)
           if (request_changed.get("key") == "service_requirements"
               and  "hotel" in request_changed.get("value",[])):
                is_service_requirements_change = True
                request.service_requirements = patch.get("service_requirements")
                   
      if request_changed == None:
           is_request_changed = False

      print("======新的request需求=======")
      print(request)     

      return {
           "is_request_changed" : is_request_changed,
           "travel_request_patch" : patch,
           "is_recommand_hostels" : is_service_requirements_change,
           "travel_request" : request
             }
    
    

def just_requst_change(request: TravelRequest, new_request: TravelRequestPatch):

       for key, value in new_request.items():

        # 用户没有修改这个字段
        if value is None:
            continue

        old_value = getattr(request, key, None)

        print(
            f"=====字段：{key}，"
            f"旧值：{old_value!r}，"
            f"新值：{value!r}====="
        )

        if old_value != value:
             if key == "service_requirements" and "hotel" not in old_value :
                  return {"key":"service_requirements","value":value,"change":True}  
               
             return {"key":key,"value":value,"change":True} 

        return {"key":key,"value":old_value,"change":False}
            
     
    
      