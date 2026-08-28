from agent.graph import graph
from agent.interrupt_handler import InterruptHandler


handler = InterruptHandler(graph)

thread_id = "thread_001"

# ==================================
# 第一次执行 Agent
# ==================================

result = handler.run(
     "计算一下10+20等于多少,然后结果再乘以2,然后再除以3，然后再加5",
    thread_id
)

print("\n========== 第一次执行结果 ==========")
print(result)

# ==================================
# 模拟用户操作
# ==================================

if result["status"] == "interrupted":
     print("\n========== 模拟用户操作 ==========")
     # 模拟用户点击「允许」
     approved = True

     # ==================================
    # Resume
    # ==================================

     result = handler.resume(thread_id,approved)
     print("\n========== Resume结果 ==========")
     print(result)










