from agent.states.travel_state import TravelState
from langgraph.types import interrupt
from agent.utils.json_util import JsonUtil
from agent.models.travel_human_approval import TravelHumanApproval
from agent.models.travel_restaurant_info import TravelRestaurantInfo,TravelRestaurantInfoList
from agent.models.travel_itineray_models.daily_plan import DailyPlan
from agent.models.travel_hotel_info import TravelHotelInfo,TravelHotelInfoList

def human_approval_node(state:TravelState) -> TravelState:
    print("==========进入 human_approval_node==========")
    itinerary = state["itinerary"]
    restaurant_info_list = state["restaurant_info"]
    hotel_info = state.get("hotel_info")
    is_hotel = state.get("is_recommand_hostels")
    print("======是否有酒店=======")
    print(is_hotel)
    #合并行程和美食信息
    itinerary.daily_plans = merge_all_info( itinerary.daily_plans, restaurant_info_list,hotel_info)
    
    approval = interrupt({
           "type" : "human_approval",
           "message" : "行程已规划完毕，是否批准？",
           "itinerary" : itinerary,
           "is_recommand_hostels" : is_hotel
         })

    print("=====用户审批结果========")
    JsonUtil.print_json(approval)

    user_approved = TravelHumanApproval(
        approval=approval["approved"], feedback=approval.get("feedback", "")
    )

    
     #人工审批的时候是将自动优化计数重置为0
    return {"user_approved": user_approved,"auto_optimization_count" : 0}


def merge_all_info(
    daily_plans: list[DailyPlan],
    restaurant_info_list: TravelRestaurantInfoList,
    travel_hotel_info_list: TravelHotelInfoList | None


):
    restaurant_map = {
        (restaurant.date, restaurant.activity): restaurant
        for restaurant in restaurant_info_list.restaurants
    }

    for daily_plan in daily_plans:
        for activity in daily_plan.activities:

            restaurant = restaurant_map.get(
                (daily_plan.date, activity.title)
            )

            if restaurant:
                activity.restaurant = restaurant

       # 酒店
    if travel_hotel_info_list:
        hotel_map = {
            hotel.date: hotel
            for hotel in travel_hotel_info_list.hotels
        }

        for daily_plan in daily_plans:
            hotel = hotel_map.get(daily_plan.date)

            if hotel:
                daily_plan.hotel = hotel            

    return daily_plans
