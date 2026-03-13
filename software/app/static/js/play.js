/**
 * Play Field tab — rolling, combat, chat, sparks, enemy tracker.
 * Depends on: state, sendWS, escapeHtml, apiFetch from app.js
 */

// ---------------------------------------------------------------------------
// Play Field initialization
// ---------------------------------------------------------------------------
function initPlayTab() {
  renderPlayCharacterSheet();
  renderPlayRollLog();
  renderPlayPlayerList();
  renderCombatPanel();
  renderMagicPanel();
  if (state.role === 'mm') {
    document.getElementById('play-mm-controls').classList.remove('hidden');
    renderEnemyTracker();
    updateSpawnEnemySelect();
  } else {
    document.getElementById('play-player-controls').classList.remove('hidden');
  }
}

// ---------------------------------------------------------------------------
// Character sheet (interactive, in play tab)
// ---------------------------------------------------------------------------
function renderPlayCharacterSheet() {
  const char = state.character;
  if (!char || !state.ruleset) return;

  const facetDef = state.ruleset.character_facets.find(cf => cf.id === char.primary_facet);
  document.getElementById('play-char-name').textContent = char.name;
  document.getElementById('play-char-facet').textContent = facetDef ? facetDef.name : char.primary_facet;
  document.getElementById('play-char-facet').className = 'facet-badge facet-' + char.primary_facet;
  document.getElementById('play-char-level').textContent = 'Facet Level ' + char.facet_level;

  renderPlayAttributeGrid(char);
  renderPlaySkillsTable(char);
  renderPlaySparkCounter();
}

function renderPlayAttributeGrid(char) {
  const container = document.getElementById('play-attr-display');
  if (!container || !state.ruleset) return;
  container.innerHTML = '';

  state.ruleset.major_attributes.forEach(major => {
    const groupDiv = document.createElement('div');
    groupDiv.className = 'major-group';
    groupDiv.innerHTML = '<div class="major-label">' + major.name + '</div>';

    const gridDiv = document.createElement('div');
    gridDiv.className = 'attr-grid';

    major.minor_attributes.forEach(minorId => {
      const minor = state.ruleset.minor_attributes.find(m => m.id === minorId);
      if (!minor) return;
      const rating = char.attributes[minorId] || 2;
      const ratingDef = state.ruleset.attribute_ratings.find(r => r.rating === rating);
      const mod = ratingDef ? ratingDef.modifier : 0;
      const modStr = mod > 0 ? '+' + mod : '' + mod;

      const block = document.createElement('div');
      block.className = 'attr-block' + (state.selectedAttributeId === minorId ? ' selected' : '');
      block.title = minor.description;
      block.innerHTML = `
        <div class="attr-name">${minor.name}</div>
        <div class="attr-rating">${rating}</div>
        <div class="attr-modifier">${modStr}</div>
        <div class="attr-label">${ratingDef ? ratingDef.label : ''}</div>
      `;
      block.onclick = () => selectAttribute(minorId);
      gridDiv.appendChild(block);
    });
    groupDiv.appendChild(gridDiv);
    container.appendChild(groupDiv);
  });
}

function renderPlaySkillsTable(char) {
  const tbody = document.getElementById('play-skills-tbody');
  if (!tbody || !state.ruleset) return;
  tbody.innerHTML = '';

  state.ruleset.skills.forEach(skill => {
    if (skill.status === 'stub') return;
    const skillState = char.skills[skill.id] || { rank: 'novice', marks: 0 };
    const marksNeeded = state.ruleset.advancement ? state.ruleset.advancement.marks_per_rank : 3;
    const dots = '\u25CF'.repeat(skillState.marks) + '\u25CB'.repeat(Math.max(0, marksNeeded - skillState.marks));
    const isPrimary = skill.facet === char.primary_facet;

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${skill.name}${isPrimary ? '' : ' <span style="color:var(--text-dim);font-size:10px">\u25CF</span>'}</td>
      <td><span class="rank-badge rank-${skillState.rank}">${skillState.rank}</span></td>
      <td class="marks-dots" title="${skillState.marks}/${marksNeeded}">${dots}</td>
      <td><button class="btn-roll-skill" onclick="rollSkill('${skill.id}')">Roll</button></td>
    `;
    tbody.appendChild(tr);
  });
}

function renderPlaySparkCounter() {
  const char = state.character;
  if (!char) return;
  const container = document.getElementById('play-spark-pips');
  if (!container) return;
  container.innerHTML = '';

  const maxSparks = Math.max(char.sparks, 6);
  for (let i = 0; i < maxSparks; i++) {
    const pip = document.createElement('div');
    pip.className = 'spark-pip' + (i < char.sparks ? ' filled' : '');
    pip.title = i < char.sparks ? 'Spark available' : 'Empty';
    pip.onclick = () => toggleSparkSpend(i);
    container.appendChild(pip);
  }

  const countEl = document.getElementById('play-spark-count');
  if (countEl) countEl.textContent = char.sparks + ' Spark' + (char.sparks !== 1 ? 's' : '');
  const spendEl = document.getElementById('play-sparks-to-spend');
  if (spendEl) spendEl.textContent = state.sparksToSpend > 0 ? '(spending ' + state.sparksToSpend + ')' : '';
}

function toggleSparkSpend(index) {
  if (!state.character) return;
  state.sparksToSpend = index + 1 <= state.character.sparks ? index + 1 : 0;
  if (state.sparksToSpend === state.character.sparks + 1) state.sparksToSpend = 0;
  renderPlaySparkCounter();
  const pips = document.querySelectorAll('#play-spark-pips .spark-pip');
  pips.forEach((pip, i) => {
    pip.style.borderColor = i < state.sparksToSpend ? 'var(--accent)' : '';
  });
}

// ---------------------------------------------------------------------------
// Rolling
// ---------------------------------------------------------------------------
function selectAttribute(attrId) {
  state.selectedAttributeId = attrId;
  state.selectedSkillId = null;
  renderPlayAttributeGrid(state.character);
  const btn = document.getElementById('play-roll-btn');
  if (btn) btn.disabled = false;
  const display = document.getElementById('play-roll-attr-display');
  if (display) {
    const minor = state.ruleset.minor_attributes.find(m => m.id === attrId);
    display.textContent = minor ? minor.name : attrId;
  }
}

function rollSkill(skillId) {
  if (!state.ruleset) return;
  const skill = state.ruleset.skills.find(s => s.id === skillId);
  if (!skill) return;
  state.selectedSkillId = skillId;
  state.selectedAttributeId = skill.attribute;
  renderPlayAttributeGrid(state.character);
  const btn = document.getElementById('play-roll-btn');
  if (btn) btn.disabled = false;
  const display = document.getElementById('play-roll-attr-display');
  if (display) {
    const minor = state.ruleset.minor_attributes.find(m => m.id === skill.attribute);
    display.textContent = (minor ? minor.name : skill.attribute) + ' + ' + skill.name;
  }
  performRoll();
}

function performRoll() {
  if (!state.selectedAttributeId) {
    addSystemChat('Select an attribute to roll.');
    return;
  }

  const diffEl = document.getElementById('play-difficulty-select');
  const descEl = document.getElementById('play-roll-description');
  const difficulty = diffEl ? diffEl.value : 'Standard';
  const description = descEl ? descEl.value.slice(0, 200) : '';

  sendWS({
    type: 'roll',
    attribute_id: state.selectedAttributeId,
    skill_id: state.selectedSkillId || null,
    difficulty,
    sparks_spent: state.sparksToSpend,
    description,
  });

  state.sparksToSpend = 0;
}

function onRollResult(msg) {
  const roll = msg.roll;
  state.rollLog.unshift({ player_name: msg.player, character_name: msg.character_name, ...roll });
  renderPlayRollLog();

  const resultBox = document.getElementById('play-roll-result-box');
  if (resultBox) {
    resultBox.className = 'roll-result-box ' + roll.outcome;
    resultBox.classList.remove('hidden');
    resultBox.innerHTML = buildRollResultHtml(msg, roll);
  }

  if (msg.player === state.playerName && state.character) {
    state.character.sparks = msg.character_sparks_remaining;
    renderPlaySparkCounter();
  }
}

function buildRollResultHtml(msg, roll) {
  const allDice = roll.dice_rolled;
  const keptDice = roll.dice_kept;
  const droppedIndices = [];
  const remaining = [...allDice];
  const keptCopy = [...keptDice];
  remaining.forEach((d, i) => {
    const ki = keptCopy.indexOf(d);
    if (ki !== -1) keptCopy.splice(ki, 1);
    else droppedIndices.push(i);
  });

  const diceHtml = allDice.map((d, i) => {
    const isDropped = droppedIndices.includes(i);
    return '<div class="die ' + (isDropped ? 'dropped' : 'kept') + '" title="' + (isDropped ? 'dropped (Spark)' : 'kept') + '">' + d + '</div>';
  }).join('');

  const modParts = [];
  if (roll.attribute_modifier !== 0) modParts.push('Attr ' + (roll.attribute_modifier > 0 ? '+' : '') + roll.attribute_modifier);
  if (roll.skill_modifier !== 0) modParts.push('Skill +' + roll.skill_modifier);
  if (roll.difficulty_modifier !== 0) modParts.push('Diff ' + (roll.difficulty_modifier > 0 ? '+' : '') + roll.difficulty_modifier);
  const modStr = modParts.length ? ' (' + modParts.join(', ') + ')' : '';

  const whoStr = msg.player === state.playerName ? 'You' : (msg.character_name || msg.player);

  return `
    <div style="font-size:0.8rem;color:var(--text-dim);margin-bottom:4px;">${whoStr} rolled ${roll.attribute_id}${roll.skill_id ? ' + ' + roll.skill_id : ''}${roll.difficulty !== 'Standard' ? ' [' + roll.difficulty + ']' : ''}${roll.sparks_spent > 0 ? ' x' + roll.sparks_spent : ''}</div>
    <div class="dice-display">${diceHtml}</div>
    <div class="roll-total">${roll.total}</div>
    <div class="roll-outcome-label">${roll.outcome_label}</div>
    <div class="roll-outcome-desc">${roll.outcome_description}</div>
    <div class="roll-breakdown">Dice sum: ${roll.dice_sum}${modStr} = ${roll.total}</div>
    ${roll.description ? '<div style="font-size:0.8rem;color:var(--text-dim);margin-top:4px;font-style:italic;">"' + escapeHtml(roll.description) + '"</div>' : ''}
  `;
}

// ---------------------------------------------------------------------------
// Roll log
// ---------------------------------------------------------------------------
function renderPlayRollLog() {
  const container = document.getElementById('play-roll-log');
  if (!container) return;
  container.innerHTML = '';
  const DESC_MAX = 40;
  state.rollLog.slice(0, 30).forEach(entry => {
    const div = document.createElement('div');
    div.className = 'roll-log-entry';
    const desc = (entry.description || '').trim();
    const descHtml = desc
      ? '<div class="roll-log-desc" title="' + desc.replace(/"/g, '&quot;') + '">' + (desc.length > DESC_MAX ? desc.slice(0, DESC_MAX) + '...' : desc) + '</div>'
      : '';
    div.innerHTML = `
      <span class="who">${entry.character_name || entry.player_name}</span>
      <span class="outcome-${entry.outcome}"> ${entry.total} -- ${entry.outcome_label}</span>
      <span style="color:var(--text-dim);float:right">${entry.attribute_id}${entry.skill_id ? '+' + entry.skill_id : ''}</span>
      ${descHtml}
    `;
    container.appendChild(div);
  });
}

// ---------------------------------------------------------------------------
// Player list
// ---------------------------------------------------------------------------
function renderPlayPlayerList() {
  const ul = document.getElementById('play-player-list');
  if (!ul) return;
  ul.innerHTML = '';
  Object.values(state.allCharacters).forEach(char => {
    const li = document.createElement('li');
    const isOnline = state.connectedPlayers.has(char.player_name);
    li.innerHTML = `
      <span class="${isOnline ? 'player-online' : ''}">${escapeHtml(char.player_name)}${char.name !== char.player_name ? ' (' + escapeHtml(char.name) + ')' : ''}</span>
      <span class="facet-badge facet-${char.primary_facet}">${char.primary_facet}</span>
    `;
    ul.appendChild(li);
  });
}

// ---------------------------------------------------------------------------
// Chat — these are the canonical chat functions called by handleServerMessage
// ---------------------------------------------------------------------------
function addChatMessage(from, text) {
  const log = document.getElementById('play-chat-log');
  if (!log) return;
  const div = document.createElement('div');
  div.className = 'chat-msg';
  div.innerHTML = '<span class="from">' + escapeHtml(from) + '</span>: ' + escapeHtml(text);
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

function addSystemChat(text) {
  const log = document.getElementById('play-chat-log');
  if (!log) return;
  const div = document.createElement('div');
  div.className = 'chat-msg system';
  div.textContent = text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

function sendChat() {
  const input = document.getElementById('play-chat-input');
  const text = input ? input.value.trim() : '';
  if (!text) return;
  sendWS({ type: 'chat', text });
  if (input) input.value = '';
}

// ---------------------------------------------------------------------------
// Spark controls
// ---------------------------------------------------------------------------
function mmAwardSpark() {
  const playerName = document.getElementById('play-mm-spark-player').value.trim();
  const reason = document.getElementById('play-mm-spark-reason').value.trim() || 'MM award';
  if (!playerName) return;
  sendWS({ type: 'spark_earn', player_name: playerName, reason });
}

function nominateForSpark() {
  const playerName = document.getElementById('play-peer-spark-player').value.trim();
  if (!playerName) return;
  sendWS({ type: 'spark_earn_peer', player_name: playerName });
}

function onSparkNomination(msg) {
  const banner = document.getElementById('play-spark-nomination-banner');
  if (!banner) return;
  banner.classList.remove('hidden');
  banner.querySelector('.nomination-text').textContent = msg.message;
  banner.dataset.nominatedPlayer = msg.player;
}

function confirmSparkNomination() {
  const banner = document.getElementById('play-spark-nomination-banner');
  const playerName = banner.dataset.nominatedPlayer;
  if (playerName) {
    sendWS({ type: 'spark_earn', player_name: playerName, reason: 'Peer nomination' });
  }
  banner.classList.add('hidden');
}

// ---------------------------------------------------------------------------
// Enemy Tracker (MM only, in Play Field)
// ---------------------------------------------------------------------------
function renderEnemyTracker() {
  const container = document.getElementById('play-enemy-tracker');
  if (!container) return;
  container.innerHTML = '';

  if (Object.keys(state.activeEnemies).length === 0) {
    container.innerHTML = '<div style="font-size:12px;color:var(--text-dim);">No active enemies.</div>';
    return;
  }

  Object.entries(state.activeEnemies).forEach(([key, enemy]) => {
    const condStr = enemy.conditions && enemy.conditions.length > 0 ? enemy.conditions.join(', ') : 'none';
    const div = document.createElement('div');
    div.className = 'enemy-tracker-entry';
    div.innerHTML = `
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <strong>${escapeHtml(enemy.name)}</strong>
        <span style="font-size:11px;color:var(--text-dim);">${enemy.tier} | TR ${enemy.tr || '?'}</span>
      </div>
      <div style="font-size:12px;margin-top:4px;">
        ${enemy.tier !== 'mook' ? 'End: <span class="enemy-endurance">' + (enemy.endurance_current !== null && enemy.endurance_current !== undefined ? enemy.endurance_current : enemy.endurance) + '</span>/' + enemy.endurance : 'Mook'}
        | Cond: ${condStr}
      </div>
      <div class="btn-row" style="margin-top:4px;">
        ${enemy.tier !== 'mook' ? '<button class="btn btn-secondary btn-sm" onclick="enemyTakeDamage(\'' + escapeHtml(key) + '\')">-1 End</button>' : ''}
        <button class="btn btn-secondary btn-sm" onclick="enemyAddCondition('${escapeHtml(key)}')">+Cond</button>
        <button class="btn btn-secondary btn-sm" onclick="removeEnemy('${escapeHtml(key)}')">Remove</button>
      </div>
    `;
    container.appendChild(div);
  });
}

function spawnEnemyFromLibrary() {
  const enemyId = document.getElementById('play-spawn-enemy-select').value;
  const instanceName = document.getElementById('play-spawn-instance-name').value.trim();
  if (!enemyId) return;
  sendWS({ type: 'spawn_enemy', enemy_id: enemyId, instance_name: instanceName || undefined });
  const nameEl = document.getElementById('play-spawn-instance-name');
  if (nameEl) nameEl.value = '';
}

function enemyTakeDamage(trackerKey) {
  const enemy = state.activeEnemies[trackerKey];
  if (!enemy) return;
  const current = enemy.endurance_current !== null && enemy.endurance_current !== undefined ? enemy.endurance_current : enemy.endurance;
  sendWS({ type: 'enemy_update', tracker_key: trackerKey, endurance_current: Math.max(0, current - 1) });
}

function enemyAddCondition(trackerKey) {
  const cond = prompt('Condition to add:');
  if (!cond) return;
  sendWS({ type: 'enemy_update', tracker_key: trackerKey, add_condition: cond.trim() });
}

function removeEnemy(trackerKey) {
  sendWS({ type: 'remove_enemy', tracker_key: trackerKey });
}

function onEnemySpawned(msg) {
  state.activeEnemies[msg.tracker_key] = { ...msg.enemy, tr: msg.tr };
  renderEnemyTracker();
  updateSpawnEnemySelect();
}

function onEnemyUpdated(msg) {
  const enemy = state.activeEnemies[msg.tracker_key];
  if (enemy) {
    enemy.endurance_current = msg.endurance_current;
    enemy.conditions = msg.conditions;
    renderEnemyTracker();
  }
}

function onEnemyRemoved(msg) {
  delete state.activeEnemies[msg.tracker_key];
  renderEnemyTracker();
}

function updateSpawnEnemySelect() {
  const select = document.getElementById('play-spawn-enemy-select');
  if (!select) return;
  select.innerHTML = '<option value="">-- select enemy --</option>';
  Object.entries(state.enemyLibrary).forEach(([id, enemy]) => {
    const opt = document.createElement('option');
    opt.value = id;
    opt.textContent = enemy.name + ' (TR ' + (enemy.tr || '?') + ')';
    select.appendChild(opt);
  });
}

// ---------------------------------------------------------------------------
// Combat controls (MM)
// ---------------------------------------------------------------------------
function startCombat() {
  sendWS({ type: 'combat_start' });
}

function endCombat() {
  sendWS({ type: 'combat_end' });
  state.activeEnemies = {};
  renderEnemyTracker();
}

function endExchange() {
  sendWS({ type: 'end_exchange' });
}

// ---------------------------------------------------------------------------
// Combat Panel — rendering and state
// ---------------------------------------------------------------------------

function renderCombatPanel() {
  const panel = document.getElementById('combat-panel');
  if (!panel || !state.character) return;

  if (!state.inCombat) {
    panel.classList.add('hidden');
    return;
  }

  panel.classList.remove('hidden');
  updateEnduranceBar();
  updatePostureBadge(state.character.posture || 'measured');
  updateConditionsDisplay();
  populateCombatSelects();
  updateReactCostPreview();
}

function updateEnduranceBar() {
  const char = state.character;
  if (!char) return;
  const current = char.endurance_current != null ? char.endurance_current : 0;
  const max = char.endurance_max || current || 1;
  const pct = Math.round((current / max) * 100);

  const fill = document.getElementById('combat-endurance-fill');
  const text = document.getElementById('combat-endurance-text');
  if (fill) {
    fill.style.width = pct + '%';
    fill.className = 'endurance-fill' + (pct <= 25 ? ' critical' : pct <= 50 ? ' low' : '');
  }
  if (text) text.textContent = current + '/' + max;
}

function updatePostureBadge(posture) {
  const badge = document.getElementById('combat-posture-badge');
  if (!badge) return;
  badge.textContent = posture.charAt(0).toUpperCase() + posture.slice(1);
  badge.className = 'posture-badge posture-' + posture;
  // Sync radio
  const radio = document.querySelector('input[name="combat-posture"][value="' + posture + '"]');
  if (radio) radio.checked = true;
}

function updateConditionsDisplay() {
  const container = document.getElementById('combat-conditions');
  if (!container || !state.character) return;
  const conditions = state.character.conditions || [];
  if (conditions.length === 0) {
    container.innerHTML = '';
    return;
  }
  container.innerHTML = conditions.map(c => {
    const tier = getConditionTier(c);
    const desc = getConditionDescription(c);
    return '<span class="condition-badge condition-tier' + tier + '" title="' + escapeHtml(desc) + '">' + escapeHtml(c.replace(/_/g, ' ')) + '</span>';
  }).join(' ');
}

function getConditionTier(condId) {
  if (!state.ruleset || !state.ruleset.combat || !state.ruleset.combat.conditions) return 1;
  const conds = state.ruleset.combat.conditions;
  if (conds.tier1 && conds.tier1.some(c => c.id === condId)) return 1;
  if (conds.tier2 && conds.tier2.some(c => c.id === condId)) return 2;
  if (conds.tier3 && conds.tier3.some(c => c.id === condId)) return 3;
  return 1;
}

function getConditionDescription(condId) {
  if (!state.ruleset || !state.ruleset.combat || !state.ruleset.combat.conditions) return '';
  const conds = state.ruleset.combat.conditions;
  const all = (conds.tier1 || []).concat(conds.tier2 || []).concat(conds.tier3 || []);
  const match = all.find(c => c.id === condId);
  return match ? match.description : '';
}

function populateCombatSelects() {
  // Populate attribute selects for strike/support/maneuver
  ['strike-attribute', 'support-attribute', 'maneuver-attribute'].forEach(selId => {
    const sel = document.getElementById(selId);
    if (!sel || sel.options.length > 1) return;
    sel.innerHTML = '';
    if (state.ruleset && state.ruleset.minor_attributes) {
      state.ruleset.minor_attributes.forEach(attr => {
        const opt = document.createElement('option');
        opt.value = attr.id;
        opt.textContent = attr.name;
        sel.appendChild(opt);
      });
    }
  });

  // Populate skill selects
  ['strike-skill', 'support-skill', 'maneuver-skill'].forEach(selId => {
    const sel = document.getElementById(selId);
    if (!sel || sel.options.length > 1) return;
    sel.innerHTML = '<option value="">-- none --</option>';
    if (state.ruleset && state.ruleset.skills) {
      state.ruleset.skills.forEach(skill => {
        if (skill.status === 'stub') return;
        const opt = document.createElement('option');
        opt.value = skill.id;
        opt.textContent = skill.name;
        sel.appendChild(opt);
      });
    }
  });

  // Populate support target (ally players)
  const supportTarget = document.getElementById('support-target');
  if (supportTarget && supportTarget.options.length <= 1) {
    supportTarget.innerHTML = '<option value="">-- select ally --</option>';
    Object.keys(state.allCharacters).forEach(pn => {
      if (pn === state.playerName) return;
      const opt = document.createElement('option');
      opt.value = pn;
      opt.textContent = state.allCharacters[pn].name || pn;
      supportTarget.appendChild(opt);
    });
  }
}

function updateReactCostPreview() {
  const preview = document.getElementById('react-cost-preview');
  if (!preview || !state.character) return;
  const posture = state.character.posture || 'measured';
  const baseCosts = { dodge: 1, parry: 1, absorb: 0, intercept: 2 };
  const postureMod = posture === 'aggressive' ? 1 : (posture === 'defensive' || posture === 'withdrawn') ? -1 : 0;
  const lines = Object.entries(baseCosts).map(([r, base]) => {
    const cost = posture === 'withdrawn' ? 0 : Math.max(0, base + postureMod);
    return r.charAt(0).toUpperCase() + r.slice(1) + ': ' + cost + ' End';
  });
  preview.textContent = 'Costs (' + posture + '): ' + lines.join(' | ');
}

function showCombatAction(action) {
  ['strike', 'react', 'support', 'maneuver'].forEach(a => {
    const form = document.getElementById('combat-form-' + a);
    if (form) form.classList.toggle('hidden', a !== action || !form.classList.contains('hidden'));
  });
}

// ---------------------------------------------------------------------------
// Combat Panel — player actions
// ---------------------------------------------------------------------------

function declarePosture() {
  const checked = document.querySelector('input[name="combat-posture"]:checked');
  const posture = checked ? checked.value : 'measured';
  sendWS({ type: 'declare_posture', posture });
}

function performStrike() {
  const target = (document.getElementById('strike-target').value || '').trim();
  const attrId = document.getElementById('strike-attribute').value;
  const skillId = document.getElementById('strike-skill').value || null;
  const difficulty = document.getElementById('strike-difficulty').value;
  const press = document.getElementById('strike-press').checked;

  sendWS({
    type: 'strike',
    target,
    attribute_id: attrId,
    skill_id: skillId,
    difficulty,
    press,
    sparks_spent: state.sparksToSpend,
  });
  state.sparksToSpend = 0;
  renderPlaySparkCounter();
}

function performReact(reaction) {
  sendWS({
    type: 'react',
    reaction,
    difficulty: 'Standard',
  });
}

function performSupport() {
  const target = document.getElementById('support-target').value;
  const bonusType = document.getElementById('support-bonus-type').value;
  const attrId = document.getElementById('support-attribute').value;
  const skillId = document.getElementById('support-skill').value || null;

  if (!target) { addSystemChat('Select a target ally.'); return; }
  sendWS({
    type: 'support',
    target,
    bonus_type: bonusType,
    attribute_id: attrId,
    skill_id: skillId,
    difficulty: 'Standard',
  });
}

function performManeuver() {
  const target = (document.getElementById('maneuver-target').value || '').trim();
  const attrId = document.getElementById('maneuver-attribute').value;
  const skillId = document.getElementById('maneuver-skill').value || null;
  const description = (document.getElementById('maneuver-description').value || '').trim();

  sendWS({
    type: 'maneuver',
    target,
    attribute_id: attrId,
    skill_id: skillId,
    difficulty: 'Standard',
    description,
  });
}

// ---------------------------------------------------------------------------
// Combat Panel — broadcast handlers
// ---------------------------------------------------------------------------

function onCombatStarted(msg) {
  state.inCombat = true;
  state.postures = {};
  addSystemChat('Combat has begun!');

  // Update character combat state from server
  if (state.character && msg.characters) {
    const myState = msg.characters[state.playerName];
    if (myState) {
      state.character.endurance_current = myState.endurance_current;
      state.character.endurance_max = myState.endurance_max;
      state.character.conditions = myState.conditions || [];
      state.character.posture = myState.posture || 'measured';
    }
  }

  // Store all characters' combat state
  if (msg.characters) {
    Object.entries(msg.characters).forEach(([pn, cs]) => {
      if (state.allCharacters[pn]) {
        state.allCharacters[pn].endurance_current = cs.endurance_current;
        state.allCharacters[pn].endurance_max = cs.endurance_max;
        state.allCharacters[pn].conditions = cs.conditions || [];
        state.allCharacters[pn].posture = cs.posture || 'measured';
      }
    });
  }

  renderCombatPanel();
  renderMagicPanel();
}

function onPostureDeclared(msg) {
  if (state.character) {
    state.character.posture = msg.posture;
    updatePostureBadge(msg.posture);
    updateReactCostPreview();
  }
  addSystemChat('Posture declared: ' + msg.posture);
}

function onPosturesRevealed(msg) {
  state.postures = msg.postures || {};
  const container = document.getElementById('combat-postures-revealed');
  const list = document.getElementById('combat-postures-list');
  if (container && list) {
    container.classList.remove('hidden');
    list.innerHTML = Object.entries(state.postures).map(([pn, p]) => {
      const name = (state.allCharacters[pn] && state.allCharacters[pn].name) || pn;
      return '<div class="posture-reveal-entry"><span class="posture-badge posture-' + p + '">' + p + '</span> ' + escapeHtml(name) + '</div>';
    }).join('');
  }

  // Update all characters' postures
  Object.entries(state.postures).forEach(([pn, p]) => {
    if (state.allCharacters[pn]) state.allCharacters[pn].posture = p;
    if (pn === state.playerName && state.character) {
      state.character.posture = p;
      updatePostureBadge(p);
      updateReactCostPreview();
    }
  });

  addSystemChat('Postures revealed: ' + Object.entries(state.postures).map(([pn, p]) => pn + '=' + p).join(', '));
}

function onStrikeResult(msg) {
  const roll = msg.roll;
  state.rollLog.unshift({ player_name: msg.attacker, character_name: (state.allCharacters[msg.attacker] || {}).name, ...roll });
  renderPlayRollLog();

  // Update attacker state
  if (msg.attacker === state.playerName && state.character) {
    state.character.endurance_current = msg.endurance_remaining;
    state.character.sparks = msg.sparks_remaining;
    updateEnduranceBar();
    renderPlaySparkCounter();
  }
  if (state.allCharacters[msg.attacker]) {
    state.allCharacters[msg.attacker].endurance_current = msg.endurance_remaining;
  }

  const attackerName = (state.allCharacters[msg.attacker] || {}).name || msg.attacker;
  const targetStr = msg.target ? ' vs ' + msg.target : '';
  addSystemChat(attackerName + ' strikes' + targetStr + ': ' + roll.outcome_label + ' (total ' + roll.total + ')' + (msg.press_used ? ' [Press]' : ''));

  // Show result box for own strikes
  if (msg.attacker === state.playerName) {
    const resultBox = document.getElementById('play-roll-result-box');
    if (resultBox) {
      resultBox.className = 'roll-result-box ' + roll.outcome;
      resultBox.classList.remove('hidden');
      resultBox.innerHTML = buildRollResultHtml({ player: msg.attacker, character_name: attackerName }, roll);
    }
  }
}

function onReactResult(msg) {
  const roll = msg.roll;
  if (roll) {
    state.rollLog.unshift({ player_name: msg.player, character_name: (state.allCharacters[msg.player] || {}).name, ...roll });
    renderPlayRollLog();
  }

  // Update reactor state
  if (msg.player === state.playerName && state.character) {
    state.character.endurance_current = msg.endurance_remaining;
    updateEnduranceBar();
  }
  if (state.allCharacters[msg.player]) {
    state.allCharacters[msg.player].endurance_current = msg.endurance_remaining;
  }

  const reactorName = (state.allCharacters[msg.player] || {}).name || msg.player;
  const rollStr = roll ? ' — ' + roll.outcome_label : '';
  addSystemChat(reactorName + ' reacts: ' + msg.reaction + ' (cost ' + msg.endurance_cost + ' End)' + rollStr);
}

function onSupportResult(msg) {
  const roll = msg.roll;
  state.rollLog.unshift({ player_name: msg.player, character_name: (state.allCharacters[msg.player] || {}).name, ...roll });
  renderPlayRollLog();

  const supporterName = (state.allCharacters[msg.player] || {}).name || msg.player;
  const targetName = msg.target || '?';
  addSystemChat(supporterName + ' supports ' + targetName + ' (' + msg.bonus_type + '): ' + roll.outcome_label);
}

function onManeuverResult(msg) {
  const roll = msg.roll;
  state.rollLog.unshift({ player_name: msg.player, character_name: (state.allCharacters[msg.player] || {}).name, ...roll });
  renderPlayRollLog();

  const mName = (state.allCharacters[msg.player] || {}).name || msg.player;
  const targetStr = msg.target ? ' on ' + msg.target : '';
  addSystemChat(mName + ' maneuvers' + targetStr + ': ' + roll.outcome_label);
}

function onConditionApplied(msg) {
  // Update character conditions
  if (msg.player_name === state.playerName && state.character) {
    state.character.conditions = msg.conditions || [];
    updateConditionsDisplay();
  }
  if (state.allCharacters[msg.player_name]) {
    state.allCharacters[msg.player_name].conditions = msg.conditions || [];
  }

  const name = (state.allCharacters[msg.player_name] || {}).name || msg.player_name;
  addSystemChat(name + ': condition ' + (msg.applied_condition || msg.condition || '?').replace(/_/g, ' ') + (msg.downgraded ? ' (downgraded by armor)' : ''));
}

function onConditionCleared(msg) {
  if (msg.player_name === state.playerName && state.character) {
    state.character.conditions = msg.conditions || [];
    updateConditionsDisplay();
  }
  if (state.allCharacters[msg.player_name]) {
    state.allCharacters[msg.player_name].conditions = msg.conditions || [];
  }
  const name = (state.allCharacters[msg.player_name] || {}).name || msg.player_name;
  addSystemChat(name + ': condition cleared — ' + (msg.condition || '?').replace(/_/g, ' '));
}

function onExchangeEnded(msg) {
  addSystemChat('Exchange ended.');
  state.postures = {};
  const posturesPanel = document.getElementById('combat-postures-revealed');
  if (posturesPanel) posturesPanel.classList.add('hidden');

  if (msg.characters) {
    Object.entries(msg.characters).forEach(([pn, upd]) => {
      if (state.allCharacters[pn]) {
        state.allCharacters[pn].conditions = upd.conditions || [];
        state.allCharacters[pn].endurance_current = upd.endurance_current;
      }
      if (pn === state.playerName && state.character) {
        state.character.conditions = upd.conditions || [];
        state.character.endurance_current = upd.endurance_current;
        updateEnduranceBar();
        updateConditionsDisplay();
      }
      if (upd.cleared_conditions && upd.cleared_conditions.length > 0) {
        addSystemChat(pn + ': cleared ' + upd.cleared_conditions.join(', ').replace(/_/g, ' '));
      }
    });
  }
}

function onCombatEnded(msg) {
  state.inCombat = false;
  state.postures = {};
  addSystemChat('Combat has ended.');

  if (state.character) {
    state.character.endurance_current = null;
    state.character.conditions = [];
    state.character.posture = null;
  }
  Object.values(state.allCharacters).forEach(c => {
    c.endurance_current = null;
    c.conditions = [];
    c.posture = null;
  });

  const panel = document.getElementById('combat-panel');
  if (panel) panel.classList.add('hidden');
  const posturesPanel = document.getElementById('combat-postures-revealed');
  if (posturesPanel) posturesPanel.classList.add('hidden');
}

// ---------------------------------------------------------------------------
// Magic Panel — rendering and casting
// ---------------------------------------------------------------------------

function renderMagicPanel() {
  const panel = document.getElementById('magic-panel');
  if (!panel || !state.character) return;

  if (!state.character.magic_domain) {
    panel.classList.add('hidden');
    return;
  }

  panel.classList.remove('hidden');

  // Domain name and type
  const domainName = state.character.magic_domain.replace(/_/g, ' ');
  document.getElementById('magic-domain-name').textContent = domainName.charAt(0).toUpperCase() + domainName.slice(1);

  // Domain type badge (try to determine from ruleset, default to "standard")
  const domainType = getDomainType(state.character.magic_domain);
  const typeBadge = document.getElementById('magic-domain-type-badge');
  if (typeBadge) {
    typeBadge.textContent = domainType;
    typeBadge.className = 'domain-type-badge domain-type-' + domainType;
  }

  // Secondary domain
  const secWrap = document.getElementById('magic-secondary-wrap');
  if (state.character.secondary_magic_domain) {
    secWrap.classList.remove('hidden');
    const optPrimary = document.getElementById('magic-domain-opt-primary');
    const optSecondary = document.getElementById('magic-domain-opt-secondary');
    if (optPrimary) {
      optPrimary.value = state.character.magic_domain;
      optPrimary.textContent = domainName.charAt(0).toUpperCase() + domainName.slice(1) + ' (primary)';
    }
    if (optSecondary) {
      const secName = state.character.secondary_magic_domain.replace(/_/g, ' ');
      optSecondary.value = state.character.secondary_magic_domain;
      optSecondary.textContent = secName.charAt(0).toUpperCase() + secName.slice(1) + ' (secondary)';
    }
  } else {
    secWrap.classList.add('hidden');
  }

  // Pre-technique warning
  const warn = document.getElementById('magic-pre-technique-warn');
  if (warn) {
    warn.classList.toggle('hidden', state.character.magic_technique_active !== false || !state.character.magic_domain);
    // If technique is active, hide warning
    if (state.character.magic_technique_active) warn.classList.add('hidden');
  }

  // Ease Major option: only for focused domains
  const easeLabel = document.getElementById('magic-spark-ease-label');
  if (easeLabel) {
    easeLabel.classList.toggle('hidden', domainType !== 'focused');
  }

  // Disable significant/major if pre-technique
  const scopeRadios = document.querySelectorAll('input[name="magic-scope"]');
  scopeRadios.forEach(radio => {
    if (radio.value !== 'minor') {
      radio.disabled = !state.character.magic_technique_active;
    }
  });

  updateMagicDifficultyPreview();

  // Listen for scope changes to update preview
  scopeRadios.forEach(radio => {
    radio.onchange = updateMagicDifficultyPreview;
  });
  const domainSelect = document.getElementById('magic-domain-select');
  if (domainSelect) domainSelect.onchange = updateMagicDifficultyPreview;
}

function getDomainType(domainId) {
  // Try to find in ruleset's domain catalog; fall back to "standard"
  if (state.ruleset && state.ruleset.magic && state.ruleset.magic.all_domains) {
    const found = state.ruleset.magic.all_domains.find(d => d.id === domainId);
    if (found) return found.type;
  }
  // Check soul_domains / mind_domains
  if (state.ruleset && state.ruleset.magic) {
    const allDomains = (state.ruleset.magic.soul_domains || []).concat(state.ruleset.magic.mind_domains || []);
    const found = allDomains.find(d => d.id === domainId);
    if (found) return found.type;
  }
  return 'standard';
}

function getScopeDifficulty(domainType, scope) {
  if (!state.ruleset || !state.ruleset.magic || !state.ruleset.magic.domain_types) return 'Standard';
  const typeCfg = state.ruleset.magic.domain_types[domainType];
  if (!typeCfg || !typeCfg.scope_difficulties) return 'Standard';
  return typeCfg.scope_difficulties[scope] || 'Standard';
}

function updateMagicDifficultyPreview() {
  const preview = document.getElementById('magic-difficulty-preview');
  if (!preview || !state.character) return;

  const domainSelect = document.getElementById('magic-domain-select');
  const domainId = (domainSelect && !domainSelect.closest('.hidden'))
    ? domainSelect.value
    : state.character.magic_domain;

  const domainType = getDomainType(domainId);
  const scope = (document.querySelector('input[name="magic-scope"]:checked') || {}).value || 'minor';
  let difficulty = getScopeDifficulty(domainType, scope);

  // Note pre-technique penalty
  let notes = '';
  if (!state.character.magic_technique_active) {
    notes += ' (+1 step harder, pre-technique)';
  }
  if (domainId === state.character.secondary_magic_domain) {
    notes += ' (+1 step harder, secondary domain)';
  }

  preview.textContent = 'Base difficulty: ' + difficulty + notes;
}

function performCast() {
  if (!state.character || !state.character.magic_domain) return;

  const domainSelect = document.getElementById('magic-domain-select');
  const domainId = (domainSelect && !domainSelect.closest('.hidden'))
    ? domainSelect.value
    : state.character.magic_domain;

  const scope = (document.querySelector('input[name="magic-scope"]:checked') || {}).value || 'minor';
  const intent = (document.getElementById('magic-intent').value || '').trim();
  const sparkUse = (document.querySelector('input[name="magic-spark-use"]:checked') || {}).value || null;

  if (!intent) {
    addSystemChat('Describe your intent before casting.');
    return;
  }

  sendWS({
    type: 'cast',
    domain_id: domainId,
    scope,
    intent,
    spark_use: sparkUse || undefined,
  });
}

function onCastResult(msg) {
  const roll = msg.roll;
  state.rollLog.unshift({
    player_name: msg.player,
    character_name: (state.allCharacters[msg.player] || {}).name,
    ...roll,
  });
  renderPlayRollLog();

  // Update sparks
  if (msg.player === state.playerName && state.character) {
    state.character.sparks = msg.sparks_remaining;
    renderPlaySparkCounter();
  }

  const casterName = (state.allCharacters[msg.player] || {}).name || msg.player;
  const techStr = msg.technique_active ? '' : ' (pre-technique)';
  addSystemChat(casterName + ' casts ' + msg.domain_id.replace(/_/g, ' ') + ' [' + msg.scope + ']: ' + roll.outcome_label + techStr);

  // Show result box for own casts
  if (msg.player === state.playerName) {
    const resultBox = document.getElementById('play-roll-result-box');
    if (resultBox) {
      resultBox.className = 'roll-result-box ' + roll.outcome;
      resultBox.classList.remove('hidden');
      resultBox.innerHTML = buildRollResultHtml({ player: msg.player, character_name: casterName }, roll);
    }
  }
}
