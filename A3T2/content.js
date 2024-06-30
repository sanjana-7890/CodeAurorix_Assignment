function logLinks() {
  try {
    const links = Array.from(document.querySelectorAll('a')).map(link => link.href);
    const site = window.location.hostname;

    chrome.runtime.sendMessage({
      type: 'log_links',
      data: {
        site: site,
        links: links.map(link => ({ href: link, count: 1 }))
      }
    }, response => {
      console.log('Response from background script:', response);
    });
  } catch (err) {
    console.error(`Error logging links: ${err.message}`);
  }
}

logLinks();
