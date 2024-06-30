chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ sites: [] });
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url && !tab.url.startsWith('chrome://')) {
    chrome.scripting.executeScript({
      target: { tabId: tabId },
      files: ['content.js']
    }).catch(err => console.error(`Failed to inject content script: ${err.message}`));
  }
});
