// backend/web_extension/background.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log(request.action);
    if (request.action === "OPEN_SIDEPANEL") {
        chrome.sidePanel.setOptions({
        tabId: request.tabId,
        path: "../frontend/sidepanel/sidepanel.html",
        enabled: true,
        });
        chrome.sidePanel.open({ tabId: request.tabId });
    }
    else if (request.action === "summarizePage") {
        const productData = request.productData || {};
        console.log("📦 받은 데이터:", productData);
        
        // 서버로 전송할 데이터
        const data = {
            name: productData["name"]|| "상품명 없음",
            price: productData["price"]|| "가격 없음",
            shipping_fee: productData["shipping_fee"] || "배송 정보 없음",
            comment_data: productData["comment_data"] || "리뷰 없음",
            average_grade: productData["average_grade"] || "평균 평점 없음", 
            review_all:productData["review_all"]||"리뷰 정보 없음",
            review_length: productData["review_length"] || 0,
    };

        console.log("🔗 서버로 전송할 데이터:", data);

        // 서버로 전송
        summarize_2(data, sendResponse);

        // 비동기 응답 허용
        return true;
    }
});


async function summarize_2(data, sendResponse) {
    try {
        const response = await fetch("http://localhost:5000/summarize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });
        
        const resultData = await response.json();
        console.log("📥 서버 응답:", resultData);

        let result = "";

        try {
            // 단일 객체인지 배열인지 확인
             if (Array.isArray(resultData)) {
                result = resultData.map((item, index) => {
                    return `[${index + 1}] 
상품명: ${item.name || '이름 없음'} 
가격: ${item.price || '없음'}
배송정보: ${item.shipping_fee || '없음'}
평균만족도" ${item.average_grade || '없음'}
리뷰정보: ${item.review_all || '없음'}
리뷰개수: ${item.review_length || '없음'}
대표리뷰: ${item.comment_data || '없음'}`
;
                }).join('\n');
            } else if (typeof resultData === "object" && resultData !== null) {
                result = `
상품명: ${resultData.name || '이름 없음'} 
가격: ${resultData.price || '없음'}
배송정보: ${resultData.shipping_fee || '없음'}
평균만족도: ${resultData.average_grade || '없음'}
리뷰정보: ${resultData.review_all||'없음'}
리뷰개수: ${resultData.review_length || '없음'}
대표리뷰: ${resultData.comment_data || '없음'}`;
            } else {
                result = JSON.stringify(resultData, null, 2);
                console.error("❌ Unexpected data format:", resultData);
            }
        } catch (e) {
            console.error("⚠️ Error processing data:", e);
            result = "Invalid data format received.";
        }

        console.log("✅ 정돈된 결과:\n", result);
        sendResponse({ action: "summaryResponse", summary: resultData });

        // sidepanel로 데이터 전송
        chrome.runtime.sendMessage({
            action: "updateSidepanel",
            data: resultData
        });
    } catch (error) {
        console.error("🚫 Error during fetch:", error);
        sendResponse({ action: "summaryResponse", error: "An error occurred while summarizing." });
    }
}
