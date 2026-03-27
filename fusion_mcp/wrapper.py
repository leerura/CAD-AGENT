from langchain_core.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import os


load_dotenv()

FUSION_URL = os.getenv("FUSION_URL")
FUSION_TOKEN = os.getenv("FUSION_TOKEN")
FUSION_AUTH = os.getenv("FUSION_AUTH")

@tool
async def fusion360_facade(operation: str, code: str = "") -> str:
    """
    Fusion 360을 제어하는 통합 도구입니다.
    operation: execute_python, get_best_practices, get_api_documentation
    code: execute_python일 때 Fusion 360 Python 코드
    """
    client = MultiServerMCPClient(
        {
            "fusion360": {
                "transport": "sse",
                "url": FUSION_URL,
                "headers": {"Authorization": FUSION_AUTH}
            }
        }
    )

    # async with 대신 직접 get_tools 호출
    tools = await client.get_tools()
    fusion_tool = next(t for t in tools if t.name == "fusion360")

    params = {
        "operation": operation,
        "tool_unlock_token": FUSION_TOKEN
    }

    if code:
        params["code"] = code

    result = await fusion_tool.ainvoke(params)
    return str(result)