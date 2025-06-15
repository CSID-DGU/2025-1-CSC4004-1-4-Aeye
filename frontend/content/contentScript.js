chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if(request.action === "EXTRACT_BASIC") { // Basic 정보 추출
        const basicData = {};

        // 상품명
        const name = document.querySelector('.prod-buy-header') || document.querySelector('.product-buy-header');
        basicData["name"] = name ? name.textContent.trim().replace(/\s+/g, ' ') : '상품명 없음';

        // 가격
        const price = document.querySelector('.prod-price') || document.querySelector('.price-container');
        basicData["price"] = price ? price.textContent.trim().replace(/\s+/g, ' ') : '가격 없음';

        // 배송 정보
        const shippingFee = document.querySelector('.shipping-fee-and-pdd-prod') || document.querySelector('.pdd-toggle-container');
        basicData["shipping_fee"] = shippingFee ? shippingFee.textContent.trim().replace(/\s+/g, ' ') : '배송 정보 없음';

        sendResponse(basicData);
        return true;

    } else if(request.action === "EXTRACT_DETAIL") { // Detail 정보 추출
        const detailData = {};

        // 이미지 URL 추출(상품 정보)
        const container = document.querySelector('.product-detail-content-inside');
        const imgs = container
            ? Array.from(container.querySelectorAll('img'))
                .filter(img => img.src && !img.src.startsWith('data:'))
            : [];
        const imgPaths = imgs.map(img => img.src);
        detailData["img_paths"] = imgPaths;
  
        sendResponse(detailData);
        return true;

    } else if(request.action === "EXTRACT_REVIEW") { // Review 정보 추출
        const reviewData = {};

        // 리뷰 수
        const reviewCount = document.querySelector('.sdp-review__average__total-star__info-count') || document.querySelector('.review-average-header-total-count');
        reviewData["review_count"] = reviewCount ? reviewCount.textContent.trim().replace(/\s+/g, ' ') : "0";

        // 평균 평점
        const averagGrade=document.querySelector('.sdp-review__average__summary__section') || document.querySelector('.review-summary-survey-container');
        reviewData["average_grade"] = averagGrade? averagGrade.textContent.trim().replace(/\s+/g, ' ') : '평균 평점 없음';

        // 리뷰 정보
        const reviewInfo=document.querySelector('.sdp-review__article__order__star__all') || document.querySelector('.review-star-search-selector');
        reviewData["review_info"] = reviewInfo ? reviewInfo.textContent.trim().replace(/\s+/g, ' ') : "리뷰 정보 없음";

        // 대표 리뷰
        const mainComment = document.querySelector('.sdp-review__article__list__review__content');
        reviewData["comment_data"] = mainComment ? mainComment.textContent.trim().replace(/\s+/g, ' ') : '대표 리뷰 없음';
        
        sendResponse(reviewData);
        return true;

    }
});