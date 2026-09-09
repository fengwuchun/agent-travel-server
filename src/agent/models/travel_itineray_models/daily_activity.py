from pydantic import BaseModel, Field

class DailyActivity(BaseModel):

    start_time: str | None = Field(
        default=None, description="活动预计开始时间，例如：08:00"
      
    )
    end_time: str | None = Field(
        default=None, description="活动预计结束时间，例如：10:00"
    ),
    title:str | None = Field(
        default=None, description="活动或景点名称，例如：成都大熊猫繁育研究基地，不要显示时间"
    )

    description: str = Field(description=
                             '''结合用户偏好说明该活动的特点，控制在20字以内''')