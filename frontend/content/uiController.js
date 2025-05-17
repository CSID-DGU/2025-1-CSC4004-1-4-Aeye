function extractProductData() {
    const data = {};
    // Product Name
    const nameElement = document.querySelector('.prod-buy-header');
    data.name = nameElement ? nameElement.textContent.trim() : '상품명 없음';
    
    // Price
    const priceElement = document.querySelector('.prod-price');
    data.price = priceElement ? priceElement.textContent.trim() : '가격 없음';
    
    // More Options
    const moreOptionElement = document.querySelector('.prod-more-option');
    data.more_option = moreOptionElement ? moreOptionElement.textContent.trim() : '옵션 없음';
    
    // Shipping Info
    const shippingFeeElement = document.querySelector('.shipping-fee-and-pdd-prod');
    data.shipping_fee = shippingFeeElement ? shippingFeeElement.textContent.trim() : '배송 정보 없음';

    // Representative Comment
    const commentElement = document.querySelector('.sdp-review__article__list__review__content');
    data.comment_data = commentElement ? commentElement.textContent.trim() : '대표 리뷰 없음';
    
    // Overall Review Summary
    const reviewAll = document.querySelector('.sdp-review__article__order__star');
    data.review_all = reviewAll ? reviewAll.textContent.trim() : '리뷰 정보 없음';
    
    // Average Grade
    const averagGrade = document.querySelector('.sdp-review__average__summary');
    data.average_grade = averagGrade ? averagGrade.textContent.trim() : '평균 평점 없음';
    
    // Review Length
    const reviewLength = document.querySelector('.sdp-review__average__total-star__info-count');
    data.review_length = reviewLength ? reviewLength.textContent.trim() : '0';
    
    return data;
}


document.addEventListener('DOMContentLoaded', () => {
    const summarizeButton = document.getElementById('summarizeBtn');
    const summaryDiv = document.getElementById('summaryContainer');
    


    summarizeButton.addEventListener('click', () => {
        chrome.tabs.query({ active: true, lastFocusedWindow: true }, ([tab]) => {
            if (tab) {
                chrome.scripting.executeScript(
                    {
                        target: { tabId: tab.id },
                        func: extractProductData,
                    },
                    (results) => {
                        const productData = results[0].result || {};

                        console.error('review_All:', productData.review_All);
                        console.error('commentData:', productData.commentData);

                        console.log('🔗 Sending product data:', productData);
                        chrome.runtime.sendMessage(
                            { action: 'summarizePage', productData, tabId: tab.id },
                            (response) => {
                                if (response && response.summary) {
                                    summaryDiv.innerText = response.summary.name || 'No summary available.';
                                } else {
                                    summaryDiv.innerText = 'No summary available.';
                                }
                            }
                        );
                    }
                );
            } else {
                console.error('No active tab.');
            }
        });
    });
});
