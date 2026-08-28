from pydantic import BaseModel, Field


# ============================================================
# 住宿信息
# ============================================================


class Accommodation(BaseModel):
    # 酒店或住宿名称
    name: str = Field(description="酒店或住宿名称，例如：成都太古里附近酒店")

    # 酒店位置
    location: str = Field(description="酒店所在位置或区域，例如：成都太古里附近")

    # 入住日期
    check_in: str = Field(description="酒店入住日期，格式建议为 YYYY-MM-DD")

    # 退房日期
    check_out: str = Field(description="酒店退房日期，格式建议为 YYYY-MM-DD")

    # 入住晚数
    nights: int = Field(description="入住晚数，例如：4")

    # 每晚价格
    price_per_night: float = Field(description="酒店每晚预计价格，单位：人民币")

    # 住宿总费用
    total_cost: float = Field(description="整个住宿期间的预计总费用，单位：人民币")

    # 酒店描述
    description: str | None = Field(
        default=None, description="酒店或住宿的详细说明，例如交通便利、靠近景点等"
    )
