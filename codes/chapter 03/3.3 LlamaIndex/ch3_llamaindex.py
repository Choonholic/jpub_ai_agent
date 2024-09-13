from dotenv import load_dotenv

load_dotenv()

# '꽃말의 비밀 정원 이야기' 문서 적재
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()

# 문서의 색인 생성
from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)

# 요청 엔진 생성
agent = index.as_query_engine()

# 요청 예제
response = agent.query("꽃말의 비밀 정원의 직원에게는 몇 가지 역할이 있나요?")

print("꽃말의 비밀 정원의 직원들에게는 몇 가지 역할이 있나요?", response)

response = agent.query("꽃말의 비밀 정원의 에이전트 이름은 무엇인가요?")

print("꽃말의 비밀 정원의 에이전트 이름은 무엇인가요?", response)

# 색인을 로컬에 저장
index.storage_context.persist()
