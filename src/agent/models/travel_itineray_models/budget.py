from pydantic import BaseModel, Field

# ============================================================
# 整体旅行预算
# ============================================================


class Budget(BaseModel):
    # 交通总费用
    transportation: float = Field(
        default=0, description="整个旅行期间的交通预计总费用，单位：人民币"
    )

    # 住宿总费用
    accommodation: float = Field(
        default=0, description="整个旅行期间的住宿预计总费用，单位：人民币"
    )

    # 餐饮总费用
    meals: float = Field(
        default=0, description="整个旅行期间的餐饮预计总费用，单位：人民币"
    )

    # 景点门票总费用
    attractions: float = Field(
        default=0, description="整个旅行期间的景点门票及游览费用，单位：人民币"
    )

    # 其他费用
    other: float = Field(
        default=0, description="整个旅行期间其他无法分类的预计费用，单位：人民币"
    )

    # 旅行总费用
    total: float = Field(default=0, description="整个旅行预计总费用，单位：人民币")
