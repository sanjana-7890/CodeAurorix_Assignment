document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get("sites", function(result) {
    const sites = result.sites || [];
    let totalLinks = 0;
    let uniqueLinks = 0;

    sites.forEach(site => {
      uniqueLinks += site.links.length;
      site.links.forEach(link => {
        totalLinks += link.count;
      });
    });

    document.getElementById("stats").innerHTML = `Total Links: ${totalLinks}, Unique Links: ${uniqueLinks}`;
  });

  document.getElementById('details').addEventListener('click', () => {
    chrome.tabs.create({ url: "details.html" }).catch(err => console.error(`Failed to open details page: ${err.message}`));
  });
});
