# autogen 패키지 가져오기
import autogen

# 대형 언어 모델 설정
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o",
            "api_key": 'OpenAI API Key'
        }
    ],
}

# 꽃말의 비밀 정원 운영 관련 작업 정의
inventory_tasks = [
    """현재 재고에 있는 다양한 꽃의 수량을 확인하고, 어떤 꽃의 재고가 부족한지 보고하세요.""",
    """지난 한 달간의 판매 데이터를 바탕으로 다음 달에 어떤 꽃의 수요가 증가할지 예측하세요.""",
]

market_research_tasks = [
    """시장 동향을 분석하고 현재 가장 인기 있는 꽃 종류와 그 이유를 찾아보세요.""",
]

content_creation_tasks = [
    """제공된 정보를 바탕으로 가장 인기 있는 꽃과 구매 팁을 소개하는 매력적인 블로그 게시글을 작성하세요.""",
]

# 에이전트 역할 생성
inventory_assistant = autogen.AssistantAgent(
    name="InventoryAssistant",
    llm_config=llm_config,
)

market_research_assistant = autogen.AssistantAgent(
    name="MarketResearchAssistant",
    llm_config=llm_config,
)

content_creator = autogen.AssistantAgent(
    name="ContentCreator",
    llm_config=llm_config,
    system_message="""
    당신은 통찰력이 뛰어나고 매력적인 글을 쓰는 것으로 유명한 전문 작가입니다.
    복잡한 개념을 흥미로운 이야기로 변환할 수 있습니다.
    """,
)

# 사용자 프록시 에이전트 생성
user_proxy_auto = autogen.UserProxyAgent(
    name="UserProxyAuto",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },
)

user_proxy = autogen.UserProxyAgent(
    name="UserProxy",
    human_input_mode="ALWAYS",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },
)

# 대화 시작
chat_results = autogen.initiate_chats([
    {
        "sender": user_proxy_auto,
        "recipient": inventory_assistant,
        "message": inventory_tasks[0],
        "clear_history": True,
        "silent": False,
        "summary_method": "last_msg",
    },
    {
        "sender": user_proxy_auto,
        "recipient": market_research_assistant,
        "message": market_research_tasks[0],
        "max_turns": 2,
        "summary_method": "reflection_with_llm",
    },
    {
        "sender": user_proxy,
        "recipient": content_creator,
        "message": content_creation_tasks[0],
        "carryover": "블로그 게시물에 데이터 표나 그래프를 포함하고 싶습니다.",
    },
])
