/**
 * Builder tab — character advancement (player), enemy/encounter builder (MM).
 * Depends on: state, sendWS, escapeHtml, apiFetch from app.js
 */

// ---------------------------------------------------------------------------
// Builder tab initialization
// ---------------------------------------------------------------------------
function initBuilderTab() {
  if (state.role === 'mm') {
    document.getElementById('builder-player-section').classList.add('hidden');
    document.getElementById('builder-mm-section').classList.remove('hidden');
    renderBuilderEnemyLibrary();
    renderBuilderEncounterEnemySelect();
    renderBuilderAdvanceSkillSelect();
  } else {
    document.getElementById('builder-player-section').classList.remove('hidden');
    document.getElementById('builder-mm-section').classList.add('hidden');
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
    spEl.textContent = 'No character yet.';
    listEl.innerHTML = '';
    return;
  }

  spEl.textContent = 'Session Skill Points Remaining: ' + (char.session_skill_points_remaining || 0);

  listEl.innerHTML = '';
  state.ruleset.skills.forEach(skill => {
    if (skill.status === 'stub') return;
    const ss = char.skills[skill.id] || { rank: 'novice', marks: 0 };
    const isPrimary = skill.facet === char.primary_facet;
    const cost = isPrimary ? 1 : 2;
    const canAfford = (char.session_skill_points_remaining || 0) >= cost;
    const marksNeeded = state.ruleset.advancement ? state.ruleset.advancement.marks_per_rank : 3;
    const dots = '\u25CF'.repeat(ss.marks) + '\u25CB'.repeat(Math.max(0, marksNeeded - ss.marks));

    const div = document.createElement('div');
    div.style.cssText = 'display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:13px;';
    div.innerHTML = `
      <div>
        <span>${skill.name}</span>
        ${isPrimary ? '' : '<span style="color:var(--text-dim);font-size:10px;margin-left:4px;">(cross ' + cost + ' SP)</span>'}
        <span class="rank-badge rank-${ss.rank}" style="margin-left:6px;">${ss.rank}</span>
        <span class="marks-dots" style="margin-left:6px;">${dots}</span>
      </div>
      <button class="btn btn-secondary btn-sm" ${canAfford ? '' : 'disabled'} onclick="spendSkillPoint('${skill.id}')" style="padding:3px 10px;min-height:28px;font-size:11px;">Spend</button>
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
    container.innerHTML = '<div style="color:var(--text-dim);font-size:13px;">No character yet.</div>';
    return;
  }

  // Show current techniques
  let html = '';
  if (char.techniques && char.techniques.length > 0) {
    html += '<div style="margin-bottom:8px;"><strong style="font-size:12px;color:var(--text-dim);">LEARNED</strong></div>';
    char.techniques.forEach(t => {
      const choice = char.technique_choices && char.technique_choices[t];
      html += '<div style="font-size:13px;padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.04);">' + escapeHtml(t) + (choice ? ' (' + escapeHtml(choice) + ')' : '') + '</div>';
    });
  }

  // Show available techniques
  const facetDef = state.ruleset.character_facets.find(cf => cf.id === char.primary_facet);
  if (facetDef && facetDef.techniques) {
    const available = facetDef.techniques.filter(t => {
      if (char.techniques && char.techniques.includes(t.id)) return false;
      if (t.prerequisite && t.prerequisite.facet_level && char.facet_level < t.prerequisite.facet_level) return false;
      return true;
    });

    if (available.length > 0) {
      html += '<div style="margin-top:12px;margin-bottom:8px;"><strong style="font-size:12px;color:var(--text-dim);">AVAILABLE</strong></div>';
      available.forEach(t => {
        const prereq = t.prerequisite ? ' (requires Facet Level ' + t.prerequisite.facet_level + ')' : '';
        html += '<div style="font-size:13px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04);display:flex;justify-content:space-between;align-items:center;">';
        html += '<div><strong>' + escapeHtml(t.id) + '</strong>' + prereq + '<br><span style="color:var(--text-dim);font-size:12px;">' + escapeHtml(t.description || '') + '</span></div>';
        html += '<button class="btn btn-secondary btn-sm" onclick="selectTechnique(\'' + escapeHtml(t.id) + '\')" style="padding:3px 10px;min-height:28px;font-size:11px;">Select</button>';
        html += '</div>';
      });
    }
  }

  if (!html) {
    html = '<div style="color:var(--text-dim);font-size:13px;">No techniques available at current level.</div>';
  }

  container.innerHTML = html;
}

function selectTechnique(techId) {
  // Some techniques require a choice (e.g., which skill to specialize in)
  // For now, just send without choice — MM confirms via separate event
  sendWS({ type: 'technique_select', technique_id: techId });
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
function previewEnemyTR() {
  const tier = document.getElementById('builder-enemy-tier').value;
  const endurance = parseInt(document.getElementById('builder-enemy-endurance').value) || 0;
  const attackMod = parseInt(document.getElementById('builder-enemy-attack').value) || 0;
  const armor = document.getElementById('builder-enemy-armor').value;
  const techniques = document.getElementById('builder-enemy-techniques').value.split(',').map(s => s.trim()).filter(Boolean);

  // Approximate TR calculation (mirrors server-side logic)
  // Offense value
  const offenseMap = { '-2': 0, '-1': 1, '0': 2, '1': 3, '2': 4, '3': 5, '4': 6 };
  const offenseValue = offenseMap[String(attackMod)] !== undefined ? offenseMap[String(attackMod)] : 2;

  // Durability value
  let durabilityValue = 0;
  if (tier === 'mook') {
    durabilityValue = 0;
  } else if (endurance <= 4) {
    durabilityValue = 2;
  } else if (endurance <= 6) {
    durabilityValue = 3;
  } else if (endurance <= 8) {
    durabilityValue = 4;
  } else if (endurance <= 10) {
    durabilityValue = 5;
  } else if (endurance <= 12) {
    durabilityValue = 6;
  } else {
    durabilityValue = 7;
  }

  const armorBonus = armor === 'light' ? 1 : armor === 'heavy' ? 2 : 0;
  const techniqueBonus = techniques.length;
  const tr = offenseValue + durabilityValue + armorBonus + techniqueBonus;

  // Apply minimums
  const minimums = { mook: 1, named: 8, boss: 12 };
  const finalTR = Math.max(tr, minimums[tier] || 0);

  document.getElementById('builder-enemy-tr').textContent = 'Threat Rating: ' + finalTR;
}

async function saveEnemy() {
  const name = document.getElementById('builder-enemy-name').value.trim();
  if (!name) { alert('Enemy name is required.'); return; }

  const id = name.toLowerCase().replace(/[^a-z0-9]+/g, '_');
  const techniques = document.getElementById('builder-enemy-techniques').value.split(',').map(s => s.trim()).filter(Boolean);

  const enemy = {
    session_id: state.sessionId,
    id: id,
    name: name,
    tier: document.getElementById('builder-enemy-tier').value,
    endurance: parseInt(document.getElementById('builder-enemy-endurance').value) || 0,
    attack_modifier: parseInt(document.getElementById('builder-enemy-attack').value) || 0,
    defense_modifier: parseInt(document.getElementById('builder-enemy-defense').value) || 0,
    armor: document.getElementById('builder-enemy-armor').value,
    techniques: techniques,
    special: document.getElementById('builder-enemy-special').value.trim() || null,
    description: document.getElementById('builder-enemy-description').value.trim(),
    tactics: document.getElementById('builder-enemy-tactics').value.trim(),
  };

  const resp = await apiFetch('/api/enemies/', 'POST', enemy);
  if (resp.ok) {
    const data = await resp.json();
    state.enemyLibrary[data.enemy.id] = data.enemy;
    renderBuilderEnemyLibrary();
    renderBuilderEncounterEnemySelect();
    updateSpawnEnemySelect();
    document.getElementById('builder-enemy-status').textContent = 'Saved: ' + name + ' (TR ' + data.enemy.tr + ')';
    setTimeout(() => { document.getElementById('builder-enemy-status').textContent = ''; }, 3000);
  } else {
    const err = await resp.json();
    alert(err.detail || 'Failed to save enemy.');
  }
}

function renderBuilderEnemyLibrary() {
  const container = document.getElementById('builder-enemy-library-list');
  if (!container) return;

  if (Object.keys(state.enemyLibrary).length === 0) {
    container.innerHTML = '<div style="font-size:13px;color:var(--text-dim);">No enemies saved.</div>';
    return;
  }

  container.innerHTML = '';
  Object.entries(state.enemyLibrary).forEach(([id, enemy]) => {
    const div = document.createElement('div');
    div.style.cssText = 'display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:13px;';
    div.innerHTML = `
      <div>
        <strong>${escapeHtml(enemy.name)}</strong>
        <span style="color:var(--text-dim);margin-left:6px;">${enemy.tier} | TR ${enemy.tr || '?'}</span>
      </div>
      <button class="btn btn-secondary btn-sm" onclick="deleteEnemy('${escapeHtml(id)}')" style="padding:3px 8px;min-height:24px;font-size:11px;">x</button>
    `;
    container.appendChild(div);
  });
}

async function deleteEnemy(enemyId) {
  const resp = await apiFetch('/api/enemies/' + state.sessionId + '/' + enemyId, 'DELETE');
  if (resp.ok) {
    delete state.enemyLibrary[enemyId];
    renderBuilderEnemyLibrary();
    renderBuilderEncounterEnemySelect();
    updateSpawnEnemySelect();
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
  if (!enemyId) return;

  const container = document.getElementById('builder-encounter-enemies');
  if (!container) return;

  const enemy = state.enemyLibrary[enemyId];
  if (!enemy) return;

  const div = document.createElement('div');
  div.className = 'encounter-enemy-row';
  div.dataset.enemyId = enemyId;
  div.style.cssText = 'display:flex;justify-content:space-between;align-items:center;padding:4px 0;font-size:13px;';
  div.innerHTML = `
    <span>${escapeHtml(enemy.name)} (TR ${enemy.tr || '?'})</span>
    <div style="display:flex;align-items:center;gap:6px;">
      <label style="margin:0;font-size:11px;">Count:</label>
      <input type="number" class="encounter-enemy-count" value="1" min="1" style="width:50px;padding:4px;margin:0;">
      <button class="btn btn-secondary btn-sm" onclick="this.closest('.encounter-enemy-row').remove()" style="padding:2px 8px;min-height:24px;font-size:11px;">x</button>
    </div>
  `;
  container.appendChild(div);
}

async function saveEncounter() {
  const name = document.getElementById('builder-encounter-name').value.trim();
  if (!name) { alert('Encounter name is required.'); return; }

  const id = name.toLowerCase().replace(/[^a-z0-9]+/g, '_');
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

  const resp = await apiFetch('/api/encounters/', 'POST', encounter);
  if (resp.ok) {
    const data = await resp.json();
    state.encounterLibrary[data.encounter.id] = data.encounter;
    document.getElementById('builder-encounter-status').textContent = 'Saved: ' + name;
    setTimeout(() => { document.getElementById('builder-encounter-status').textContent = ''; }, 3000);
  } else {
    const err = await resp.json();
    alert(err.detail || 'Failed to save encounter.');
  }
}

// ---------------------------------------------------------------------------
// MM: Campaign notes (stored in sessionStorage for now)
// ---------------------------------------------------------------------------
function saveCampaignNotes() {
  const notes = document.getElementById('builder-campaign-notes').value;
  sessionStorage.setItem('facets_campaign_notes_' + state.sessionId, notes);
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
  const playerName = document.getElementById('builder-advance-player').value.trim();
  const skillId = document.getElementById('builder-advance-skill').value;
  if (!playerName || !skillId) { alert('Player name and skill are required.'); return; }
  sendWS({ type: 'skill_advance', player_name: playerName, skill_id: skillId });
  document.getElementById('builder-advance-status').textContent = 'Mark awarded to ' + playerName + ' for ' + skillId;
  setTimeout(() => { document.getElementById('builder-advance-status').textContent = ''; }, 3000);
}
