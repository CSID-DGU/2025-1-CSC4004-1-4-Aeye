// popup.js: 요약 버튼 클릭 시 sidePanel 열기
document.getElementById("summarizeBtn").addEventListener("click", async () => {
  // sidePanel 요청 메시지 전송
  // 현재 탭을 가져옴 
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  // 해당 탭에서 sidepanel 열기
  await chrome.sidePanel.setOptions({
    tabId: tab.id,
    path: "frontend/sidepanel/sidepanel.html",
    enabled: true,
  });

  // 실제로 열기 
  await chrome.sidePanel.open({ tabId: tab.id });

  // 팝업 창 닫기
  window.close();
});
