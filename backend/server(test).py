'''from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import requests

#oepn ai 키 설정 
app=Flask(__name__) #Flask 객체를 만들고 웹 서버의 이름을 app 이라고 지정
CORS(app) 
def ask_chatgpt(prompt):  # gpt에게 묻는 함수
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 모델.. 추후 변경 가능
        messages=[
            {"role": "system", "content": "너는 쇼핑몰 요약 도우미야."},  # 소문자로 수정
            {"role": "user", "content": prompt}
        ],
        temperature=0.7  # 일단 이렇게 지정
    )
    return response['choices'][0]['message']['content']  # choices의 첫 번째 index의 message 부분의 content를 return

def summarize_chunks(chunks):  #실제 요약 진행 함수
    summaries=[] #요약본 저장 배열 
    for i, chunk in enumerate(chunks):  #chunk 수에 따른 for 문 생성
        print(f"chunk {i+1}/{len(chunks)} 요약 중입니다.")
        prompt=f"""이 쇼핑몰 페이지에서 상품 정보를 JSON 형식으로 요약해줘.
각 상품마다 다음 항목을 포함해 줘:
- name: 상품명
- price: 가격
- description: 설명
- image_url: 대표 이미지 주소
- product_url: 상세 페이지 주소 (가능한 경우)
결과는 JSON 배열 형식으로 보여줘.
내용:{chunk}"""  
        summary=ask_chatgpt(prompt) #요약본 저장
        summaries.append(summary) #배열에 저장
    return "\n".join(summaries) #요약 내용들 합치기
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
    return jsonify({"summary": result}) #json 형태로 return

if __name__=="__main__": #이 파일을 직접 실행했을때만 아래 코드를 실행해달라는 코드
    app.run(debug=True) #flask 서버를 실제로 실행시켜줌'''