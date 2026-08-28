from pydantic import BaseModel, Field

# ============================================================
# 旅行基本信息
# ============================================================


class TripInfo(BaseModel):
    # 出发城市
    departure: str = Field(description="旅行出发城市，例如：深圳")

    # 目的地城市
    destination: str = Field(description="旅行目的地城市，例如：成都")

    # 旅行开始日期
    start_date: str = Field(
        description="旅行开始日期，格式建议为 YYYY-MM-DD，例如：2026-09-01"
    )

    # 旅行结束日期
    end_date: str = Field(
        description="旅行结束日期，格式建议为 YYYY-MM-DD，例如：2026-09-05"
    )

    # 旅行天数
    days: int = Field(description="旅行总天数，例如：5")

    # 出行人数
    travelers: int = Field(description="本次旅行的出行人数，例如：2")

    # 用户预算
    budget: float = Field(
        description="用户为本次旅行设置的预算上限，单位：人民币，例如：4000"
    )

    # 用户旅行偏好
    preferences: list[str] = Field(
        default_factory=list,
        description="用户的旅行偏好，例如：自然风光、大熊猫、美食、温泉",
    )














