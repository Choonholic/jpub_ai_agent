# 환경 변수 적재하기
from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# 실행 세션 생성
run = client.beta.threads.runs.create(
    thread_id='thread_83sOASNiEwhmQOmqW9Kmyico',
    assistant_id='asst_aaIDR7JUjOKNKyKv65l2CYmV',
    instructions="질문에 답변해 주세요." # 여기서 새로운 지침을 설정할 수 있습니다.
)

# 실행 세션 출력
print(run)

# 실행 세션 상태 다시 가져오기
run = client.beta.threads.runs.retrieve(
    thread_id='thread_83sOASNiEwhmQOmqW9Kmyico',
    run_id=run.id
)

# 실행 세션 출력
print(run)
