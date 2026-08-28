from pydantic import BaseModel,Field
from agent.models.travel_itineray_models.daily_plan import DailyPlan

# ============================================================
# 完整旅行指南
# ============================================================


class TravelItinerary(BaseModel):
           destination: str
           daily_plans: list[DailyPlan]


# # 旅行基本信息
# trip_info: TripInfo = Field(
#     description="本次旅行的基本信息，包括出发地、目的地、日期、人数、预算和偏好"
# )

# # 整个旅行的交通安排
# transportation: list[Transportation] = Field(
#     default_factory=list,
#     description="整个旅行期间的主要交通安排，包括往返交通和跨城市交通",
# )

# # 整个旅行的住宿安排
# accommodation: list[Accommodation] = Field(
#     default_factory=list, description="整个旅行期间的酒店或住宿安排"
# )

# # 每日详细行程
# daily_plans: list[DailyPlan] = Field(
#     default_factory=list, description="按照日期排列的每日详细旅行计划"
# )

# # 整体预算
# budget: Budget = Field(default_factory=Budget, description="整个旅行的费用预算汇总")

# # 旅行小贴士
# tips: list[str] = Field(
#     default_factory=list,
#     description="整个旅行期间的实用建议，例如天气、饮食、景点游览、安全等",
# )

# # 旅行备注
# notes: list[str] = Field(
#     default_factory=list,
#     description="整个旅行计划的补充说明，例如价格可能波动、需要提前预约等",
# )
