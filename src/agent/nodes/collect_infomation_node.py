from agent.states.travel_state import TravelState
from agent.models.travel_collection_info import TravelCollectionInfo

def collection_info_node(state:TravelState)->TravelState:
    info = TravelCollectionInfo(
                   weather = ["晴","多云","雨"],
                   attractions=[],  #景点
                   hotels=[],
                   transportation=[],
                   rotues=[]
      )

    return {"travel_collection_info": info}
