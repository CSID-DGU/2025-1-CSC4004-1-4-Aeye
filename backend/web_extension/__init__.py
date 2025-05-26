from flask import Flask, request, jsonify
from flask_cors import CORS
from .gpt import ask_chatgpt_dom, ask_chatgpt_ocr
from .config import load_openai_key
from .prompt_dom import make_prompt_dom
from .prompt_ocr import make_prompt_ocr

def create_app():
    app = Flask(__name__)
    CORS(app)

    # 환경 변수 로드
    load_openai_key()
    
    # 라우팅 설정
    @app.route("/summarize", methods=["POST"])
    def summarize_api():
        print("요약 시작")
        data = request.get_json()
        name = data.get("name", "상품명 없음")
        price = data.get("price", "가격 없음")
        shipping_fee = data.get("shipping_fee", "배송 정보 없음")
        average_grade = data.get("average_grade", "만족도 조사 없음")
        review_all = data.get("review_all", "리뷰 정보 없음")
        comment_data = data.get("comment_data", "리뷰 없음")
        review_length = data.get("review_length", "리뷰 길이 없음") 
        prompt_dom = make_prompt_dom(name,price,shipping_fee,average_grade,review_all,comment_data)
        prompt_ocr = make_prompt_ocr(ocr="")

        # GPT 호출
        summary = ask_chatgpt_dom(prompt_dom)
        detailed_info = ask_chatgpt_ocr(prompt_ocr)

        summary["detailed_info"] = detailed_info
        comment_data=summary.get("comment_data", "리뷰 요약 없음")
        summary["review_length"] = review_length
        print(summary["review_length"])
        if summary:
            print("---------------------------------------------------")
            print("last received json:", summary)
            return jsonify(summary)
        else:
            return jsonify({"error": "GPT 응답 없음"}), 500

    return app
