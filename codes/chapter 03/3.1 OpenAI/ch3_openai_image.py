# OpenAI API 키 설치
import os

os.environ["OPENAI_API_KEY"] = 'OpenAI API Key'

# OpenAI 가져오기
from openai import OpenAI

# client 인스턴스 생성하기
client = OpenAI()

# DALL·E 3에 이미지 생성 요청
response = client.images.generate(
    model="dall-e-3",
    prompt="'꽃말의 비밀 정원' 전자상거래 앱의 새해 장미 꽃 홍보 포스터, 문구도 포함해서",
    size="1024x1024",
    quality="standard",
    n=1
)

# 이미지 URL 가져오기
image_url = response.data[0].url

# 이미지 읽어오기
import requests

image = requests.get(image_url).content

# Jupyter Notebook에서 이미지 표시
from IPython.display import Image

Image(image)
