from llm.gemini_client import GeminiClient
from chat.conversation import start_chat

from agent.graph import create_agent
from langchain_core.messages import HumanMessage


def main():
    agent = create_agent(tools=[])

    config = {"configurable": {"thread_id": "1"}}

    print("대화를 시작합니다. 종료하려면 'quit'을 입력하세요.\n")

    while True:
        user_input = input("나: ")

        if user_input.lower() == "quit":
            print("대화를 종료합니다.")
            break

        result = agent.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )

        print(f"\nAgent: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()