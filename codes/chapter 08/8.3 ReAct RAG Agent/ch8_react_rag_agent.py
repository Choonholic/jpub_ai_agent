from dotenv import load_dotenv

load_dotenv()

# 재무 보고서 파일 적재
from llama_index.core import SimpleDirectoryReader

A_docs = SimpleDirectoryReader(
    input_files=["./data/E-commerce A - Third Quarter 2023 Results.pdf"]
).load_data()

B_docs = SimpleDirectoryReader(
    input_files=["./data/E-commerce B - Third Quarter 2023 Results.pdf"]
).load_data()

# 재무 보고서 파일 기반의 벡터 데이터 구축
from llama_index.core import VectorStoreIndex

A_index = VectorStoreIndex.from_documents(A_docs)
B_index = VectorStoreIndex.from_documents(B_docs)

# 색인 영속화
from llama_index.core import StorageContext

A_index.storage_context.persist(persist_dir="./storage/A")
B_index.storage_context.persist(persist_dir="./storage/B")

# 로컬에서 색인 적재하기
from llama_index.core import load_index_from_storage

try:
    # 색인 A 적재하기
    A_storage_context_A = StorageContext.from_defaults(persist_dir="./storage/A")
    A_index = load_index_from_storage(A_storage_context)

    # 색인 B 적재하기
    B_storage_context = StorageContext.from_defaults(persist_dir="./storage/B")
    B_index = load_index_from_storage(B_storage_context)

    index_loaded = True
except:
    index_loaded = False

# 요청 엔진 생성
A_engine = A_index.as_query_engine(similarity_top_k=3)
B_engine = B_index.as_query_engine(similarity_top_k=3)

# 요청 도구 구성
from llama_index.core.tools import QueryEngineTool, ToolMetadata

query_engine_tools = [
    QueryEngineTool(
        query_engine=A_engine,
        metadata=ToolMetadata(
            name="A_Finance",
            description="전자 상거래 업체 A의 재무 정보를 제공하는 도구"
        ),
    ),
    QueryEngineTool(
        query_engine=B_engine,
        metadata=ToolMetadata(
            name="B_Finance",
            description="전자 상거래 업체 B의 재무 정보를 제공하는 도구"
        ),
    )
]

# 대형 언어 모델 설정
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o-mini")

# ReAct 검색 강화 생성 에이전트 생성
from llama_index.core.agent import ReActAgent

agent = ReActAgent.from_tools(query_engine_tools, llm=llm, verbose=True)

# 에이전트에게 작업 수행 요청
agent.chat("전자 상거래 업체 A와 전자 상거래 B의 매출을 비교 분석해 주세요.")
