/**
 * Facets of Origin — Core application shell.
 *
 * Manages: auth, WebSocket, state, routing, tab switching, character creation.
 * Tab-specific logic lives in play.js, tools.js, builder.js.
 * Shared rendering components live in components.js.
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
  activeEnemies: {},       // tracker_key -> enemy
  enemyLibrary: {},        // enemy_id -> enemy
  encounterLibrary: {},    // encounter_id -> encounter
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

// In-game invite generation for MM
async function generateInviteInGame() {
  const playerName = document.getElementById('play-invite-player-name').value.trim();
  if (!playerName) { alert('Enter a player name.'); return; }
  const resp = await apiFetch('/api/sessions/invite', 'POST', {
    session_id: state.sessionId,
    player_name: playerName,
  });
  if (resp.ok) {
    const data = await resp.json();
    document.getElementById('play-invite-result').textContent = data.invite_url;
  } else {
    const err = await resp.json();
    alert(err.detail || 'Failed.');
  }
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
      renderPlayPlayerList();
      break;
    case 'player_left':
      state.connectedPlayers.delete(msg.player);
      addSystemChat(`${msg.player} left the session.`);
      renderPlayPlayerList();
      break;
    case 'spark_earned':
      addSystemChat(`${msg.player} earned a Spark! (${msg.reason}). Sparks now: ${msg.sparks_now}`);
      if (msg.player === state.playerName && state.character) {
        state.character.sparks = msg.sparks_now;
        renderPlaySparkCounter();
      }
      break;
    case 'spark_nomination':
      onSparkNomination(msg);
      break;
    case 'skill_advanced':
      addSystemChat(`${msg.player} advanced ${msg.skill_id} to ${msg.new_rank}${msg.facet_level_advances > 0 ? ' -- FACET LEVEL UP!' : ''}!`);
      if (state.character && msg.player === state.playerName) {
        if (state.character.skills[msg.skill_id]) {
          state.character.skills[msg.skill_id].rank = msg.new_rank;
          state.character.facet_level = msg.new_facet_level;
          renderPlayCharacterSheet();
          if (typeof renderBuilderSkills === 'function') renderBuilderSkills();
        }
      }
      break;
    case 'chat':
      addChatMessage(msg.from, msg.text);
      break;
    case 'enemy_spawned':
      onEnemySpawned(msg);
      addSystemChat(`Enemy spawned: ${msg.enemy.name}`);
      break;
    case 'enemy_updated':
      onEnemyUpdated(msg);
      break;
    case 'enemy_removed':
      onEnemyRemoved(msg);
      addSystemChat(`Enemy removed: ${msg.tracker_key}`);
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
  state.activeEnemies = data.active_enemies || {};
  state.enemyLibrary = data.enemy_library || {};
  state.encounterLibrary = data.encounter_library || {};

  if (state.role === 'player' && data.your_character) {
    state.character = data.your_character;
  }

  // Hide auth screens, show game screen
  document.getElementById('auth-screen').classList.add('hidden');
  document.getElementById('setup-screen').classList.add('hidden');
  document.getElementById('join-screen').classList.add('hidden');
  document.getElementById('mm-dashboard').classList.add('hidden');
  document.getElementById('game-screen').classList.remove('hidden');

  renderHeader();

  // Show character creation if player has no character yet
  if (state.role === 'player' && !state.character) {
    document.getElementById('char-create-panel').classList.remove('hidden');
    document.getElementById('character-panel').classList.add('hidden');
    populateCharacterCreation();
  } else {
    document.getElementById('char-create-panel').classList.add('hidden');
    document.getElementById('character-panel').classList.remove('hidden');
  }

  // Initialize all tabs
  initPlayTab();
  initToolsTab();
  if (typeof initBuilderTab === 'function') initBuilderTab();
}

// ---------------------------------------------------------------------------
// Tab switching
// ---------------------------------------------------------------------------
function switchTab(tabName) {
  ['play', 'tools', 'builder'].forEach(t => {
    const content = document.getElementById('tab-' + t);
    const btns = document.querySelectorAll('.tab-bar .tab-btn[data-tab="' + t + '"]');
    if (content) content.classList.toggle('hidden', t !== tabName);
    btns.forEach(btn => btn.classList.toggle('active', t === tabName));
  });

  // Refresh tab data when switching
  if (tabName === 'tools') initToolsTab();
  if (tabName === 'builder' && typeof initBuilderTab === 'function') initBuilderTab();
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

  const attrContainer = document.getElementById('cc-attributes');
  attrContainer.innerHTML = '';

  const dist = state.ruleset.attribute_distribution;
  const totalPoints = dist ? dist.total_points : 18;
  const maxRating = dist ? dist.max_per_attribute : 3;

  state.ruleset.major_attributes.forEach(major => {
    const groupDiv = document.createElement('div');
    groupDiv.className = 'major-group';
    groupDiv.innerHTML = '<div class="major-label">' + major.name + '</div>';

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
          ${[1,2,3].filter(r => r <= maxRating).map(r => '<option value="' + r + '"' + (r===2?' selected':'') + '>' + r + '</option>').join('')}
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
  el.textContent = (remaining >= 0 ? remaining : 0) + ' points remaining (' + total + '/' + target + ')';
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
    initPlayTab();
    initToolsTab();
    if (typeof initBuilderTab === 'function') initBuilderTab();
  } else {
    const err = await resp.json();
    errEl.textContent = JSON.stringify(err.detail || 'Character creation failed.');
  }
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
  if (state.token) opts.headers['Authorization'] = 'Bearer ' + state.token;
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
  if (e.key === 'Enter' && document.activeElement && document.activeElement.id === 'play-chat-input') {
    sendChat();
  }
});
