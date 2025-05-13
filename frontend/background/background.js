// background.js: 메시지 리스너 및 sidePanel 열기 기능
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "OPEN_SIDEPANEL") {
    chrome.sidePanel.setOptions({
      path: "sidepanel/sidepanel.html",
      enabled: true,
    });
    chrome.sidePanel.open();
  } else if(message.type === "SUMMARIZE_PAGE") {
    const tabId = message.tabId;
    
    // 이미지 URL 추출 메시지 전송 (contentScript.js)
    chrome.tabs.sendMessage(tabId, { action: "EXTRACT_IMG"}, async(response) => {
      const imgUrls = response.imgUrls;
      }
    );
  }
});
