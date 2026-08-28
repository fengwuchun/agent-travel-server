from pydantic import BaseModel, Field


# ============================================================
# 每日行程
# ============================================================


class DailyPlan(BaseModel):
    # 日期
    date: str = Field(description="当天日期，格式建议为 YYYY-MM-DD，例如：2026-09-01")

    # 当天旅行主题
    theme: str = Field(
        description="当天行程的核心主题，用一句简短的中文概括当天主要活动。"
        "必须根据当天activities生成，不能直接复制用户preferences。"
        "例如：抵达成都与熊猫初体验、青城山自然探索、"
        "都江堰文化与夜景、成都历史文化与城市休闲、成都自由活动与返程。"
    )

    # 活动
    activities: list[str] = Field(
        default_factory=list, description="当天安排的活动或景点"
    )
