
def make_prompt(name,price,shipping_fee,average_grade,review_all,comment_data):
    return f"""
        상품명은\n{name}\n입니다. 원산지 부분은 제거하시고 보여주십시오.
        가격은\n{price}\n입니다. 그 중 제일 낮은 숫자가 판매가입니다. 단위로는 원을 붙여서 보여주십시오.
        배송정보는\n{shipping_fee}\n입니다. 언제 도착하는지만 보여주십시오.
        사용자들의 평균 만족도는 \n{average_grade}\n입니다. 항목과 %를 있는 그대로 보여주심시오.
        리뷰정보는\n{review_all}\n입니다. 나쁨부터 최고 순서로 되어 있는데, 각 상태 왼쪽에 있는게 그 상태의 숫자입니다. 출력할때는 상태와 그 상태의 갯수를 연결지어서 보여주십시오. 예를 들어 최고: 23개, 좋음: 12개, 보통: 31개, 별로: 20개, 나쁨: 50개 이런 식으로 보여주십시오.
        대표리뷰는 \n{comment_data}입니다. 이를 2~3줄로 요약해서 보여주십시오.
        이 정보를 토대로
        상품명:\n가격:\n배송정보:\n평균 만족도:\n리뷰 정보:\n대표 리뷰:\n형태로 보여주십시오.
        """ 

def make_prompt2(id,ocr=""):
    if id == 185635 :
        item_type = "주방용품"
        given_task = "식기세척기 가능여부"
    elif id == 501348 :
        item_type = "헬스/건강식품"
        given_task = "복용방법, 보관방법, 주요성분"
    else :
        item_type = "정보없음"
        given_task = "주어진 테스크 없음"
    return f"""
         현재 상품은 {item_type}입니다. 다음 ocr 정보를 가지고 {given_task}를 판별하세요:
        \n{ocr}
        """
#추가 필요합니다. 
