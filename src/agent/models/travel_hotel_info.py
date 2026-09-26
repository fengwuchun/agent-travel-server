from pydantic import BaseModel, Field


class TravelHotelInfo(BaseModel):
    date: str = Field(
        description="入住日期，格式为 YYYY-MM-DD"
    )

    activity: str = Field(
        description="当天最后一个有效行程或活动名称"
    )

    name: str = Field(
        description="酒店名称"
    )

    room_price: float = Field(
        description="每晚房间预计价格，单位：人民币"
    )

    reason: str = Field(
        description="推荐该酒店的原因，例如距离当天最后一个行程较近、交通方便等"
    )


class TravelHotelInfoList(BaseModel):
    hotels: list[TravelHotelInfo] = Field(
        description="酒店推荐列表"
    )