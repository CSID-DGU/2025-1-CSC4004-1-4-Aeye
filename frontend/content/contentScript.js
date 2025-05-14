//import { cleanText } from './4_1.js';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    // 이미지 URL 추출
    if(request.action === 'EXTRACT_IMG') {
        const container = document.querySelector('.product-detail-content-inside');
        const imgs = container
            ? Array.from(container.querySelectorAll('img'))
                .filter(img => img.src && !img.src.startsWith('data:'))
            : [];

        const imgUrls = imgs.map(img => img.src);
        sendResponse({ imgUrls });

        return true;
    } else if(request.action === 'EXTRACT_TEXT') {
        const data = {};

        // 상품명
        const nameElement = document.querySelector('.prod-buy-header');
        data.name = nameElement ? nameElement.textContent : '상품명 없음';
        
        // 가격
        const priceElement = document.querySelector('.prod-price');
        data.price = priceElement ? priceElement.textContent : '가격 없음';

        // 더 많은 옵션
        const moreOptionElement = document.querySelector('.prod-more-option');
        data["more_option"] = moreOptionElement ? moreOptionElement.textContent: '옵션 없음';
        
        // 배송 정보
        const shippingFeeElement = document.querySelector('.shipping-fee-and-pdd-prod');
        data["shipping_fee"] = shippingFeeElement ? shippingFeeElement.textContent : '배송 정보 없음';

        // 대표 리뷰
        const commentElement = document.querySelector('.sdp-review__article__list__review__content');
        data["commentData"] = commentElement ? commentElement.textContent : '대표 리뷰 없음';

        // 부정 리뷰
        const reviewElements = document.querySelectorAll(".sdp-review__article__list__review__content");
        const worstCommentElement = reviewElements.length > 0 ? reviewElements[reviewElements.length - 1] : null;
        data["worstCommentData"] = worstCommentElement ? worstCommentElement.textContent : '부정 리뷰 없음';

        // 리뷰 정보
        const reviewAll=document.querySelector('.sdp-review__article__order__star__all');
        data.review_All=reviewAll?reviewAll.textContent.trim():"리뷰 정보 없음";

        // 평균 평점
        const averagGrade=document.querySelector('.sdp-review__average__summary__section');
        data.average_grade = averagGrade? averagGrade.textContent.trim() : '평균 평점 없음';

        const review_length = document.querySelector('.sdp-review__average__total-star__info-count');
        data.review_length = review_length ? review_length.textContent.trim() : 0;

        sendResponse({ productData: data });
        return true;
    }   
})