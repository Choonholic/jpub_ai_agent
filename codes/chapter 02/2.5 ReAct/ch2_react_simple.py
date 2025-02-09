# API 키 설치
import os

os.environ["OPENAI_API_KEY"] = 'OpenAI API Key'
os.environ["SERPAPI_API_KEY"] = 'SerpApi API Key'

# LangChain Hub 가져오기
from langchain import hub

# LangChain Hub에서 ReAct의 프롬프트 가져오기
prompt = hub.pull("hwchase17/react", api_key='LangSmith API Key')

print(prompt)

# OpenAI 가져오기
from langchain_openai import OpenAI

# 사용할 대형 언어 모델 선택
llm = OpenAI()

# SerpAPIWrapper를 통해 도구 모듈 가져오기
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool

# SerpAPIWrapper 인스턴스화
search = SerpAPIWrapper()

# 도구 목록 준비
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="대형 언어 모델이 관련 지식이 없을 때 지식 검색에 사용됩니다."
    ),
]

# create_react_agent 기능 가져오기
from langchain.agents import create_react_agent

# ReAct 에이전트 생성
agent = create_react_agent(llm, tools, prompt)

# AgentExecutor 가져오기
from langchain.agents import AgentExecutor

# 에이전트와 도구를 전달하여 AgentExecutor 생성
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# AgentExecutor를 호출하여 입력 데이터 전달
print("첫 번째 실행 결과:")
agent_executor.invoke({"input": "현재 인공 지능 에이전트의 최신 연구 진전은 무엇입니까?"})
print("두 번째 실행 결과:")
agent_executor.invoke({"input": "현재 인공 지능 에이전트의 최신 연구 진전은 무엇입니까?"})
