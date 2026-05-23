/* guides.js — Guides page */

let allGuides = [];
let activeType = '';

const TYPE_COLORS = {
    'install':           'green',
    'upgrade':           'blue',
    'root':              'orange',
    'bootloader-unlock': 'red',
    'recovery':          'blue',
    'backup':            'gray',
    'unbrick':           'red',
};

const TYPE_ICONS = {
    'install':           '📦',
    'upgrade':           '⬆️',
    'root':              '🔓',
    'bootloader-unlock': '🔑',
    'recovery':          '🛠',
    'backup':            '💾',
    'unbrick':           '🆘',
};

function guideCardHTML(guide, index) {
    const icon      = TYPE_ICONS[guide.type] || '📄';
    const chipColor = TYPE_COLORS[guide.type] || 'gray';
    const sections  = guide.sections || [];
    const hasLive   = ['lineageos_wiki','grapheneos_docs'].includes(guide.data_source);

    // Build sections HTML
    let sectionsHTML = '';
    for (const sec of sections) {
        if (!sec.steps || !sec.steps.length) continue;
        sectionsHTML += `<div class="guide-section">
            <h3>${escHtml(sec.title)}</h3>
            <ol class="guide-steps">
                ${sec.steps.map(step => {
                    const isNote = step.startsWith('⚠');
                    return `<li class="${isNote ? 'note-item' : ''}">${escHtml(step)}</li>`;
                }).join('')}
            </ol>
        </div>`;
    }

    const note = guide.notes
        ? `<div class="guide-note">${escHtml(guide.notes)}</div>`
        : '';

    const sourceLink = guide.source_url
        ? `<a href="${escHtml(guide.source_url)}" target="_blank" rel="noopener" class="rom-link" style="margin-top:.85rem;display:inline-block">
             Full guide on ${escHtml(guide.source)} →
           </a>`
        : '';

    const liveBadge = hasLive
        ? chip('Live from wiki', 'green')
        : chip('Compiled guide', 'gray');

    return `
        <div class="guide-card">
            <div class="guide-header" onclick="toggleGuide(${index})">
                <div>
                    <div style="display:flex;align-items:center;gap:.6rem;margin-bottom:.3rem">
                        <span style="font-size:1.2rem">${icon}</span>
                        <span class="guide-title">${escHtml(guide.title)}</span>
                        ${chip(guide.type, chipColor)}
                        ${liveBadge}
                    </div>
                    <div class="guide-source">Source: ${escHtml(guide.source)}</div>
                </div>
                <span class="guide-toggle" id="toggle-${index}">▼</span>
            </div>
            <div class="guide-body" id="body-${index}">
                ${note}
                ${sectionsHTML || `<ol class="guide-steps">${(guide.steps || []).map(s =>
                    `<li class="${s.startsWith('⚠') ? 'note-item' : ''}">${escHtml(s)}</li>`
                ).join('')}</ol>`}
                ${sourceLink}
            </div>
        </div>`;
}

window.toggleGuide = function(index) {
    const body   = document.getElementById(`body-${index}`);
    const toggle = document.getElementById(`toggle-${index}`);
    if (!body) return;
    const isOpen = body.classList.contains('open');
    body.classList.toggle('open', !isOpen);
    toggle.classList.toggle('open', !isOpen);
};

function renderGuides(guides) {
    const container = document.getElementById('guides-container');
    const filtered  = activeType ? guides.filter(g => g.type === activeType) : guides;

    if (!filtered.length) {
        container.innerHTML = '<div class="empty-state">No guides found for this filter.</div>';
        return;
    }

    container.innerHTML = filtered.map((g, i) => guideCardHTML(g, i)).join('');
}

async function loadGuides(codename, manufacturer) {
    const container = document.getElementById('guides-container');
    const tabs      = document.getElementById('type-tabs');

    container.innerHTML = '<div class="skeleton" style="height:200px;margin-bottom:1rem"></div>'
                        + '<div class="skeleton" style="height:200px;margin-bottom:1rem"></div>'
                        + '<div class="skeleton" style="height:200px"></div>';

    try {
        const params = codename
            ? `/${encodeURIComponent(codename)}${manufacturer ? '?manufacturer=' + encodeURIComponent(manufacturer) : ''}`
            : '';

        const data = codename
            ? await api.get(`/guides/${encodeURIComponent(codename)}`, { manufacturer: manufacturer || undefined })
            : await api.get('/guides');

        allGuides = data.guides || [];
        tabs.style.display = allGuides.length ? 'flex' : 'none';
        renderGuides(allGuides);

    } catch (err) {
        container.innerHTML = `<div class="error-state">${escHtml(err.message)}</div>`;
    }
}

// Type tab filter
document.getElementById('type-tabs').addEventListener('click', e => {
    const tab = e.target.closest('.type-tab');
    if (!tab) return;
    document.querySelectorAll('.type-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    activeType = tab.dataset.type;
    renderGuides(allGuides);
});

// Load device-specific guides
document.getElementById('load-btn').addEventListener('click', () => {
    const codename = document.getElementById('codename-input').value.trim();
    const mfr      = document.getElementById('mfr-select').value;
    if (!codename) {
        loadGuides(null, null);  // load universal guides
    } else {
        loadGuides(codename, mfr);
    }
});

document.getElementById('codename-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') document.getElementById('load-btn').click();
});

// Load universal guides on page load
loadGuides(null, null);

// Also check if we came from device page with ?c=codename
const urlParams = new URLSearchParams(window.location.search);
const preloadCodename = urlParams.get('c');
const preloadMfr      = urlParams.get('m');
if (preloadCodename) {
    document.getElementById('codename-input').value = preloadCodename;
    if (preloadMfr) document.getElementById('mfr-select').value = preloadMfr;
    loadGuides(preloadCodename, preloadMfr);
}
