import os
from dotenv import load_dotenv
import openai

def load_openai_key():
    load_dotenv()  # .env 파일 로드
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise EnvironmentError("OPENAI_API_KEY가 설정되지 않았습니다.")