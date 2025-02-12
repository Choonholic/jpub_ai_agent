import os

# API 키 설치
os.environ["OPENAI_API_KEY"] = 'OpenAI API Key'
os.environ["SERPAPI_API_KEY"] = 'SerpApi API Key'

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_experimental.tools.python.tool import PythonAstREPLTool

# LLM 인스턴스 생성
llm = ChatOpenAI(model="gpt-4", temperature=0)

# SerpAPI 기반의 구글 검색 도구
search = SerpAPIWrapper()

search_tool = Tool(
    name="search",
    func=search.run,
    description="현재 정보를 검색하는 도구"
)

# LLM 기반 수학 계산 도구
math_prompt = ChatPromptTemplate.from_messages([
    ("system", "Solve the math problem carefully."),
    ("user", "{question}")
])

# 파이프 연산자로 체인 구성
llm_math_chain = math_prompt | llm

math_tool = Tool(
    name="llm-math",
    func=lambda x: llm_math_chain.invoke({"question": x}),
    description="수학 문제를 해결하는 도구"
)

# 파이썬 실행 도구
python_tool = PythonAstREPLTool()

# 도구 목록 생성
tools = [search_tool, math_tool, python_tool]

# ReAct 프롬프트 템플릿 정의
react_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful AI agent that follows the ReAct framework.\n\n"
     "You can use the following tools:\n"
     "{tools}\n\n"
     "Use the following format:\n\n"
     "Question: the input question you must answer\n"
     "Thought: you should always think about what to do\n"
     "Action: the action to take, should be one of [{tool_names}]\n"
     "Action Input: the input to the action\n"
     "Observation: the result of the action\n"
     "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
     "Thought: I now know the final answer\n"
     "Final Answer: the final answer to the original input question\n\n"
     "Begin!\n\n"
    ),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# ReAct 에이전트 생성
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    agent_kwargs={"prompt": react_prompt},
    verbose=True
)

# 에이전트 실행
input_question = (
    "현재 시장에서 장미의 일반적인 구매 가격은 얼마인가요?\n"
    "이 가격에 마진을 5%를 추가하려면 어떻게 가격을 책정해야 합니까?"
)

result = agent.invoke(input_question)

# 결과 출력
print(result)

# 결과를 한국어로 출력하도록 유도하는 프롬프트 템플릿
react_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "최선을 다해 다음 질문에 답해 주세요."
     "능력이 부족할 경우, 아래 도구를 사용할 수 있습니다:\n\n"
     "You are a helpful AI agent that follows the ReAct framework.\n\n"
     "You can use the following tools:\n"
     "{tools}\n\n"
     "Use the following format:\n\n"
     "Question: the input question you must answer\n"
     "Thought: you should always think about what to do\n"
     "Action: the action to take, should be one of [{tool_names}]\n"
     "Action Input: the input to the action\n"
     "Observation: the result of the action\n"
     "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
     "Thought: I now know the final answer\n"
     "Final Answer: the final answer to the original input question\n\n"
     "Begin!\n\n"
    ),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])
