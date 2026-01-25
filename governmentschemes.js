let schemesData = [];
let newsData = [];

async function fetchData() {
  const schemesRes = await fetch('/api/schemes');
  schemesData = await schemesRes.json();
  const newsRes = await fetch('/api/news');
  newsData = await newsRes.json();
  populateFilters();
  renderContent();
}

function populateFilters() {
  const categoryFilter = document.getElementById('categoryFilter');
  const regionFilter = document.getElementById('regionFilter');

  const categories = ['All', ...new Set(schemesData.map(s => s.category))];
  categoryFilter.innerHTML = categories.map(c => `<option>${c}</option>`).join('');

  const regions = ['All', ...new Set([...schemesData.flatMap(s=>s.stateCoverage), ...newsData.map(n=>n.region)])];
  regionFilter.innerHTML = regions.map(r => `<option>${r}</option>`).join('');
}

function renderContent() {
  const searchQuery = document.getElementById('search').value.toLowerCase();
  const categoryValue = document.getElementById('categoryFilter').value;
  const regionValue = document.getElementById('regionFilter').value;

  const filteredSchemes = schemesData.filter(s => {
    const matchSearch = s.title.toLowerCase().includes(searchQuery) || s.summary.toLowerCase().includes(searchQuery);
    const matchCategory = categoryValue === 'All' || s.category === categoryValue;
    const matchRegion = regionValue === 'All' || s.stateCoverage.includes(regionValue);
    return matchSearch && matchCategory && matchRegion;
  });

  const filteredNews = newsData.filter(n => {
    const matchSearch = n.title.toLowerCase().includes(searchQuery) || n.excerpt.toLowerCase().includes(searchQuery);
    const matchRegion = regionValue === 'All' || n.region === regionValue;
    return matchSearch && matchRegion;
  });

  document.getElementById('schemes').innerHTML = `<h2>Schemes</h2>` + 
    filteredSchemes.map(s => `
      <article>
        <h3>${s.title}</h3>
        <p>${s.summary}</p>
        <p><strong>Benefits:</strong> ${s.benefits.join(', ')}</p>
        <a href="${s.applyLink}" target="_blank">Apply</a>
      </article>
    `).join('');

  document.getElementById('news').innerHTML = `<h2>News</h2>` +
    filteredNews.map(n => `
      <article>
        <h3>${n.title}</h3>
        <p>${n.excerpt}</p>
        <small>${n.source} • ${n.date}</small><br>
        <a href="${n.url}" target="_blank">Read more</a>
      </article>
    `).join('');
}

// Event listeners
document.getElementById('search').addEventListener('input', renderContent);
document.getElementById('categoryFilter').addEventListener('change', renderContent);
document.getElementById('regionFilter').addEventListener('change', renderContent);

// Initial fetch
fetchData();

async function subscribeAlert(schemeId) {
  const res = await fetch('/api/alerts', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scheme_id: schemeId })
  });
  const data = await res.json();
  if (data.success) alert('Subscribed to alerts for this scheme!');
}



