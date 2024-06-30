function logLinks() {
  try {
    const links = Array.from(document.querySelectorAll('a')).map(link => link.href);
    const site = window.location.hostname;

    chrome.storage.local.get("sites", function(result) {
      const sites = result.sites || [];
      const existingSite = sites.find(s => s.site === site);

      if (existingSite) {
        links.forEach(link => {
          const existingLink = existingSite.links.find(l => l.href === link);
          if (existingLink) {
            existingLink.count++;
          } else {
            existingSite.links.push({ href: link, count: 1 });
          }
        });
      } else {
        sites.push({ site: site, links: links.map(link => ({ href: link, count: 1 })) });
      }

      chrome.storage.local.set({ sites: sites });
    });
  } catch (err) {
    console.error(`Error logging links: ${err.message}`);
  }
}

logLinks();
