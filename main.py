import asyncio
from agent.graph import create_agent
from fusion_mcp.wrapper import fusion360_facade
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

async def main():
    agent = create_agent(tools=[fusion360_facade])
    config = {"configurable": {"thread_id": "1"}}

    print("대화를 시작합니다. 종료하려면 'quit'을 입력하세요.\n")

    while True:
        user_input = input("나: ")

        if user_input.lower() == "quit":
            print("대화를 종료합니다.")
            break

        async for chunk in agent.astream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="values"
        ):
            last_msg = chunk["messages"][-1]

            if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
                for tc in last_msg.tool_calls:
                    print(f"\n[툴 호출: {tc['name']}]")
                    print(f"  파라미터: {tc['args']}")

            elif isinstance(last_msg, ToolMessage):
                print(f"\n[툴 결과]: {last_msg.content[:200]}")

            elif isinstance(last_msg, AIMessage) and last_msg.content:
                print(f"\nAgent: {last_msg.content}\n")

if __name__ == "__main__":
    asyncio.run(main())