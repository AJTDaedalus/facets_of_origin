/**
 * Tools tab — character sheet read-only, inventory, rule summaries, export.
 * Depends on: state, apiFetch, escapeHtml from app.js
 *             renderCharacterSheetReadOnly from components.js
 */

// ---------------------------------------------------------------------------
// Tools tab initialization
// ---------------------------------------------------------------------------
function initToolsTab() {
  renderToolsCharacterSheet();
  renderToolsInventory();
  renderToolsRuleSummaries();
  if (state.role === 'mm') {
    renderToolsAllCharacters();
    renderToolsBudgetCalculator();
  }
}

// ---------------------------------------------------------------------------
// Character sheet (read-only)
// ---------------------------------------------------------------------------
function renderToolsCharacterSheet() {
  if (state.role === 'mm') {
    // MM sees all character sheets
    document.getElementById('tools-own-sheet').classList.add('hidden');
    document.getElementById('tools-all-sheets').classList.remove('hidden');
  } else {
    // Player sees their own
    document.getElementById('tools-own-sheet').classList.remove('hidden');
    document.getElementById('tools-all-sheets').classList.add('hidden');
    if (state.character) {
      renderCharacterSheetReadOnly(state.character, state.ruleset, 'tools-sheet-content');
    }
  }
}

function renderToolsAllCharacters() {
  const container = document.getElementById('tools-all-sheets-content');
  if (!container) return;
  container.innerHTML = '';

  Object.entries(state.allCharacters).forEach(([pname, char]) => {
    const div = document.createElement('div');
    div.className = 'card';
    div.innerHTML = `<div class="card-title" style="cursor:pointer;" onclick="this.nextElementSibling.classList.toggle('hidden')">${escapeHtml(char.name)} (${escapeHtml(pname)}) <span class="toggle-arrow">+</span></div><div id="tools-sheet-${pname}" class="hidden"></div>`;
    container.appendChild(div);
    // Render after DOM insertion
    setTimeout(() => renderCharacterSheetReadOnly(char, state.ruleset, `tools-sheet-${pname}`), 0);
  });
}

// ---------------------------------------------------------------------------
// Inventory
// ---------------------------------------------------------------------------
function renderToolsInventory() {
  const container = document.getElementById('tools-inventory-list');
  if (!container) return;

  const char = state.role === 'mm' ? null : state.character;
  if (!char && state.role !== 'mm') {
    container.innerHTML = '<div style="color:var(--text-dim);font-size:13px;">No character yet.</div>';
    return;
  }

  if (state.role === 'mm') {
    // MM sees inventory per character
    container.innerHTML = '';
    Object.entries(state.allCharacters).forEach(([pname, c]) => {
      const items = c.inventory || [];
      const div = document.createElement('div');
      div.style.marginBottom = '12px';
      div.innerHTML = `<div style="font-weight:600;font-size:13px;margin-bottom:4px;">${escapeHtml(c.name)}</div>`;
      const ul = document.createElement('ul');
      ul.style.cssText = 'list-style:none;font-size:13px;';
      items.forEach(item => {
        const li = document.createElement('li');
        li.style.cssText = 'padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.04);';
        li.textContent = item;
        ul.appendChild(li);
      });
      if (items.length === 0) ul.innerHTML = '<li style="color:var(--text-dim);">Empty</li>';
      div.appendChild(ul);
      container.appendChild(div);
    });
    return;
  }

  // Player inventory
  const items = char.inventory || [];
  container.innerHTML = '';
  items.forEach((item, i) => {
    const div = document.createElement('div');
    div.style.cssText = 'display:flex;justify-content:space-between;align-items:center;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:13px;';
    div.innerHTML = `<span>${escapeHtml(item)}</span><button class="btn btn-secondary btn-sm" style="padding:2px 8px;min-height:24px;font-size:11px;" onclick="removeInventoryItem(${i})">x</button>`;
    container.appendChild(div);
  });
  if (items.length === 0) {
    container.innerHTML = '<div style="color:var(--text-dim);font-size:13px;">Empty inventory.</div>';
  }
}

async function addInventoryItem() {
  const input = document.getElementById('tools-inventory-input');
  const item = input ? input.value.trim() : '';
  if (!item || !state.character) return;

  const newInv = [...(state.character.inventory || []), item];
  const resp = await apiFetch(`/api/characters/${state.sessionId}/${state.playerName}/inventory`, 'PUT', { inventory: newInv });
  if (resp.ok) {
    const data = await resp.json();
    state.character.inventory = data.inventory;
    renderToolsInventory();
    if (input) input.value = '';
  }
}

async function removeInventoryItem(index) {
  if (!state.character) return;
  const newInv = [...(state.character.inventory || [])];
  newInv.splice(index, 1);
  const resp = await apiFetch(`/api/characters/${state.sessionId}/${state.playerName}/inventory`, 'PUT', { inventory: newInv });
  if (resp.ok) {
    const data = await resp.json();
    state.character.inventory = data.inventory;
    renderToolsInventory();
  }
}

// ---------------------------------------------------------------------------
// Rule summaries
// ---------------------------------------------------------------------------
function renderToolsRuleSummaries() {
  const container = document.getElementById('tools-rule-summaries');
  if (!container) return;

  let html = '';

  html += renderRuleSummaryCard('Core Resolution', `
    <div style="font-size:13px;">
      <p><strong>Roll:</strong> 2d6 + Attribute Modifier + Skill Modifier + Difficulty Modifier</p>
      <table class="skills-table" style="margin-top:8px;">
        <tr><td><strong>10+</strong></td><td style="color:var(--success);">Full Success</td><td>You achieve your goal cleanly.</td></tr>
        <tr><td><strong>7-9</strong></td><td style="color:var(--partial);">Success with Cost</td><td>You succeed, but with a complication.</td></tr>
        <tr><td><strong>6-</strong></td><td style="color:var(--failure);">Things Go Wrong</td><td>The story moves forward, not in your favor.</td></tr>
      </table>
      <p style="margin-top:8px;"><strong>Sparks:</strong> Spend before rolling. Each adds 1d6, drop lowest.</p>
      <p><strong>Difficulty:</strong> Easy (+1), Standard (0), Hard (-1), Very Hard (-2)</p>
    </div>
  `);

  html += renderRuleSummaryCard('Combat Quick Reference', `
    <div style="font-size:13px;">
      <p><strong>Exchange Flow:</strong> Declare Posture &rarr; Actions &rarr; Reactions &rarr; Conditions &rarr; End Exchange</p>
      <p style="margin-top:6px;"><strong>Postures:</strong></p>
      <ul style="list-style:disc;padding-left:20px;">
        <li>Aggressive: +1 offense, +1 reaction cost</li>
        <li>Measured: baseline</li>
        <li>Defensive: -1 offense, -1 reaction cost</li>
        <li>Withdrawn: no offense, free reactions, recover 2 End</li>
      </ul>
      <p style="margin-top:6px;"><strong>Reactions:</strong> Dodge (1 End), Parry (1 End), Absorb (0 End), Intercept (2 End)</p>
      <p><strong>0 Endurance:</strong> Absorb only.</p>
      <p style="margin-top:6px;"><strong>Strike Outcomes:</strong> 10+ = Tier 2 Condition, 7-9 = Tier 1, 6- = consequence for attacker</p>
      <p><strong>Armor:</strong> Light (Tier 2&rarr;1), Heavy (Tier 3&rarr;2)</p>
      <p><strong>Conditions:</strong> Tier 1 clears at end of exchange. 2nd Tier 2 = Broken (out).</p>
    </div>
  `);

  html += renderRuleSummaryCard('Magic Quick Reference', `
    <div style="font-size:13px;">
      <p><strong>Framework:</strong> Domain + Intent + Scope</p>
      <p><strong>Scopes:</strong> Minor, Significant, Major</p>
      <p><strong>Domain Types:</strong></p>
      <ul style="list-style:disc;padding-left:20px;">
        <li>Focused: Easy/Standard/Hard</li>
        <li>Standard: Standard/Hard/Very Hard</li>
        <li>Broad (Prismatic): Hard/VH/VH (ceiling unmovable)</li>
      </ul>
      <p style="margin-top:6px;"><strong>Spark Uses:</strong> Improve Roll (add die), Push Scope (harder), Ease Focused Major</p>
      <p><strong>Pre-Technique:</strong> Minor scope only, +1 difficulty step</p>
    </div>
  `);

  html += renderRuleSummaryCard('Skill Advancement', `
    <div style="font-size:13px;">
      <p><strong>Ranks:</strong> Novice (0) &rarr; Practiced (+1) &rarr; Expert (+2) &rarr; Master (+3)</p>
      <p><strong>Marks per rank:</strong> 3</p>
      <p><strong>SP Cost:</strong> Primary Facet: 1 SP, Cross-Facet: 2 SP</p>
      <p><strong>Facet Level:</strong> Every 6 primary skill rank advances = +1 Facet Level</p>
      <p><strong>Major Advancement:</strong> Every 4 total Facet levels</p>
    </div>
  `);

  container.innerHTML = html;
}

// ---------------------------------------------------------------------------
// Encounter budget calculator (MM only)
// ---------------------------------------------------------------------------
function renderToolsBudgetCalculator() {
  const container = document.getElementById('tools-budget-calculator');
  if (!container) return;
  container.classList.remove('hidden');
}

function calculateBudget() {
  const advances = parseInt(document.getElementById('tools-budget-advances').value) || 0;
  const difficulty = document.getElementById('tools-budget-difficulty').value;
  const multipliers = { skirmish: 1.0, standard: 2.0, hard: 3.0, deadly: 4.0 };
  const budget = advances * (multipliers[difficulty] || 2.0);
  document.getElementById('tools-budget-result').textContent = `TR Budget: ${budget}`;
}

// ---------------------------------------------------------------------------
// Export character
// ---------------------------------------------------------------------------
async function exportCharacter() {
  if (!state.character || !state.sessionId) return;
  const resp = await apiFetch(`/api/characters/${state.sessionId}/${state.playerName}/export`, 'GET');
  if (resp.ok) {
    const text = await resp.text();
    const blob = new Blob([text], { type: 'application/yaml' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${state.playerName}.fof`;
    a.click();
    URL.revokeObjectURL(url);
  }
}
