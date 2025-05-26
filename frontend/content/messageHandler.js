chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'summarizePage') {
        const data = message.productData || {};
        console.log('🔗 Received product data:', data);
        sendResponse({ summary: data });
    }
});