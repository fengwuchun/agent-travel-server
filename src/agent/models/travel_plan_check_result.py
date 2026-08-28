from pydantic import BaseModel, Field

class TravelPlanCheckResult(BaseModel):
    """
    旅行计划检查结果
    """

    is_valid: bool = Field(
         description="旅行方案是否合理"
    )

    problems: list[str] = Field(
        default_factory=list,
        description="旅行方案不合理的方面"
    )

    suggestions: list[str] = Field(
        default_factory=list,
        description="针对不合理方面进行优化"
    )


