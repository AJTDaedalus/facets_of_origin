/**
 * Facets of Origin — Digital Tabletop Client
 *
 * Single-file vanilla JS app. No build step required.
 * Manages auth, WebSocket, character sheet, dice rolling, and chat.
 */

// ---------------------------------------------------------------------------
// State
// ---------------------------------------------------------------------------
const state = {
  token: null,
  role: null,           // 'mm' | 'player'
  playerName: null,
  sessionId: null,
  sessionName: null,
  character: null,      // own character object
  allCharacters: {},    // player_name -> character
  ruleset: null,        // merged ruleset from server
  rollLog: [],
  connectedPlayers: new Set(),
  selectedAttributeId: null,
  selectedSkillId: null,
  sparksToSpend: 0,
  ws: null,
};

// ---------------------------------------------------------------------------
// Routing — check URL to determine which screen to show
// ---------------------------------------------------------------------------
window.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const inviteToken = params.get('token');

  if (inviteToken) {
    showJoinScreen(inviteToken);
  } else {
    const stored = sessionStorage.getItem('facets_token');
    const storedRole = sessionStorage.getItem('facets_role');
    if (stored) {
      state.token = stored;
      state.role = storedRole;
      state.playerName = sessionStorage.getItem('facets_player_name');
      state.sessionId = sessionStorage.getItem('facets_session_id');
      state.sessionName = sessionStorage.getItem('facets_session_name');
      connectWebSocket();
    } else {
      checkSetupNeeded();
    }
  }
});

// ---------------------------------------------------------------------------
// Auth screens
// ---------------------------------------------------------------------------
async function checkSetupNeeded() {
  // Try to log in with no password to check if setup is needed
  // (the setup endpoint returns 400 if already configured)
  const el = document.getElementById('auth-screen');
  el.classList.remove('hidden');
  document.getElementById('game-screen').classList.add('hidden');
}

function showSetupScreen() {
  document.getElementById('auth-screen').classList.add('hidden');
  document.getElementById('setup-screen').classList.remove('hidden');
}

function showJoinScreen(inviteToken) {
  document.getElementById('auth-screen').classList.add('hidden');
  document.getElementById('game-screen').classList.add('hidden');
  const joinScreen = document.getElementById('join-screen');
  joinScreen.classList.remove('hidden');
  joinScreen.dataset.inviteToken = inviteToken;
}

async function mmLogin() {
  const password = document.getElementById('mm-password').value;
  const errEl = document.getElementById('auth-error');
  errEl.textContent = '';

  const resp = await apiFetch('/api/sessions/auth/mm-login', 'POST', { password });
  if (resp.ok) {
    const data = await resp.json();
    storeToken(data.access_token, 'mm', 'MM', null, null);
    document.getElementById('auth-screen').classList.add('hidden');
    showMMDashboard();
  } else {
    const err = await resp.json();
    errEl.textContent = err.detail || 'Login failed.';
  }
}

async function setupPassword() {
  const password = document.getElementById('setup-password').value;
  const confirm = document.getElementById('setup-confirm').value;
  const errEl = document.getElementById('setup-error');
  errEl.textContent = '';

  if (password !== confirm) { errEl.textContent = 'Passwords do not match.'; return; }
  if (password.length < 8) { errEl.textContent = 'Password must be at least 8 characters.'; return; }

  const resp = await apiFetch('/api/sessions/auth/setup', 'POST', { password });
  if (resp.ok) {
    document.getElementById('setup-screen').classList.add('hidden');
    document.getElementById('auth-screen').classList.remove('hidden');
    document.getElementById('auth-error').textContent = '';
    document.getElementById('setup-success').textContent = 'Password set! Log in above.';
  } else {
    const err = await resp.json();
    errEl.textContent = err.detail || 'Setup failed.';
  }
}

async function redeemInvite() {
  const inviteToken = document.getElementById('join-screen').dataset.inviteToken;
  const errEl = document.getElementById('join-error');
  errEl.textContent = '';

  const resp = await apiFetch('/api/sessions/join', 'POST', { invite_token: inviteToken });
  if (resp.ok) {
    const data = await resp.json();
    storeToken(data.access_token, 'player', data.player_name, data.session_id, data.session_name);
    document.getElementById('join-screen').classList.add('hidden');
    connectWebSocket();
  } else {
    const err = await resp.json();
    errEl.textContent = err.detail || 'Failed to join session.';
  }
}

function storeToken(token, role, playerName, sessionId, sessionName) {
  state.token = token;
  state.role = role;
  state.playerName = playerName;
  state.sessionId = sessionId;
  state.sessionName = sessionName;
  sessionStorage.setItem('facets_token', token);
  sessionStorage.setItem('facets_role', role);
  sessionStorage.setItem('facets_player_name', playerName || '');
  sessionStorage.setItem('facets_session_id', sessionId || '');
  sessionStorage.setItem('facets_session_name', sessionName || '');
}

function logout() {
  sessionStorage.clear();
  location.reload();
}

// ---------------------------------------------------------------------------
// MM Dashboard (session management)
// ---------------------------------------------------------------------------
function showMMDashboard() {
  document.getElementById('game-screen').classList.add('hidden');
  document.getElementById('mm-dashboard').classList.remove('hidden');
  loadSessionList();
  loadAvailableFacets();
}

async function loadSessionList() {
  const resp = await apiFetch('/api/sessions/', 'GET');
  if (!resp.ok) return;
  const data = await resp.json();
  const list = document.getElementById('session-list');
  list.innerHTML = '';
  if (data.sessions.length === 0) {
    list.innerHTML = '<li style="color:var(--text-dim);font-size:13px;">No sessions yet.</li>';
    return;
  }
  data.sessions.forEach(s => {
    const li = document.createElement('li');
    li.className = 'player-list-item';
    li.innerHTML = `
      <span>${s.name} <small style="color:var(--text-dim)">(${s.player_count} players)</small></span>
      <button class="btn btn-sm btn-primary" onclick="enterSession('${s.id}', '${s.name}')">Open</button>
    `;
    list.appendChild(li);
  });
}

async function loadAvailableFacets() {
  const resp = await apiFetch('/api/facets/available', 'GET');
  if (!resp.ok) return;
  const data = await resp.json();
  const list = document.getElementById('facet-list');
  list.innerHTML = '';
  data.facets.forEach(f => {
    if (f.error) {
      list.innerHTML += `<div style="color:var(--failure);font-size:12px;">Error in ${f.path}: ${f.error}</div>`;
      return;
    }
    list.innerHTML += `<div style="margin-bottom:6px;font-size:13px;">
      <strong>${f.name}</strong> <span style="color:var(--text-dim)">v${f.version}</span>
      ${f.id !== 'base' ? `<input type="checkbox" id="facet-${f.id}" value="${f.id}" style="width:auto;margin-left:8px;">` : '<span style="color:var(--text-dim);font-size:11px;margin-left:8px;">(always loaded)</span>'}
    </div>`;
  });
}

async function createSession() {
  const name = document.getElementById('new-session-name').value.trim();
  if (!name) { alert('Session name is required.'); return; }

  const checkboxes = document.querySelectorAll('[id^="facet-"]:checked');
  const activeFacetIds = Array.from(checkboxes).map(cb => cb.value);

  const resp = await apiFetch('/api/sessions/', 'POST', { name, active_facet_ids: activeFacetIds });
  if (resp.ok) {
    const data = await resp.json();
    document.getElementById('new-session-name').value = '';
    loadSessionList();
    document.getElementById('session-created-msg').textContent = `Session "${data.name}" created (ID: ${data.session_id})`;
  } else {
    const err = await resp.json();
    alert(err.detail || 'Failed to create session.');
  }
}

async function generateInvite() {
  const sessionId = state.sessionId || document.getElementById('invite-session-id').value.trim();
  const playerName = document.getElementById('invite-player-name').value.trim();
  if (!sessionId || !playerName) { alert('Session ID and player name are required.'); return; }

  const resp = await apiFetch('/api/sessions/invite', 'POST', { session_id: sessionId, player_name: playerName });
  if (resp.ok) {
    const data = await resp.json();
    document.getElementById('invite-result').textContent = data.invite_url;
    document.getElementById('invite-result').style.display = 'block';
  } else {
    const err = await resp.json();
    alert(err.detail || 'Failed to generate invite.');
  }
}

function enterSession(sessionId, sessionName) {
  storeToken(state.token, 'mm', 'MM', sessionId, sessionName);
  document.getElementById('mm-dashboard').classList.add('hidden');
  connectWebSocket();
}

// ---------------------------------------------------------------------------
// WebSocket
// ---------------------------------------------------------------------------
function connectWebSocket() {
  const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${location.host}/ws`;
  const ws = new WebSocket(wsUrl);
  state.ws = ws;

  ws.onopen = () => {
    // Authenticate: send token as first message (NOT in URL to avoid logging)
    ws.send(JSON.stringify({
      token: state.token,
      session_id: state.sessionId,
    }));
  };

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    handleServerMessage(msg);
  };

  ws.onclose = () => {
    addSystemChat('Disconnected from server. Attempting to reconnect in 3s...');
    setTimeout(connectWebSocket, 3000);
  };

  ws.onerror = () => {
    addSystemChat('Connection error.');
  };
}

function sendWS(msg) {
  if (state.ws && state.ws.readyState === WebSocket.OPEN) {
    state.ws.send(JSON.stringify(msg));
  }
}

// ---------------------------------------------------------------------------
// Server message handling
// ---------------------------------------------------------------------------
function handleServerMessage(msg) {
  switch (msg.type) {
    case 'state':
      onStateReceived(msg.data);
      break;
    case 'roll_result':
      onRollResult(msg);
      break;
    case 'player_joined':
      state.connectedPlayers.add(msg.player);
      addSystemChat(`${msg.player} joined the session.`);
      renderPlayerList();
      break;
    case 'player_left':
      state.connectedPlayers.delete(msg.player);
      addSystemChat(`${msg.player} left the session.`);
      renderPlayerList();
      break;
    case 'spark_earned':
      addSystemChat(`✨ ${msg.player} earned a Spark! (${msg.reason}). Sparks now: ${msg.sparks_now}`);
      if (msg.player === state.playerName) {
        state.character.sparks = msg.sparks_now;
        renderSparkCounter();
      }
      break;
    case 'spark_nomination':
      onSparkNomination(msg);
      break;
    case 'skill_advanced':
      addSystemChat(`📈 ${msg.player} advanced ${msg.skill_id} to ${msg.new_rank}${msg.facet_level_advances > 0 ? ' — FACET LEVEL UP!' : ''}!`);
      if (state.character && msg.player === state.playerName) {
        if (state.character.skills[msg.skill_id]) {
          state.character.skills[msg.skill_id].rank = msg.new_rank;
          state.character.facet_level = msg.new_facet_level;
          renderCharacterSheet();
        }
      }
      break;
    case 'chat':
      addChatMessage(msg.from, msg.text);
      break;
    case 'error':
      addSystemChat(`Error: ${msg.message}`);
      break;
    case 'pong':
      break;
  }
}

function onStateReceived(data) {
  state.sessionId = data.session_id;
  state.sessionName = data.session_name;
  state.ruleset = data.ruleset;
  state.rollLog = data.roll_log || [];
  state.allCharacters = data.all_characters || {};

  if (state.role === 'player' && data.your_character) {
    state.character = data.your_character;
  }

  document.getElementById('auth-screen').classList.add('hidden');
  document.getElementById('setup-screen').classList.add('hidden');
  document.getElementById('join-screen').classList.add('hidden');
  document.getElementById('mm-dashboard').classList.add('hidden');
  document.getElementById('game-screen').classList.remove('hidden');

  renderHeader();
  renderCharacterSheet();
  renderRollLog();
  renderPlayerList();

  if (state.role === 'mm') {
    document.getElementById('mm-controls').classList.remove('hidden');
  } else {
    document.getElementById('player-controls').classList.remove('hidden');
  }

  // Show character creation if player has no character yet
  if (state.role === 'player' && !state.character) {
    document.getElementById('char-create-panel').classList.remove('hidden');
    document.getElementById('character-panel').classList.add('hidden');
    populateCharacterCreation();
  } else {
    document.getElementById('char-create-panel').classList.add('hidden');
    document.getElementById('character-panel').classList.remove('hidden');
  }
}

// ---------------------------------------------------------------------------
// Character creation
// ---------------------------------------------------------------------------
function populateCharacterCreation() {
  if (!state.ruleset) return;
  const facetSelect = document.getElementById('cc-facet');
  facetSelect.innerHTML = '';
  state.ruleset.character_facets.forEach(cf => {
    const opt = document.createElement('option');
    opt.value = cf.id;
    opt.textContent = cf.name;
    facetSelect.appendChild(opt);
  });

  // Build attribute inputs
  const attrContainer = document.getElementById('cc-attributes');
  attrContainer.innerHTML = '';

  const dist = state.ruleset.attribute_distribution;
  const totalPoints = dist ? dist.total_points : 18;
  const maxRating = dist ? dist.max_per_attribute : 3;

  state.ruleset.major_attributes.forEach(major => {
    const groupDiv = document.createElement('div');
    groupDiv.className = 'major-group';
    groupDiv.innerHTML = `<div class="major-label">${major.name}</div>`;

    const gridDiv = document.createElement('div');
    gridDiv.className = 'attr-grid';

    major.minor_attributes.forEach(minorId => {
      const minor = state.ruleset.minor_attributes.find(m => m.id === minorId);
      if (!minor) return;
      const block = document.createElement('div');
      block.className = 'attr-block';
      block.innerHTML = `
        <div class="attr-name">${minor.name}</div>
        <select class="attr-input" id="cc-attr-${minor.id}" data-attr="${minor.id}" onchange="updateAttrPointsDisplay()" style="width:60px;text-align:center;">
          ${[1,2,3].filter(r => r <= maxRating).map(r => `<option value="${r}" ${r===2?'selected':''}>${r}</option>`).join('')}
        </select>
      `;
      gridDiv.appendChild(block);
    });
    groupDiv.appendChild(gridDiv);
    attrContainer.appendChild(groupDiv);
  });

  updateAttrPointsDisplay();
}

function updateAttrPointsDisplay() {
  const inputs = document.querySelectorAll('.attr-input');
  let total = 0;
  inputs.forEach(inp => total += parseInt(inp.value));
  const dist = state.ruleset && state.ruleset.attribute_distribution;
  const target = dist ? dist.total_points : 18;
  const el = document.getElementById('cc-points-remaining');
  const remaining = target - total;
  el.textContent = `${remaining >= 0 ? remaining : 0} points remaining (${total}/${target})`;
  el.style.color = remaining === 0 ? 'var(--success)' : remaining < 0 ? 'var(--failure)' : 'var(--text-dim)';
}

async function submitCharacterCreation() {
  const name = document.getElementById('cc-name').value.trim();
  const primaryFacet = document.getElementById('cc-facet').value;
  const errEl = document.getElementById('cc-error');
  errEl.textContent = '';

  if (!name) { errEl.textContent = 'Character name is required.'; return; }

  const attributes = {};
  document.querySelectorAll('.attr-input').forEach(inp => {
    attributes[inp.dataset.attr] = parseInt(inp.value);
  });

  const resp = await apiFetch('/api/characters/', 'POST', {
    session_id: state.sessionId,
    character_name: name,
    primary_facet: primaryFacet,
    attributes,
  });

  if (resp.ok) {
    const data = await resp.json();
    state.character = data.character;
    document.getElementById('char-create-panel').classList.add('hidden');
    document.getElementById('character-panel').classList.remove('hidden');
    renderCharacterSheet();
  } else {
    const err = await resp.json();
    errEl.textContent = JSON.stringify(err.detail || 'Character creation failed.');
  }
}

// ---------------------------------------------------------------------------
// Character sheet rendering
// ---------------------------------------------------------------------------
function renderCharacterSheet() {
  const char = state.character;
  if (!char || !state.ruleset) return;

  // Name and facet
  const facetDef = state.ruleset.character_facets.find(cf => cf.id === char.primary_facet);
  document.getElementById('char-name').textContent = char.name;
  document.getElementById('char-facet').textContent = facetDef ? facetDef.name : char.primary_facet;
  document.getElementById('char-facet').className = `facet-badge facet-${char.primary_facet}`;
  document.getElementById('char-level').textContent = `Facet Level ${char.facet_level}`;

  // Attributes
  renderAttributeGrid(char);

  // Skills
  renderSkillsTable(char);

  // Sparks
  renderSparkCounter();
}

function renderAttributeGrid(char) {
  const container = document.getElementById('attr-display');
  if (!container || !state.ruleset) return;
  container.innerHTML = '';

  state.ruleset.major_attributes.forEach(major => {
    const groupDiv = document.createElement('div');
    groupDiv.className = 'major-group';
    groupDiv.innerHTML = `<div class="major-label">${major.name}</div>`;

    const gridDiv = document.createElement('div');
    gridDiv.className = 'attr-grid';

    major.minor_attributes.forEach(minorId => {
      const minor = state.ruleset.minor_attributes.find(m => m.id === minorId);
      if (!minor) return;
      const rating = char.attributes[minorId] || 2;
      const ratingDef = state.ruleset.attribute_ratings.find(r => r.rating === rating);
      const mod = ratingDef ? ratingDef.modifier : 0;
      const modStr = mod > 0 ? `+${mod}` : `${mod}`;

      const block = document.createElement('div');
      block.className = `attr-block${state.selectedAttributeId === minorId ? ' selected' : ''}`;
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

function renderSkillsTable(char) {
  const tbody = document.getElementById('skills-tbody');
  if (!tbody || !state.ruleset) return;
  tbody.innerHTML = '';

  state.ruleset.skills.forEach(skill => {
    if (skill.status === 'stub') return; // hide stub skills for now
    const skillState = char.skills[skill.id] || { rank: 'novice', marks: 0 };
    const rankDef = state.ruleset.advancement ? state.ruleset.advancement.skill_ranks.find(r => r.id === skillState.rank) : null;
    const marksNeeded = state.ruleset.advancement ? state.ruleset.advancement.marks_per_rank : 3;
    const dots = '●'.repeat(skillState.marks) + '○'.repeat(Math.max(0, marksNeeded - skillState.marks));

    const facetLabel = state.ruleset.character_facets.find(cf => cf.id === skill.facet);
    const isPrimary = skill.facet === char.primary_facet;

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${skill.name}${isPrimary ? '' : ' <span style="color:var(--text-dim);font-size:10px">●</span>'}</td>
      <td><span class="rank-badge rank-${skillState.rank}">${rankDef ? rankDef.label : skillState.rank}</span></td>
      <td class="marks-dots" title="${skillState.marks}/${marksNeeded} marks">${dots}</td>
      <td><button class="btn-roll-skill" onclick="rollSkill('${skill.id}')">Roll</button></td>
    `;
    tbody.appendChild(tr);
  });
}

function renderSparkCounter() {
  const char = state.character;
  if (!char) return;
  const container = document.getElementById('spark-pips');
  if (!container) return;
  container.innerHTML = '';

  const maxSparks = Math.max(char.sparks, 6); // show at least 6 slots
  for (let i = 0; i < maxSparks; i++) {
    const pip = document.createElement('div');
    pip.className = `spark-pip${i < char.sparks ? ' filled' : ''}`;
    pip.title = i < char.sparks ? 'Spark available' : 'Empty';
    pip.onclick = () => toggleSparkSpend(i);
    container.appendChild(pip);
  }

  document.getElementById('spark-count').textContent = `${char.sparks} Spark${char.sparks !== 1 ? 's' : ''}`;
  document.getElementById('sparks-to-spend').textContent = state.sparksToSpend > 0
    ? `(spending ${state.sparksToSpend})`
    : '';
}

function toggleSparkSpend(index) {
  if (!state.character) return;
  state.sparksToSpend = index + 1 <= state.character.sparks ? index + 1 : 0;
  if (state.sparksToSpend === state.character.sparks + 1) state.sparksToSpend = 0;
  renderSparkCounter();
  // Update spend indicator
  const pips = document.querySelectorAll('.spark-pip');
  pips.forEach((pip, i) => {
    pip.style.borderColor = i < state.sparksToSpend ? 'var(--accent)' : 'var(--gold)';
  });
}

// ---------------------------------------------------------------------------
// Rolling
// ---------------------------------------------------------------------------
function selectAttribute(attrId) {
  state.selectedAttributeId = attrId;
  state.selectedSkillId = null;
  renderAttributeGrid(state.character);
  document.getElementById('roll-btn').disabled = false;
  document.getElementById('roll-attr-display').textContent =
    state.ruleset.minor_attributes.find(m => m.id === attrId)?.name || attrId;
}

function rollSkill(skillId) {
  if (!state.ruleset) return;
  const skill = state.ruleset.skills.find(s => s.id === skillId);
  if (!skill) return;
  state.selectedSkillId = skillId;
  state.selectedAttributeId = skill.attribute;
  renderAttributeGrid(state.character);
  document.getElementById('roll-btn').disabled = false;
  document.getElementById('roll-attr-display').textContent =
    `${state.ruleset.minor_attributes.find(m => m.id === skill.attribute)?.name} + ${skill.name}`;
  performRoll();
}

function performRoll() {
  if (!state.selectedAttributeId) {
    addSystemChat('Select an attribute to roll.');
    return;
  }

  const difficulty = document.getElementById('difficulty-select').value;
  const description = document.getElementById('roll-description').value.slice(0, 200);

  sendWS({
    type: 'roll',
    attribute_id: state.selectedAttributeId,
    skill_id: state.selectedSkillId || null,
    difficulty,
    sparks_spent: state.sparksToSpend,
    description,
  });

  // Reset spark spend
  state.sparksToSpend = 0;
}

function onRollResult(msg) {
  const roll = msg.roll;

  // Add to log
  state.rollLog.unshift({ player_name: msg.player, character_name: msg.character_name, ...roll });
  renderRollLog();

  // Show result in panel
  const resultBox = document.getElementById('roll-result-box');
  resultBox.className = `roll-result-box ${roll.outcome}`;
  resultBox.classList.remove('hidden');

  // Build dice display
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
    return `<div class="die ${isDropped ? 'dropped' : 'kept'}" title="${isDropped ? 'dropped (Spark)' : 'kept'}">${d}</div>`;
  }).join('');

  const modParts = [];
  if (roll.attribute_modifier !== 0) modParts.push(`Attr ${roll.attribute_modifier > 0 ? '+' : ''}${roll.attribute_modifier}`);
  if (roll.skill_modifier !== 0) modParts.push(`Skill +${roll.skill_modifier}`);
  if (roll.difficulty_modifier !== 0) modParts.push(`Diff ${roll.difficulty_modifier > 0 ? '+' : ''}${roll.difficulty_modifier}`);
  const modStr = modParts.length ? ` (${modParts.join(', ')})` : '';

  const whoStr = msg.player === state.playerName ? 'You' : `${msg.character_name || msg.player}`;

  resultBox.innerHTML = `
    <div style="font-size:0.8rem;color:var(--text-dim);margin-bottom:4px;">${whoStr} rolled ${roll.attribute_id}${roll.skill_id ? ' + ' + roll.skill_id : ''}${roll.difficulty !== 'Standard' ? ' [' + roll.difficulty + ']' : ''}${roll.sparks_spent > 0 ? ' ✨×' + roll.sparks_spent : ''}</div>
    <div class="dice-display">${diceHtml}</div>
    <div class="roll-total">${roll.total}</div>
    <div class="roll-outcome-label">${roll.outcome_label}</div>
    <div class="roll-outcome-desc">${roll.outcome_description}</div>
    <div class="roll-breakdown">Dice sum: ${roll.dice_sum}${modStr} = ${roll.total}</div>
    ${roll.description ? `<div style="font-size:0.8rem;color:var(--text-dim);margin-top:4px;font-style:italic;">"${roll.description}"</div>` : ''}
  `;

  // Update spark pips if it was our roll
  if (msg.player === state.playerName && state.character) {
    state.character.sparks = msg.character_sparks_remaining;
    renderSparkCounter();
  }
}

// ---------------------------------------------------------------------------
// Roll log
// ---------------------------------------------------------------------------
function renderRollLog() {
  const container = document.getElementById('roll-log');
  if (!container) return;
  container.innerHTML = '';
  state.rollLog.slice(0, 30).forEach(entry => {
    const div = document.createElement('div');
    div.className = 'roll-log-entry';
    div.innerHTML = `
      <span class="who">${entry.character_name || entry.player_name}</span>
      <span class="outcome-${entry.outcome}"> ${entry.total} — ${entry.outcome_label}</span>
      <span style="color:var(--text-dim);float:right">${entry.attribute_id}${entry.skill_id ? '+'+entry.skill_id : ''}</span>
    `;
    container.appendChild(div);
  });
}

// ---------------------------------------------------------------------------
// Player list
// ---------------------------------------------------------------------------
function renderPlayerList() {
  const ul = document.getElementById('player-list');
  if (!ul) return;
  ul.innerHTML = '';
  Object.values(state.allCharacters).forEach(char => {
    const li = document.createElement('li');
    const isOnline = state.connectedPlayers.has(char.player_name);
    li.innerHTML = `
      <span class="${isOnline ? 'player-online' : ''}">${char.player_name}${char.name !== char.player_name ? ` (${char.name})` : ''}</span>
      <span class="facet-badge facet-${char.primary_facet}">${char.primary_facet}</span>
    `;
    ul.appendChild(li);
  });
}

// ---------------------------------------------------------------------------
// Chat
// ---------------------------------------------------------------------------
function addChatMessage(from, text) {
  const log = document.getElementById('chat-log');
  if (!log) return;
  const div = document.createElement('div');
  div.className = 'chat-msg';
  div.innerHTML = `<span class="from">${escapeHtml(from)}</span>: ${escapeHtml(text)}`;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

function addSystemChat(text) {
  const log = document.getElementById('chat-log');
  if (!log) return;
  const div = document.createElement('div');
  div.className = 'chat-msg system';
  div.textContent = text;
  log.appendChild(div);
  log.scrollTop = log.scrollHeight;
}

function sendChat() {
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;
  sendWS({ type: 'chat', text });
  input.value = '';
}

// MM: award Spark
function mmAwardSpark() {
  const playerName = document.getElementById('mm-spark-player').value.trim();
  const reason = document.getElementById('mm-spark-reason').value.trim() || 'MM award';
  if (!playerName) { alert('Enter a player name.'); return; }
  sendWS({ type: 'spark_earn', player_name: playerName, reason });
}

// Player: nominate peer for Spark
function nominateForSpark() {
  const playerName = document.getElementById('peer-spark-player').value.trim();
  if (!playerName) { alert('Enter a player name.'); return; }
  sendWS({ type: 'spark_earn_peer', player_name: playerName });
}

function onSparkNomination(msg) {
  const banner = document.getElementById('spark-nomination-banner');
  if (!banner) return;
  banner.classList.remove('hidden');
  banner.querySelector('.nomination-text').textContent = msg.message;
  banner.dataset.nominatedPlayer = msg.player;
}

function confirmSparkNomination() {
  const banner = document.getElementById('spark-nomination-banner');
  const playerName = banner.dataset.nominatedPlayer;
  if (playerName) {
    sendWS({ type: 'spark_earn', player_name: playerName, reason: 'Peer nomination' });
  }
  banner.classList.add('hidden');
}

// ---------------------------------------------------------------------------
// Header
// ---------------------------------------------------------------------------
function renderHeader() {
  document.getElementById('header-session-name').textContent = state.sessionName || 'Session';
  document.getElementById('header-identity').textContent = state.role === 'mm' ? 'Mirror Master' : (state.playerName || 'Player');
}

// ---------------------------------------------------------------------------
// Utilities
// ---------------------------------------------------------------------------
async function apiFetch(url, method, body) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (state.token) opts.headers['Authorization'] = `Bearer ${state.token}`;
  if (body) opts.body = JSON.stringify(body);
  return fetch(url, opts);
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// Enter key to send chat
document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && document.activeElement.id === 'chat-input') {
    sendChat();
  }
});
