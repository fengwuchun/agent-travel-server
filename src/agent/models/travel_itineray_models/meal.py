from pydantic import BaseModel, Field


# ============================================================
# 餐饮信息
# ============================================================


class Meal(BaseModel):
    # 餐饮类型
    meal_type: str = Field(description="餐饮类型，例如：早餐、午餐、晚餐")

    # 餐厅名称
    restaurant: str | None = Field(
        default=None, description="推荐餐厅名称，如果没有具体餐厅可以为空"
    )

    # 餐饮说明
    description: str | None = Field(
        default=None, description="餐饮安排的详细说明，例如：品尝当地特色川菜"
    )

    # 推荐菜品
    recommended_dishes: list[str] = Field(
        default_factory=list,
        description="推荐的当地特色菜品，例如：火锅、夫妻肺片、担担面",
    )

    # 人均费用
    cost_per_person: float | None = Field(
        default=None, description="预计人均餐饮费用，单位：人民币"
    )

    # 餐饮总费用
    total_cost: float = Field(default=0, description="本次餐饮预计总费用，单位：人民币")
