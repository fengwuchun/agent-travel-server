from pydantic import BaseModel, Field

# ============================================================
# 每日预算
# ============================================================


class DailyBudget(BaseModel):
    # 当天交通费用
    transportation: float = Field(
        default=0, description="当天所有交通产生的预计费用，单位：人民币"
    )

    # 当天住宿费用
    accommodation: float = Field(
        default=0, description="当天住宿产生的预计费用，单位：人民币"
    )

    # 当天餐饮费用
    meals: float = Field(
        default=0, description="当天所有餐饮产生的预计费用，单位：人民币"
    )

    # 当天景点门票费用
    attractions: float = Field(
        default=0, description="当天景点门票等游览费用，单位：人民币"
    )

    # 其他费用
    other: float = Field(
        default=0, description="当天无法归类到其他类别的费用，单位：人民币"
    )

    # 当天总费用
    total: float = Field(default=0, description="当天所有费用的总和，单位：人民币")
