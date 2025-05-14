// background.js: 메시지 리스너 및 sidePanel 열기 기능
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "OPEN_SIDEPANEL") {
    chrome.sidePanel.setOptions({
      tabId: message.tabId,
      path: "sidepanel/sidepanel.html",
      enabled: true,
    });
    chrome.sidePanel.open({ tabId: message.tabId });
  } else if(message.type === "SUMMARIZE_PAGE") {
    (async() => {
      const tabId = message.tabId;

      // 이미지 URL 추출 메시지 전송 (contentScript.js)
      const imgRes = await new Promise((resolve) => {
        chrome.tabs.sendMessage(tabId, { action: "EXTRACT_IMG" }, resolve);
      });
      const imgUrls = imgRes?.imgUrls || [];

      // 텍스트 추출 메시지 전송 (contentScript.js)
      const textRes = await new Promise((resolve) => {
        chrome.tabs.sendMessage(tabId, { action: "EXTRACT_TEXT" }, resolve);
      })
      const productData = textRes?.productData || {};

      // 서버로 전송할 데이터
      const data = {
        name: productData.name || "상품명 없음",
        price: productData.price || "가격 없음",
        more_option: productData["more_option"] || "옵션 없음",
        shipping_fee: productData["shipping_fee"] || "배송 정보 없음",
        commentData: productData["commentData"] || "리뷰 없음",
        worstCommentData: productData["worstCommentData"] || "부정 리뷰 없음",
        average_grade: productData["average_grade"] || "평균 평점 없음", 
        review_All:productData["review_All"]||"리뷰 정보 없음",
        review_length: productData["review_length"] || 0,
        imgUrls: imgUrls,
      };

      // 서버로 전송
      try{
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

        try{
          // 단일 객체인지 배열인지 확인
          if(Array.isArray(resultData)) {
            result = resultData.map((item, index) => {
              return `[${index + 1}]
              상품명: ${item.name || '이름 없음'}
              가격: ${item.price || '없음'}
              옵션정보: ${item.more_option || '없음'}
              배송정보: ${item.shipping_fee || '없음'}
              평균만족도" ${item.average_grade || '없음'}
              리뷰정보: ${item.review_All || '없음'}
              리뷰개수: ${item.review_length || '없음'}
              대표리뷰: ${item.commentData || '없음'}`;
            }).join('\n');
          } else if(typeof resultData === "object" && resultData != null) {
            result = `
            상품명: ${resultData.name || '이름 없음'}
            가격: ${resultData.price || '없음'}
            옵션정보: ${resultData.more_option || '없음'}
            배송정보: ${resultData.shipping_fee || '없음'}
            평균만족도: ${resultData.average_grade || '없음'}
            리뷰정보: ${resultData.review_All||'없음'}
            리뷰개수: ${resultData.review_length || '없음'}
            대표리뷰: ${resultData.commentData || '없음'}`;
          } else {
            result = JSON.stringify(resultData, null, 2);
            console.error("❌ Unexpected data format:", resultData);
          }
        } catch(e) {
          console.error("⚠️ Error processing data:", e);
          result = "Invalid data format received.";
        }

        console.log("✅ 정돈된 결과:\n", result);
        sendResponse()

        // sidepanel로 데이터 전송
        chrome.runtime.sendMessage({
          action: "UPDATE_SIDEPANEL",
          data: resultData
        });
      } catch(e) {
        console.error("🚫 Error during fetch:", e);
        sendResponse()
      }
    })();
    // 비동기 응답 허용
    return true;
  }
});
