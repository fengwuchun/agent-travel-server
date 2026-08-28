
from langgraph.types import interrupt
from langgraph.prebuilt import ToolNode

from agent.tools import calculator


tools = [
    calculator.calculator_add,
    calculator.calculator_subtract,
    calculator.calculator_multiply,
     calculator.calculator_divide
]
tool_node =ToolNode(tools)

def human_tool_node(state):
    last_message = state["messages"][-1]

    # LLM 没有要求调用 Tool
    if not last_message.tool_calls:
        return {}
    # 当前准备执行的 Tool
    tool_call = last_message.tool_calls[0]
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]
    print("\n准备执行 Tool:")
    print("tool",tool_name)
    print("arg:",tool_args)

    # ==============================
    # Interrupt
    # ==============================

    approved = interrupt({
        "question":"是否允许执行这个 Tolls",
        "tool":tool_name,
        "args":tool_args
    })

    print("人工决定:",approved)

    # ==============================
    # 拒绝
    # ==============================

    if not approved:
        raise ValueError("人工拒绝执行 Tools")

    # ==============================
    # 执行 Tool
    # ==============================
    return tool_node.invoke(state)



    
    

 
# 测试结构
# {
#   "messages": [
#     {
#       "type": "HumanMessage",
#       "content": "请帮我计算一下 123 + 456 的计算结果"
#     },
#     {
#       "type": "AIMessage",
#       "content": "",
#       "tool_calls": [
#         {
#           "name": "calculator_add",
#           "args": {
#             "a": 123,
#             "b": 456
#           },
#           "id": "call_f68d3c4e80a94465a20ff8",
#           "type": "tool_call"
#         }
#       ]
#     }
#   ]
# }