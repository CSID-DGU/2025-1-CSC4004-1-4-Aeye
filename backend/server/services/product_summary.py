from openai import OpenAI
from dotenv import load_dotenv
import os
from .ocr_runner import extract_text_from_images

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_basic_info(basic_data):
    prompt = f"""상품명은\n{basic_data["name"]}\n입니다. 원산지 부분은 제거하시고 보여주십시오.
        가격은\n{basic_data["price"]}\n입니다. 그 중 제일 낮은 숫자가 판매가입니다. 단위로는 원을 붙여서 보여주십시오.
        배송정보는\n{basic_data["shipping_fee"]}\n입니다. 언제 도착하는지만 보여주십시오.
        이 정보를 토대로
        상품명:\n가격:\n배송정보:\n형태로 보여주십시오.
        """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 시각장애인이나 노인과 같은 디지털 취약계층에게 도움을 주기 위한 쇼핑몰 요약 도우미 입니다. 상품명, 가격, 배송정보를 출력 하십시오."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"basic": response.choices[0].message.content}

def summarize_detail_info(detail_data):
    ocr_text = extract_text_from_images(detail_data["img_paths"])

    prompt = f"""
        ocr 정보는 다음과 같습니다.
        ocr 정보: \n{ocr_text}\n 
        ocr 정보를 바탕으로 상품의 카테고리를 분류하십시오. 상품의 카테고리에 따라 반드시 들어가야 할 필수정보들과 함께 소비자에게 필요한 정보들을 5줄~7줄로 정리해서 보여주십시오.
        이때 이 정보가 ocr 정보다라는 내용과 어떤 카테고리에 속한다는 내용은 출력하지 마십시오. OCR 안에 있는 내용만을 바탕으로 출력하십시오.
        이때 해당 내용들을 보기 좋게 정리해서 보여주십시오. 예를 들어\n1. 색상: 빨강색, 흰색\n 2. 영양정보: 단백질 200g, 탄수화물 100g\n 이와 같이 출력하십시오. 이때 모든 정보는 '-입니다' 체로 출력하십시오.
        카테고리에 따른 필수정보들은 다음과 같습니다. 
        상품의 카테고리가 패션의류/잡화일 경우 색상과 사이즈 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 뷰티일 경우 추천 대상에 관한 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 출산/유아동일 경우 안전에 대한 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 식품일 경우 영양정보를 반드시 보여주십시오.\n
        상품의 카테고리가 주방용품일 경우 사용시 주의사항에 관한 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 생활용품일 경우 사용 및 보관시 주의사항에 관한 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 홈인테리어일 경우 제품 크기에 대한 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 가전디지털일 경우 호환기종 및 교환.환불 규정에 대한 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 스포츠/레저일 경우 의류 제품이면 크기와 구성정보를 보여주십시오.\n
        상품의 카테고리가 자동차 용품일 경우 제품의 용도에 대한 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 도서/음반/DVD일 경우 추천 대상에 관한 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 완구/취미일 경우 구성성품에 대한 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 문구/오피스일 경우 색상정보를 반드시 보여주십시오.\n
        상품의 카테고리가 반려 동물 용품일 경우 사용방법 및 주의사항에 대한 정보를 반드시 보여주십시오.\n
        상품의 카테고리가 헬스/건강식품일 경우 복용방법 및 주요성분에 대한 정보를 반드시 보여주십시오.\n
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 시각장애인이나 노인과 같은 디지털 취약계층에게 도움을 주기 위한 쇼핑몰 요약 도우미 입니다. 해당 OCR 정보를 바탕으로 사용자에게 도움이 되는 정보를 요약하여 출력하십시오."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"detail": response.choices[0].message.content}
