from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_review_info(review_data):
    prompt = f"""
        사용자들의 평균 만족도는 \n{review_data["average_grade"]}\n입니다. 항목과 %를 있는 그대로 보여주심시오.
        리뷰정보는\n{review_data["review_info"]}\n입니다. 나쁨부터 최고 순서로 되어 있는데, 각 상태 왼쪽에 있는게 그 상태의 숫자입니다. 출력할때는 상태와 그 상태의 갯수를 연결지어서 보여주십시오. 예를 들어 최고: 23개, 좋음: 12개, 보통: 31개, 별로: 20개, 나쁨: 50개 이런 식으로 보여주십시오.
        대표리뷰는 \n{review_data["comment_data"]}입니다. 이를 2~3줄로 요약해서 보여주십시오.
        이 정보를 토대로
        평균 만족도:\n리뷰 정보:\n대표 리뷰:\n형태로 보여주십시오.
        """ 

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
                                "average_grade" : {"type" : "string", "description": "평균 만족도" },
                                "review_all" : {"type" : "string", "description": "리뷰 상태별 갯수"},
                                "comment_data" : {"type" : "string", "description": "대표 리뷰 요약"}
                            },
                             "required": [ "average_grade","review_all","comment_data"]
                            
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
                "average_grade": product_info.get("average_grade"),
                "review_all" :product_info.get("review_all"),
                "comment_data" : product_info.get("comment_data"),  
            }
       
    except Exception as e:
        print("오류 발생: ",e)
        return None

    return {"reviewSummary": response.choices[0].message.content}
