# OpenAI API 키 설정
import os

os.environ["OPENAI_API_KEY"] = 'OpenAI API Key'

# 라이브러리 가져오기
from typing import List
from langchain_openai import ChatOpenAI
from langchain.prompts.chat import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    BaseMessage
)

# CAMELAgent 클래스 정의
class CAMELAgent:
    def __init__(self, system_message: SystemMessage, model: ChatOpenAI) -> None:
        self.system_message = system_message
        self.model = model
        self.init_messages()

    def reset(self) -> None:
        """대화 메시지 초기화"""
        self.init_messages()
        return self.stored_messages

    def init_messages(self) -> None:
        """대화 메시지 초기화"""
        self.stored_messages = [self.system_message]

    def update_messages(self, message: BaseMessage) -> List[BaseMessage]:
        """대화 메시지 목록 갱신"""
        self.stored_messages.append(message)
        return self.stored_messages

    def step(self, input_message: HumanMessage) -> AIMessage:
        """대형 언어 모델과 상호 작용"""
        messages = self.update_messages(input_message)
        output_message = self.model(messages)
        self.update_messages(output_message)
        return output_message

# 역할과 작업 프롬프트 설정
assistant_role_name = "꽃가게 마케팅 전문가"
user_role_name = "꽃가게 주인"
task = "여름 장미의 밤 마케팅 캠페인 전략을 작성하세요"
word_limit = 200  # 각 논의에서의 글자 수 제한

# 지정된 작업과 관련된 프롬프트 템플릿 정의. 이 단계 후 작업이 구체화됨
task_specifier_sys_msg = SystemMessage(content="당신은 작업을 더 구체적으로 만들 수 있습니다.")
task_specifier_prompt = """
다음은 {assistant_role_name}이 {user_role_name}을 도와서 완료해야 할 작업입니다: {task}.
작업을 더 구체적으로 만들어 주세요. 창의력과 상상력을 발휘해 주세요.
{word_limit}자 이내로 구체적인 작업을 작성해 주세요. 추가적인 내용은 포함하지 마세요.
"""

task_specifier_template = HumanMessagePromptTemplate.from_template(
    template=task_specifier_prompt
)

# CAMEL 에이전트 초기화
task_specify_agent = CAMELAgent(
    task_specifier_sys_msg,
    ChatOpenAI(model_name='gpt-4', temperature=1.0)
)

# 프롬프트 메시지 생성
task_specifier_msg = task_specifier_template.format_messages(
    assistant_role_name=assistant_role_name,
    user_role_name=user_role_name,
    task=task,
    word_limit=word_limit,
)[0]

# 작업을 구체화하는 에이전트 실행
specified_task_msg = task_specify_agent.step(task_specifier_msg)
specified_task = specified_task_msg.content

# 결과 출력
print(f"Original task prompt:\n{task}\n")
print(f"Specified task prompt:\n{specified_task}\n")

# 시스템 메시지 템플릿 정의
assistant_inception_prompt = """
당신은 {assistant_role_name}이고, 저는 {user_role_name}라는 것을 절대 잊으면 안 됩니다.
역할을 절대 바꾸지 마세요!
저에게 지시하지 마세요!
성공적으로 작업을 완료하는 것이 우리 공동의 관심사입니다.
당신은 저를 도와 이 작업을 완료해야 합니다.
작업은 {task}입니다.
절대 작업을 잊지 마세요!
저는 당신의 전문 지식과 제 요구에 따라 작업 지침을 내릴 것입니다.
한 번에 하나의 지침만 내릴 것입니다.
당신은 지침을 적절히 완료하는 구체적인 해결책을 작성해야 합니다.
물리적, 도덕적, 법적 이유나 당신의 능력 문제로 인해 지침을 따를 수 없는 경우, 정직하게 지침을 거부하고 그 이유를 설명해야 합니다.
제가 내린 지침에 대한 해결책 외에 추가 내용을 아무 것도 포함하지 마세요.
저에게 질문하지 말고 오직 문제에 대한 답변만 하세요.
잘못된 해결책을 제시하지 마세요.
해결책을 설명하고, 해결책은 현재형으로 작성하세요.
제가 작업이 완료되었다고 말할 때까지, 항상 다음과 같이 응답해야 합니다:

해결책: <YOUR_SOLUTION>
<YOUR_SOLUTION>은 구체적이어야 하며, 작업을 완료하기 위한 최적의 구현과 예를 제공해야 합니다.
항상 "다음 요청."으로 끝내세요.
"""

user_inception_prompt = """
당신은 {user_role_name}이고, 저는 {assistant_role_name}라는 것을 절대 잊으면 안 됩니다.
역할을 절대 바꾸지 마세요!
당신은 저에게 계속해서 지침을 내려야 합니다!
성공적으로 작업을 완료하는 것이 우리 공동의 관심사입니다.
당신은 저를 도와 이 작업을 완료해야 합니다.
작업은 {task}입니다.
절대 작업을 잊지 마세요!

1. 필요한 입력과 함께 지침 하달:
지침: <YOUR_INSTRUCTION>
입력: <YOUR_INPUT>
2. 입력 없이 지침 하달:
지침: <YOUR_INSTRUCTION>
입력: 없음
"지침"은 작업이나 문제를 설명합니다.
"입력"은 요청된 "지침"에 대한 추가 배경 또는 정보를 제공합니다.
한 번에 하나의 지침만 내려야 합니다.
저는 지침을 적절히 완료하는 응답을 작성해야 합니다.
물리적, 도덕적, 법적 이유나 제 능력 문제로 인해 지침을 따를 수 없는 경우, 정직하게 지침을 거부하고 그 이유를 설명해야 합니다.
저에게 질문하지 말고, 저에게 지침을 내리세요.
이제 위 두 가지 방식으로 저에게 지침을 내리세요.
지침과 선택적 입력 외에는 아무런 추가 내용을 포함하지 마세요!
작업이 완료되었다고 생각할 때까지 계속 지침을 내리세요.
작업이 완료되면, 한 단어로만 답변하세요: <CAMEL_TASK_DONE>.
제가 작업을 완료하는 답변을 하지 않으면 절대 <CAMEL_TASK_DONE>을 말하지 마세요.
"""

# 설정된 역할과 작업 프롬프트를 기반으로 시스템 메시지 생성
def get_sys_msgs(assistant_role_name: str, user_role_name: str, task: str):
    assistant_sys_template = SystemMessagePromptTemplate.from_template(
        template=assistant_inception_prompt
    )
    assistant_sys_msg = assistant_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
    )[0]

    user_sys_template = SystemMessagePromptTemplate.from_template(
        template=user_inception_prompt
    )
    user_sys_msg = user_sys_template.format_messages(
        assistant_role_name=assistant_role_name,
        user_role_name=user_role_name,
        task=task,
    )[0]

    return assistant_sys_msg, user_sys_msg

# 시스템 메시지 생성
assistant_sys_msg, user_sys_msg = get_sys_msgs(
    assistant_role_name, user_role_name, specified_task
)

# 인공 지능 도우미와 인공 지능 사용자의 CAMELAgent 인스턴스 생성
assistant_agent = CAMELAgent(assistant_sys_msg, ChatOpenAI(temperature=0.2))
user_agent = CAMELAgent(user_sys_msg, ChatOpenAI(temperature=0.2))

# 에이전트 초기화
assistant_agent.reset()
user_agent.reset()

# 대화 상호 작용 초기화
assistant_msg = HumanMessage(
    content=(
        f"{user_sys_msg.content}。"
        " 이제 하나씩 소개를 시작하세요."
        " 지침과 입력만을 포함해 답변하세요."
    )
)

user_msg = HumanMessage(content=f"{assistant_sys_msg.content}")
user_msg = assistant_agent.step(user_msg)

# 대화 상호 작용 시뮬레이션, 대화 회수 제한 또는 작업 완료 시 종료
chat_turn_limit, n = 30, 0

while n < chat_turn_limit:
    n += 1

    # 사용자 에이전트의 응답 생성
    user_ai_msg = user_agent.step(assistant_msg)
    user_msg = HumanMessage(content=user_ai_msg.content)
    print(f"인공 지능 사용자 ({user_role_name}):\n\n{user_msg.content}\n\n")

    # 도우미 에이전트의 응답 생성
    assistant_ai_msg = assistant_agent.step(user_msg)
    assistant_msg = HumanMessage(content=assistant_ai_msg.content)
    print(f"인공 지능 도우미 ({assistant_role_name}):\n\n{assistant_msg.content}\n\n")

    # 작업 완료 확인
    if "<CAMEL_TASK_DONE>" in user_msg.content:
        break
