
from agent.states.travel_state import TravelState
from agent.nodes.llm_node import llm
from agent.models.travel_request import TravelRequest
from agent.models.travel_hotel_info import TravelHotelInfo,TravelHotelInfoList



def hotel_info_node(state:TravelState) -> TravelState:
     itinerary = state["itinerary"]
     request = state["travel_request"]

     prompt = f"""
        请根据【用户需求】和【旅游行程】，为行程中的每一天推荐合适的酒店。
       
             【用户需求】
             {request}
       
             【旅游行程】
             {itinerary}
       
             【要求】
            1. 根据每天最后一个有效行程，就近推荐酒店。
            2. 最后一天不需要推荐酒店，因为用户当天需要返程。
            3. 如果当天最后一个活动是“返程准备”“返回出发地”等离开行程，则不作为酒店推荐依据。
            4. 根据用户的预算、人数、目的地等需求，选择合适的酒店。
            5. 酒店名称必须是具体的酒店名称，不要输出“附近酒店”“某某区域酒店”等泛化名称。
            6. room_price 表示每晚房间价格，单位为人民币。
            7. reason 说明推荐该酒店的原因，例如距离当天最后一个行程较近、交通方便等。
            8. 严格按照 TravelHotelInfoList 的结构化格式输出。

        """
     struct_output = llm.with_structured_output(TravelHotelInfoList)
     result = struct_output.invoke(prompt)
     return {"hotel_info" : result}


      

