from typing import List
class MessageUntil:

      # 1.缺少目的地 2.缺少出发地  3.缺少旅行者数量  4.缺少旅行天数 5.缺少预算上限 6.缺少旅行偏好
    def paser_request_need_msg_tip(self, status: List[int]):
        tips = {
            1: "目的地",
            2: "出发地",
            3: "旅行者数量",
            4: "旅行天数",
            5: "预算上限",
            6: "旅行偏好",
        }

        missing = [tips[i] for i in status if i in tips]

        if not missing:
            return ""

        return f"您的旅游需求还缺少：{'、'.join(missing)}，请补充。"
         