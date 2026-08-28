from pydantic import BaseModel,Field

# ============================================================
# 交通信息
# ============================================================


class Transportation(BaseModel):
    # 交通方式
    type: str = Field(
        description="交通方式，例如：飞机、高铁、地铁、公交、出租车、步行"
    )

    # 出发地点
    departure: str = Field(description="交通出发地点，例如：深圳宝安国际机场")

    # 到达地点
    destination: str = Field(description="交通目的地，例如：成都双流国际机场")

    # 交通耗时
    duration: str | None = Field(
        default=None, description="预计交通耗时，例如：2小时30分钟"
    )

    # 交通费用
    cost: float = Field(default=0, description="本次交通预计总费用，单位：人民币")

    # 交通说明
    description: str | None = Field(
        default=None, description="交通安排的详细说明，例如：建议乘坐早班飞机"
    )
