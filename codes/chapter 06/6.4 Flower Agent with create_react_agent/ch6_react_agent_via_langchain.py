# API 키 설치
import os

os.environ["OPENAI_API_KEY"] = 'OpenAI API Key'
os.environ["SERPAPI_API_KEY"] = 'SerpApi API Key'

# 대형 언어 모델 인스턴스 생성
from langchain_openai import OpenAI

llm = OpenAI(temperature=0)

# 도구 적재
from langchain_community.agent_toolkits.load_tools import load_tools

tools = load_tools(["serpapi", "llm-math"], llm=llm)

# 프롬프트 템플릿 설계
from langchain.prompts import PromptTemplate

template = (
    'Do your best to answer the following question. If you are unable to do so, you may use the following tools:\n\n'
    '{tools}\n\nUse the following format:\n\n'
    'Question: the input question you must answer\n'
    'Thought: you should always think about what to do\n'
    'Action: the action to take, should be one of [{tool_names}]\n'
    'Action Input: the input to the action\n'
    'Observation: the result of the action\n'
    '... (this Thought/Action/Action Input/Observation can repeat N times)\n'
    'Thought: I now know the final answer\n'
    'Final Answer: the final answer to the original input question\n\n'
    'Begin!\n\n'
    'Question: {input}\n'
    'Thought:{agent_scratchpad}'
)

prompt = PromptTemplate.from_template(template)

# 에이전트 생성
from langchain.agents import create_react_agent

agent = create_react_agent(llm, tools, prompt)

# 에이전트와 도구를 사용하여 에이전트 실행기 생성
from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 에이전트 실행기를 통한 작업 실행
agent_executor.invoke({
    "input": "현재 시장에서 장미의 일반적인 구매 가격은 얼마인가요?\n이 가격에 마진을 5%를 추가하려면 어떻게 가격을 책정해야 합니까?"
})

# 한국어로 답변을 받기 위한 템플릿
template = (
    '최선을 다해 다음 질문에 답해 주세요. 능력이 부족할 경우, 아래 도구를 사용할 수 있습니다:\n\n'
    '{tools}\n\nUse the following format:\n\n'
    'Question: the input question you must answer\n'
    'Thought: you should always think about what to do\n'
    'Action: the action to take, should be one of [{tool_names}]\n'
    'Action Input: the input to the action\n'
    'Observation: the result of the action\n'
    '... (this Thought/Action/Action Input/Observation can repeat N times)\n'
    'Thought: I now know the final answer\n'
    'Final Answer: the final answer to the original input question\n\n'
    'Begin!\n\n'
    'Question: {input}\n'
    'Thought:{agent_scratchpad}'
)
