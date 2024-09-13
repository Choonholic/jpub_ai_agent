# 환경 변수 설정
from dotenv import load_dotenv

load_dotenv()

# 프롬프트 템플릿 설정
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template("{flower}의 꽃말은?")

# 대형 모델 설정
from langchain_openai import OpenAI

model = OpenAI()

# 출력 파서 설정
from langchain.schema.output_parser import StrOutputParser

output_parser = StrOutputParser()

# 연쇄 구성
chain = prompt | model | output_parser

# 연쇄를 실행하고 결과를 출력
result = chain.invoke({"flower": "라일락"})

print(result)
