// frontend/popup/popup.js
// popup.js: 요약 버튼 클릭 시 sidePanel 열기
document.getElementById("summarizeBtn").addEventListener("click", async () => {
  // sidePanel 요청 메시지 전송
  // 현재 탭을 가져옴 
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // sidepanel 열기 메시지 전송 (background.js)
  await chrome.runtime.sendMessage({
    tabId: tab.id,
    action: "OPEN_SIDEPANEL"
  })

  // 페이지 요약 메시지 전송 (background.js)
  // await chrome.runtime.sendMessage({
  //   tabId: tab.id,
  //   type: "SUMMARIZE_PAGE"
  // });

  // 팝업 창 닫기
  window.close();
});
