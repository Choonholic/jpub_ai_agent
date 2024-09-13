import json

from dotenv import load_dotenv

load_dotenv()

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# 지정된 도시의 꽃 재고 조회 함수
def get_flower_inventory(city):
    """지정된 도시의 꽃 재고를 조회합니다."""
    if "서울" in city:
        return json.dumps({"city": "서울", "inventory": "장미: 100, 튤립: 150"})
    elif "대전" in city:
        return json.dumps({"city": "대전", "inventory": "백합: 80, 카네이션: 120"})
    elif "광주" in city:
        return json.dumps({"city": "광주", "inventory": "해바라기: 200, 목련: 90"})
    else:
        return json.dumps({"city": city, "inventory": "알 수 없음"})

# 도구 목록 정의 (함수 속성 정보)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_flower_inventory",
            "description": "지정된 도시의 꽃 재고를 조회합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "도시, 예: 서울, 대전, 광주"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 대화 내용 초기화
messages = [{"role": "user", "content": "서울, 대전, 광주의 꽃 재고는 얼마인가요?"}]

print("message:", messages)

# 첫 번째 대화 응답
first_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# 응답 내용 출력
print(first_response)

response_message = first_response.choices[0].message

# 도구 호출이 필요한지 확인
tool_calls = response_message.tool_calls

if tool_calls:
    messages.append(response_message)

# 도구 호출이 필요할 경우, 도구를 호출하고 재고 조회 결과 추가
for tool_call in tool_calls:
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)
    function_response = get_flower_inventory(
        city=function_args.get("city")
    )
    messages.append(
        {
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": function_response,
        }
    )

# 현재 메시지 목록 출력
print("message:", messages)

# 두 번째 요청을 통해 최종 응답 받기
final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

print(final_response)

# 최종 응답의 내용만 출력
content = final_response.choices[0].message.content

print(content)
