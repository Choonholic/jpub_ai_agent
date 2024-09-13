# API 키 설치
import os

os.environ["OPENAI_API_KEY"] = 'OpenAI API Key'

# 출력을 문자열로 변환하기 위한 출력 분석기
from langchain_core.output_parsers import StrOutputParser
# 대화 프롬프트 템플릿을 생성하기 위한 모듈
from langchain_core.prompts import ChatPromptTemplate
# OpenAI GPT 모델을 호출하기 위한 모듈
from langchain_openai import ChatOpenAI

# {topic}은 나중에 특정 주제가 삽입될 위치표시자
# 주제에 관한 이야기를 요청하는 대화 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_template("{topic}에 대한 이야기를 들려주세요.")

# OpenAI GPT-4 모델을 사용하여 ChatOpenAI 객체 초기화
model = ChatOpenAI(model="gpt-4")

# 모델의 출력을 문자열로 변환하기 위한 출력 파서 초기화
output_parser = StrOutputParser()

'''
파이프라인 연산자(|)를 사용하여 각 처리 단계를 연결해 하나의 처리 연쇄를 생성
prompt는 구체적인 프롬프트 텍스트를 생성하고,
model은 그 텍스트에 대한 응답을 생성하며,
output_parser는 그 응답을 처리하여 문자열로 변환
'''
chain = prompt | model | output_parser

# 연쇄를 호출하고, 주제 "수선화"를 입력하여 이야기 생성 작업 실행
message = chain.invoke({"topic": "수선화"})

# 결과 출력
print(message)
