from langgraph.types import Command


class InterruptHandler:

    def get_interrupt_info(self, result, graph, config):
        # 先判断是否有中断
        if "__interrupt__" not in result:

            return {}
        interrupt_info = result["__interrupt__"][0]
        print("==================中断信息===================")
        print(interrupt_info.value)
        return interrupt_info.value

    def user_opration(self,info, graph, config):
        print("=====进入用户=====")  
        if info["type"] == "travel_request":
           return  self.handle_travel_request_interrupt(info, graph, config)
        else: 
         while True:  #输入无效指令循环
            print("用户操作")
            print("1. 批准")
            print("2. 拒绝")
            print("请输入命令：\n")
            command = input().strip()

            if command == "1":
                print("继续执行")
                return graph.invoke(
                            Command(
                            resume={
                                   "approved": True,
                                   "feedback": "",
                            }
                            ),
                            config,
                     )

            elif command == "2":
                print("请输入修改内容：\n")
                modify_content = input().strip()
                return graph.invoke(
                            Command(
                            resume={
                                   "approved": False,
                                   "feedback": modify_content,
                            }
                            ),
                            config,
                     )
            else:
                print("无效命令，请输入 1 批准 或 2 拒绝")


    def handle_travel_request_interrupt(self,info, graph, config): 
         msg = info["message"]
         print("======================================")
         print(msg)
         print("请输入旅行需求：") 
         content = input().strip()
         return graph.invoke(
             Command(resume={ 
                 "approved": True,
                 "travel_request_other": content
                 }),
             config
             )
    

              
