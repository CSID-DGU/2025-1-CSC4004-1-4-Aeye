def generate_tts_script(summary, mode="basic"):
    if mode == "basic":
        return f"이 제품은 {summary.get('name', '이름 없음')}이며, 가격은 {summary.get('price', '없음')}입니다. 배송 정보는 {summary.get('shipping_fee', '정보 없음')}이고, 평균 만족도는 {summary.get('average_grade', '정보 없음')}입니다."
    elif mode == "review":
        return f"사용자 리뷰에 따르면, {summary.get('commentData', '대표 리뷰 없음')} 이 대표적인 평가입니다."
    else:
        return "TTS 스크립트를 생성할 수 없습니다."
