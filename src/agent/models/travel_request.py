from dataclasses import dataclass
@dataclass

class TravelRequest:
        departure: str
        destination: str
        start_date: str
        end_date: str
        duration: int
        travelers: int
        budget: float
        preferences: list[str]
        service_requirements: list[str] 


        def travelRequestFormJson(travel_request_data:dict):
                travel_request = TravelRequest(
                        # departure=travel_request_data["departure"],
                        # destination=travel_request_data["destination"],
                        # start_date=travel_request_data["start_date"],
                        # end_date=travel_request_data["end_date"],
                        # duration=travel_request_data["duration"],
                        # travelers=travel_request_data["travelers"],
                        # budget=travel_request_data["budget"],
                        # preferences=travel_request_data["preferences"],
                        # service_requirements=travel_request_data["service_requirements"]

                         departure=travel_request_data["departure"],
                        destination=travel_request_data["destination"],
                        start_date=travel_request_data["start_date"],
                        end_date=travel_request_data["end_date"],
                        duration=travel_request_data["duration"],
                        travelers=travel_request_data["travelers"],
                        budget=travel_request_data["budget"],
                        preferences=travel_request_data["preferences"],
                        service_requirements=travel_request_data["service_requirements"]
                )
                return travel_request
        
              