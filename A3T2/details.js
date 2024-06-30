document.addEventListener('DOMContentLoaded', () => {
  chrome.storage.local.get("sites", function(result) {
    const sites = result.sites || [];
    const table = document.getElementById("detailsTable");

    sites.forEach(site => {
      site.links.forEach((link, index) => {
        const row = table.insertRow();
        const cell1 = row.insertCell(0);
        const cell2 = row.insertCell(1);
        const cell3 = row.insertCell(2);
        if (index === 0) {
          cell1.innerHTML = site.site;
        } else {
          cell1.innerHTML = '';
        }
        cell2.innerHTML = link.href;
        cell3.innerHTML = link.count;
      });
    });
  });
});
