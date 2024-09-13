# 환경 변수 적재하기
from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# 도우미 생성
assistant = client.beta.assistants.create(
    name="꽃 가격 계산기",
    instructions="당신은 제게 꽃의 가격을 계산해 줄 수 있습니다.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4o-mini"
)

# 도우미 출력
print(assistant)

# 생성한 도우미 목록 얻기
assistants = client.beta.assistants.list()

print(assistants)
