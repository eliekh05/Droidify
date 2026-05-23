/* tools.js — Tools page */
async function loadTools(category, status) {
  const container = document.getElementById('tools-container');
  container.innerHTML = '<div class="skeleton" style="height:300px"></div>';

  try {
    const data = await api.tools({ category: category || undefined, status: status || undefined });
    const tools = data.tools;
    if (!tools.length) {
      container.innerHTML = '<div class="empty-state">No tools found.</div>';
      return;
    }

    // Group by category
    const groups = {};
    for (const t of tools) {
      (groups[t.category] ??= []).push(t);
    }
    const catOrder = ['root', 'xposed', 'flashing', 'recovery'];
    const sortedCats = [
      ...catOrder.filter(c => groups[c]),
      ...Object.keys(groups).filter(c => !catOrder.includes(c)),
    ];

    container.innerHTML = sortedCats.map(cat => `
      <div class="tools-section">
        <h2>${escHtml(cat)}</h2>
        <div class="tools-grid">
          ${groups[cat].map(t => {
            const status_chip = t.status === 'active'
              ? chip('Active', 'green')
              : chip('Discontinued', 'gray');
            const ver = t.latest_version
              ? `<span class="tool-version">v${escHtml(t.latest_version)}</span>`
              : '';
            const rel = t.release_date
              ? `<span class="tool-platform">${escHtml(t.release_date)}</span>`
              : '';
            const plat = t.platforms?.length
              ? `<span class="tool-platform">Platforms: ${escHtml(t.platforms.join(', '))}</span>`
              : '';
            const links = [
              t.official_url ? `<a href="${escHtml(t.official_url)}" target="_blank" rel="noopener" class="tool-link">Official →</a>` : '',
              ...(t.download_urls || []).slice(0,2).map(u =>
                `<a href="${escHtml(u)}" target="_blank" rel="noopener" class="tool-link">Download →</a>`
              ),
            ].filter(Boolean).join('');

            return `<div class="tool-card">
              <div class="tool-header">
                <span class="tool-name">${escHtml(t.name)}</span>
                ${status_chip}
              </div>
              <div class="tool-desc">${escHtml(t.description || '')}</div>
              <div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-bottom:.4rem">${ver}${rel}${plat}</div>
              <div class="tool-links">${links}</div>
              <div style="margin-top:.4rem;font-size:.72rem;color:var(--muted)">Source: ${escHtml(t.source || '')}</div>
            </div>`;
          }).join('')}
        </div>
      </div>`).join('');
  } catch (err) {
    container.innerHTML = `<div class="error-state">${escHtml(err.message)}</div>`;
  }
}

document.getElementById('filter-btn').addEventListener('click', () => {
  loadTools(
    document.getElementById('cat-filter').value,
    document.getElementById('status-filter').value,
  );
});
document.getElementById('cat-filter').addEventListener('change', () =>
  loadTools(document.getElementById('cat-filter').value, document.getElementById('status-filter').value));

loadTools();