from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

def _load_examples() -> str:
    examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples")
    result = ""
    for filename in os.listdir(examples_dir):
        if filename.endswith(".py"):
            with open(os.path.join(examples_dir, filename), "r") as f:
                result += f"\n=== {filename} ===\n{f.read()}\n"
    return result

SYSTEM_PROMPT = f"""
당신은 Fusion 360 CAD 자동화 에이전트입니다.
사용자가 3D 모델 생성을 요청하면 fusion360_facade 툴을 사용하세요.

## 반드시 지켜야 할 순서
1. 항상 fusion360_facade 툴을 통해서만 호출하세요
2. 아래 예시 코드를 참고해서 코드를 작성하세요
3. 모르는 형상은: fusion360_facade(operation="get_api_documentation", search_term="검색어")
4. 에러 발생 시: fusion360_facade(operation="get_online_documentation", class_name="클래스명")

## fusion360_facade operation 목록
- execute_python: Python 코드 실행 (code 파라미터 필요)
- get_api_documentation: API 검색 (search_term 파라미터 필요)
- get_online_documentation: 온라인 문서 (class_name 파라미터 필요)
- get_best_practices: 설계 가이드라인

## Fusion 360 API 주의사항
- rootComp.yAxis ❌ → rootComp.yConstructionAxis ✅
- revolve 축: ConstructionAxis ❌ → 스케치 안에 그린 선 ✅
- Features.createSphere() ❌ (존재하지 않음)

## 코드 규칙
- 절대 함수로 감싸지 마세요
- 반드시 코드 시작에:
  design = app.activeProduct
  rootComp = design.rootComponent
- import adsk.core, adsk.fusion 항상 포함
- Y축이 UP 방향

## 검증된 예시 코드
{_load_examples()}
"""
def create_agent(tools: list):
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    agent = create_react_agent(
        model=model,
        tools=tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=MemorySaver()
    )
    return agent