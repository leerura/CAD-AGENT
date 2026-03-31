# CAD Agent 🤖

자연어로 Fusion 360 3D 모델을 자동 생성하는 LLM 기반 CAD 자동화 에이전트

## 개요

터미널에서 한국어로 입력하면 Fusion 360에서 3D 모델이 자동으로 생성됩니다.
```
나: 반지름 5 높이 10인 원기둥 만들어줘
→ Fusion 360에서 원기둥 자동 생성 
```

## 기술 스택

| 항목 | 기술 |
|------|------|
| LLM | Gemini 2.5 Flash |
| Agent Framework | LangGraph |
| MCP | AuraFriday mcp-link-server (SSE) |
| CAD | Autodesk Fusion 360 |
| Language | Python 3.11 |

## 아키텍처
```
사용자 입력 (자연어)
    ↓
LangGraph ReAct Agent (Gemini 2.5 Flash)
    ↓
fusion360_facade (Facade Pattern)
    ↓ tool_unlock_token 자동 처리
AuraFriday MCP Server (SSE)
    ↓
Fusion 360 Python API
    ↓
3D 모델 생성 
```

## 핵심 설계 결정

**Facade Pattern 적용**

Gemini가 AuraFriday의 `readme → execute` 2단계 토큰 시스템을 직접 처리하지 못하는 문제를 해결하기 위해 `fusion360_facade` 래퍼 툴을 만들어 토큰 관리를 내부화했습니다.

**Self-correction**

툴 실행 에러 발생 시 프로그램을 종료하지 않고 에러 메시지를 Agent에게 반환하여 스스로 코드를 수정하고 재시도합니다.

**Dynamic Few-shot**

`examples/` 폴더의 검증된 코드를 자동으로 읽어 System Prompt에 주입합니다. 새로운 형상 코드를 추가하려면 `examples/` 폴더에 `.py` 파일만 넣으면 됩니다.

## 설치
```bash
git clone https://github.com/your-repo/cad-agent
cd cad-agent
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 환경 변수 설정

`.env` 파일 생성:
```
GEMINI_API_KEY=your_gemini_api_key
FUSION_URL=https://127-0-0-1.local.aurafriday.com:31173/sse
FUSION_TOKEN=your_fusion_token
FUSION_AUTH=Bearer your_fusion_auth_token
```

## 사전 준비

1. Autodesk Fusion 360 설치 및 실행
2. [AuraFriday mcp-link-server](https://github.com/AuraFriday/mcp-link-server) 설치
3. Fusion 360에 MCP-Link Add-In 설치 및 실행

## 실행
```bash
python main.py
```

## 디렉토리 구조
```
cad-agent/
├── .env
├── requirements.txt
├── main.py                   # 진입점 (대화 루프)
├── agent/
│   └── graph.py              # LangGraph Agent + System Prompt
├── fusion_mcp/
│   └── wrapper.py            # Facade Pattern 래퍼 툴
├── llm/
│   ├── base.py               # LLMClient 추상 클래스
│   └── gemini_client.py      # Gemini 구현체
├── examples/                 # 검증된 Fusion 360 코드
│   ├── cylinder.py
│   ├── box.py
│   └── sphere.py
└── .github/
    ├── ISSUE_TEMPLATE/
    └── pull_request_template.md
```

## 지원 형상

| 형상 | 상태 |
|------|------|
| 원기둥 | ✅ |
| 박스 | ✅ |
| 구 | ✅ |
| 기타 | 🔄 Self-correction으로 시도 |

## 새로운 형상 추가

`examples/` 폴더에 검증된 코드를 추가하면 자동으로 반영됩니다:
```python
# examples/cone.py
# 키워드: 원뿔, cone
# 파라미터: radius, height

import adsk.core, adsk.fusion
design = app.activeProduct
# ... 코드 작성
```
