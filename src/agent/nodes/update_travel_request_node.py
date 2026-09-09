

from agent.states.travel_state import TravelState
from agent.models.travel_request import TravelRequest
from datetime import date, timedelta


def update_travel_request_node(state: TravelState) -> TravelState:
     travel_request_patch =  state["travel_request_patch"]
     travel_request = state["travel_request"]
     request_data = travel_request.__dict__.copy()
     patch_data = travel_request_patch
     for key, value in patch_data.items():
          if value is not None:
               request_data[key] = value

      # 4. 用户修改了天数
     if travel_request_patch.get("duration") is not None:
          request_data["end_date"] = calculate_end_date(
               request_data["start_date"],
               request_data["duration"]
          )

    # 5. 用户修改了开始日期
     elif travel_request_patch.get("start_date") is not None:
               request_data["end_date"] = calculate_end_date(
               request_data["start_date"],
               request_data["duration"]
        )          

     new_request = TravelRequest(**request_data)  
     print("=======更新后的TravelRequest：=======")  
     print(new_request)
      
     return {
          "travel_request" : new_request,
          "auto_optimization_count": 0,
          "travel_request_patch" : None
     }


def calculate_end_date(start_date: str, duration: int) -> str:
    start = date.fromisoformat(start_date)
    end = start + timedelta(days=duration - 1)
    return end.isoformat()


      

     