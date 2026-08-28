import json
from typing import Any


class JsonUtil:

    @staticmethod
    def dumps(data: Any) -> str:
        """
        将对象转换成格式化后的 JSON 字符串
        """

        if hasattr(data, "model_dump"):
            data = data.model_dump()

        return json.dumps(data, ensure_ascii=False, indent=2)

    @staticmethod
    def print_json(data: Any):
        """
        将对象格式化成 JSON 并打印
        """

        print(JsonUtil.dumps(data))
