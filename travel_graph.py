from agent.graph import graph
from agent.interrupt_handler import InterruptHandler
from agent.utils.json_util import JsonUtil

config = {
    "configurable" : {
        "thread_id" : "travel_thread_001"
    }
    }

# 我想去成都玩三天，预计花销4000，两个人，请帮我制定一个行程
result = graph.invoke({
      "messages" :[
          {
              "role" : "user",
              "content" : "我想去成都旅游，请帮我制定一个行程"
          }
      ]
    },
    config
    )

print("========结果========")
print(result)
interruptHandler = InterruptHandler()
while "__interrupt__" in result:
    print("========检测到人工审批========")
    info = interruptHandler.get_interrupt_info(result,graph,config)
    result = interruptHandler.user_opration(info,graph,config)
print("========最终结果========")
JsonUtil.print_json(result["itinerary"])
