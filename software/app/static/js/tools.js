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
  renderToolsPartySheets();
  renderToolsExport();
  renderToolsDanger();
  if (state.role === 'mm') {
    renderToolsBudgetCalculator();
  }
}

// ---------------------------------------------------------------------------
// Character sheet (read-only)
// ---------------------------------------------------------------------------
function renderToolsCharacterSheet() {
  const own = document.getElementById('tools-own-sheet');
  if (!own) return;

  if (state.role === 'mm' || !state.character) {
    own.classList.add('hidden');
    return;
  }
  own.classList.remove('hidden');
  renderCharacterSheetReadOnly(state.character, state.ruleset, 'tools-sheet-content');
}

/**
 * The party roster.
 *
 * The MM got every sheet and players got none — so "what skills does the party
 * actually have?" could not be answered from the app. Everyone now sees the
 * party; only the MM sees the MM-private notes on each.
 */
function renderToolsPartySheets() {
  const section = document.getElementById('tools-all-sheets');
  const container = document.getElementById('tools-all-sheets-content');
  if (!section || !container) return;

  const others = Object.entries(state.allCharacters)
    .filter(([pname]) => state.role === 'mm' || pname !== state.playerName);

  section.classList.remove('hidden');
  document.getElementById('tools-all-sheets-title').textContent =
    state.role === 'mm' ? 'All Characters' : 'The Party';

  if (others.length === 0) {
    container.innerHTML = `<div class="empty-state">${state.role === 'mm'
      ? 'No characters yet. Invite players from the Play tab.'
      : 'No other characters in the session yet.'}</div>`;
    return;
  }

  container.innerHTML = '';
  others.forEach(([pname, char]) => {
    const wrap = document.createElement('div');
    wrap.className = 'card collapsible';
    const bodyId = `tools-sheet-${pname.replace(/[^a-zA-Z0-9_-]/g, '_')}`;
    wrap.innerHTML = `
      <button class="card-title collapsible-toggle" aria-expanded="false" aria-controls="${bodyId}">
        ${escapeHtml(char.name)} <span class="library-meta">${escapeHtml(pname)}</span>
        <span class="facet-badge facet-${escapeHtml(char.primary_facet)}">${escapeHtml(char.primary_facet)}</span>
        <span class="toggle-arrow" aria-hidden="true">+</span>
      </button>
      <div id="${bodyId}" class="collapsible-body hidden"></div>`;

    const toggle = wrap.querySelector('.collapsible-toggle');
    const body = wrap.querySelector('.collapsible-body');
    toggle.onclick = () => {
      const open = body.classList.toggle('hidden');
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.querySelector('.toggle-arrow').textContent = open ? '+' : '−';
    };

    container.appendChild(wrap);
    renderCharacterSheetReadOnly(char, state.ruleset, bodyId);

    if (state.role === 'mm' && char.notes_mm) {
      const note = document.createElement('div');
      note.className = 'inline-note';
      note.style.marginTop = '12px';
      note.innerHTML = `<strong>MM notes:</strong> ${escapeHtml(char.notes_mm)}`;
      body.appendChild(note);
    }
  });
}

// ---------------------------------------------------------------------------
// Inventory
// ---------------------------------------------------------------------------
function renderToolsInventory() {
  const container = document.getElementById('tools-inventory-list');
  const addRow = document.getElementById('tools-inventory-add');
  if (!container) return;

  if (state.role === 'mm') {
    // The MM reads every pack; editing an item belongs to its owner.
    if (addRow) addRow.classList.add('hidden');
    const entries = Object.entries(state.allCharacters);
    if (entries.length === 0) {
      container.innerHTML = '<div class="empty-state">No characters yet.</div>';
      return;
    }
    container.innerHTML = '';
    entries.forEach(([pname, c]) => {
      const items = c.inventory || [];
      const div = document.createElement('div');
      div.style.marginBottom = '12px';
      div.innerHTML = `<div style="font-weight:600;font-size:13px;margin-bottom:4px;">${escapeHtml(c.name)}</div>`
        + (items.length
          ? '<ul style="list-style:none;font-size:13px;">' + items.map(i =>
              `<li style="padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.04);">${escapeHtml(i)}</li>`).join('') + '</ul>'
          : '<div style="color:var(--text-dim);font-size:13px;">Carrying nothing.</div>');
      container.appendChild(div);
    });
    return;
  }

  if (!state.character) {
    if (addRow) addRow.classList.add('hidden');
    container.innerHTML = '<div class="empty-state">Create your character on the Play tab first.</div>';
    return;
  }

  if (addRow) addRow.classList.remove('hidden');
  const items = state.character.inventory || [];
  container.innerHTML = '';
  if (items.length === 0) {
    container.innerHTML = '<div class="empty-state">Nothing carried yet. Add what your character has on them.</div>';
    return;
  }
  items.forEach((item, i) => {
    const div = document.createElement('div');
    div.className = 'inventory-row';
    div.innerHTML = `<span>${escapeHtml(item)}</span>`;
    const btn = document.createElement('button');
    btn.className = 'btn btn-secondary btn-sm';
    btn.style.cssText = 'padding:2px 8px;min-height:24px;font-size:11px;';
    btn.textContent = '×';
    btn.title = 'Remove ' + item;
    btn.onclick = () => removeInventoryItem(i);
    div.appendChild(btn);
    container.appendChild(div);
  });
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

  // Numbers come from the loaded ruleset, never from literals — a quick
  // reference that drifts from facet.yaml is a rules bug (see CLAUDE.md).
  const adv = Object.assign({
    marks_per_rank: 3,
    session_skill_points: 4,
    facet_level_threshold: 5,
    major_advancement_threshold: 3,
  }, (state.ruleset && state.ruleset.advancement) || {});

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
      <p><strong>Exchange Flow:</strong> Declare Posture &rarr; Reveal &rarr; Actions &rarr; Reactions &rarr; Conditions &rarr; End Exchange</p>
      <p style="margin-top:6px;"><strong>Postures:</strong></p>
      <ul style="list-style:disc;padding-left:20px;">
        <li>Aggressive: +1 offense, +1 reaction cost</li>
        <li>Measured: baseline</li>
        <li>Defensive: -1 offense, -1 reaction cost</li>
        <li>Withdrawn: no offense, free reactions, recover 2 End</li>
      </ul>
      <p style="margin-top:6px;"><strong>Reactions:</strong> Dodge (1 End, Dexterity), Parry (1 End, Strength+Combat),
         Absorb (0 End), Intercept (2 End, once per exchange)</p>
      <p><strong>0 Endurance:</strong> Absorb only.</p>
      <p style="margin-top:6px;"><strong>Strike vs an enemy:</strong> 10+ depletes 2 Resolve and may hang a rider
         Condition; 7-9 depletes 1. At 0 Resolve the enemy is defeated. Mooks have no Resolve &mdash; they fall to
         one Strike (10+ if armoured).</p>
      <p><strong>Strike vs another character:</strong> 10+ = Tier 2 Condition, 7-9 = Tier 1.</p>
      <p style="margin-top:6px;"><strong>Enemy attacks:</strong> NPCs never roll. The MM applies the incoming
         Condition (Mook = Tier 1, Named/Boss = Tier 2) and the PC reacts to reduce it.</p>
      <p style="margin-top:6px;"><strong>Armor (PC):</strong> a per-scene downgrade budget. Light softens the first
         2 incoming Conditions one tier each, Heavy the first 4. Resets at end of scene. Armor and a partial
         reaction never stack &mdash; only the greater reduction applies, and no charge is spent when the reaction
         already covered it.</p>
      <p><strong>Armor (enemy):</strong> flat extra Resolve &mdash; light +1, heavy +2.</p>
      <p><strong>Conditions:</strong> Tier 1 clears at end of exchange. Tier 2 persists until treated.
         A second Tier 2 of the same kind escalates to Broken (out of the fight).</p>
    </div>
  `);

  html += renderRuleSummaryCard('Magic Quick Reference', `
    <div style="font-size:13px;">
      <p><strong>Framework:</strong> Domain + Intent + Scope. No spell lists.</p>
      <p><strong>Scopes:</strong> Minor, Significant, Major</p>
      <p><strong>Domain Types:</strong></p>
      <ul style="list-style:disc;padding-left:20px;">
        <li>Focused: Easy/Standard/Hard</li>
        <li>Standard: Standard/Hard/Very Hard</li>
        <li>Broad (Prismatic): Hard/VH/VH (ceiling unmovable by Sparks)</li>
      </ul>
      <p style="margin-top:6px;"><strong>Spark Uses:</strong> Improve Roll (add die, drop lowest),
         Push Scope (one step harder), Ease Focused Major</p>
      <p><strong>Pre-Technique:</strong> Minor scope only. The scope restriction is the whole limitation
         &mdash; there is no extra difficulty step.</p>
      <p><strong>Secondary domain:</strong> always one difficulty step harder than the primary.</p>
    </div>
  `);

  html += renderRuleSummaryCard('Skill Advancement', `
    <div style="font-size:13px;">
      <p><strong>Ranks:</strong> Novice (0) &rarr; Practiced (+1) &rarr; Expert (+2) &rarr; Master (+3)</p>
      <p><strong>Marks per rank:</strong> ${adv.marks_per_rank}</p>
      <p><strong>SP Cost:</strong> Primary Facet: 1 SP, Cross-Facet: 2 SP</p>
      <p><strong>Session Skill Points:</strong> ${adv.session_skill_points}</p>
      <p><strong>Facet Level:</strong> Every ${adv.facet_level_threshold} primary skill rank advances = +1 Facet Level</p>
      <p><strong>Major Advancement:</strong> Every ${adv.major_advancement_threshold} total Facet levels</p>
      <p style="margin-top:6px;color:var(--text-dim);">You may only spend a Skill Point on a skill the MM has
         marked as used this session. Rolling a skill marks it automatically.</p>
    </div>
  `);

  html += renderRuleSummaryCard('Sparks', `
    <div style="font-size:13px;">
      <p>Spend a Spark <em>before</em> rolling. Each adds 1d6 and drops the lowest die.</p>
      <p style="margin-top:6px;"><strong>Earning:</strong> MM award, peer nomination at an act break
         (the MM confirms), and Graceful Failure &mdash; on a 6-, narrate how the failure makes the story
         richer and claim it.</p>
      <p style="margin-top:6px;">Click the Spark pips on your sheet to stage how many to spend. The staged
         amount applies to your next Roll, Strike, or Cast.</p>
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

  // Pre-fill from the actual party rather than making the MM total it by hand.
  const advances = Object.values(state.allCharacters)
    .reduce((sum, c) => sum + (c.career_advances || 0), 0);
  const field = document.getElementById('tools-budget-advances');
  if (field && !field.dataset.touched) field.value = advances;

  const partyField = document.getElementById('tools-budget-party-size');
  if (partyField && !partyField.dataset.touched) {
    partyField.value = Object.keys(state.allCharacters).length || 3;
  }
  calculateBudget();
}

/**
 * Encounter difficulty readout.
 *
 * The TR budget alone used to be the whole answer, which reads as more precise
 * than it is: simulation settled that the number of Named/Boss actors is the
 * dial and the TR total is a rough ordering check. Both are shown, actor
 * recipe first.
 */
function calculateBudget() {
  const advances = parseInt(document.getElementById('tools-budget-advances').value) || 0;
  const partySize = Math.max(1, parseInt(document.getElementById('tools-budget-party-size').value) || 3);
  const difficulty = document.getElementById('tools-budget-difficulty').value;
  const multipliers = { skirmish: 1, standard: 2, hard: 3, deadly: 4 };
  const budget = advances * (multipliers[difficulty] || 2);

  // Recipes are calibrated for a 3-character party and scale by head count.
  const scale = n => Math.max(1, Math.round(n * (partySize / 3)));
  const recipes = {
    skirmish: `${scale(3)} Mooks — a warm-up, not a threat.`,
    standard: `${scale(3)} Named + ${scale(1)} Mook.`,
    hard: `${scale(3)} Named + ${scale(3)} Mooks.`,
    deadly: `${scale(4)} Named + ${scale(1)} Mook, or ${scale(3)} Named + ${scale(4)} Mooks.`,
  };

  document.getElementById('tools-budget-result').innerHTML = `
    <div style="font-size:15px;">${escapeHtml(recipes[difficulty] || recipes.standard)}</div>
    <div style="font-size:12px;color:var(--text-dim);font-weight:400;margin-top:6px;">
      Rough TR budget ${budget} (party career advances ${advances} × ${multipliers[difficulty] || 2}).
      Use it to order encounters against each other, not to set difficulty — actor count is the dial.
      Mooks alone are never dangerous no matter how many you field.
    </div>`;
}

// ---------------------------------------------------------------------------
// Export character
// ---------------------------------------------------------------------------
/**
 * Download a character as .fof. The MM can export any character; a player
 * exports their own. Previously the button was rendered for the MM too and did
 * nothing at all, because the MM has no `state.character`.
 */
async function exportCharacter(playerName) {
  const who = playerName || state.playerName;
  if (!who || !state.sessionId) return;

  const resp = await apiFetch(`/api/characters/${state.sessionId}/${who}/export`, 'GET');
  if (!resp.ok) {
    notify('Export failed.', 'error');
    return;
  }
  const text = await resp.text();
  const blob = new Blob([text], { type: 'application/yaml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${who}.fof`;
  a.click();
  URL.revokeObjectURL(url);
  notify(`${who}.fof downloaded.`, 'success');
}

function renderToolsExport() {
  const container = document.getElementById('tools-export-content');
  if (!container) return;

  if (state.role === 'mm') {
    const entries = Object.keys(state.allCharacters);
    if (entries.length === 0) {
      container.innerHTML = '<div class="empty-state">No characters to export yet.</div>';
      return;
    }
    container.innerHTML = '<div class="btn-row" style="margin:0;"></div>';
    const row = container.querySelector('.btn-row');
    entries.forEach(pn => {
      const btn = document.createElement('button');
      btn.className = 'btn btn-secondary btn-sm';
      btn.textContent = (state.allCharacters[pn].name || pn) + '.fof';
      btn.onclick = () => exportCharacter(pn);
      row.appendChild(btn);
    });
    return;
  }

  if (!state.character) {
    container.innerHTML = '<div class="empty-state">Create a character first.</div>';
    return;
  }
  container.innerHTML = '';
  const btn = document.createElement('button');
  btn.className = 'btn btn-secondary';
  btn.textContent = 'Export Character (.fof)';
  btn.onclick = () => exportCharacter();
  container.appendChild(btn);
  const note = document.createElement('div');
  note.className = 'inline-note';
  note.style.marginTop = '8px';
  note.textContent = 'A .fof file is a portable character — keep it as a backup, or import it into another '
    + 'session from the character creation panel.';
  container.appendChild(note);
}

/**
 * Start over. Kept away from the export button and behind a confirmation, since
 * it discards everything, but it has to exist: an invite is single-use, so a
 * player who mis-built their character could not otherwise rebuild.
 */
function renderToolsDanger() {
  const container = document.getElementById('tools-danger-content');
  const card = document.getElementById('tools-danger');
  if (!container || !card) return;

  const targets = state.role === 'mm'
    ? Object.keys(state.allCharacters)
    : (state.character ? [state.playerName] : []);

  card.classList.toggle('hidden', targets.length === 0);
  if (targets.length === 0) return;

  container.innerHTML = '<div class="btn-row" style="margin:0;"></div>';
  const row = container.querySelector('.btn-row');
  targets.forEach(pn => {
    const btn = document.createElement('button');
    btn.className = 'btn btn-secondary btn-sm btn-danger';
    btn.textContent = state.role === 'mm'
      ? `Delete ${(state.allCharacters[pn] || {}).name || pn}`
      : 'Delete & Rebuild My Character';
    btn.onclick = () => deleteCharacter(pn);
    row.appendChild(btn);
  });
}
