from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_review_info(data):
    review_text = "\n".join([r["text"] for r in data.get("reviews", [])])
    prompt = f"""아래 사용자 리뷰를 요약해줘.

요약 항목:
- 전체 리뷰 개수
- 평점 분포 (별점별 개수 및 비율)
- 대표 리뷰 요약 (2~3줄)

리뷰 내용:
{review_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "너는 리뷰 요약 도우미야."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"reviewSummary": response.choices[0].message.content}
