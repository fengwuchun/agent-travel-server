import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from agent.states.travel_state import TravelState
from agent.models.travel_request import TravelRequest
from agent.nodes.llm_node import llm
from datetime import datetime, timedelta
from langgraph.types import interrupt
from agent.utils.message_until import MessageUntil
from langchain_core.messages import HumanMessage

def parse_request_node(state:TravelState) -> TravelState:
    messages = state["messages"]
    print("=======收到用户的描述：=======")
    print(messages)

    prompt = """
    你是一个旅游需求解析助手。

    请从用户的旅游请求中提取以下信息：

    - departure：出发地
    - destination：目的地
    - start_date：开始日期
    - end_date：结束日期
    - duration：旅行天数
    - travelers：旅行人数
    - budget：预算
    - preferences：旅行偏好

    请严格根据用户实际提供的信息进行提取，
    不要使用示例数据，不要根据示例进行猜测。

    如果用户没有提供某些信息，请根据 TravelRequest
    的字段要求处理。
    【特殊情况处理】
    1.如何用户没有日期，开始日期则从当天的后一天开始算，结束日期为开始日期加上旅行天数
    2.旅行人数如果没有说明具体人数默认为1人
    """
    #保存整个对话
    new_mesages = list(messages)
    struct_out = llm.with_structured_output(TravelRequest)
    while True:
        result = struct_out.invoke([{"role": "system", "content": prompt}, *new_mesages])
        print("=======用户描述转换成json格式：=======")
        print(result)
     
        print(isinstance(result, TravelRequest))
        result = TravelRequest(**result)
        print("=====转换后=====")
        print("=====结果是否为TravelRequest===")
        print(isinstance(result, TravelRequest))

        approval = interrupt_use(result)
        if not approval:
            print("===进入退出对话=====")
            break  #退出循环
        content = approval["travel_request_other"]
        print("=====补充的内容========")
        print(content)
        #重新解析
        #原始用户请求 + 补充内容
        new_mesages.append(HumanMessage(content=content))
        #回到循环开头再次结构化一下
      
           

    if result.travelers is None:
        result.travelers = 1

    if not result.start_date:
        result.start_date = (datetime.now() + timedelta(days=1)).strftime(
            "%Y-%m-%d"
        )

    duration = result.duration  

    if not result.end_date:
        result.end_date = (datetime.strptime(result.start_date, "%Y-%m-%d") + timedelta(days=duration-1)).strftime(
            "%Y-%m-%d"
        )  

    print("=====最后请求数据========")
    print(result)      

    # request = TravelRequest(
    #             departure= "深圳",
    #             destination= "成都",
    #             start_date= "2026-09-01",
    #             end_date= "2026-09-05",
    #             travelers= 2,
    #             budget= 4000,
    #             preferences=["自然风光","大熊猫"]
    #   )

    return {"travel_request": result}


def interrupt_use(result:TravelRequest):
    need_data = []
    if not result.destination:
        need_data.append(1)

    # if not result.departure:  
    #     need_data.append(2)  

    if not result.travelers:   
        need_data.append(3)

    if not result.duration:  
        need_data.append(4)

    if not result.budget:  
        need_data.append(5)  

    # if not result.preferences:   
    #     need_data.append(6)   

    # 1,3,4,5 必须参数

    required_fields = [1, 3, 4, 5]

    has_missing_required = any(
    i in need_data
    for i in required_fields
    )

    if has_missing_required:
        message_util = MessageUntil()
        msg = message_util.paser_request_need_msg_tip(need_data)
        print("======用户请求缺少参数，返回中断信息======")
        return interrupt(
            {
                "type": "travel_request",
                "message": msg,
                 
            }
        )
    else:
        print("======用户请求正常，返回False======")
        return False
