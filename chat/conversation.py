from llm.base import LLMClient

def start_chat(llm: LLMClient):
    print("대화를 시작합니다. 종료하려면 'quit'을 입력하세요. \n")

    while True:
        user_input = input("나: ")

        if user_input.lower() == "quit":
            print("대화를 종료합니다.")
            break

        response = llm.chat(user_input)
        print(f"\nGemini: {response}\n")
