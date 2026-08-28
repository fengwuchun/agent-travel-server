import json


def print_messages(messages):
    print("\n========== Messages ==========")

    data = [
        message.model_dump()
        for message in messages
    ]

    print(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
            default=str
        )
    )

    print("===============================\n")





def print_state(state):
    data = {
        "checkpoint_id": state.config["configurable"].get("checkpoint_id"),
        "thread_id": state.config["configurable"].get("thread_id"),
        "checkpoint_ns": state.config["configurable"].get("checkpoint_ns"),

        "metadata": state.metadata,

        "messages": [
            message.model_dump()
            for message in state.values.get("messages", [])
        ],

        "parent_checkpoint_id": (
            state.parent_config["configurable"].get("checkpoint_id")
            if state.parent_config
            else None
        ),

        "next": state.next,
    }

    print(json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
        default=str
    )) 





def print_checkpoint(checkpoint):
    """
    将 LangGraph StateSnapshot 格式化为 JSON 打印
    """

    data = {
        "values": {
            "messages": [
                message.model_dump()
                for message in checkpoint.values.get("messages", [])
            ]
        },

        "next": checkpoint.next,

        "config": checkpoint.config,

        "metadata": checkpoint.metadata,

        "created_at": checkpoint.created_at,

        "parent_config": checkpoint.parent_config,

        "tasks": [
            task.model_dump() if hasattr(task, "model_dump")
            else str(task)
            for task in checkpoint.tasks
        ],

        "interrupts": [
            interrupt.model_dump() if hasattr(interrupt, "model_dump")
            else str(interrupt)
            for interrupt in checkpoint.interrupts
        ]
    }

    print(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
            default=str
        )
    )       