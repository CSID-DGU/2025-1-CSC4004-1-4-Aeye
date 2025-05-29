from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_review_info(review_data):
    review_text = "\n".join([r["text"] for r in review_data.get("reviews", [])])
    prompt = f"""
        사용자들의 평균 만족도는 \n{review_data.average_grade}\n입니다. 항목과 %를 있는 그대로 보여주심시오.
        리뷰정보는\n{review_data.review_all}\n입니다. 나쁨부터 최고 순서로 되어 있는데, 각 상태 왼쪽에 있는게 그 상태의 숫자입니다. 출력할때는 상태와 그 상태의 갯수를 연결지어서 보여주십시오. 예를 들어 최고: 23개, 좋음: 12개, 보통: 31개, 별로: 20개, 나쁨: 50개 이런 식으로 보여주십시오.
        대표리뷰는 \n{review_data.comment_data}입니다. 이를 2~3줄로 요약해서 보여주십시오.
        이 정보를 토대로
        상품명:\n가격:\n배송정보:\n평균 만족도:\n리뷰 정보:\n대표 리뷰:\n형태로 보여주십시오.
        """ 

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "당신은 시각장애인이나 노인과 같은 디지털 취약계층에게 도움을 주기 위한 쇼핑몰 요약 도우미 입니다. 평균 만족도, 상태별 리뷰 개수, 대표 리뷰 내용을 출력 하십시오."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"reviewSummary": response.choices[0].message.content}
