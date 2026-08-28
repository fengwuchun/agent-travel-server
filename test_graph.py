from agent.graph import graph
from agent.utils.print_messages import print_messages,print_state,print_checkpoint

config = {
    "configurable" : {
        "thread_id" : "thread_001"
    }
}

#计算一下10+20等于多少,然后结果再乘以2,然后再除以3，然后再加5
#config作为参数传入
result = graph.invoke({
    "messages":[
        {
            "role" : "user",
            "content":"计算一下10+20等于多少,然后结果再乘以2,然后再除以3，然后再加5"
        }
    ]
},
config

)

print("最终结果为:\n")
# print(result)
print_messages(result["messages"])

print("\n===============当前 State================")

snapshot = graph.get_state(config)

print("\n=============== 当前 State Snapshot ===============")
print(snapshot)

print("\n=============== next ===============")
print(snapshot.next)

print("\n=============== tasks ===============")
print(snapshot.tasks)

state = graph.get_state(config)

print("thread_id:")
print(state.config["configurable"]["thread_id"])

print("\ncheckpoint_id:")
print(state.config["configurable"]["checkpoint_id"])

print("\n当前 messages:")
for message in state.values["messages"]:
    print(
        type(message).__name__,
        "=>",
        message.content
    )


print("\n========== 历史 Checkpoint ==========")

for state in graph.get_state_history(config):
    print("=======State=====\n")
    #print(state)

    configurable = state.config["configurable"]

    print("thread_id:",
          configurable.get("thread_id"))

    print("checkpoint_id:",
          configurable.get("checkpoint_id"))

    print("parent_checkpoint_id:",
          state.parent_config["configurable"]["checkpoint_id"]
          if state.parent_config
          else None)

    print("messages数量:",
          len(state.values["messages"]))

    print("--------------------------------")












   




