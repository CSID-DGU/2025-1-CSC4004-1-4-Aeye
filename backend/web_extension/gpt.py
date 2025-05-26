import openai
import json
import os
from dotenv import load_dotenv

# .env 파일 로드 (필수)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 초기화 (필수)
client = openai.OpenAI()

def ask_chatgpt_dom(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 시각장애인이나 노인과 같은 디지털 취약계층에게 도움을 주기 위한 쇼핑몰 요약 도우미 입니다. 상품명, 가격, 배송정보, 평균 만족도, 상태별 리뷰 개수, 대표 리뷰 요약을 하십시오. "},
                {"role": "user", "content": prompt}
            ],
            tools=[  # 필수 필드만 포함
                {
                    "type": "function",
                    "function": {
                        "name": "get_product_info",
                        "description": "상품 정보를 JSON 형태로 제공합니다.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "상품명"},
                                "price": {"type": "string", "description": "상품 가격 (단위 포함)"},
                                "shipping_fee": {"type": "string", "description": "배송 정보"},
                                "average_grade" : {"type" : "string", "description": "평균 만족도" },
                                "review_all" : {"type" : "string", "description": "리뷰 상태별 갯수"},
                                "comment_data" : {"type" : "string", "description": "대표 리뷰 요약"}
                            },
                             "required": ["name", "price", "shipping_fee", "average_grade","review_all","comment_data"]
                            
                        }
                    }
                }
            ],
            tool_choice="auto"
            )
        
        tool_calls = response.choices[0].message.tool_calls
        # JSON 형식으로 변환
        if tool_calls and len(tool_calls) > 0:
            arguments = tool_calls[0].function.arguments
            product_info = json.loads(arguments)  # 문자열 -> 딕셔너리로 변환
            return {
                "name": product_info.get("name"),
                "price": product_info.get("price"),
                "shipping_fee": product_info.get("shipping_fee"),
                "average_grade": product_info.get("average_grade"),
                "review_all" :product_info.get("review_all"),
                "comment_data" : product_info.get("comment_data"),  
            }
       
    except Exception as e:
        print("오류 발생: ",e)
        return None
    

def ask_chatgpt_ocr(given_prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 시각장애인이나 노인과 같은 디지털 취약계층에게 도움을 주기 위한 쇼핑몰 요약 도우미 입니다. ocr 정보를 바탕으로 소비자에게 필요할만한 정보들을 주어진 조건에 맞추어 보여주십시오."},
                {"role": "user", "content": given_prompt}
            ]
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        print("오류 발생: ", e)
        return None