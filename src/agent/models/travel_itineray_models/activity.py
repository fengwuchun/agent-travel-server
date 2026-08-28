from pydantic import BaseModel, Field

# ============================================================
# 每日活动
# ============================================================


class Activity(BaseModel):
    # 活动或景点名称
    name: str = Field(description="活动或景点名称，例如：成都大熊猫繁育研究基地")

    # 活动详细描述
    description: str = Field(description="活动或景点的详细介绍")

    # 开始时间
    start_time: str | None = Field(
        default=None, description="活动预计开始时间，例如：08:00"
    )

    # 结束时间
    end_time: str | None = Field(
        default=None, description="活动预计结束时间，例如：10:00"
    )

    # 活动持续时间
    duration: str | None = Field(
        default=None, description="预计活动持续时间，例如：2小时"
    )

    # 活动费用
    cost: float = Field(
        default=0, description="该活动预计产生的总费用，例如景点门票，单位：人民币"
    )

    # 活动注意事项
    tips: list[str] = Field(
        default_factory=list,
        description="该活动相关的注意事项，例如：建议提前预约、建议早上前往",
    )
