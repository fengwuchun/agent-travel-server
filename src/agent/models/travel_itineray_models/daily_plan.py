from pydantic import BaseModel, Field
from agent.models.travel_itineray_models.daily_activity import DailyActivity



# ============================================================
# 每日行程
# ============================================================


class DailyPlan(BaseModel):
    # 日期
    date: str = Field(description="当天日期，格式建议为 YYYY-MM-DD，例如：2026-09-01")
    daily_title: str = Field(
        description="当天行程主题，例如：成都文化探索、自然风光体验,不要显示时间"
    )

    # 当天旅行主题
    theme: str = Field(
        description=''' 当天行程主题标签。
        必须根据当天 activities 总结，
        描述当天“主要做什么”。

        不允许直接复制或罗列用户 preferences。
        不能为空
        '''
    )

    # 活动
    activities: list[DailyActivity] = Field(
        default_factory=list, description="当天安排的活动或景点"
    )
