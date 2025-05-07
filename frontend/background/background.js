// background.js: 메시지 리스너 및 sidePanel 열기 기능
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "OPEN_SIDEPANEL") {
    chrome.sidePanel.setOptions({
      path: "sidepanel/sidepanel.html",
      enabled: true,
    });
    chrome.sidePanel.open();
  }
});
