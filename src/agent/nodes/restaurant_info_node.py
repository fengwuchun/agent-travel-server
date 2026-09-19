from agent.states.travel_state import TravelState
from agent.models.travel_restaurant_info import TravelRestaurantInfo,TravelRestaurantInfoList
from agent.nodes.llm_node import llm


def restaurant_info_node(state:TravelState):
      itinerary = state["itinerary"]
      travel_request = state["travel_request"]

      prompt = f"""
      你是一名专业的成都旅游美食规划师。

      请根据【用户需求】和【旅游行程】，为行程中的用餐时间推荐合适的餐厅。

      【用户需求】
      {travel_request}

      【旅游行程】
      {itinerary}

      【要求】

      1. 必须逐天分析 daily_plans 中的 activities。
      2. 必须根据具体的景点或活动安排餐厅。
      3. 每条餐厅推荐必须明确对应一个 activity。
      4. 优先选择对应景点附近的餐厅。
      5. 根据活动时间判断午餐或晚餐。
      6. 每个适合用餐的活动推荐 1～2 家餐厅,不是美食。
      7. 推荐当地特色美食，推荐最多4种，并考虑用户预算。
      8. 不要生成“成都美食规划”“美食推荐”等泛化名称，name 必须是真实的具体餐厅名称。
      9. 不要把总预算、总消费等信息填写到 average_price。
      10. 如果无法确定真实餐厅信息，不要编造地址、评分等信息。

      【特别重要】

      你必须建立：

      景点/活动 → 用餐时间 → 餐厅

      例如：

      宽窄巷子游览
      → 晚餐
      → 某具体餐厅

      锦里古街体验
      → 晚餐/小吃
      → 某具体餐厅

      都江堰游览
      → 午餐
      → 某具体餐厅

      武侯祠参观
      → 午餐/晚餐
      → 某具体餐厅

      最终返回餐厅列表。
      """

      struct_out = llm.with_structured_output(TravelRestaurantInfoList)
      result = struct_out.invoke(prompt)
      return {"restaurant_info":result}


    
