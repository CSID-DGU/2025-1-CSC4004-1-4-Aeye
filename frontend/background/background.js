// background.js: 메시지 리스너 및 sidePanel 열기 기능
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "OPEN_SIDEPANEL") {
    chrome.sidePanel.setOptions({
      tabId: message.tabId,
      path: "frontend/sidepanel/sidepanel.html",
      enabled: true,
    });
    chrome.sidePanel.open({ tabId: message.tabId });

  } else if(message.type === "SUMMARIZE_BASIC") {
    chrome.tabs.sendMessage(message.tabId, { action: "EXTRACT_BASIC" }, async (basicData) => {
      const response = await fetch("http://localhost:5000/summary/basic", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(basicData)
      });

      const basicResult = await response.json();
      console.log("📥 서버 응답:", basicResult);
      // 서버 응답을 sidePanel로 전달
      chrome.runtime.sendMessage({ tabId: message.tabId, action: "BASIC_SUMMARY_RESULT", data: basicResult });
    });

  } else if(message.type === "SUMMARIZE_DETAIL") {
    chrome.tabs.sendMessage(message.tabId, { action: "EXTRACT_DETAIL" }, async (detailData) => {
      const response = await fetch("http://localhost:5000/summary/detail", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(detailData)
      });

      const detailResult = await response.json();
      console.log("📥 서버 응답:", detailResult);
      // 서버 응답을 sidePanel로 전달

      chrome.runtime.sendMessage({ tabId: message.tabId, action: "DETAIL_SUMMARY_RESULT", data: detailResult });
    });

  } else if(message.type === "SUMMARIZE_REVIEW") {
    chrome.tabs.sendMessage(message.tabId, { action: "EXTRACT_REVIEW" }, async (reviewData) => {
      const response = await fetch("http://localhost:5000/review-summary", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(reviewData)
      });

      const reviewResult = await response.json();
      console.log("📥 서버 응답:", reviewResult);
      // 서버 응답을 sidePanel로 전달
      chrome.runtime.sendMessage({ tabId: message.tabId, action: "REVIEW_SUMMARY_RESULT", data: reviewResult });
    });
  }
});