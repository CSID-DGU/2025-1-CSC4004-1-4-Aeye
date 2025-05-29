// popup.js: 요약 버튼 클릭 시 sidePanel 열기
document.getElementById("summarizeBtn").addEventListener("click", async () => {
  // sidePanel 요청 메시지 전송
  // 현재 탭을 가져옴 
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const messages = [
    { tabId: tab.id, type: "OPEN_SIDEPANEL" },
    { tabId: tab.id, type: "SUMMARIZE_BASIC" },
    { tabId: tab.id, type: "SUMMARIZE_DETAIL" },
    { tabId: tab.id, type: "SUMMARIZE_REVIEW"}
  ]

  const messagePromises = messages.map(msg => chrome.runtime.sendMessage(msg));
  Promise.all(messagePromises).then(() => {
    // 팝업창 닫기
    window.close();
  });
});
