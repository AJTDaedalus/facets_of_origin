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
