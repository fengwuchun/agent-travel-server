
from agent.states.travel_state import TravelState

def is_recomand_hotels_node(state:TravelState):
      request = state["travel_request"]
     
      is_need_hotel:bool
      if "hotel" in request.service_requirements:
           is_need_hotel = True
      else:
           is_need_hotel = False 
      print("=======酒店推荐==========")
      print(is_need_hotel)
      return {"is_recommand_hostels" : is_need_hotel}
     