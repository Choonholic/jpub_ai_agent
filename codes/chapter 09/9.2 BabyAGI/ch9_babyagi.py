# OpenAI API 키 설정
import os

os.environ["OPENAI_API_KEY"] = 'OpenAI API Key'

# 라이브러리와 모듈 가져오기
import faiss

from collections import deque
from langchain.chains import LLMChain
from langchain.chains.base import Chain
from langchain.docstore import InMemoryDocstore
from langchain.llms import BaseLLM
from langchain_openai import OpenAIEmbeddings, OpenAI
from langchain.prompts import PromptTemplate
from langchain.vectorstores import FAISS
from langchain.vectorstores.base import VectorStore
from langchain_experimental.autonomous_agents import BabyAGI
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

# 임베딩 모델 정의
embeddings_model = OpenAIEmbeddings()

# 벡터 데이터베이스 초기화
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model, index, InMemoryDocstore({}), {})

# 작업 생성 연쇄 정의
class TaskCreationChain(LLMChain):
    """작업 생성을 담당하는 연쇄"""

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        """대형 언어 모델에서 응답 분석기 가져오기"""
        task_creation_template = (
            "You are a task creation AI that uses the result of an execution agent"
            " to create new tasks with the following objective: {objective},"
            " The last completed task has the result: {result}."
            " This result was based on this task description: {task_description}."
            " These are incomplete tasks: {incomplete_tasks}."
            " Based on the result, create new tasks to be completed"
            " by the AI system that do not overlap with incomplete tasks."
            " Return the tasks as an array."

        )

        prompt = PromptTemplate(
            template=task_creation_template,
            input_variables=[
                "result",
                "task_description",
                "incomplete_tasks",
                "objective"
            ],
        )

        return cls(prompt=prompt, llm=llm, verbose=verbose)

# 작업 우선 순위 연쇄 정의
class TaskPrioritizationChain(LLMChain):
    """작업 우선 순위 정렬을 담당하는 연쇄"""

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        """대형 언어 모델에서 응답 분석기 가져오기"""
        task_prioritization_template = (
            "You are a task prioritization AI tasked with cleaning the formatting of and reprioritizing"
            " the following tasks: {task_names}."
            " Consider the ultimate objective of your team: {objective}."
            " Do not remove any tasks. Return the result as a numbered list, like:"
            " #. First task"
            " #. Second task"
            " Start the task list with number {next_task_id}."
        )

        prompt = PromptTemplate(
            template=task_prioritization_template,
            input_variables=[
                "task_names",
                "next_task_id",
                "objective"],
        )

        return cls(prompt=prompt, llm=llm, verbose=verbose)

# 작업 실행 연쇄 정의
class ExecutionChain(LLMChain):
    """작업 실행을 담당하는 연쇄"""

    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        """대형 언어 모델에서 응답 분석기 가져오기"""
        execution_template = (
            "You are an AI who performs one task based on the following objective: {objective}."
            " Take into account these previously completed tasks: {context}."
            " Your task: {task}."
            " Response:"
        )

        prompt = PromptTemplate(
            template=execution_template,
            input_variables=[
                "objective",
                "context",
                "task"
            ],
        )

        return cls(prompt=prompt, llm=llm, verbose=verbose)

# 다음 작업 가져오기
def get_next_task(
    task_creation_chain: LLMChain,
    result: Dict,
    task_description: str,
    task_list: List[str],
    objective: str
) -> List[Dict]:
    """다음 작업을 가져옵니다."""
    incomplete_tasks = ", ".join(task_list)
    response = task_creation_chain.run(
        result=result,
        task_description=task_description,
        incomplete_tasks=incomplete_tasks,
        objective=objective,
    )
    new_tasks = response.split("\n")
    return [{"task_name": task_name} for task_name in new_tasks if task_name.strip()]

# 작업 우선 순위 설정
def prioritize_tasks(
    task_prioritization_chain: LLMChain,
    this_task_id: int,
    task_list: List[Dict],
    objective: str
) -> List[Dict]:
    """작업의 우선 순위를 설정합니다."""
    task_names = [t["task_name"] for t in task_list]
    next_task_id = int(this_task_id) + 1
    response = task_prioritization_chain.run(
        task_names=task_names,
        next_task_id=next_task_id,
        objective=objective
    )
    new_tasks = response.split("\n")
    prioritized_task_list = []

    for task_string in new_tasks:
        if not task_string.strip():
            continue

        task_parts = task_string.strip().split(".", 1)

        if len(task_parts) == 2:
            task_id = task_parts[0].strip()
            task_name = task_parts[1].strip()
            prioritized_task_list.append({"task_id": task_id, "task_name": task_name})

    return prioritized_task_list

# 최상위 작업 가져오기
def _get_top_tasks(
    vectorstore, query: str,
    k: int
) -> List[str]:
    """요청을 기반으로 상위 k개의 작업을 가져옵니다."""
    results = vectorstore.similarity_search_with_score(query, k=k)

    if not results:
        return []

    sorted_results, _ = zip(*sorted(results, key=lambda x: x[1], reverse=True))
    return [str(item.metadata["task"]) for item in sorted_results]

# 작업 실행
def execute_task(
    vectorstore,
    execution_chain: LLMChain,
    objective: str,
    task: str,
    k: int = 5
) -> str:
    """작업을 실행합니다."""
    context = _get_top_tasks(vectorstore, query=objective, k=k)
    return execution_chain.run(objective=objective, context=context, task=task)

# 주 기능 실행 부분
if __name__ == "__main__":
    OBJECTIVE = "서울의 오늘 기후를 분석하고, 꽃 보관 전략을 작성하세요."
    llm = OpenAI(temperature=0)
    verbose = False
    max_iterations: Optional[int] = 6

    # BabyAGI 에이전트 초기화 및 실행
    baby_agi = BabyAGI.from_llm(
        llm=llm,
        vectorstore=vectorstore,
        verbose=verbose,
        max_iterations=max_iterations
    )

    baby_agi({"objective": OBJECTIVE})
