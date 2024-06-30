chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && !tab.url.startsWith('chrome://')) {
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      files: ['content.js']
    }).catch(err => console.error(`Failed to inject content script: ${err.message}`));
  }
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'log_links') {
    const port = chrome.runtime.connectNative('com.yourcompany.yourapp');
    port.postMessage(request.data);
    port.onMessage.addListener((response) => {
      console.log('Received response from native app:', response);
      sendResponse(response);
    });
    port.onDisconnect.addListener(() => {
      console.error('Disconnected from native app');
    });
    return true; // Indicates that the response will be sent asynchronously
  }
});

