// sidepanel.js: 백그라운드로부터 상품 요약 정보를 수신
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "SUMMARY_DATA") {
    document.getElementById("summaryContainer").innerText = message.summary;
  }
});
