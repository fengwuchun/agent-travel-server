from types import SimpleNamespace

from openai import LengthFinishReasonError

from agent.models.travel_itinerary import TravelItinerary
from agent.models.travel_request import TravelRequest
from agent.nodes import plan_itineray_node


class FakeChatModel:
    def __init__(self):
        self.structured = False

    def with_structured_output(self, _schema):
        self.structured = True
        return self

    def bind(self, **kwargs):
        self.structured = True
        return self

    def invoke(self, _prompt):
        if self.structured:
            raise LengthFinishReasonError(completion=None)
        return SimpleNamespace(content='{"destination":"Tokyo","daily_plans":[]}')


def test_plan_itinerary_falls_back_when_structured_output_hits_length_limit(monkeypatch):
    fake_llm = FakeChatModel()
    monkeypatch.setattr(plan_itineray_node, "llm", fake_llm)

    state = {
        "travel_request": TravelRequest(
            departure="Shanghai",
            destination="Tokyo",
            start_date="2026-11-01",
            end_date="2026-11-05",
            duration=4,
            travelers=2,
            budget=12000,
            preferences=["food", "culture"],
            service_requirements=["hotel", "restaurant"],
        ),
        "travel_collection_info": None,
    }

    result = plan_itineray_node.plan_itinerary_node(state)

    assert isinstance(result["itinerary"], TravelItinerary)
    assert result["itinerary"].destination == "Tokyo"
    assert result["itinerary"].daily_plans == []
