# 환경 변수 적재하기
from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()


# 대화 흐름 생성
thread = client.beta.threads.create()

# 대화 흐름 출력
print(thread)

# 대화 흐름에 메시지 추가
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="각 꽃다발의 가격을 원가에 20%를 더한 가격으로 책정합니다. 원가가 1600원일 때, 제 판매 가격은 얼마인가요?"
)

# 메시지 출력
print(message)

# 메시지 목록 가져오기
messages = client.beta.threads.messages.list(
    thread_id='thread_83sOASNiEwhmQOmqW9Kmyico'
)

# 메시지 출력
print(messages)
