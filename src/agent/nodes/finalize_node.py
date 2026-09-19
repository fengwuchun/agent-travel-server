from agent.states.travel_state import TravelState
from agent.utils.json_util import JsonUtil
from agent.models.travel_restaurant_info import TravelRestaurantInfo,TravelRestaurantInfoList
from agent.models.travel_itineray_models.daily_plan import DailyPlan
def finalize_node(state:TravelState) -> TravelState:
         itinerary = state["itinerary"]
         print("=====最终行程========")
         print(itinerary)
         JsonUtil.print_json(itinerary)
        #  restaurant_info_list = state["restaurant_info"]
     
        #  #合并行程和美食信息
        #  itinerary.daily_plans = merge_all_info( itinerary.daily_plans, restaurant_info_list)
         return {"finalize" : itinerary}



  