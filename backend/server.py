from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import requests
import json
#openai.api_key=""
openai.api_key=''
#oepn ai 키 설정 
app=Flask(__name__) #Flask 객체를 만들고 웹 서버의 이름을 app 이라고 지정
CORS(app) 
def ask_chatgpt(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        
            {"role": "system", "content": "너는 쇼핑몰 요약 도우미야."},  
            {"role": "user", "content": prompt}
        
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_product_info",
                "description": "상품 정보를 JSON 형태로 제공합니다.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "상품명"
                        },
                        "price": {
                            "type": "string",
                            "description": "상품 가격 (단위 포함)"
                        },
                        "description": {
                            "type": "string",
                            "description": "상품 설명"
                        },
                        "image_url": {
                            "type": "string",
                            "description": "상품의 대표 이미지 주소(URL)"  # 
                        },
                        "product_url": {
                            "type": "string",
                            "description": "상품 상세 페이지 주소(URL)" #삭제
                        }
                    },
                    "required": ["name", "price", "description", "image_url"]
                }
            }
        }
    ],
    tool_choice="auto")
    response_dict = response.to_dict()
    
    choices = response_dict["choices"]
    tool_calls = choices[0]["message"]["tool_calls"]

    products = []

    for call in tool_calls:
        args_str = call["function"]["arguments"]
        try:
            product = json.loads(args_str)
            products.append(product)
        except json.JSONDecodeError:
            print("JSON 파싱 오류:", args_str)

    # 결과 출력
    if products:
        product = products[0]
        print("상품명:", product.get("name"))
        print("가격:", product.get("price"))
        print("설명:", product.get("description"))
        print("이미지 주소:", product.get("image_url"))
        print("상세 주소:", product.get("product_url"))
    print("-------------------------------------")
    print("json :",product)
    return product
    """
    products_json = []
    if products:
        product = products[0]
        product_info = {
            "상품명": product.get("name"),
            "가격": product.get("price"),
            "설명": product.get("description"),
            "이미지 주소": product.get("image_url"),
            "상세 주소": product.get("product_url")
        }
        products_json.append(product_info)
        

    result_string = "\n\n".join(
        [f"상품명: {p['상품명']}\n가격: {p['가격']}\n설명: {p['설명']}\n이미지 주소: {p['이미지 주소']}\n상세 주소: {p.get('상세 주소', '없음')}\n---------"
         for p in products_json]
    )
    """
    

def summarize_chunks(chunks):  #실제 요약 진행 함수
    summaries=[] #요약본 저장 배열 
    
    print(f"{len(chunks)} 요약 중입니다.")
    prompt=f"""이 쇼핑몰 페이지에서 상품 정보를 JSON 형식으로 요약해줘.
각 상품마다 다음 항목을 포함해 줘:
- name: 상품명
- price: 가격
- description: 설명
- image_url: 대표 이미지 주소
- product_url: 상세 페이지 주소 (가능한 경우)
결과는 JSON 배열 형식으로 보여줘.
내용:{chunks}"""  
    summary=ask_chatgpt(prompt) #요약본 저장
    #summaries.append(summary) #배열에 저장
    #return "\n".join(summaries) #요약 내용들 합치기
    print("---------------------------------------------------")
    print("recieved json: ",summary)
    return summary
@app.route("/summarize", methods=["POST"])
def summarize_api(): # fetch 관련 함수 
    print("요약 시작")
    data=request.get_json()  #json 형태로 받는 것을 python 딕셔너리로 변경
   
    chunks =data.get("chunks", []) #chunks에 배열 형태로 저장하고

    if not chunks:
        print("청크가 비어있음")
        return jsonify({"error" :"chunks가 비어 있음"})
    print("청크 확인됨")
    result=summarize_chunks(chunks) #summarize 진행
    print("---------------------------------------------------")
    print("last recieved json: ",result)
    return jsonify(result) if isinstance(result, dict) else jsonify({"error": "Invalid result format"})

if __name__=="__main__": #이 파일을 직접 실행했을때만 아래 코드를 실행해달라는 코드
    app.run(port=5000) #flask 서버를 실제로 실행시켜줌