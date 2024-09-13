# 환경 변수 적재하기
from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# 대화 흐름 ID 설정
thread_id = 'thread_83sOASNiEwhmQOmqW9Kmyico'

# 대화 흐름에서 메시지 읽기
messages = client.beta.threads.messages.list(
    thread_id=thread_id
)

# 메시지 출력
print(messages)
