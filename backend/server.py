from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import os
from dotenv import load_dotenv
import json

# .env 파일 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

client = openai.OpenAI()

def ask_chatgpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "너는 쇼핑몰 요약 도우미야."},
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
                                "more_option": {"type": "string", "description": "더 많은 옵션"},
                                "shipping_fee": {"type": "string", "description": "배송 정보"},
                                "average_grade" : {"type" : "string", "description": "평균 만족도" },
                                "review_All" : {"type" : "string", "description": "리뷰"},
                                "commentData" : {"type" : "string", "description": "리뷰 요약"}
                            },
                             "required": ["name", "price", "more_option", "shipping_fee", "average_grade","review_All","commentData"]
                            
                        }
                    }
                }
            ],
            tool_choice="auto"
        )
        
        tool_calls = response.choices[0].message.tool_calls
        if tool_calls and len(tool_calls) > 0:
            arguments = tool_calls[0].function.arguments
            product_info = json.loads(arguments)  # 문자열 -> 딕셔너리로 변환
            return {
                "name": product_info.get("name"),
                "price": product_info.get("price"),
                "more_option": product_info.get("more_option"),
                "average_grade": product_info.get("average_grade"),
                "shipping_fee": product_info.get("shipping_fee"),
                "review_All" :product_info.get("average_review"),
                "commentData" : product_info.get("commentData")
            }
    except Exception as e:
        print("오류 발생:", e)
        return None

def ask_chatgpt2(review_All, commentData):
            
            try:
                prompt=f"""리뷰정보는
    \n{review_All}\n 이야.
    나쁨부터 최고 순서로 되어 있는데, 각 상태 왼쪽에 있는게 그 상태의 숫자이고. 출력할때는 상태와 그 상태의 갯수를 연결지어서 보여줘. 예를 들어 최고: 23개, 좋음: 12개, 보통: 31개, 별로: 20개, 나쁨: 50개 이런 식으로 출력해줘.
    리뷰정보:
        최고: 
        좋음:
        보통:
        별로:
        나쁨:
        이 형태로 보여줘! 
        대표리뷰는
        \n{commentData}\n
    여기서 원산지나 유통기한 같은 거 빼고 사람들에게 도움될만한 리뷰로 최대한 압축해서 요약해줘. 두세줄 정도로 요약해줘
    """
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "너는 리뷰 3줄요약 도우미야."},
                        {"role": "user", "content": prompt}
                    ],
                    tools=[
                        {
                            "type": "function",
                            "function": {
                                "name": "summarize_reviews",
                                "description": "리뷰 정보를 짧게 요약합니다.",
                                "parameters": {
                                    "type": "object",
                                    "properties": {
                                        "review_summary": {
                                            "type": "string",
                                            "description": "리뷰 데이터"
                                        },
                                        "commentData": {
                                            "type": "string",
                                            "description": "짧게 요약된 대표 리뷰"
                                        }
                                    },
                                    "required": ["review_summary","commentData"]
                                }
                            }
                        }
                    ],
                    tool_choice="auto"
                )
                
                tool_calls = response.choices[0].message.tool_calls
                if tool_calls and len(tool_calls) > 0:

                    arguments = tool_calls[0].function.arguments
                    review_summary = json.loads(arguments).get("review_summary")
                    commentData = json.loads(arguments).get("commentData")
                    return {
                        "review_summary": review_summary,
                        "commentData": commentData
                    }
            except Exception as e:
                print("오류 발생:", e)
                return None


@app.route("/summarize", methods=["POST"])
def summarize_api():
    print("요약 시작")
    data = request.get_json()
    # 필수 필드 추출
    #product_data = data.get("productData", {})
    name =data.get("name", "상품명 없음")
    price = data.get("price", "가격 없음")
    more_option = data.get("more_option", "옵션 없음")
    shipping_fee =data.get("shipping_fee", "배송 정보 없음")
    commentData = data.get("commentData", "리뷰 없음")
    average_grade=data.get("average_grade", "만족도 조사 없음")
    review_All=data.get("review_All", "리뷰 정보 없음")
    worstComment = data.get("worstCommentData", "최악의 리뷰 없음")
    reviewlegnth = data.get("review_length", "리뷰 길이 없음")
    # 프롬프트 생성
    prompt = f"""
상품명은----- \\n{name}\\n -----인데 출력할때 수정하지 말고 그대로 보여줘!, /////////////////
    가격은----- \\n{price}\\n -----에서 제일 낮은 숫자고, 그게 바로 판매가야! 단위는 원!, 배송정보는 \n{shipping_fee}\n 인데, 언제 도착하는지만 걸러서 보여줘!,
    ////////////////사용자들의 평균 만족도는----- \\n{average_grade}\\n -----
    인데, %랑 항목을 사실대로 보여줘! /////////////////
    /////////////////리뷰정보는----- \\n{review_All}\\n -----
    인데, 나쁨부터 최고 순서로 되어 있는데, 각 상태 왼쪽에 있는게 그 상태의 숫자이고. 출력할때는 상태와 그 상태의 갯수를 연결지어서 보여줘. 예를 들어 최고: 23개, 좋음: 12개, 보통: 31개, 별로: 20개, 나쁨: 50개 이런 식으로로
    {commentData}
    는 대표 리뷰야. 이걸 2, 3줄로 요약해줘
    이 정보를 토대로
    상품명:
    가격:
    배송정보: 
    평균 만족도:
    리뷰 정보:
    대표 리뷰:
    형태로 보여줘!
   
    """
   
    # GPT 호출
    summary = ask_chatgpt(prompt)
    commentData = summary.get("commentData", "리뷰 요약 없음")
    data2 =  ask_chatgpt2(review_All, commentData)
    summary["review_All"] = data2["review_summary"]
    summary["commentData"] = data2["commentData"]

    #summary["worstCommentData"] = worstComment
    summary["review_length"] = reviewlegnth
    # 요약 결과 반환
    if summary:
        print("---------------------------------------------------")
        print("last received json:", summary)
        return jsonify(summary)
    else:
        return jsonify({"error": "GPT 응답 없음"}), 500
    


if __name__ == "__main__":
    app.run(port=5000)
