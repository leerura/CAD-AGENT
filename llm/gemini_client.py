from google import genai
from google.genai import types
from dotenv import load_dotenv
from llm.base import LLMClient
import os

load_dotenv()

class GeminiClient(LLMClient):

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.session = self.client.chats.create(model="gemini-2.0-flash")

    def chat(self, message: str) -> str:
        response = self.session.send_message(message)
        return response.text
