from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver #이건 뭐고
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def create_agent(tools: list):
    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

    agent = create_react_agent(model=model, tools=tools, checkpointer=MemorySaver())
    return agent
