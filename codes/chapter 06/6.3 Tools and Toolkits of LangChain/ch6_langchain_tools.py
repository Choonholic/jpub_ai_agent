# 필요 모듈 가져오기
import os

from langgraph.prebuilt import create_react_agent
from langchain_google_community import GmailToolkit
from langchain_openai import OpenAI

# API 키 설치
os.environ["OPENAI_API_KEY"] = 'OpenAI API Key'

# 대형 언어 모델 인스턴스 생성
llm = OpenAI(temperature=0)

# 도구 모음 초기화
toolkit = GmailToolkit()
tools = toolkit.get_tools()

# 에이전트 실행기 생성 후 도구 할당
agent_executor = create_react_agent(llm, tools)
