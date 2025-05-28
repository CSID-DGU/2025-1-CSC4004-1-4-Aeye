from openai import OpenAI
import os
from .ocr_runner import extract_text_from_images

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_basic_info(html_text):
    prompt = f"""다음 HTML 텍스트를 바탕으로 상품 정보를 요약해줘.

요약 항목:
- 상품명
- 가격
- 배송 정보
- 옵션 정보
- 사용자 평균 만족도

HTML 내용:
{html_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 쇼핑몰 요약 도우미야."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"summary": response.choices[0].message.content}

# def summarize_detail_info(ocr_text):
#     prompt = f"""아래 OCR 텍스트를 기반으로 상세 상품 정보를 요약해줘.

# 요약 항목:
# - 스펙 정보
# - 특징 설명
# - 주의사항 또는 관리 방법

# OCR 추출 텍스트:
# {ocr_text}
# """

#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "너는 상세정보 요약 도우미야."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return {"detail": response.choices[0].message.content}

def summarize_detail_info_from_images(image_paths):
    ocr_text = extract_text_from_images(image_paths)

    prompt = f"""아래 텍스트는 상세페이지 이미지에서 추출된 내용입니다. 이를 바탕으로:

- 스펙 요약
- 핵심 특징
- 사용시 유의사항

을 문장형태로 요약해줘:

{ocr_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 상세정보 요약 도우미야."},
            {"role": "user", "content": prompt}
        ]
    )

    return {"detail": response.choices[0].message.content}