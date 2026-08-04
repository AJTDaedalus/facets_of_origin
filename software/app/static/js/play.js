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
  renderEnemyTracker();
  renderThreatClocks();
  populateSavingThrowSelect();
  updateRollSelectionDisplay();
  if (state.role === 'mm') {
    updateSpawnEnemySelect();
    renderMMCombatConsole();
    populateContestedSelects();
  }
  renderPlayerPickers();
  updateCombatStatusBanner();
}

/**
 * Fill every "which player?" control from live session state.
 *
 * These were all free-text inputs. A typo produced no error at all — the server
 * looks the name up, finds nothing, and returns silently — so an MM could award
 * Sparks into the void for a whole session without noticing.
 */
function renderPlayerPickers() {
  const players = Object.keys(state.allCharacters).sort();
  document.querySelectorAll('select[data-player-picker]').forEach(sel => {
    const previous = sel.value;
    const allowBlank = sel.dataset.playerPicker === 'optional';
    sel.innerHTML = (allowBlank ? '<option value="">-- select player --</option>' : '')
      + players.map(pn => {
        const c = state.allCharacters[pn];
        const label = c && c.name && c.name !== pn ? `${c.name} (${pn})` : pn;
        return `<option value="${escapeHtml(pn)}">${escapeHtml(label)}</option>`;
      }).join('');
    if (players.includes(previous)) sel.value = previous;
    if (!players.length) sel.innerHTML = '<option value="">-- no characters yet --</option>';
  });
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
      // Always signed: a bare "0" sitting under the rating reads as a second value.
      const modStr = mod >= 0 ? '+' + mod : '' + mod;

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
    // data-marks feeds the mobile layout, where the Progress column is hidden
    // and the marks are re-shown under the skill name instead.
    tr.innerHTML = `
      <td data-marks="${dots}">${skill.name}${isPrimary ? '' : ' <span style="color:var(--text-dim);font-size:10px" title="Outside your primary Facet \u2014 2 SP to advance">\u25CF</span>'}</td>
      <td><span class="rank-badge rank-${skillState.rank}">${skillState.rank}</span></td>
      <td class="marks-dots" title="${skillState.marks}/${marksNeeded} marks toward the next rank">${dots}</td>
      <td><button class="btn-roll-skill" onclick="rollSkill('${skill.id}')" title="Roll ${skill.name}">Roll</button></td>
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
  updateRollSelectionDisplay();
}

function rollSkill(skillId) {
  if (!state.ruleset) return;
  const skill = state.ruleset.skills.find(s => s.id === skillId);
  if (!skill) return;
  state.selectedSkillId = skillId;
  state.selectedAttributeId = skill.attribute;
  renderPlayAttributeGrid(state.character);
  updateRollSelectionDisplay();
  performRoll();
}

/**
 * Show what is about to be rolled, with the modifiers already worked out.
 *
 * The Roll button used to sit disabled behind a grey "-- click an attribute
 * above --" with nothing indicating the two were connected.
 */
function updateRollSelectionDisplay() {
  const display = document.getElementById('play-roll-selection');
  const btn = document.getElementById('play-roll-btn');
  if (!display) return;

  if (!state.selectedAttributeId) {
    display.classList.remove('roll-selection-active');
    display.textContent = 'Pick an Attribute above, or hit Roll on any skill.';
    if (btn) btn.disabled = true;
    return;
  }

  const char = state.character || {};
  const attr = (state.ruleset.minor_attributes || []).find(m => m.id === state.selectedAttributeId);
  const rating = (char.attributes || {})[state.selectedAttributeId] || 2;
  const ratingDef = (state.ruleset.attribute_ratings || []).find(r => r.rating === rating);
  const attrMod = ratingDef ? ratingDef.modifier : 0;

  const parts = [`${attr ? attr.name : state.selectedAttributeId} ${attrMod >= 0 ? '+' : ''}${attrMod}`];
  if (state.selectedSkillId) {
    const skill = (state.ruleset.skills || []).find(s => s.id === state.selectedSkillId);
    const skillState = (char.skills || {})[state.selectedSkillId] || { rank: 'novice' };
    const rankDef = (state.ruleset.advancement && state.ruleset.advancement.skill_ranks || [])
      .find(r => r.id === skillState.rank);
    const skillMod = rankDef ? rankDef.modifier : 0;
    parts.push(`${skill ? skill.name : state.selectedSkillId} +${skillMod}`);
  }

  display.classList.add('roll-selection-active');
  display.innerHTML = `Rolling <strong>2d6 + ${parts.join(' + ')}</strong>`;
  if (btn) btn.disabled = false;
}

function performRoll() {
  if (!state.selectedAttributeId) {
    addSystemChat('Select an attribute to roll.');
    return;
  }

  const diffEl = document.getElementById('play-difficulty-select');
  const descEl = document.getElementById('play-roll-description');
  const hazardEl = document.getElementById('play-roll-hazard-type');
  const fieldEl = document.getElementById('play-roll-knowledge-field');
  const difficulty = diffEl ? diffEl.value : 'Standard';
  const description = descEl ? descEl.value.slice(0, 200) : '';
  // Optional (B4 Q1, TD-8): absent unless the player names a hardship/field,
  // in which case Acclimated/Field of Mastery may auto-apply a step.
  const hazardType = hazardEl && hazardEl.value.trim() ? hazardEl.value.trim() : null;
  const knowledgeField = fieldEl && fieldEl.value.trim() ? fieldEl.value.trim() : null;

  sendWS({
    type: 'roll',
    attribute_id: state.selectedAttributeId,
    skill_id: state.selectedSkillId || null,
    difficulty,
    sparks_spent: state.sparksToSpend,
    description,
    hazard_type: hazardType,
    knowledge_field: knowledgeField,
  });

  state.sparksToSpend = 0;
}

function onRollResult(msg) {
  const roll = msg.roll;
  state.rollLog.unshift({ player_name: msg.player, character_name: msg.character_name, ...roll });
  renderPlayRollLog();
  showRollResultBox(msg, roll);

  if (msg.player === state.playerName && state.character) {
    state.character.sparks = msg.character_sparks_remaining;
    renderPlaySparkCounter();
  }

  checkGracefulFailPrompt(msg);
}

/**
 * Render the big result panel. Extracted because Roll, Strike, Cast, and Save
 * each had their own copy of the same six lines.
 */
function showRollResultBox(msg, roll) {
  const resultBox = document.getElementById('play-roll-result-box');
  if (!resultBox || !roll) return;
  resultBox.className = 'roll-result-box ' + roll.outcome;
  resultBox.classList.remove('hidden');
  resultBox.innerHTML = buildRollResultHtml(msg, roll);
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

  // B4 Q1 (TD-10, DESIGN §2.7): auto-apply is only legible because the
  // banner shows both moves — the MM's declared label AND the Technique
  // that stepped it. When no Technique fired, msg.technique_step is absent
  // (or null) and this renders nothing, leaving the banner unchanged.
  const stepHtml = msg.technique_step
    ? `<div class="technique-step-banner" style="font-size:0.8rem;color:var(--gold);margin-bottom:4px;">${escapeHtml(String(msg.technique_step.from))} (MM) → ${escapeHtml(String(msg.technique_step.to))} (${escapeHtml(String(msg.technique_step.technique_name))})</div>`
    : '';

  return `
    <div style="font-size:0.8rem;color:var(--text-dim);margin-bottom:4px;">${whoStr} rolled ${roll.attribute_id}${roll.skill_id ? ' + ' + roll.skill_id : ''}${roll.difficulty !== 'Standard' ? ' [' + roll.difficulty + ']' : ''}${roll.sparks_spent > 0 ? ' x' + roll.sparks_spent : ''}</div>
    ${stepHtml}
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

  const characters = Object.values(state.allCharacters);
  if (characters.length === 0) {
    ul.innerHTML = state.role === 'mm'
      ? '<li class="empty-state">No characters yet. Generate an invite link below and send it to a player.</li>'
      : '<li class="empty-state">No characters yet.</li>';
    return;
  }

  characters.forEach(char => {
    const li = document.createElement('li');
    const isOnline = state.connectedPlayers.has(char.player_name);
    const inCombat = char.endurance_current !== null && char.endurance_current !== undefined;

    // Sparks were previously visible only on your own sheet, so the MM ran the
    // Spark economy without being able to see anyone's balance.
    const sparkChip = `<span class="spark-chip" title="Sparks">✦ ${char.sparks != null ? char.sparks : 0}</span>`;
    const combatChip = inCombat
      ? `<span class="status-chip" title="Endurance">${char.endurance_current}/${char.endurance_max || '?'}</span>`
      : '';
    const condChip = (char.conditions || []).length
      ? `<span class="status-chip status-chip-warn" title="${escapeHtml((char.conditions || []).map(prettyCondition).join(', '))}">${char.conditions.length} cond</span>`
      : '';

    li.innerHTML = `
      <span class="${isOnline ? 'player-online' : ''}">${escapeHtml(char.name || char.player_name)}${
        char.name !== char.player_name ? ' <small style="color:var(--text-dim)">' + escapeHtml(char.player_name) + '</small>' : ''}</span>
      <span class="player-chips">
        ${sparkChip}${combatChip}${condChip}
        <span class="facet-badge facet-${escapeHtml(char.primary_facet)}">${escapeHtml(char.primary_facet)}</span>
      </span>`;
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
  const playerName = document.getElementById('play-mm-spark-player').value;
  const reasonEl = document.getElementById('play-mm-spark-reason');
  const reason = reasonEl.value.trim() || 'MM award';
  if (!playerName) { notify('Pick a player to award.', 'warn'); return; }
  sendWS({ type: 'spark_earn', player_name: playerName, reason });
  reasonEl.value = '';
}

function nominateForSpark() {
  const playerName = document.getElementById('play-peer-spark-player').value;
  if (!playerName) { notify('Pick who you are nominating.', 'warn'); return; }
  if (playerName === state.playerName) { notify('Nominate someone else.', 'warn'); return; }
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
  // MM gets full controls + phase markers; players get a read-only Resolve view.
  const isMM = state.role === 'mm';
  const container = document.getElementById(isMM ? 'play-enemy-tracker' : 'play-player-enemy-tracker');
  if (!container) return;

  const keys = Object.keys(state.activeEnemies);
  if (keys.length === 0) {
    container.innerHTML = '<div style="font-size:12px;color:var(--text-dim);">No active enemies.</div>';
    return;
  }

  container.innerHTML = Object.entries(state.activeEnemies).map(([key, enemy]) =>
    renderEnemyCard(key, enemy, { mmControls: isMM, showPhases: isMM })
  ).join('');
}

/**
 * Spawn N copies of a library enemy.
 *
 * A Mook swarm is the most common spawn there is, and it used to cost one
 * round-trip through a two-field form per body. Copies past the first get a
 * numbered instance name so the tracker keys stay distinguishable.
 */
function spawnEnemyFromLibrary() {
  const enemyId = document.getElementById('play-spawn-enemy-select').value;
  const baseName = document.getElementById('play-spawn-instance-name').value.trim();
  const countEl = document.getElementById('play-spawn-count');
  const count = Math.max(1, Math.min(20, parseInt(countEl && countEl.value) || 1));
  if (!enemyId) { notify('Pick an enemy from the library first.', 'warn'); return; }

  const libraryName = (state.enemyLibrary[enemyId] || {}).name || enemyId;
  const stem = baseName || libraryName;

  for (let i = 0; i < count; i++) {
    const instanceName = count > 1 ? `${stem} ${i + 1}` : (baseName || undefined);
    sendWS({ type: 'spawn_enemy', enemy_id: enemyId, instance_name: instanceName });
  }

  const nameEl = document.getElementById('play-spawn-instance-name');
  if (nameEl) nameEl.value = '';
  if (countEl) countEl.value = '1';
}

/**
 * Apply a Strike outcome to an enemy. The engine decides the cost.
 *
 * This used to compute the depletion here and send a raw `resolve_current`,
 * which meant the D1 rule (10+ takes 2, 7-9 takes 1) lived in this file and in
 * the simulator but nowhere on the server. `enemy_strike` sends the outcome and
 * lets combat.apply_resolve_damage decide — one implementation, and it also
 * handles the Mook case, where there is no Resolve pool to subtract from.
 */
function enemyStrikeOutcome(trackerKey, outcome) {
  sendWS({ type: 'enemy_strike', tracker_key: trackerKey, outcome });
}

/**
 * TD-14 (B4 Q3): commits a Final Blow removal offered by a Strike. This is
 * the MM confirmation DESIGN §4 requires before an actor is deleted from
 * the encounter — auto-apply covers difficulty steps only, never this.
 */
function confirmFinalBlow(playerName, trackerKey, offerId) {
  // The offer id names exactly which Strike's offer this commits, so a stale
  // toast left on screen by an earlier exchange cannot remove an enemy off the
  // back of a later, failed Strike (TODO T12).
  sendWS({
    type: 'final_blow_confirm', player: playerName,
    tracker_key: trackerKey, offer_id: offerId,
  });
}

/** Manual correction — an undo, not a rule. Stays on `enemy_update`. */
function enemyAdjustResolve(trackerKey, delta) {
  const enemy = state.activeEnemies[trackerKey];
  if (!enemy) return;
  const current = enemy.resolve_current !== null && enemy.resolve_current !== undefined
    ? enemy.resolve_current : enemy.resolve;
  const next = Math.max(0, Math.min(enemy.resolve || 0, current + delta));
  sendWS({ type: 'enemy_update', tracker_key: trackerKey, resolve_current: next });
}

async function enemyAddCondition(trackerKey) {
  const cond = await promptDialog('Add a Condition', 'e.g. off balance');
  if (!cond) return;
  sendWS({ type: 'enemy_update', tracker_key: trackerKey, add_condition: cond });
}

function enemyRemoveCondition(trackerKey, condition) {
  sendWS({ type: 'enemy_update', tracker_key: trackerKey, remove_condition: condition });
}

async function removeEnemy(trackerKey) {
  const enemy = state.activeEnemies[trackerKey];
  const label = enemy ? (enemy.name || trackerKey) : trackerKey;
  const ok = await confirmDialog('Remove from the fight?', `${label} leaves the tracker.`, 'Remove');
  if (!ok) return;
  sendWS({ type: 'remove_enemy', tracker_key: trackerKey });
}

function onEnemySpawned(msg) {
  state.activeEnemies[msg.tracker_key] = { ...msg.enemy, tr: msg.tr };
  renderEnemyTracker();
  updateSpawnEnemySelect();
  populateTargetSelects();  // a new enemy is immediately Strikeable
}

function onEnemyUpdated(msg) {
  const enemy = state.activeEnemies[msg.tracker_key];
  if (!enemy) return;

  const name = enemy.name || msg.tracker_key;
  enemy.resolve_current = msg.resolve_current;
  enemy.conditions = msg.conditions;

  // `defeated` comes from the engine — for a Mook that means one Strike landed
  // hard enough, for anyone else that Resolve reached 0. The client no longer
  // infers either.
  if (msg.defeated) {
    delete state.activeEnemies[msg.tracker_key];
    // TD-14/TD-13 (B4 Q3): a Final Blow removal is a licensed override, not
    // Resolve depletion — `cause` distinguishes it in the log from an
    // ordinary Resolve-0 defeat, same as it does in the transcript.
    if (msg.cause === 'final_blow') {
      addSystemChat(`${name} is removed from the conflict — The Final Blow.`);
      notify(`${name} is removed from the conflict — The Final Blow.`, 'success');
    } else {
      addSystemChat(`${name} is defeated.`);
      notify(`${name} is defeated.`, 'success');
    }
  } else if (msg.depletion) {
    addSystemChat(`${name}: −${msg.depletion} Resolve (now ${msg.resolve_current}).`);
  }

  renderEnemyTracker();
  populateTargetSelects();
}

function onEnemyRemoved(msg) {
  delete state.activeEnemies[msg.tracker_key];
  renderEnemyTracker();
  populateTargetSelects();
}

function onEnemyPhaseChange(msg) {
  const enemy = state.activeEnemies[msg.enemy_id];
  const name = enemy ? enemy.name : msg.enemy_id;
  const text = name + ' — Phase ' + (msg.phase_index + 1) + (msg.description ? ': ' + msg.description : '');
  addSystemChat('⚡ ' + text);
  // A Boss changing phase rewrites how the fight works; it must not scroll past
  // in the chat log unnoticed.
  notify(text, 'gold', { duration: 10000 });
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
// Threat Clocks (PHB III.2, D4) — visible to every player; MM-only controls
// ---------------------------------------------------------------------------
function renderThreatClocks() {
  const isMM = state.role === 'mm';
  const container = document.getElementById(isMM ? 'play-clock-tracker' : 'play-player-clock-tracker');
  if (!container) return;

  const clocks = Object.values(state.threatClocks);
  if (clocks.length === 0) {
    container.innerHTML = '<div style="font-size:12px;color:var(--text-dim);">No active Threat Clocks.</div>';
    return;
  }

  container.innerHTML = clocks.map((clock) => renderThreatClockCard(clock, { mmControls: isMM })).join('');
}

function createClock() {
  const nameEl = document.getElementById('play-clock-name');
  const segEl = document.getElementById('play-clock-segments');
  const name = nameEl ? nameEl.value.trim() : '';
  if (!name) { notify('Name the clock so the table knows what it tracks.', 'warn'); focusElement('play-clock-name'); return; }

  const msg = { type: 'clock_create', name };
  // Segment count is a real dial on the server; the UI always took the default.
  const segments = parseInt(segEl && segEl.value);
  if (segments > 0) msg.segments = segments;

  sendWS(msg);
  if (nameEl) nameEl.value = '';
}

async function deleteClock(clockId) {
  const clock = state.threatClocks[clockId];
  const ok = await confirmDialog(
    'Remove this clock?',
    `"${clock ? clock.name : clockId}" disappears from everyone's screen.`,
    'Remove');
  if (!ok) return;
  sendWS({ type: 'clock_delete', clock_id: clockId });
}

function onClockDeleted(msg) {
  delete state.threatClocks[msg.clock_id];
  renderThreatClocks();
}

function clockAdvance(clockId, outcomeTier) {
  sendWS({ type: 'clock_advance', clock_id: clockId, outcome_tier: outcomeTier });
}

function clockWindBack(clockId) {
  sendWS({ type: 'clock_wind_back', clock_id: clockId });
}

function onClockCreated(msg) {
  state.threatClocks[msg.clock.id] = msg.clock;
  renderThreatClocks();
}

function onClockAdvanced(msg) {
  state.threatClocks[msg.clock.id] = msg.clock;
  renderThreatClocks();
}

function onClockWoundBack(msg) {
  state.threatClocks[msg.clock.id] = msg.clock;
  renderThreatClocks();
}

function onClockFill(msg) {
  state.threatClocks[msg.clock.id] = msg.clock;
  addSystemChat(`⏱ ${msg.clock.name} fills — the hazard strikes!`);
  renderThreatClocks();
}

// ---------------------------------------------------------------------------
// Combat controls (MM)
// ---------------------------------------------------------------------------
function startCombat() {
  sendWS({ type: 'combat_start' });
}

/**
 * The weapon the character has declared for this exchange, as the fields the
 * server's Technique-step matcher reads.
 *
 * B7: a Technique's step applies on every roll the MM prices, so Maneuver and
 * Support have to carry the same weapon the Strike form declared — otherwise
 * Mordai Strikes with his sword and gets Easy, Maneuvers with the same sword and
 * stays Standard, which is the inconsistency B7 exists to remove. The weapon in
 * your hand does not change between two actions in one exchange, so this reads
 * one control rather than duplicating a picker onto every form.
 */
function declaredWeaponFields() {
  const categoryEl = document.getElementById('strike-weapon-category');
  const typeEl = document.getElementById('strike-weapon-type');
  return {
    weapon_category: categoryEl && categoryEl.value ? categoryEl.value : null,
    weapon_type: typeEl && typeEl.value ? typeEl.value : null,
  };
}

async function endCombat() {
  const ok = await confirmDialog(
    'End combat?',
    'Endurance, Conditions, and Postures are cleared for every character, and the enemy tracker is emptied.',
    'End Combat');
  if (!ok) return;
  sendWS({ type: 'combat_end' });
  // The server does not touch active_enemies on combat_end, so this client-side
  // clear is the only thing that empties the tracker the dialog just promised
  // to empty. Do not move it.
  state.activeEnemies = {};
  renderEnemyTracker();
}

/**
 * B6: the scene is a published boundary — armor's downgrade budget refreshes at
 * it, and it is deliberately *not* the same event as End Combat, because a scene
 * can hold two fights or none. It does not clear the enemy tracker; ending a
 * scene is not ending a fight.
 */
async function endScene() {
  const ok = await confirmDialog(
    'End the scene?',
    "Armor downgrade budgets refresh for every character. Use this between scenes, not between fights in the same scene — two fights in one scene share one budget.",
    'End Scene');
  if (!ok) return;
  sendWS({ type: 'scene_end' });
}

function endExchange() {
  sendWS({ type: 'end_exchange' });
}

function revealPostures() {
  sendWS({ type: 'reveal_postures' });
}

// ---------------------------------------------------------------------------
// MM Combat Console
//
// Enemies never roll (PHB III.3) — the MM declares an enemy's attack by applying
// the incoming Condition and the PC reacts to reduce it. `apply_condition` was
// therefore the only path by which an enemy attack could land, and it had no
// control anywhere in the UI: the enemy half of every fight was un-driveable.
// This console is that missing half.
// ---------------------------------------------------------------------------

function renderMMCombatConsole() {
  if (state.role !== 'mm') return;
  const container = document.getElementById('mm-combat-roster');
  if (!container) return;

  const entries = Object.entries(state.allCharacters);
  if (entries.length === 0) {
    container.innerHTML = '<div class="empty-state">No characters in this session yet.</div>';
    return;
  }

  container.innerHTML = entries.map(([pn, char]) => renderMMCombatantRow(pn, char)).join('');
}

function renderMMCombatantRow(playerName, char) {
  const inCombat = char.endurance_current !== null && char.endurance_current !== undefined;
  const max = char.endurance_max || 0;
  const current = inCombat ? char.endurance_current : max;
  const pct = max > 0 ? Math.round((current / max) * 100) : 0;
  const fillClass = 'endurance-fill' + (pct <= 25 ? ' critical' : pct <= 50 ? ' low' : '');

  const conditions = char.conditions || [];
  const condHtml = conditions.length
    ? conditions.map(c =>
        `<button class="condition-badge condition-tier${getConditionTier(c)} condition-clearable"
                 title="Clear ${escapeHtml(prettyCondition(c))}"
                 onclick="mmClearCondition('${escapeHtml(playerName)}','${escapeHtml(c)}')"
        >${escapeHtml(prettyCondition(c))} ×</button>`).join(' ')
    : '<span style="color:var(--text-dim);font-size:11px;">no Conditions</span>';

  const posture = char.posture || 'measured';
  const armorBudget = char.armor && char.armor !== 'none'
    ? `<span class="armor-chip" title="Per-scene downgrade charges remaining">${escapeHtml(char.armor)} armor:
       ${char.armor_downgrades_remaining != null ? char.armor_downgrades_remaining : '-'} left</span>`
    : '';

  return `
    <div class="mm-combatant">
      <div class="mm-combatant-head">
        <strong>${escapeHtml(char.name || playerName)}</strong>
        <span class="posture-badge posture-${escapeHtml(posture)}">${escapeHtml(posture)}</span>
        <span class="spark-chip" title="Sparks available">✦ ${char.sparks != null ? char.sparks : 0}</span>
        ${armorBudget}
      </div>
      ${inCombat ? `
        <div class="endurance-bar"><div class="${fillClass}" style="width:${pct}%;"></div></div>
        <div style="font-size:11px;color:var(--text-dim);">Endurance ${current}/${max}</div>` : ''}
      <div class="mm-conditions">${condHtml}</div>
      <div class="mm-attack-row">
        <label class="mm-attack-label">Enemy attack lands as</label>
        <select class="mm-attack-tier" data-player="${escapeHtml(playerName)}">
          ${enemyTierConditionOptions()}
        </select>
        <label class="checkbox-inline" title="Tick when the target's Dodge or Parry partially succeeded (7-9).
Armor and a partial reaction never stack — the engine applies whichever reduction is greater.">
          <input type="checkbox" class="mm-attack-reacted" data-player="${escapeHtml(playerName)}"> reaction softened it
        </label>
        <button class="btn btn-primary btn-sm" onclick="mmApplyConditionFor('${escapeHtml(playerName)}')">Land Hit</button>
      </div>
    </div>`;
}

/**
 * Condition options grouped by tier, straight from the ruleset. The MM sends the
 * RAW incoming Condition — armor and reaction reduction are the engine's job
 * (websocket.py `_reduce_incoming_condition`), never the MM's arithmetic.
 */
function enemyTierConditionOptions() {
  const conds = (state.ruleset && state.ruleset.combat && state.ruleset.combat.conditions) || {};
  const group = (label, list) => {
    if (!list || !list.length) return '';
    return `<optgroup label="${label}">` + list.map(c =>
      `<option value="${escapeHtml(c.id)}" title="${escapeHtml(c.description || '')}">${escapeHtml(prettyCondition(c.id))}</option>`
    ).join('') + '</optgroup>';
  };
  return group('Tier 1 — Mook attack', conds.tier1)
       + group('Tier 2 — Named / Boss attack', conds.tier2)
       + group('Tier 3', conds.tier3);
}

function mmApplyConditionFor(playerName) {
  const tierSel = document.querySelector(`.mm-attack-tier[data-player="${cssEscape(playerName)}"]`);
  const reactedBox = document.querySelector(`.mm-attack-reacted[data-player="${cssEscape(playerName)}"]`);
  const condition = tierSel ? tierSel.value : '';
  if (!condition) { notify('Pick the incoming Condition first.', 'warn'); return; }

  sendWS({
    type: 'apply_condition',
    player_name: playerName,
    condition,
    reaction_downgraded: !!(reactedBox && reactedBox.checked),
  });
  if (reactedBox) reactedBox.checked = false;
}

function mmClearCondition(playerName, condition) {
  sendWS({ type: 'clear_condition', player_name: playerName, condition });
}

/** Minimal CSS.escape shim — player names are free text and can contain quotes. */
function cssEscape(value) {
  if (window.CSS && CSS.escape) return CSS.escape(value);
  return String(value).replace(/["\\\]]/g, '\\$&');
}

/**
 * A single line saying what the table is waiting for. Nothing previously showed
 * which part of the exchange was in progress, so "have we revealed yet?" was a
 * question that had to be asked out loud every round.
 */
function updateCombatStatusBanner() {
  const banner = document.getElementById('combat-status-banner');
  if (!banner) return;

  if (!state.inCombat) {
    banner.classList.add('hidden');
    return;
  }
  banner.classList.remove('hidden');

  const revealed = Object.keys(state.postures || {}).length > 0;
  const declared = Object.values(state.allCharacters)
    .filter(c => c.endurance_current !== null && c.endurance_current !== undefined).length;

  banner.textContent = revealed
    ? `Postures revealed — take actions and reactions, then End Exchange. (${declared} in the fight)`
    : `Combat: declare Postures. The MM reveals them when everyone has chosen. (${declared} in the fight)`;
}

// ---------------------------------------------------------------------------
// Combat Panel — rendering and state
// ---------------------------------------------------------------------------

function renderCombatPanel() {
  const panel = document.getElementById('combat-panel');
  if (!panel || !state.character) return;

  panel.classList.remove('hidden');

  // Out of combat the panel stays visible in a read-only "readiness" mode.
  // Hiding it outright meant a player could not check their Endurance pool,
  // armor budget, or reaction costs while deciding whether to pick a fight.
  const live = !!state.inCombat;
  panel.classList.toggle('combat-idle', !live);
  const idleNote = document.getElementById('combat-idle-note');
  if (idleNote) idleNote.classList.toggle('hidden', live);
  document.querySelectorAll('#combat-panel .combat-live-only').forEach(el => {
    el.classList.toggle('hidden', !live);
  });

  updateEnduranceBar();
  updatePostureBadge(state.character.posture || 'measured');
  updateConditionsDisplay();
  updateArmorDisplay();
  populateCombatSelects();
  updateReactCostPreview();
  updateCombatStatusBanner();
}

/**
 * Armor is a per-scene downgrade budget, not a flat reduction, so the number of
 * charges left is a decision input every exchange. It was not shown anywhere.
 */
function updateArmorDisplay() {
  const el = document.getElementById('combat-armor-display');
  const char = state.character;
  if (!el || !char) return;

  if (!char.armor || char.armor === 'none') {
    el.innerHTML = '<span style="color:var(--text-dim);">No armor</span>';
    return;
  }
  const remaining = char.armor_downgrades_remaining;
  const budget = combatArmorBudget(char.armor);
  el.innerHTML = `<span class="armor-chip">${escapeHtml(char.armor)} armor</span>
    <span style="color:var(--text-dim);">${remaining != null ? remaining : budget}/${budget}
    downgrade${budget === 1 ? '' : 's'} left this scene</span>`;
}

/** Per-scene downgrade charges, read from `combat.armor.<type>.downgrades_per_scene`. */
function combatArmorBudget(armor) {
  const cfg = state.ruleset && state.ruleset.combat && state.ruleset.combat.armor;
  const entry = cfg && cfg[armor];
  if (entry && entry.downgrades_per_scene != null) return entry.downgrades_per_scene;
  return armor === 'heavy' ? 4 : armor === 'light' ? 2 : 0;
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

  // Support targets: allies only, rebuilt every render so someone joining
  // mid-fight becomes selectable.
  const supportTarget = document.getElementById('support-target');
  if (supportTarget) {
    const previous = supportTarget.value;
    supportTarget.innerHTML = '<option value="">-- select ally --</option>'
      + Object.keys(state.allCharacters)
          .filter(pn => pn !== state.playerName)
          .map(pn => `<option value="${escapeHtml(pn)}">${escapeHtml(state.allCharacters[pn].name || pn)}</option>`)
          .join('');
    supportTarget.value = previous;
  }

  populateTargetSelects();
}

/**
 * Strike and Maneuver targets were free-text inputs while every legal target —
 * spawned enemies and other characters — was already sitting in client state.
 * A dropdown also keeps the name matching the tracker key the MM sees.
 */
function populateTargetSelects() {
  const enemyOpts = Object.entries(state.activeEnemies).map(([key, e]) => {
    const res = enemyResolveDisplay(e);
    const detail = res ? `Resolve ${res.current}/${res.max}` : 'Mook';
    return `<option value="${escapeHtml(e.name || key)}">${escapeHtml(e.name || key)} — ${detail}</option>`;
  }).join('');

  const charOpts = Object.entries(state.allCharacters)
    .filter(([pn]) => pn !== state.playerName)
    .map(([pn, c]) => `<option value="${escapeHtml(c.name || pn)}">${escapeHtml(c.name || pn)}</option>`)
    .join('');

  ['strike-target', 'maneuver-target'].forEach(id => {
    const sel = document.getElementById(id);
    if (!sel) return;
    const previous = sel.value;
    sel.innerHTML = '<option value="">-- select target --</option>'
      + (enemyOpts ? `<optgroup label="Enemies">${enemyOpts}</optgroup>` : '')
      + (charOpts ? `<optgroup label="Characters">${charOpts}</optgroup>` : '');
    if (!enemyOpts && !charOpts) {
      sel.innerHTML = '<option value="">-- no targets on the board --</option>';
    }
    sel.value = previous;
  });
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

/**
 * TD-7 (B4 Q1 side benefit, IV.1:13-19): the weapon category picker sets the
 * Strike attribute *as a default only* — the player can still override it,
 * because the engine stays permissive on which attribute/skill a Strike uses
 * (INV-8) and the picker must never become a gate on that.
 */
function onStrikeWeaponCategoryChange() {
  const catEl = document.getElementById('strike-weapon-category');
  const attrEl = document.getElementById('strike-attribute');
  if (!catEl || !attrEl) return;
  const category = catEl.value;
  const categories = (state.ruleset && state.ruleset.equipment && state.ruleset.equipment.weapon_categories) || {};
  const def = categories[category];
  if (def && def.attributes && def.attributes.length) {
    attrEl.value = def.attributes[0];
  }
}

function performStrike() {
  const target = (document.getElementById('strike-target').value || '').trim();
  const attrId = document.getElementById('strike-attribute').value;
  const skillId = document.getElementById('strike-skill').value || null;
  const difficulty = document.getElementById('strike-difficulty').value;
  const press = document.getElementById('strike-press').checked;
  const weaponCategoryEl = document.getElementById('strike-weapon-category');
  const weaponCategory = weaponCategoryEl && weaponCategoryEl.value ? weaponCategoryEl.value : null;
  // TD-18 (DESIGN §8): weapon_type is the orthogonal, fictional vocabulary
  // (blades/blunt/polearms/unarmed) Weapon Mastery masters — separate from
  // weapon_category above, which only defaults the attribute picker.
  const weaponTypeEl = document.getElementById('strike-weapon-type');
  const weaponType = weaponTypeEl && weaponTypeEl.value ? weaponTypeEl.value : null;
  // TD-14 (B4 Q3): a player toggle, not an auto-apply — Final Blow deletes
  // an actor from the encounter, so unlike a difficulty step it always
  // needs the player's explicit ask and the MM's explicit confirmation
  // (DESIGN §4). The server enforces once-per-session, Combat-roll, and
  // Spark-spent; this checkbox only carries the player's declaration.
  const finalBlowEl = document.getElementById('strike-final-blow');
  const finalBlow = !!(finalBlowEl && finalBlowEl.checked);

  if (!target) { notify('Choose a target.', 'warn'); focusElement('strike-target'); return; }
  if (press && (state.character.endurance_current || 0) < 1) {
    notify('No Endurance left to Press.', 'warn');
    return;
  }
  if (finalBlow && state.sparksToSpend < 1) {
    notify('The Final Blow requires spending a Spark on this roll.', 'warn');
    return;
  }

  sendWS({
    type: 'strike',
    target,
    attribute_id: attrId,
    skill_id: skillId,
    difficulty,
    press,
    sparks_spent: state.sparksToSpend,
    weapon_category: weaponCategory,
    weapon_type: weaponType,
    final_blow: finalBlow,
  });
  if (finalBlowEl) finalBlowEl.checked = false;
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
    ...declaredWeaponFields(),
  });
}

function performManeuver() {
  const target = (document.getElementById('maneuver-target').value || '').trim();
  const attrId = document.getElementById('maneuver-attribute').value;
  const skillId = document.getElementById('maneuver-skill').value || null;
  const description = (document.getElementById('maneuver-description').value || '').trim();

  if (!target) { notify('Choose a target.', 'warn'); focusElement('maneuver-target'); return; }
  if (!description) {
    notify('Describe what you are trying to do — a Maneuver is defined by its fiction.', 'warn');
    focusElement('maneuver-description');
    return;
  }

  sendWS({
    type: 'maneuver',
    target,
    attribute_id: attrId,
    skill_id: skillId,
    difficulty: 'Standard',
    ...declaredWeaponFields(),
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
  renderMMCombatConsole();
  updateCombatStatusBanner();
  notify('Combat has begun — declare your Posture.', 'gold');
}

function onPostureDeclared(msg) {
  if (state.character) {
    state.character.posture = msg.posture;
    updatePostureBadge(msg.posture);
    updateReactCostPreview();
  }
  addSystemChat('Posture declared: ' + msg.posture);
  notify('Posture set to ' + msg.posture + '.', 'success', { duration: 2500 });
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
  renderMMCombatConsole();
  updateCombatStatusBanner();
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

  checkGracefulFailPrompt({ ...msg, player: msg.attacker, character_name: attackerName, roll });
  renderMMCombatConsole();

  // Show result box for own strikes
  if (msg.attacker === state.playerName) {
    showRollResultBox({ player: msg.attacker, character_name: attackerName, technique_step: msg.technique_step }, roll);
  }

  // Prompt the MM to apply the outcome. How much it costs is the engine's
  // business — this sends the outcome, not a number.
  //
  // The prompt used to say "apply it on the enemy tracker" and leave the MM to
  // find the row. A subagent playtest (playtest/08_npc_variance, F4) showed the
  // real cost of that gap: a player rolled a full success on a Mook, said "that
  // one should be gone", and it was still standing in the engine. Between the
  // roll and the MM's click, the table's model of the fight and the engine's
  // state disagree. When the target is a tracked enemy, apply it from here.
  if (state.role === 'mm' && msg.target && roll.outcome !== 'failure') {
    const tracked = state.activeEnemies && state.activeEnemies[msg.target];
    const headline = `${attackerName} hits ${msg.target} — ${roll.outcome_label}.`;
    if (tracked) {
      notify(headline, 'info', {
        duration: 12000,
        key: 'apply-strike',
        action: 'Apply',
        onAction: () => enemyStrikeOutcome(msg.target, roll.outcome),
      });
    } else {
      // Not in the tracker — a PvP Strike or an untracked target. Nothing to apply.
      notify(`${headline} Apply it on the enemy tracker.`, 'info', { duration: 7000 });
    }
  }

  // TD-14 (B4 Q3): the server only *offers* Final Blow on the roll — the
  // removal never touches an enemy until the MM explicitly confirms it.
  if (state.role === 'mm' && msg.final_blow_available && msg.target) {
    const tracked = state.activeEnemies && state.activeEnemies[msg.target];
    if (tracked) {
      notify(`${attackerName} lands The Final Blow on ${msg.target} — confirm the removal?`, 'info', {
        duration: 20000,
        key: 'confirm-final-blow',
        action: 'Confirm Final Blow',
        onAction: () => confirmFinalBlow(msg.attacker, msg.target, msg.final_blow_offer_id),
      });
    } else {
      notify(`${attackerName} lands The Final Blow, but ${msg.target} is not in the enemy tracker.`, 'info', { duration: 7000 });
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
  // B4 Q1 (TD-10): reactions have no roll-result box, so the banner text
  // goes in the chat line instead — same two moves, same visibility.
  const stepStr = msg.technique_step
    ? ' [' + msg.technique_step.from + ' (MM) → ' + msg.technique_step.to + ' (' + msg.technique_step.technique_name + ')]'
    : '';
  addSystemChat(reactorName + ' reacts: ' + msg.reaction + ' (cost ' + msg.endurance_cost + ' End)' + rollStr + stepStr);
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
  // Server sends `player` + `all_conditions` (websocket.py _handle_apply_condition).
  const playerName = msg.player;
  const conditions = msg.all_conditions || [];

  if (playerName === state.playerName && state.character) {
    state.character.conditions = conditions;
    updateConditionsDisplay();
  }
  if (state.allCharacters[playerName]) {
    state.allCharacters[playerName].conditions = conditions;
  }
  renderMMCombatConsole();

  const name = (state.allCharacters[playerName] || {}).name || playerName;
  if (!msg.condition) {
    // Reduced away entirely — armor or a partial reaction ate the whole hit.
    const by = msg.armor_absorbed ? 'armor' : 'the reaction';
    notify(name + ': incoming Condition absorbed by ' + by + '.', 'success');
    addSystemChat(name + ': incoming Condition absorbed by ' + by + '.');
    return;
  }
  const text = name + ': ' + prettyCondition(msg.condition);
  notify(text, 'warn');
  addSystemChat(text);
}

function onConditionCleared(msg) {
  const playerName = msg.player;
  const conditions = msg.all_conditions || [];

  if (playerName === state.playerName && state.character) {
    state.character.conditions = conditions;
    updateConditionsDisplay();
  }
  if (state.allCharacters[playerName]) {
    state.allCharacters[playerName].conditions = conditions;
  }
  renderMMCombatConsole();

  const name = (state.allCharacters[playerName] || {}).name || playerName;
  addSystemChat(name + ': cleared ' + prettyCondition(msg.condition));
}

function prettyCondition(condId) {
  return String(condId || '?').replace(/_/g, ' ');
}

function onExchangeEnded(msg) {
  addSystemChat('Exchange ended — Tier 1 Conditions clear, declare Postures again.');
  notify('Exchange ended — declare Postures for the next one.', 'info');
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
  renderMMCombatConsole();
  updateCombatStatusBanner();
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

  const posturesPanel = document.getElementById('combat-postures-revealed');
  if (posturesPanel) posturesPanel.classList.add('hidden');

  renderCombatPanel();       // falls back to the read-only readiness view
  renderMMCombatConsole();
  updateCombatStatusBanner();
  notify('Combat has ended.', 'success');
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

  // Note pre-technique scope limit (no difficulty penalty)
  let notes = '';
  if (!state.character.magic_technique_active) {
    notes += ' (Minor scope only, pre-technique)';
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

// ---------------------------------------------------------------------------
// Spark Cadence — Graceful Failure prompt and Nomination Round
// ---------------------------------------------------------------------------

/**
 * Called after any roll result. If the MM sees a 6- (failure), show a
 * prompt asking whether to award a Spark for graceful failure.
 */
function checkGracefulFailPrompt(msg) {
  const roll = msg.roll || msg;
  if (roll.outcome !== 'failure') return;

  const playerName = msg.player || msg.attacker || msg.player_name || 'Unknown';
  const charName = msg.character_name ||
    (state.allCharacters[playerName] && state.allCharacters[playerName].name) ||
    playerName;

  // The player who rolled the 6- gets an offer to claim it; the MM gets the
  // matching prompt to award. Previously only the MM side existed, so the
  // player half of the Graceful Failure cadence never surfaced at all.
  if (state.role !== 'mm') {
    if (playerName !== state.playerName) return;
    // Keyed: only the most recent 6- can be claimed anyway (the server checks
    // the caller's last roll), so a second prompt would be unclaimable clutter.
    notify('You rolled 6-. Narrate how it makes things worse — and claim a Spark.', 'gold', {
      sticky: true,
      key: 'graceful-fail',
      action: 'Claim Spark',
      onAction: claimGracefulFail,
    });
    return;
  }

  const banner = document.getElementById('play-graceful-fail-banner');
  if (!banner) return;
  banner.dataset.playerName = playerName;
  banner.querySelector('.graceful-fail-text').textContent =
    charName + ' rolled 6-. Award a Spark for graceful failure?';
  banner.classList.remove('hidden');
}

function awardGracefulFail() {
  const banner = document.getElementById('play-graceful-fail-banner');
  const playerName = banner.dataset.playerName;
  if (playerName) {
    sendWS({ type: 'spark_earn', player_name: playerName, reason: 'Graceful failure' });
  }
  banner.classList.add('hidden');
}

/**
 * Open an Act Break nomination window.
 *
 * This used to post a chat line and nothing else — the real `act_break` event
 * existed on the server and was never sent, so players got no prompt and the
 * cadence relied on the MM saying it out loud.
 */
function startNominationRound() {
  sendWS({ type: 'act_break' });
}

/** Player-side claim on their own 6-. Mirrors the MM's Graceful Failure prompt. */
function claimGracefulFail() {
  sendWS({ type: 'claim_graceful_fail' });
}

// ---------------------------------------------------------------------------
// Saving throws (III.1) — something happens TO the character
// ---------------------------------------------------------------------------
function populateSavingThrowSelect() {
  const sel = document.getElementById('play-save-attribute');
  if (!sel || !state.ruleset) return;
  sel.innerHTML = (state.ruleset.major_attributes || [])
    .map(m => `<option value="${escapeHtml(m.id)}">${escapeHtml(m.name)}</option>`).join('');
}

function performSavingThrow() {
  const sel = document.getElementById('play-save-attribute');
  const diff = document.getElementById('play-save-difficulty');
  if (!sel || !sel.value) return;
  sendWS({
    type: 'saving_throw',
    major_attribute_id: sel.value,
    difficulty: diff ? diff.value : 'Standard',
    sparks_spent: state.sparksToSpend,
  });
  state.sparksToSpend = 0;
  renderPlaySparkCounter();
}

// ---------------------------------------------------------------------------
// Contested rolls (MM) — two characters pushing against each other
// ---------------------------------------------------------------------------
function populateContestedSelects() {
  ['contest-attr-a', 'contest-attr-b'].forEach(id => {
    const sel = document.getElementById(id);
    if (!sel || !state.ruleset) return;
    const previous = sel.value;
    sel.innerHTML = (state.ruleset.minor_attributes || [])
      .map(a => `<option value="${escapeHtml(a.id)}">${escapeHtml(a.name)}</option>`).join('');
    if (previous) sel.value = previous;
  });
  ['contest-skill-a', 'contest-skill-b'].forEach(id => {
    const sel = document.getElementById(id);
    if (!sel || !state.ruleset) return;
    const previous = sel.value;
    sel.innerHTML = '<option value="">-- no skill --</option>'
      + (state.ruleset.skills || [])
          .filter(s => s.status !== 'stub')
          .map(s => `<option value="${escapeHtml(s.id)}">${escapeHtml(s.name)}</option>`).join('');
    if (previous) sel.value = previous;
  });
}

function performContestedRoll() {
  const playerA = document.getElementById('contest-player-a').value;
  const playerB = document.getElementById('contest-player-b').value;
  if (!playerA || !playerB) { notify('Pick both characters.', 'warn'); return; }
  if (playerA === playerB) { notify('A character cannot contest themselves.', 'warn'); return; }

  sendWS({
    type: 'contested_roll',
    player_a: playerA,
    player_b: playerB,
    attribute_a: document.getElementById('contest-attr-a').value,
    attribute_b: document.getElementById('contest-attr-b').value,
    skill_a: document.getElementById('contest-skill-a').value || null,
    skill_b: document.getElementById('contest-skill-b').value || null,
    difficulty: document.getElementById('contest-difficulty').value,
    description: document.getElementById('contest-description').value.trim(),
  });
}

// ---------------------------------------------------------------------------
// Table roller (MM) — a utility, not a mechanic
//
// Raw dice for everything around the game that is not the game: random tables,
// oracles, coin flips. It shows dice and a total and nothing else. Giving it an
// outcome tier would make it a second copy of the core resolution system and
// hand the MM a way to roll for an NPC, which PHB III.3 says never happens.
// ---------------------------------------------------------------------------

function quickTableRoll(notation) {
  const labelEl = document.getElementById('table-roll-label');
  sendWS({
    type: 'table_roll',
    notation,
    label: labelEl ? labelEl.value.trim() : '',
  });
}

function performTableRoll() {
  const input = document.getElementById('table-roll-notation');
  const notation = input ? input.value.trim() : '';
  if (!notation) {
    notify('Type dice notation, or use a quick button.', 'warn');
    focusElement('table-roll-notation');
    return;
  }
  quickTableRoll(notation);
}

function onTableRollResult(msg) {
  const parts = msg.label ? `${msg.label} — ${msg.notation}` : msg.notation;
  addSystemChat(`Table roll ${parts}: [${msg.dice.join(', ')}] = ${msg.total}`);

  // Everyone sees the result in chat; the MM also gets the readout in the panel.
  const box = document.getElementById('table-roll-result');
  if (!box || state.role !== 'mm') return;

  box.classList.remove('hidden');
  const modStr = msg.modifier ? ` ${msg.modifier > 0 ? '+' : '−'} ${Math.abs(msg.modifier)}` : '';
  box.innerHTML = `
    ${msg.label ? `<div class="table-roll-label">${escapeHtml(msg.label)}</div>` : ''}
    <div class="dice-display">${msg.dice.map(d => `<div class="die kept">${d}</div>`).join('')}</div>
    <div class="table-roll-total">${msg.total}</div>
    <div class="roll-breakdown">${escapeHtml(msg.notation)}: ${msg.dice.join(' + ')}${modStr} = ${msg.total}</div>`;

  const labelEl = document.getElementById('table-roll-label');
  if (labelEl) labelEl.value = '';
}

// ---------------------------------------------------------------------------
// Session lifecycle (MM)
// ---------------------------------------------------------------------------
async function resetSession() {
  const ok = await confirmDialog(
    'Start a new session?',
    'Every character\'s Sparks refresh to the per-session baseline and once-per-session Techniques '
    + 'become available again. Characters, advancement, and the enemy library are untouched.',
    'Start New Session');
  if (!ok) return;
  sendWS({ type: 'session_reset' });
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

  checkGracefulFailPrompt({ ...msg, character_name: casterName, roll });

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
