# 응원 메시지 함수
def get_encouragement(mood, name=None):
    # 응원 메시지
    messages = {
        "행복": "당신이 이렇게 밝게 웃고 있는 걸 보니 기분이 좋아요! 긍정적인 마음을 계속 유지하세요!",
        "슬픔": "기억하세요. 가장 어두운 구름 뒤에도 항상 햇살이 당신을 기다리고 있어요.",
        "피곤함": "당신은 이미 충분히 잘했어요. 이제 잠시 쉬어 갈 시간이예요.",
        "스트레스": "깊게 숨을 들이마시고, 천천히 내쉬세요. 모든 것이 잘 될 거예요."
    }

    # 기분에 맞는 응원 메시지 가져오기
    if name:
        message = f"{name}님, {messages.get(mood, '오늘 기분이 어떠신가요? 저는 항상 당신을 응원하고 있어요!')}"
    else:
        message = messages.get(mood, "오늘 기분이 어떠신가요? 저는 항상 당신을 응원하고 있어요!")

    # 맞춤형 응원 메시지 반환
    return message

# 사용 예시
print(get_encouragement("피곤함", "예나"))
