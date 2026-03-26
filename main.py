from llm.gemini_client import GeminiClient
from chat.conversation import start_chat

if __name__ == "__main__":
    llm = GeminiClient()
    start_chat(llm)