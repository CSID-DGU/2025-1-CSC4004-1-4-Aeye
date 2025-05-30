from openai import OpenAI
from dotenv import load_dotenv
import os
from .ocr_runner import extract_text_from_images
import json
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_basic_info(basic_data):
    prompt = f"""상품명은\n{basic_data["name"]}\n입니다. 원산지 부분은 제거하시고 보여주십시오.
        가격은\n{basic_data["price"]}\n입니다. 그 중 제일 낮은 숫자가 판매가입니다. 단위로는 원을 붙여서 보여주십시오.
        배송정보는\n{basic_data["shipping_fee"]}\n입니다. 언제 도착하는지만 보여주십시오.
        이 정보를 토대로
        상품명:\n가격:\n배송정보:\n형태로 보여주십시오.
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
                                "name": {"type": "string", "description": "상품명"},
                                "price": {"type": "string", "description": "상품 가격 (단위 포함)"},
                                "shipping_fee": {"type": "string", "description": "배송 정보"},
                            },
                             "required": ["name", "price", "shipping_fee"]
                            
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
            }
       
    except Exception as e:
        print("오류 발생: ",e)
        return None
    

def summarize_detail_info(detail_data):
    ocr_text = extract_text_from_images(detail_data["img_paths"])

    prompt = f"""
        ocr 정보: \n{ocr_text}\n Add commentMore actions
        ocr 정보를 바탕으로 상품의 카테고리를 분류하십시오. 상품의 카테고리에 따라 반드시 들어가야 할 필수정보들과 함께 소비자에게 필요한 정보들을 5줄~7줄로 정리해서 보여주십시오.
        이때 이 정보가 ocr 정보다라는 내용과 어떤 카테고리에 속한다는 내용은 출력하지 마십시오. OCR 안에 있는 내용만을 바탕으로 출력하십시오.
        이때 해당 내용들을 보기 좋게 정리해서 보여주십시오. 예를 들어\n1. 색상: 빨강색, 흰색\n 2. 영양정보: 단백질 200g, 탄수화물 100g\n 이와 같이 출력하십시오. 
        카테고리에 따른 필수정보들은 다음과 같습니다. 
        상품의 카테고리가 패션의류/잡화일 경우 색상과 사이즈 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 뷰티일 경우 추천 대상에 관한 정보를 반드시 보여주십시오.\n
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 시각장애인이나 노인과 같은 디지털 취약계층에게 도움을 주기 위한 쇼핑몰 요약 도우미 입니다. 해당 OCR 정보를 바탕으로 사용자에게 도움이 되는 정보를 요약하여 출력하십시오."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"detail": response.choices[0].message.content}
