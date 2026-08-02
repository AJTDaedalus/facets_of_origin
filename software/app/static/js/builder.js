/**
 * Builder tab — character advancement (player), enemy/encounter builder (MM).
 * Depends on: state, sendWS, escapeHtml, apiFetch from app.js
 */

// ---------------------------------------------------------------------------
// Builder tab initialization
// ---------------------------------------------------------------------------
function initBuilderTab() {
  if (state.role === 'mm') {
    renderBuilderEnemyLibrary();
    renderBuilderEncounterLibrary();
    renderBuilderEncounterEnemySelect();
    renderBuilderAdvanceSkillSelect();
    renderBuilderMarkSkillSelect();
    renderBuilderCampaignNotes();
    renderPlayerPickers();
    previewEnemyTR();
  } else {
    renderBuilderSkills();
    renderBuilderTechniques();
    renderBuilderPlayerNotes();
  }
}

// ---------------------------------------------------------------------------
// Player: Skill advancement
// ---------------------------------------------------------------------------
function renderBuilderSkills() {
  const spEl = document.getElementById('builder-sp-remaining');
  const listEl = document.getElementById('builder-skills-list');
  if (!spEl || !listEl) return;

  const char = state.character;
  if (!char || !state.ruleset) {
    spEl.textContent = '';
    listEl.innerHTML = '<div class="empty-state">Create your character on the Play tab first — '
      + 'advancement opens up once you have one.</div>';
    return;
  }

  const sp = char.session_skill_points_remaining || 0;
  spEl.innerHTML = `<strong style="color:var(--gold);">${sp}</strong> Skill Point${sp === 1 ? '' : 's'}
    left this session. Primary-Facet skills cost 1, everything else costs 2.`;

  const usedSkills = char.skills_used_this_session || [];
  const hasUsedSkills = usedSkills.length > 0;

  listEl.innerHTML = '';
  if (!hasUsedSkills) {
    // Explains why every Spend button is disabled — previously they were just
    // greyed out with nothing saying what would enable them.
    const note = document.createElement('div');
    note.className = 'inline-note';
    note.textContent = 'Nothing is marked as used yet. Roll a skill in play, or ask the MM to mark one — '
      + 'you may only advance skills you actually used this session.';
    listEl.appendChild(note);
  }

  state.ruleset.skills.forEach(skill => {
    if (skill.status === 'stub') return;
    const ss = char.skills[skill.id] || { rank: 'novice', marks: 0 };
    const isPrimary = skill.facet === char.primary_facet;
    const cost = isPrimary ? 1 : 2;
    const canAfford = (char.session_skill_points_remaining || 0) >= cost;
    const wasUsed = usedSkills.includes(skill.id);
    const canSpend = canAfford && (!hasUsedSkills || wasUsed);
    const marksNeeded = state.ruleset.advancement ? state.ruleset.advancement.marks_per_rank : 3;
    const dots = '\u25CF'.repeat(ss.marks) + '\u25CB'.repeat(Math.max(0, marksNeeded - ss.marks));

    const usedBadge = wasUsed ? '<span style="color:var(--success);font-size:10px;margin-left:4px;">USED</span>' : '';
    const notUsedNote = hasUsedSkills && !wasUsed && canAfford ? '<span style="color:var(--text-dim);font-size:10px;margin-left:4px;">not used</span>' : '';

    const div = document.createElement('div');
    div.style.cssText = 'display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:13px;';
    div.innerHTML = `
      <div>
        <span>${skill.name}</span>
        ${isPrimary ? '' : '<span style="color:var(--text-dim);font-size:10px;margin-left:4px;">(cross ' + cost + ' SP)</span>'}
        <span class="rank-badge rank-${ss.rank}" style="margin-left:6px;">${ss.rank}</span>
        <span class="marks-dots" style="margin-left:6px;">${dots}</span>
        ${usedBadge}${notUsedNote}
      </div>
      <button class="btn btn-secondary btn-sm" ${canSpend ? '' : 'disabled'} onclick="spendSkillPoint('${skill.id}')" style="padding:3px 10px;min-height:28px;font-size:11px;">Spend</button>
    `;
    listEl.appendChild(div);
  });
}

function spendSkillPoint(skillId) {
  sendWS({ type: 'spend_skill_point', skill_id: skillId });
}

// ---------------------------------------------------------------------------
// Player: Technique selection
// ---------------------------------------------------------------------------
function renderBuilderTechniques() {
  const container = document.getElementById('builder-technique-list');
  if (!container) return;

  const char = state.character;
  if (!char || !state.ruleset) {
    container.innerHTML = '<div class="empty-state">Create your character on the Play tab first.</div>';
    return;
  }

  const picks = char.technique_picks_available || 0;
  const held = char.techniques || [];

  let html = `<div class="inline-note" style="margin-bottom:10px;">
    <strong style="color:var(--gold);">${picks}</strong> Technique pick${picks === 1 ? '' : 's'} available.
    You earn one at each Facet level. Tier 2 needs a Tier 1 in the same branch; Tier 3 needs a Tier 2.
  </div>`;

  if (held.length > 0) {
    html += '<div class="section-label">Learned</div>';
    held.forEach(t => {
      const choice = char.technique_choices && char.technique_choices[t];
      html += `<div class="technique-row technique-held">
        <div><strong>${escapeHtml(techniqueDisplayName(t))}</strong>
        ${choice ? `<span class="library-meta">${escapeHtml(choice.replace(/_/g, ' '))}</span>` : ''}</div>
      </div>`;
    });
  }

  const facetDef = state.ruleset.character_facets.find(cf => cf.id === char.primary_facet);
  const techniques = (facetDef && facetDef.techniques) || [];
  const available = techniques.filter(t => !held.includes(t.id));

  if (available.length > 0) {
    html += '<div class="section-label">Available</div>';
    available.forEach(t => {
      // Show WHY a Technique is locked rather than hiding it. Seeing the shape of
      // the tree ahead is most of the point of an advancement screen.
      const missing = (t.prerequisites || []).filter(p => !held.includes(p));
      const blocked = missing.length > 0 || picks <= 0;
      const reasons = [];
      if (missing.length) reasons.push('Requires ' + missing.map(techniqueDisplayName).join(', '));
      if (picks <= 0) reasons.push('No pick available');

      html += `<div class="technique-row${blocked ? ' technique-locked' : ''}">
        <div>
          <strong>${escapeHtml(t.name || t.id)}</strong>
          ${t.has_choice ? '<span class="library-meta">choice required</span>' : ''}
          <div class="library-desc">${escapeHtml(t.description || '')}</div>
          ${reasons.length ? `<div class="technique-blocked">${escapeHtml(reasons.join(' · '))}</div>` : ''}
        </div>
        <button class="btn btn-secondary btn-sm" ${blocked ? 'disabled' : ''}
                onclick="selectTechnique('${escapeHtml(t.id)}')">Select</button>
      </div>`;
    });
  } else if (held.length) {
    html += '<div class="empty-state">Every Technique in this Facet is learned.</div>';
  }

  container.innerHTML = html;
}

/**
 * Select a Technique, prompting for its choice first when it needs one.
 *
 * This previously fired `technique_select` with no `choice` at all, even for
 * magic-granting Techniques whose whole effect is the domain they name — and the
 * event was MM-gated besides, so it always came back as an error.
 */
async function selectTechnique(techId) {
  const facetDef = state.ruleset.character_facets.find(cf => cf.id === state.character.primary_facet);
  const def = ((facetDef && facetDef.techniques) || []).find(t => t.id === techId);

  let choice;
  if (def && def.has_choice) {
    choice = await pickTechniqueChoice(def);
    if (!choice) return;  // cancelled
  }
  sendWS({ type: 'technique_select', technique_id: techId, choice });
}

/**
 * Offer the legal choices for a Technique. For the domain-granting Techniques
 * that means the right domain list: Ascendant Domain takes prismatic territories,
 * Second Domain takes standard ones only (PHB II.4b/II.4c).
 *
 * TD-20 (DESIGN §8): non-domain `has_choice` Techniques — Weapon Mastery,
 * Acclimated, Field of Mastery — used to fall through to the domain logic
 * below and get offered the character's primary Facet's *domain* names as
 * candidate weapon types, hardships, or fields of knowledge, which is not
 * merely wrong but doesn't even overlap the Technique's real vocabulary.
 * TD-19 gave these three Techniques a `choices` list of their own in
 * facet.yaml; when a Technique carries one, it is authoritative and the
 * domain-list branch never runs for it.
 */
function pickTechniqueChoice(def) {
  if (def.choices && def.choices.length) {
    return pickFromChoicesList(def);
  }

  const magic = (state.ruleset && state.ruleset.magic) || {};
  const facetForDomains = def.requires_domain || state.character.primary_facet;
  const list = (facetForDomains === 'mind' ? magic.mind_domains : magic.soul_domains) || [];

  let options = list;
  if (def.grants_prismatic_domain) {
    options = list.filter(d => d.type === 'broad' || d.type === 'prismatic');
  } else if (def.grants_secondary_domain) {
    options = list.filter(d => d.type !== 'broad' && d.type !== 'prismatic');
  }
  const held = new Set([
    state.character.magic_domain,
    state.character.secondary_magic_domain,
    state.character.ascendant_domain,
  ].filter(Boolean));
  options = options.filter(d => !held.has(d.id));

  if (options.length === 0) {
    notify('No eligible domain remains for this Technique.', 'warn');
    return Promise.resolve(null);
  }
  return selectDialog(
    def.name || def.id,
    def.choice_prompt || 'Choose a domain.',
    options.map(d => ({ value: d.id, label: `${d.name} (${d.type})` })));
}

/**
 * Picker for a non-domain Technique's `choices` list (TD-19/TD-20).
 *
 * Field of Mastery is deliberately open-ended in the fiction (II.4a: "or
 * another domain with MM approval") — nothing gates membership (INV-8) —
 * so it alone gets an "Other..." entry that drops into free text via
 * `promptDialog`. Weapon Mastery and Acclimated are closed sets (the book
 * lists exactly four/four options each) and offer only what `choices` says.
 */
async function pickFromChoicesList(def) {
  const OTHER = '__other__';
  const options = def.choices.map(c => ({ value: c, label: c }));
  if (def.id === 'field_of_mastery') {
    options.push({ value: OTHER, label: 'Other (type your own)...' });
  }
  const picked = await selectDialog(
    def.name || def.id,
    def.choice_prompt || 'Choose an option.',
    options);
  if (picked === OTHER) {
    return promptDialog('Field of Mastery', 'e.g. cartography, herbalism...', '');
  }
  return picked;
}

// ---------------------------------------------------------------------------
// Player: Character notes
// ---------------------------------------------------------------------------
function renderBuilderPlayerNotes() {
  const textarea = document.getElementById('builder-player-notes');
  if (!textarea || !state.character) return;
  textarea.value = state.character.notes_player || '';
}

async function savePlayerNotes() {
  if (!state.character || !state.sessionId) return;
  const notes = document.getElementById('builder-player-notes').value;
  const resp = await apiFetch('/api/characters/' + state.sessionId + '/' + state.playerName + '/notes', 'PUT', {
    notes_player: notes,
  });
  if (resp.ok) {
    const data = await resp.json();
    state.character.notes_player = data.notes_player;
  }
}

// ---------------------------------------------------------------------------
// MM: Enemy builder
// ---------------------------------------------------------------------------
/**
 * Score the stat line currently in the form.
 *
 * This used to carry its own copy of the MM1 Threat Rating formula in
 * JavaScript — and it had already drifted: its durability table bucketed Resolve
 * (<=4 -> 2, <=6 -> 3, ...) while the engine simply uses Resolve, so the preview
 * disagreed with the TR the server assigned on save. Duplicated rule logic is
 * the exact failure the Software-PHB sync policy forbids, so the engine scores
 * it now.
 */
async function previewEnemyTR() {
  const out = document.getElementById('builder-enemy-tr');
  if (!out) return;

  const resp = await apiFetch('/api/enemies/preview-tr', 'POST', {
    tier: document.getElementById('builder-enemy-tier').value,
    resolve: parseInt(document.getElementById('builder-enemy-resolve').value) || 0,
    attack_modifier: parseInt(document.getElementById('builder-enemy-attack').value) || 0,
    armor: document.getElementById('builder-enemy-armor').value,
    techniques: document.getElementById('builder-enemy-techniques').value
      .split(',').map(s => s.trim()).filter(Boolean),
  });

  if (!resp.ok) { out.textContent = ''; return; }
  const { tr } = await resp.json();
  const tier = document.getElementById('builder-enemy-tier').value;
  const floors = { mook: 1, named: 8, boss: 12 };
  out.textContent = `Threat Rating: ${tr}`
    + (tr === floors[tier] ? ` (the ${tier} minimum)` : '');
}

async function saveEnemy(ev) {
  const name = document.getElementById('builder-enemy-name').value.trim();
  if (!name) { notify('Give the enemy a name.', 'warn'); focusElement('builder-enemy-name'); return; }

  // Editing keeps the original id so the save overwrites rather than forking a
  // near-duplicate under a new slug.
  const id = state.editingEnemyId || name.toLowerCase().replace(/[^a-z0-9]+/g, '_');
  const techniques = document.getElementById('builder-enemy-techniques').value.split(',').map(s => s.trim()).filter(Boolean);

  const enemy = {
    session_id: state.sessionId,
    id: id,
    name: name,
    tier: document.getElementById('builder-enemy-tier').value,
    resolve: parseInt(document.getElementById('builder-enemy-resolve').value) || 0,
    attack_modifier: parseInt(document.getElementById('builder-enemy-attack').value) || 0,
    defense_modifier: parseInt(document.getElementById('builder-enemy-defense').value) || 0,
    armor: document.getElementById('builder-enemy-armor').value,
    techniques: techniques,
    special: document.getElementById('builder-enemy-special').value.trim() || null,
    description: document.getElementById('builder-enemy-description').value.trim(),
    tactics: document.getElementById('builder-enemy-tactics').value.trim(),
  };

  await withPending(ev && ev.target, 'Saving...', async () => {
    const resp = await apiFetch('/api/enemies/', 'POST', enemy);
    if (resp.ok) {
      const data = await resp.json();
      state.enemyLibrary[data.enemy.id] = data.enemy;
      renderBuilderEnemyLibrary();
      renderBuilderEncounterEnemySelect();
      updateSpawnEnemySelect();
      notify(`${name} saved (TR ${data.enemy.tr}).`, 'success');
      clearEnemyForm();
    } else {
      const err = await resp.json().catch(() => ({}));
      notify(formatApiError(err.detail, 'Failed to save enemy.'), 'error');
    }
  });
}

/**
 * Load a saved enemy back into the form. Without this, changing one stat meant
 * retyping the whole block and hoping the generated slug matched.
 */
function editEnemy(enemyId) {
  const enemy = state.enemyLibrary[enemyId];
  if (!enemy) return;
  state.editingEnemyId = enemyId;

  document.getElementById('builder-enemy-name').value = enemy.name || '';
  document.getElementById('builder-enemy-tier').value = enemy.tier || 'named';
  document.getElementById('builder-enemy-resolve').value = enemy.resolve != null ? enemy.resolve : 0;
  document.getElementById('builder-enemy-attack').value = enemy.attack_modifier || 0;
  document.getElementById('builder-enemy-defense').value = enemy.defense_modifier || 0;
  document.getElementById('builder-enemy-armor').value = enemy.armor || 'none';
  document.getElementById('builder-enemy-techniques').value = (enemy.techniques || []).join(', ');
  document.getElementById('builder-enemy-special').value = enemy.special || '';
  document.getElementById('builder-enemy-description').value = enemy.description || '';
  document.getElementById('builder-enemy-tactics').value = enemy.tactics || '';

  updateEnemyFormMode();
  previewEnemyTR();
  focusElement('builder-enemy-name');
}

function clearEnemyForm() {
  state.editingEnemyId = null;
  ['builder-enemy-name', 'builder-enemy-techniques', 'builder-enemy-special',
   'builder-enemy-description', 'builder-enemy-tactics'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  document.getElementById('builder-enemy-tier').value = 'named';
  document.getElementById('builder-enemy-resolve').value = 4;
  document.getElementById('builder-enemy-attack').value = 0;
  document.getElementById('builder-enemy-defense').value = 0;
  document.getElementById('builder-enemy-armor').value = 'none';
  updateEnemyFormMode();
  previewEnemyTR();
}

function updateEnemyFormMode() {
  const title = document.getElementById('builder-enemy-form-title');
  const cancel = document.getElementById('builder-enemy-cancel-edit');
  const editing = !!state.editingEnemyId;
  if (title) title.textContent = editing ? 'Editing: ' + state.editingEnemyId : 'Enemy Builder';
  if (cancel) cancel.classList.toggle('hidden', !editing);
}

function renderBuilderEnemyLibrary() {
  const container = document.getElementById('builder-enemy-library-list');
  if (!container) return;

  const entries = Object.entries(state.enemyLibrary);
  if (entries.length === 0) {
    container.innerHTML = '<div class="empty-state">No enemies saved yet. Build one above — '
      + 'saved enemies can be spawned into the tracker from the Play tab and added to Encounters.</div>';
    return;
  }

  container.innerHTML = '';
  entries.forEach(([id, enemy]) => {
    const div = document.createElement('div');
    div.className = 'library-row';
    div.innerHTML = `
      <div>
        <strong>${escapeHtml(enemy.name)}</strong>
        <span class="library-meta">${escapeHtml(enemy.tier)} · TR ${enemy.tr || '?'}
          · Resolve ${enemy.resolve != null ? enemy.resolve : 0}
          ${enemy.armor && enemy.armor !== 'none' ? '· ' + escapeHtml(enemy.armor) + ' armor' : ''}</span>
        ${enemy.description ? `<div class="library-desc">${escapeHtml(enemy.description)}</div>` : ''}
      </div>
      <span class="btn-row" style="margin:0;"></span>`;
    const actions = div.querySelector('.btn-row');

    const spawn = document.createElement('button');
    spawn.className = 'btn btn-secondary btn-sm';
    spawn.textContent = 'Spawn';
    spawn.title = 'Put one into the active tracker';
    spawn.onclick = () => spawnEnemyById(id);
    actions.appendChild(spawn);

    const edit = document.createElement('button');
    edit.className = 'btn btn-secondary btn-sm';
    edit.textContent = 'Edit';
    edit.onclick = () => editEnemy(id);
    actions.appendChild(edit);

    const del = document.createElement('button');
    del.className = 'btn btn-secondary btn-sm';
    del.textContent = 'Delete';
    del.onclick = () => deleteEnemy(id);
    actions.appendChild(del);

    container.appendChild(div);
  });
}

function spawnEnemyById(enemyId) {
  sendWS({ type: 'spawn_enemy', enemy_id: enemyId });
  notify(`${(state.enemyLibrary[enemyId] || {}).name || enemyId} added to the tracker on the Play tab.`, 'success');
}

async function deleteEnemy(enemyId) {
  const enemy = state.enemyLibrary[enemyId];
  const ok = await confirmDialog(
    'Delete this enemy?',
    `"${enemy ? enemy.name : enemyId}" is removed from the library. Encounters that reference it will no longer resolve.`,
    'Delete');
  if (!ok) return;

  const resp = await apiFetch('/api/enemies/' + state.sessionId + '/' + enemyId, 'DELETE');
  if (resp.ok) {
    delete state.enemyLibrary[enemyId];
    if (state.editingEnemyId === enemyId) clearEnemyForm();
    renderBuilderEnemyLibrary();
    renderBuilderEncounterEnemySelect();
    updateSpawnEnemySelect();
    notify('Enemy deleted.', 'success');
  } else {
    notify('Failed to delete enemy.', 'error');
  }
}

// ---------------------------------------------------------------------------
// MM: Encounter builder
// ---------------------------------------------------------------------------
function renderBuilderEncounterEnemySelect() {
  const select = document.getElementById('builder-encounter-add-enemy');
  if (!select) return;
  select.innerHTML = '<option value="">-- add enemy --</option>';
  Object.entries(state.enemyLibrary).forEach(([id, enemy]) => {
    const opt = document.createElement('option');
    opt.value = id;
    opt.textContent = enemy.name + ' (TR ' + (enemy.tr || '?') + ')';
    select.appendChild(opt);
  });
}

function addEncounterEnemy() {
  const select = document.getElementById('builder-encounter-add-enemy');
  const enemyId = select ? select.value : '';
  if (!enemyId) { notify('Pick an enemy to add.', 'warn'); return; }
  addEncounterEnemyRow(enemyId, 1);
  updateEncounterBudget();
}

function addEncounterEnemyRow(enemyId, count) {
  const container = document.getElementById('builder-encounter-enemies');
  const enemy = state.enemyLibrary[enemyId];
  if (!container || !enemy) return;

  const div = document.createElement('div');
  div.className = 'encounter-enemy-row';
  div.dataset.enemyId = enemyId;
  div.innerHTML = `
    <span>${escapeHtml(enemy.name)}
      <span class="library-meta">${escapeHtml(enemy.tier)} · TR ${enemy.tr || '?'}</span></span>
    <div style="display:flex;align-items:center;gap:6px;">
      <label style="margin:0;font-size:11px;">Count</label>
      <input type="number" class="encounter-enemy-count" value="${count || 1}" min="1" max="20"
             style="width:56px;padding:4px;margin:0;" oninput="updateEncounterBudget()">
      <button class="btn btn-secondary btn-sm" style="padding:2px 8px;min-height:24px;font-size:11px;"
              onclick="this.closest('.encounter-enemy-row').remove(); updateEncounterBudget();">×</button>
    </div>`;
  container.appendChild(div);
}

/**
 * Live encounter readout.
 *
 * The `builder-encounter-budget` element existed but nothing ever wrote to it.
 * Actor count is the real difficulty dial in v0.3 — the TR total is only a rough
 * ordering check — so both are shown, with the actor count first.
 */
function updateEncounterBudget() {
  const el = document.getElementById('builder-encounter-budget');
  if (!el) return;

  let totalTR = 0, mooks = 0, actors = 0;
  document.querySelectorAll('.encounter-enemy-row').forEach(row => {
    const enemy = state.enemyLibrary[row.dataset.enemyId];
    const count = parseInt(row.querySelector('.encounter-enemy-count').value) || 1;
    if (!enemy) return;
    totalTR += (enemy.tr || 0) * count;
    if (enemy.tier === 'mook') mooks += count; else actors += count;
  });

  if (totalTR === 0 && mooks === 0) {
    el.innerHTML = '<span style="color:var(--text-dim);">Add enemies to see the difficulty readout.</span>';
    return;
  }

  el.innerHTML = `
    <div><strong style="color:var(--gold);">${actors}</strong> Named/Boss actor${actors === 1 ? '' : 's'}
      · <strong>${mooks}</strong> Mook${mooks === 1 ? '' : 's'} · total TR ${totalTR}</div>
    <div style="color:var(--text-dim);margin-top:2px;">Difficulty tracks the number of Named/Boss actors, not
      total TR. A Mook swarm on its own is never dangerous. For a 3-character party: 3 Named + 1 Mook is
      Standard; add 2 Mooks for Hard; add 3, or use 4 Named + 1 Mook, for Deadly.</div>`;
}

async function saveEncounter(ev) {
  const name = document.getElementById('builder-encounter-name').value.trim();
  if (!name) { notify('Give the encounter a name.', 'warn'); focusElement('builder-encounter-name'); return; }

  const id = state.editingEncounterId || name.toLowerCase().replace(/[^a-z0-9]+/g, '_');
  const enemies = [];
  document.querySelectorAll('.encounter-enemy-row').forEach(row => {
    enemies.push({
      enemy_id: row.dataset.enemyId,
      count: parseInt(row.querySelector('.encounter-enemy-count').value) || 1,
    });
  });

  const laterals = document.getElementById('builder-encounter-laterals').value.split('\n').map(s => s.trim()).filter(Boolean);

  const encounter = {
    session_id: state.sessionId,
    id: id,
    name: name,
    difficulty: document.getElementById('builder-encounter-difficulty').value,
    environment: document.getElementById('builder-encounter-environment').value.trim(),
    description: document.getElementById('builder-encounter-description').value.trim(),
    enemies: enemies,
    lateral_solutions: laterals,
  };

  await withPending(ev && ev.target, 'Saving...', async () => {
    const resp = await apiFetch('/api/encounters/', 'POST', encounter);
    if (resp.ok) {
      const data = await resp.json();
      state.encounterLibrary[data.encounter.id] = data.encounter;
      renderBuilderEncounterLibrary();
      notify(`Encounter "${name}" saved.`, 'success');
      clearEncounterForm();
    } else {
      const err = await resp.json().catch(() => ({}));
      notify(formatApiError(err.detail, 'Failed to save encounter.'), 'error');
    }
  });
}

/**
 * The encounter library.
 *
 * Encounters could previously be saved and never seen again — nothing rendered,
 * loaded, ran, or deleted them, so the Encounter Builder was a write-only form.
 * "Run" is the point of the whole feature: it spawns every enemy in the recipe
 * into the live tracker in one action.
 */
function renderBuilderEncounterLibrary() {
  const container = document.getElementById('builder-encounter-library-list');
  if (!container) return;

  const entries = Object.entries(state.encounterLibrary);
  if (entries.length === 0) {
    container.innerHTML = '<div class="empty-state">No encounters saved yet. Build one below, '
      + 'then Run it to drop every enemy into the tracker at once.</div>';
    return;
  }

  container.innerHTML = '';
  entries.forEach(([id, enc]) => {
    const roster = (enc.enemies || []).map(e => {
      const name = (state.enemyLibrary[e.enemy_id] || {}).name || e.enemy_id;
      return e.count > 1 ? `${e.count}× ${name}` : name;
    }).join(', ');

    const div = document.createElement('div');
    div.className = 'library-row';
    div.innerHTML = `
      <div>
        <strong>${escapeHtml(enc.name)}</strong>
        <span class="library-meta">${escapeHtml(enc.difficulty || 'standard')}
          ${enc.environment ? '· ' + escapeHtml(enc.environment) : ''}</span>
        ${roster ? `<div class="library-desc">${escapeHtml(roster)}</div>`
                 : '<div class="library-desc" style="color:var(--failure);">No enemies in this encounter.</div>'}
      </div>
      <span class="btn-row" style="margin:0;"></span>`;
    const actions = div.querySelector('.btn-row');

    const run = document.createElement('button');
    run.className = 'btn btn-primary btn-sm';
    run.textContent = 'Run';
    run.title = 'Spawn every enemy in this encounter into the tracker';
    run.disabled = !(enc.enemies || []).length;
    run.onclick = () => runEncounter(id);
    actions.appendChild(run);

    const edit = document.createElement('button');
    edit.className = 'btn btn-secondary btn-sm';
    edit.textContent = 'Edit';
    edit.onclick = () => editEncounter(id);
    actions.appendChild(edit);

    const del = document.createElement('button');
    del.className = 'btn btn-secondary btn-sm';
    del.textContent = 'Delete';
    del.onclick = () => deleteEncounter(id);
    actions.appendChild(del);

    container.appendChild(div);
  });
}

async function runEncounter(encounterId) {
  const enc = state.encounterLibrary[encounterId];
  if (!enc) return;

  const missing = (enc.enemies || []).filter(e => !state.enemyLibrary[e.enemy_id]);
  if (missing.length) {
    notify(`Cannot run: ${missing.map(m => m.enemy_id).join(', ')} no longer in the enemy library.`, 'error');
    return;
  }

  const total = (enc.enemies || []).reduce((n, e) => n + (e.count || 1), 0);
  const ok = await confirmDialog(
    `Run "${enc.name}"?`,
    `${total} enem${total === 1 ? 'y' : 'ies'} join the active tracker on the Play tab.`,
    'Run Encounter');
  if (!ok) return;

  (enc.enemies || []).forEach(entry => {
    const base = (state.enemyLibrary[entry.enemy_id] || {}).name || entry.enemy_id;
    const count = entry.count || 1;
    for (let i = 0; i < count; i++) {
      sendWS({
        type: 'spawn_enemy',
        enemy_id: entry.enemy_id,
        instance_name: count > 1 ? `${base} ${i + 1}` : undefined,
      });
    }
  });
  notify(`"${enc.name}" is on the board. Switch to Play to run it.`, 'success');
}

function editEncounter(encounterId) {
  const enc = state.encounterLibrary[encounterId];
  if (!enc) return;
  state.editingEncounterId = encounterId;

  document.getElementById('builder-encounter-name').value = enc.name || '';
  document.getElementById('builder-encounter-difficulty').value = enc.difficulty || 'standard';
  document.getElementById('builder-encounter-environment').value = enc.environment || '';
  document.getElementById('builder-encounter-description').value = enc.description || '';
  document.getElementById('builder-encounter-laterals').value = (enc.lateral_solutions || []).join('\n');

  const container = document.getElementById('builder-encounter-enemies');
  container.innerHTML = '';
  (enc.enemies || []).forEach(e => addEncounterEnemyRow(e.enemy_id, e.count || 1));

  updateEncounterFormMode();
  updateEncounterBudget();
  focusElement('builder-encounter-name');
}

function clearEncounterForm() {
  state.editingEncounterId = null;
  ['builder-encounter-name', 'builder-encounter-environment',
   'builder-encounter-description', 'builder-encounter-laterals'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = '';
  });
  document.getElementById('builder-encounter-difficulty').value = 'standard';
  document.getElementById('builder-encounter-enemies').innerHTML = '';
  updateEncounterFormMode();
  updateEncounterBudget();
}

function updateEncounterFormMode() {
  const title = document.getElementById('builder-encounter-form-title');
  const cancel = document.getElementById('builder-encounter-cancel-edit');
  const editing = !!state.editingEncounterId;
  if (title) title.textContent = editing ? 'Editing: ' + state.editingEncounterId : 'Encounter Builder';
  if (cancel) cancel.classList.toggle('hidden', !editing);
}

async function deleteEncounter(encounterId) {
  const enc = state.encounterLibrary[encounterId];
  const ok = await confirmDialog(
    'Delete this encounter?',
    `"${enc ? enc.name : encounterId}" is removed. The enemies in it stay in the enemy library.`,
    'Delete');
  if (!ok) return;

  const resp = await apiFetch('/api/encounters/' + state.sessionId + '/' + encounterId, 'DELETE');
  if (resp.ok) {
    delete state.encounterLibrary[encounterId];
    if (state.editingEncounterId === encounterId) clearEncounterForm();
    renderBuilderEncounterLibrary();
    notify('Encounter deleted.', 'success');
  } else {
    notify('Failed to delete encounter.', 'error');
  }
}

// ---------------------------------------------------------------------------
// MM: Campaign notes
//
// These were written to sessionStorage and never read back — and logout() clears
// sessionStorage anyway, so the MM's notes vanished on reload. localStorage
// keyed by session survives both, and the field is now loaded on tab init.
// ---------------------------------------------------------------------------
function campaignNotesKey() {
  return 'facets_campaign_notes_' + state.sessionId;
}

function renderBuilderCampaignNotes() {
  const el = document.getElementById('builder-campaign-notes');
  if (!el || el.dataset.loaded === '1') return;
  try {
    el.value = localStorage.getItem(campaignNotesKey())
      || sessionStorage.getItem(campaignNotesKey())  // migrate any pre-existing draft
      || '';
  } catch (e) { /* storage disabled — the textarea still works for this sitting */ }
  el.dataset.loaded = '1';

  // Autosave on idle so a note is never lost to a mistimed reload.
  let timer = null;
  el.oninput = () => {
    clearTimeout(timer);
    timer = setTimeout(() => saveCampaignNotes(true), 800);
  };
}

function saveCampaignNotes(silent) {
  const notes = document.getElementById('builder-campaign-notes').value;
  try {
    localStorage.setItem(campaignNotesKey(), notes);
    const stamp = document.getElementById('builder-campaign-notes-status');
    if (stamp) stamp.textContent = 'Saved to this browser.';
    if (!silent) notify('Campaign notes saved to this browser.', 'success');
  } catch (e) {
    notify('Could not save notes — browser storage is unavailable.', 'error');
  }
}

// ---------------------------------------------------------------------------
// MM: Mark skill as used (PHB II.4 enforcement)
// ---------------------------------------------------------------------------
function renderBuilderMarkSkillSelect() {
  const select = document.getElementById('builder-mark-skill');
  if (!select || !state.ruleset) return;
  select.innerHTML = '';
  state.ruleset.skills.forEach(skill => {
    if (skill.status === 'stub') return;
    const opt = document.createElement('option');
    opt.value = skill.id;
    opt.textContent = skill.name;
    select.appendChild(opt);
  });
}

function mmMarkSkillUsed() {
  const playerName = document.getElementById('builder-mark-player').value;
  const skillId = document.getElementById('builder-mark-skill').value;
  if (!playerName || !skillId) { notify('Pick a player and a skill.', 'warn'); return; }
  sendWS({ type: 'mark_skill_used', player_name: playerName, skill_id: skillId });
}

// ---------------------------------------------------------------------------
// MM: Skill advancement controls
// ---------------------------------------------------------------------------
function renderBuilderAdvanceSkillSelect() {
  const select = document.getElementById('builder-advance-skill');
  if (!select || !state.ruleset) return;
  select.innerHTML = '';
  state.ruleset.skills.forEach(skill => {
    if (skill.status === 'stub') return;
    const opt = document.createElement('option');
    opt.value = skill.id;
    opt.textContent = skill.name;
    select.appendChild(opt);
  });
}

function mmAdvanceSkill() {
  const playerName = document.getElementById('builder-advance-player').value;
  const skillId = document.getElementById('builder-advance-skill').value;
  if (!playerName || !skillId) { notify('Pick a player and a skill.', 'warn'); return; }
  sendWS({ type: 'skill_advance', player_name: playerName, skill_id: skillId });
}

// ---------------------------------------------------------------------------
// MM: private per-character notes
//
// The character model and the notes endpoint both carry `notes_mm`, and nothing
// in the UI ever wrote it — the MM's private notes on a PC had nowhere to live.
// ---------------------------------------------------------------------------
function renderBuilderMMNotes() {
  const picker = document.getElementById('builder-mm-notes-player');
  const area = document.getElementById('builder-mm-notes');
  if (!picker || !area) return;
  const char = state.allCharacters[picker.value];
  area.value = (char && char.notes_mm) || '';
  area.disabled = !char;
}

async function saveMMNotes(ev) {
  const playerName = document.getElementById('builder-mm-notes-player').value;
  if (!playerName) { notify('Pick a character first.', 'warn'); return; }
  const notes = document.getElementById('builder-mm-notes').value;

  await withPending(ev && ev.target, 'Saving...', async () => {
    const resp = await apiFetch(`/api/characters/${state.sessionId}/${playerName}/notes`, 'PUT', {
      notes_mm: notes,
    });
    if (resp.ok) {
      const data = await resp.json();
      if (state.allCharacters[playerName]) state.allCharacters[playerName].notes_mm = data.notes_mm;
      notify('Notes saved.', 'success');
    } else {
      notify('Failed to save notes.', 'error');
    }
  });
}
