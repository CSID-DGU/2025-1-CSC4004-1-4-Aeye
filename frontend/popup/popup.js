// popup.js: 요약 버튼 클릭 시 sidePanel 열기
document.getElementById("summarizeBtn").addEventListener("click", async () => {
  // sidePanel 요청 메시지 전송
  await chrome.runtime.sendMessage({ type: "OPEN_SIDEPANEL" });
});
