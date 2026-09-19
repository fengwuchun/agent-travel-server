from pydantic import BaseModel, Field
#推荐餐厅
class TravelRestaurantInfo(BaseModel):
       
       date: str = Field(description="推荐日期")
       activity: str = Field(description="对应的旅游景点或活动")
       meal_time: str = Field(description="建议用餐时间，例如午餐、晚餐")
       name: str = Field(description="餐厅名称")
       recommended_dishes: list[str] = Field(
              description="推荐菜品"
       )
       average_price: float = Field(
              description="人均价格，单位：人民币"
       )
       reason: str = Field(
              description="为什么适合当前景点和行程"
       )

class TravelRestaurantInfoList(BaseModel):
    restaurants: list[TravelRestaurantInfo] = Field(
        description="根据旅游行程推荐的餐厅列表"
    )        
