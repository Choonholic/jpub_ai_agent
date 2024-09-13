# API 키 설치
import os

os.environ["OPENAI_API_KEY"] = 'OpenAI API Key'
os.environ['ANTHROPIC_API_KEY'] = 'Anthropic API Key'

# langchain_openai 모듈에서 OpenAI 클래스 가져오기
from langchain_openai import OpenAI

# langchain_anthropic 모듈에서 ChatAnthropic 클래스 가져오기
from langchain_anthropic import ChatAnthropic

# 대형 언어 모델 인스턴스 초기화 및 온도 매개 변수 설정
openai_model = OpenAI(temperature=0.1)
claude_model = ChatAnthropic(model='claude-3-opus-20240229', temperature=0.1)

# ModelLaboratory 클래스 가져오기: 여러 대형 언어 모델의 관리와 비교에 사용
from langchain.model_laboratory import ModelLaboratory

# 모델 실험실 인스턴스 생성 후, 모델 통합
model_lab = ModelLaboratory.from_llms([openai_model, claude_model])

# 모델 실험실을 사용하여 동일한 질문에 대해 각기 다른 모델의 답변을 비교
model_lab.compare("백합은 어느 나라에서 유래되었나요?")
