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
  threatClocks: {},        // clock_id -> clock (PHB III.2, D4)
  inCombat: false,
  postures: {},            // player_name -> posture (after reveal)
  connectionStatus: 'connecting',  // 'online' | 'connecting' | 'offline'
  sessions: [],            // MM dashboard: sessions listed from the API
  editingEnemyId: null,    // Builder: enemy currently loaded for edit, if any
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
  state.sessions = data.sessions || [];

  const list = document.getElementById('session-list');
  list.innerHTML = '';
  if (state.sessions.length === 0) {
    list.innerHTML = `<li class="empty-state">No sessions yet. Create one above, then generate an
      invite link for each player.</li>`;
  } else {
    state.sessions.forEach((s, i) => {
      const li = document.createElement('li');
      li.className = 'player-list-item';
      li.innerHTML = `
        <span><strong>${escapeHtml(s.name)}</strong>
          <small style="color:var(--text-dim)">${s.player_count} player${s.player_count === 1 ? '' : 's'}</small></span>
        <span class="btn-row" style="margin:0;"></span>`;
      const actions = li.querySelector('.btn-row');

      const open = document.createElement('button');
      open.className = 'btn btn-sm btn-primary';
      open.textContent = 'Open';
      open.onclick = () => enterSession(s.id, s.name);
      actions.appendChild(open);

      const copyId = document.createElement('button');
      copyId.className = 'btn btn-sm btn-secondary';
      copyId.textContent = 'Copy ID';
      copyId.onclick = () => copyToClipboard(s.id, 'Session ID copied.');
      actions.appendChild(copyId);

      const del = document.createElement('button');
      del.className = 'btn btn-sm btn-secondary';
      del.textContent = 'Delete';
      del.onclick = () => deleteSession(s.id, s.name, s.player_count);
      actions.appendChild(del);

      list.appendChild(li);
    });
  }

  // The invite form used to require pasting a session ID that was listed
  // directly above it. It picks from the same list now.
  const picker = document.getElementById('invite-session-id');
  if (picker) {
    const previous = picker.value;
    picker.innerHTML = state.sessions.length
      ? state.sessions.map(s => `<option value="${escapeHtml(s.id)}">${escapeHtml(s.name)}</option>`).join('')
      : '<option value="">-- create a session first --</option>';
    if (state.sessions.some(s => s.id === previous)) picker.value = previous;
  }
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

async function createSession(ev) {
  const name = document.getElementById('new-session-name').value.trim();
  if (!name) { notify('Give the session a name first.', 'warn'); focusElement('new-session-name'); return; }

  const checkboxes = document.querySelectorAll('[id^="facet-"]:checked');
  const activeFacetIds = Array.from(checkboxes).map(cb => cb.value);

  await withPending(ev && ev.target, 'Creating...', async () => {
    const resp = await apiFetch('/api/sessions/', 'POST', { name, active_facet_ids: activeFacetIds });
    if (resp.ok) {
      const data = await resp.json();
      document.getElementById('new-session-name').value = '';
      await loadSessionList();
      document.getElementById('session-created-msg').textContent =
        `Session "${data.name}" created. Generate an invite link for each player below.`;
      notify(`Session "${data.name}" created.`, 'success');
    } else {
      const err = await resp.json();
      notify(err.detail || 'Failed to create session.', 'error');
    }
  });
}

async function generateInvite(ev) {
  const picker = document.getElementById('invite-session-id');
  const sessionId = picker ? picker.value : state.sessionId;
  const playerName = document.getElementById('invite-player-name').value.trim();
  if (!sessionId) { notify('Create a session first.', 'warn'); return; }
  if (!playerName) { notify('Enter the player\'s name.', 'warn'); focusElement('invite-player-name'); return; }

  await withPending(ev && ev.target, 'Generating...', async () => {
    const resp = await apiFetch('/api/sessions/invite', 'POST', { session_id: sessionId, player_name: playerName });
    if (resp.ok) {
      const data = await resp.json();
      renderInviteResult('invite-result', data.invite_url, playerName);
    } else {
      const err = await resp.json();
      notify(err.detail || 'Failed to generate invite.', 'error');
    }
  });
}

/**
 * Invite links are single-use and get pasted into a chat app, so the copy button
 * matters more than the link text. Rendered the same way in both places it appears.
 */
function renderInviteResult(containerId, url, playerName) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.style.display = 'block';
  el.classList.remove('hidden');
  el.innerHTML = `
    <div class="invite-label">Single-use invite for <strong>${escapeHtml(playerName)}</strong></div>
    <div class="invite-url"></div>
    <div class="btn-row" style="margin-top:6px;"></div>`;
  el.querySelector('.invite-url').textContent = url;
  const copy = document.createElement('button');
  copy.className = 'btn btn-primary btn-sm';
  copy.textContent = 'Copy Link';
  copy.onclick = () => copyToClipboard(url, `Invite for ${playerName} copied.`);
  el.querySelector('.btn-row').appendChild(copy);
}

async function deleteSession(sessionId, sessionName, playerCount) {
  const ok = await confirmDialog(
    `Delete "${sessionName}"?`,
    playerCount
      ? `${playerCount} character${playerCount === 1 ? '' : 's'} in this session will be lost, and every `
        + 'invite link for it stops working. Export any character you want to keep first.'
      : 'Every invite link for this session stops working.',
    'Delete Session');
  if (!ok) return;

  const resp = await apiFetch(`/api/sessions/${sessionId}`, 'DELETE');
  if (resp.ok) {
    await loadSessionList();
    notify(`"${sessionName}" deleted.`, 'success');
  } else {
    notify('Failed to delete the session.', 'error');
  }
}

function enterSession(sessionId, sessionName) {
  storeToken(state.token, 'mm', 'MM', sessionId, sessionName);
  document.getElementById('mm-dashboard').classList.add('hidden');
  connectWebSocket();
}

// In-game invite generation for MM
async function generateInviteInGame(ev) {
  const playerName = document.getElementById('play-invite-player-name').value.trim();
  if (!playerName) { notify('Enter a player name.', 'warn'); focusElement('play-invite-player-name'); return; }
  await withPending(ev && ev.target, 'Generating...', async () => {
    const resp = await apiFetch('/api/sessions/invite', 'POST', {
      session_id: state.sessionId,
      player_name: playerName,
    });
    if (resp.ok) {
      const data = await resp.json();
      renderInviteResult('play-invite-result', data.invite_url, playerName);
    } else {
      const err = await resp.json();
      notify(err.detail || 'Failed to generate invite.', 'error');
    }
  });
}

// ---------------------------------------------------------------------------
// WebSocket
// ---------------------------------------------------------------------------
function connectWebSocket() {
  const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${location.host}/ws`;
  setConnectionStatus('connecting');
  const ws = new WebSocket(wsUrl);
  state.ws = ws;

  ws.onopen = () => {
    setConnectionStatus('online');
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
    setConnectionStatus('offline');
    addSystemChat('Disconnected from server. Reconnecting in 3s...');
    setTimeout(connectWebSocket, 3000);
  };

  ws.onerror = () => {
    setConnectionStatus('offline');
  };
}

/**
 * Connection state is shown as a persistent dot in the header rather than a
 * single line in a scrolling chat log — a dropped socket silently stops every
 * action in the app, so it has to stay visible.
 */
function setConnectionStatus(status) {
  state.connectionStatus = status;
  const el = document.getElementById('header-connection');
  if (!el) return;
  const labels = { online: 'Connected', connecting: 'Connecting...', offline: 'Offline — reconnecting' };
  el.className = 'conn-dot conn-' + status;
  el.title = labels[status] || status;
  el.setAttribute('aria-label', labels[status] || status);
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
    case 'character_created':
      onCharacterCreated(msg);
      break;
    case 'character_removed':
      onCharacterRemoved(msg);
      break;
    case 'player_joined':
      state.connectedPlayers.add(msg.player);
      addSystemChat(`${msg.player} joined the session.`);
      renderPlayPlayerList();
      if (typeof renderPlayerPickers === 'function') renderPlayerPickers();
      break;
    case 'player_left':
      state.connectedPlayers.delete(msg.player);
      addSystemChat(`${msg.player} left the session.`);
      renderPlayPlayerList();
      break;
    case 'spark_earned': {
      const who = (state.allCharacters[msg.player] || {}).name || msg.player;
      addSystemChat(`${who} earned a Spark — ${msg.reason}. Sparks now: ${msg.sparks_now}`);
      notify(`${who} earned a Spark (${msg.reason}).`, 'gold');
      if (state.allCharacters[msg.player]) state.allCharacters[msg.player].sparks = msg.sparks_now;
      if (msg.player === state.playerName && state.character) {
        state.character.sparks = msg.sparks_now;
        renderPlaySparkCounter();
      }
      renderPlayPlayerList();
      renderMMCombatConsole();
      break;
    }
    case 'spark_nomination':
      onSparkNomination(msg);
      break;
    case 'skill_advanced':
      addSystemChat(`${msg.player} advanced ${msg.skill_id} to ${msg.new_rank}${msg.facet_level_advances > 0 ? ' -- FACET LEVEL UP!' : ''}!`);
      if (state.character && msg.player === state.playerName) {
        if (state.character.skills[msg.skill_id]) {
          state.character.skills[msg.skill_id].rank = msg.new_rank;
          state.character.facet_level = msg.new_facet_level;
          // A Facet level earns a Technique pick; without applying it here the
          // advancement panel keeps showing the old count until a reload.
          if (msg.technique_picks_available !== undefined) {
            state.character.technique_picks_available = msg.technique_picks_available;
          }
          renderPlayCharacterSheet();
          if (typeof renderBuilderSkills === 'function') renderBuilderSkills();
          if (typeof renderBuilderTechniques === 'function') renderBuilderTechniques();
        }
      }
      break;
    case 'skill_marked_used':
      addSystemChat(`Skill '${msg.skill_id}' marked as used for ${msg.player}.`);
      if (state.character && msg.player === state.playerName) {
        state.character.skills_used_this_session = msg.skills_used || [];
        if (typeof renderBuilderSkills === 'function') renderBuilderSkills();
      }
      break;
    case 'skill_point_spent':
      addSystemChat(`${msg.player} spent ${msg.sp_cost} SP on ${msg.skill_id}${msg.rank_advances > 0 ? ' -- rank up!' : ''}.`);
      if (state.character && msg.player === state.playerName) {
        state.character.session_skill_points_remaining = msg.session_skill_points_remaining;
        if (state.character.skills[msg.skill_id]) {
          state.character.skills[msg.skill_id].marks = msg.new_marks;
          if (msg.rank_advances > 0) state.character.skills[msg.skill_id].rank = msg.new_rank;
          if (msg.facet_level_advances > 0) state.character.facet_level = msg.new_facet_level;
        }
        if (msg.technique_picks_available !== undefined) {
          state.character.technique_picks_available = msg.technique_picks_available;
        }
        renderPlayCharacterSheet();
        if (typeof renderBuilderSkills === 'function') renderBuilderSkills();
        if (typeof renderBuilderTechniques === 'function') renderBuilderTechniques();
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
    case 'enemy_phase_change':
      onEnemyPhaseChange(msg);
      break;
    // Threat Clock broadcasts (PHB III.2, D4)
    case 'clock_created':
      onClockCreated(msg);
      break;
    case 'clock_advanced':
      onClockAdvanced(msg);
      break;
    case 'clock_wound_back':
      onClockWoundBack(msg);
      break;
    case 'clock_fill':
      onClockFill(msg);
      break;
    case 'clock_deleted':
      onClockDeleted(msg);
      break;
    // Combat broadcasts
    case 'combat_started':
      onCombatStarted(msg);
      break;
    case 'posture_declared':
      onPostureDeclared(msg);
      break;
    case 'postures_revealed':
      onPosturesRevealed(msg);
      break;
    case 'strike_result':
      onStrikeResult(msg);
      break;
    case 'react_result':
      onReactResult(msg);
      break;
    case 'support_result':
      onSupportResult(msg);
      break;
    case 'maneuver_result':
      onManeuverResult(msg);
      break;
    case 'condition_applied':
      onConditionApplied(msg);
      break;
    case 'condition_cleared':
      onConditionCleared(msg);
      break;
    case 'exchange_ended':
      onExchangeEnded(msg);
      break;
    case 'combat_ended':
      onCombatEnded(msg);
      break;
    case 'scene_ended':
      // B6: armor budgets refreshed server-side; the sheet shows the budget, so
      // it has to re-render or it keeps displaying the spent one.
      if (state.character) state.character.armor_downgrades_remaining = null;
      addSystemChat('Scene ended — armor downgrade budgets refresh.');
      renderPlayCharacterSheet();
      break;
    // Magic broadcasts
    case 'cast_result':
      onCastResult(msg);
      break;
    case 'saving_throw_result':
      onSavingThrowResult(msg);
      break;
    case 'contested_roll_result':
      onContestedRollResult(msg);
      break;
    case 'table_roll_result':
      onTableRollResult(msg);
      break;
    // Advancement
    case 'technique_selected':
      onTechniqueSelected(msg);
      break;
    // Spark cadence
    case 'act_break_opened':
      onActBreakOpened(msg);
      break;
    case 'graceful_fail_claimed':
      onGracefulFailClaimed(msg);
      break;
    case 'session_reset':
      onSessionReset();
      break;
    case 'error':
      addSystemChat(`Error: ${msg.message}`);
      notify(msg.message, 'error');
      break;
    case 'pong':
      break;
    default:
      // Loud in development, harmless in play: an unhandled broadcast means the
      // server grew a feature the UI has not caught up with.
      console.warn('Unhandled server message type:', msg.type, msg);
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
  state.threatClocks = data.threat_clocks || {};

  if (state.role === 'player' && data.your_character) {
    state.character = data.your_character;
  }

  // Combat has no explicit flag in session state — a character in combat is one
  // with a live Endurance pool, which is exactly the test the server itself uses
  // ("Not in combat" == endurance_current is None). Deriving it here means a
  // reconnect mid-fight restores the combat panel instead of hiding it until the
  // next broadcast.
  state.inCombat = Object.values(state.allCharacters)
    .some(c => c.endurance_current !== null && c.endurance_current !== undefined);

  // Hide auth screens, show game screen
  document.getElementById('auth-screen').classList.add('hidden');
  document.getElementById('setup-screen').classList.add('hidden');
  document.getElementById('join-screen').classList.add('hidden');
  document.getElementById('mm-dashboard').classList.add('hidden');
  document.getElementById('game-screen').classList.remove('hidden');

  renderHeader();
  applyRoleVisibility();

  // The character panel is a player's sheet. The MM has no character, so
  // showing it left them staring at an empty Attributes grid, a dead Roll Dice
  // form, and an empty Skills table down the whole main column.
  const needsCreation = state.role === 'player' && !state.character;
  document.getElementById('char-create-panel').classList.toggle('hidden', !needsCreation);
  document.getElementById('character-panel').classList.toggle('hidden', needsCreation || state.role === 'mm');
  if (needsCreation) populateCharacterCreation();

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

  // When facet changes, update background list and the Facet blurb
  facetSelect.onchange = () => { populateBackgroundSelect(); renderFacetDescription(); };
  populateBackgroundSelect();
  renderFacetDescription();

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

function populateBackgroundSelect() {
  const facetId = document.getElementById('cc-facet').value;
  const bgSelect = document.getElementById('cc-background');
  const infoEl = document.getElementById('cc-background-info');
  bgSelect.innerHTML = '<option value="">-- none (custom) --</option>';

  const backgrounds = (state.ruleset.backgrounds || []).filter(bg => bg.facet === facetId);
  backgrounds.forEach(bg => {
    const opt = document.createElement('option');
    opt.value = bg.id;
    opt.textContent = bg.name;
    bgSelect.appendChild(opt);
  });

  bgSelect.onchange = onBackgroundChanged;
  onBackgroundChanged();
}

function onBackgroundChanged() {
  const bgId = document.getElementById('cc-background').value;
  const infoEl = document.getElementById('cc-background-info');
  const domainWrap = document.getElementById('cc-magic-domain-wrap');

  if (!bgId) {
    infoEl.textContent = '';
    domainWrap.classList.add('hidden');
    return;
  }

  const bg = (state.ruleset.backgrounds || []).find(b => b.id === bgId);
  if (!bg) { infoEl.innerHTML = ''; domainWrap.classList.add('hidden'); return; }

  const skillName = id => {
    const s = (state.ruleset.skills || []).find(s => s.id === id);
    return s ? s.name : id;
  };

  // A Background's five elements, laid out as rows rather than a run-on line
  // with a literal newline in it (PHB II.5).
  const rows = [];
  if (bg.description) rows.push(`<div class="bg-desc">${escapeHtml(bg.description)}</div>`);
  rows.push(`<div><span class="bg-key">Starting Skill</span> ${escapeHtml(skillName(bg.starting_skill))}
             <span class="rank-badge rank-practiced">Practiced</span></div>`);

  // Magic-granting Backgrounds replace the secondary skill with a domain origin.
  if (bg.domain_origin) {
    rows.push(`<div><span class="bg-key">Magic Origin</span> ${escapeHtml(bg.domain_origin)} domain
               &mdash; replaces the secondary skill</div>`);
  } else if (bg.secondary_skill) {
    rows.push(`<div><span class="bg-key">Secondary Skill</span> ${escapeHtml(skillName(bg.secondary_skill))}
               <span class="rank-badge rank-novice">Novice</span>
               <span style="color:var(--text-dim);">+1 mark already recorded</span></div>`);
  }
  if (bg.specialty) {
    rows.push(`<div><span class="bg-key">Specialty</span> ${escapeHtml(bg.specialty)}</div>
               <div style="color:var(--text-dim);">A Standard roll becomes Easy when your Specialty applies
               directly, and tangential knowledge needs no roll at all.</div>`);
  }
  infoEl.innerHTML = rows.join('');

  // Show magic domain selector if background has domain_origin or is a Soul magic background
  if (bg.domain_origin) {
    domainWrap.classList.remove('hidden');
    populateMagicDomainSelect(bg.domain_origin);
  } else {
    domainWrap.classList.add('hidden');
    document.getElementById('cc-magic-domain').value = '';
  }
}

/**
 * Facets are the first choice a new player makes and the one with the least
 * context on screen, so the chosen Facet describes itself.
 */
function renderFacetDescription() {
  const el = document.getElementById('cc-facet-info');
  if (!el || !state.ruleset) return;
  const facetId = document.getElementById('cc-facet').value;
  const facet = (state.ruleset.character_facets || []).find(cf => cf.id === facetId);
  if (!facet) { el.innerHTML = ''; return; }

  const skills = (state.ruleset.skills || [])
    .filter(s => s.facet === facetId && s.status !== 'stub')
    .map(s => s.name);

  el.innerHTML = `
    ${facet.description ? `<div class="bg-desc">${escapeHtml(facet.description)}</div>` : ''}
    ${skills.length ? `<div><span class="bg-key">Facet Skills</span> ${escapeHtml(skills.join(', '))}</div>` : ''}
    <div style="color:var(--text-dim);">Skills in your primary Facet cost 1 Skill Point to advance;
    everything else costs 2.</div>`;
}

function populateMagicDomainSelect(domainOrigin) {
  const domainSelect = document.getElementById('cc-magic-domain');
  domainSelect.innerHTML = '<option value="">-- no magic --</option>';

  if (!state.ruleset.magic) return;

  // Get domains for the origin facet (mind or soul)
  const domainList = domainOrigin === 'mind'
    ? (state.ruleset.magic.mind_domains || [])
    : domainOrigin === 'soul'
      ? (state.ruleset.magic.soul_domains || [])
      : [];

  domainList.forEach(d => {
    const opt = document.createElement('option');
    opt.value = d.id;
    opt.textContent = d.name + ' (' + d.type + ')';
    domainSelect.appendChild(opt);
  });
}

/**
 * Import an existing .fof character instead of rebuilding it by hand.
 *
 * The server validates the file against the session's ruleset and rejects a
 * player_name that doesn't match the caller's token, so the client only has to
 * read the file and surface whatever comes back.
 */
async function importCharacterFile(input) {
  const file = input && input.files && input.files[0];
  if (!file) return;
  const errEl = document.getElementById('cc-error');
  if (errEl) errEl.textContent = '';

  let text;
  try {
    text = await file.text();
  } catch (e) {
    notify('Could not read that file.', 'error');
    return;
  }

  const resp = await apiFetch('/api/characters/upload', 'POST', {
    session_id: state.sessionId,
    fof_yaml: text,
  });
  input.value = '';  // allow re-selecting the same file after a fix

  if (resp.ok) {
    const data = await resp.json();
    state.character = data.character;
    state.allCharacters[data.character.player_name] = data.character;
    notify(`${data.character.name} imported.`, 'success');
    showCharacterPanels();
  } else {
    const err = await resp.json().catch(() => ({}));
    const detail = err.detail;
    const message = typeof detail === 'string'
      ? detail
      : (detail && detail.errors ? detail.errors.join('; ') : 'Import failed.');
    if (errEl) errEl.textContent = message;
    notify(message, 'error');
  }
}

function showCharacterPanels() {
  document.getElementById('char-create-panel').classList.add('hidden');
  document.getElementById('character-panel').classList.remove('hidden');
  applyRoleVisibility();
  initPlayTab();
  initToolsTab();
  if (typeof initBuilderTab === 'function') initBuilderTab();
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

async function submitCharacterCreation(ev) {
  const name = document.getElementById('cc-name').value.trim();
  const primaryFacet = document.getElementById('cc-facet').value;
  const errEl = document.getElementById('cc-error');
  errEl.textContent = '';

  if (!name) {
    errEl.textContent = 'Give your character a name.';
    focusElement('cc-name');
    return;
  }

  const attributes = {};
  document.querySelectorAll('.attr-input').forEach(inp => {
    attributes[inp.dataset.attr] = parseInt(inp.value);
  });

  // Catch the point budget here rather than letting the server bounce it back
  // as a validation blob — the user is looking straight at the counter.
  const dist = state.ruleset && state.ruleset.attribute_distribution;
  const target = dist ? dist.total_points : 18;
  const spent = Object.values(attributes).reduce((a, b) => a + b, 0);
  if (spent !== target) {
    errEl.textContent = spent > target
      ? `You have spent ${spent} of ${target} points — lower ${spent - target} rating${spent - target === 1 ? '' : 's'}.`
      : `You have ${target - spent} point${target - spent === 1 ? '' : 's'} left to spend.`;
    return;
  }

  const backgroundId = document.getElementById('cc-background').value || null;
  const magicDomain = document.getElementById('cc-magic-domain').value || null;

  await withPending(ev && ev.target, 'Creating...', async () => {
    const resp = await apiFetch('/api/characters/', 'POST', {
      session_id: state.sessionId,
      character_name: name,
      primary_facet: primaryFacet,
      attributes,
      background_id: backgroundId,
      magic_domain: magicDomain,
    });

    if (resp.ok) {
      const data = await resp.json();
      state.character = data.character;
      state.allCharacters[data.character.player_name] = data.character;
      notify(`${data.character.name} is ready to play.`, 'success');
      showCharacterPanels();
    } else {
      const err = await resp.json().catch(() => ({}));
      errEl.textContent = formatApiError(err.detail, 'Character creation failed.');
    }
  });
}

/**
 * FastAPI validation details arrive as a string, a list of pydantic error
 * objects, or a {errors: [...]} dict. They used to be JSON.stringify'd straight
 * into the page.
 */
function formatApiError(detail, fallback) {
  if (!detail) return fallback;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    return detail.map(d => (typeof d === 'string' ? d : d.msg || JSON.stringify(d))).join('; ');
  }
  if (detail.errors) return [].concat(detail.errors).join('; ');
  return fallback;
}

// ---------------------------------------------------------------------------
// Header
// ---------------------------------------------------------------------------
function renderHeader() {
  document.getElementById('header-session-name').textContent = state.sessionName || 'Session';
  document.getElementById('header-identity').textContent = state.role === 'mm' ? 'Mirror Master' : (state.playerName || 'Player');
  setConnectionStatus(state.connectionStatus || 'online');
}

/**
 * Show or hide every role-scoped block in one place.
 *
 * Role visibility used to be set piecemeal inside each tab's init, which meant a
 * block hidden by one init could be re-shown by another (and MM-only controls
 * leaked onto the player view after a reconnect). `data-role` on the element is
 * now the single declaration.
 */
function applyRoleVisibility() {
  const role = state.role;
  document.querySelectorAll('[data-role]').forEach(el => {
    el.classList.toggle('hidden', el.dataset.role !== role);
  });
  // Controls that need a character, which the MM never has.
  const hasCharacter = !!state.character;
  document.querySelectorAll('[data-requires-character]').forEach(el => {
    el.classList.toggle('hidden', !hasCharacter);
  });
}

// ---------------------------------------------------------------------------
// Broadcast handlers for advancement, saves, contests, and Spark cadence
// ---------------------------------------------------------------------------
/**
 * A character now exists in the session.
 *
 * Everything that reads `allCharacters` has to refresh: the MM's combat roster,
 * every player picker, the party list, and the party sheets. Without this the MM
 * sat looking at an empty roster while players built characters in front of them.
 */
function onCharacterCreated(msg) {
  const isNew = !state.allCharacters[msg.player];
  state.allCharacters[msg.player] = msg.character;

  if (msg.player === state.playerName) state.character = msg.character;

  if (isNew) {
    addSystemChat(`${msg.character.name} joins the party.`);
    if (msg.player !== state.playerName) notify(`${msg.character.name} joins the party.`, 'success');
  }

  renderPlayPlayerList();
  renderPlayerPickers();
  renderMMCombatConsole();
  if (typeof populateTargetSelects === 'function') populateTargetSelects();
  if (typeof initToolsTab === 'function') initToolsTab();
}

function onCharacterRemoved(msg) {
  delete state.allCharacters[msg.player];
  addSystemChat(`${msg.player}'s character was removed.`);

  if (msg.player === state.playerName) {
    // Your own sheet is gone — drop straight back into creation rather than
    // leaving a stale sheet on screen that no longer exists server-side.
    state.character = null;
    notify('Your character was removed. Build a new one.', 'warn');
    document.getElementById('character-panel').classList.add('hidden');
    document.getElementById('char-create-panel').classList.remove('hidden');
    populateCharacterCreation();
  } else {
    notify(`${msg.player}'s character was removed.`, 'warn');
  }

  renderPlayPlayerList();
  renderPlayerPickers();
  renderMMCombatConsole();
  if (typeof populateTargetSelects === 'function') populateTargetSelects();
  if (typeof initToolsTab === 'function') initToolsTab();
}

/**
 * Delete a character. Players rebuild their own; the MM may clear anyone's.
 * Their single-use invite is already spent, so without this a misbuilt
 * character was permanent.
 */
async function deleteCharacter(playerName) {
  const who = playerName || state.playerName;
  const char = state.allCharacters[who];
  const ok = await confirmDialog(
    `Delete ${char ? char.name : who}?`,
    'Attributes, skills, Techniques, advancement, and inventory are all lost. '
    + 'Export the character first if you want to keep any of it.',
    'Delete Character');
  if (!ok) return;

  const resp = await apiFetch(`/api/characters/${state.sessionId}/${who}`, 'DELETE');
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    notify(formatApiError(err.detail, 'Failed to delete the character.'), 'error');
  }
  // The success path is driven by the character_removed broadcast, so both the
  // deleter and everyone else take exactly the same code path.
}

function onTechniqueSelected(msg) {
  const name = (state.allCharacters[msg.player] || {}).name || msg.player;
  const label = techniqueDisplayName(msg.technique_id) + (msg.choice ? ' (' + msg.choice + ')' : '');
  addSystemChat(`${name} learned ${label}.`);
  notify(`${name} learned ${label}.`, 'success');

  if (state.allCharacters[msg.player]) {
    state.allCharacters[msg.player].techniques = msg.all_techniques || [];
    state.allCharacters[msg.player].technique_picks_available = msg.technique_picks_available;
  }
  if (msg.player === state.playerName && state.character) {
    state.character.techniques = msg.all_techniques || [];
    state.character.technique_picks_available = msg.technique_picks_available;

    // The choice is what makes a choice-bearing Technique work at all: Weapon
    // Mastery's step is matched against technique_choices[id], so leaving this
    // unset client-side meant the Technique looked learned and behaved inert
    // until the next reload.
    if (msg.choice !== undefined && msg.choice !== null) {
      state.character.technique_choices = state.character.technique_choices || {};
      state.character.technique_choices[msg.technique_id] = msg.choice;
    }

    // Only a magic-granting Technique lifts the pre-Technique scope cap. This
    // used to fire for every Technique, so learning Weapon Mastery told the
    // Magic panel the character had unlocked full-scope magic.
    //
    // The test is `magic_granting` alone, mirroring `Character.select_technique`
    // exactly. Second Domain and Ascendant Domain carry only
    // `grants_secondary_domain` / `grants_prismatic_domain` and do NOT set the
    // flag server-side; including them here made the client enable Significant
    // and Major scope on a character the server still capped at Minor, and the
    // resulting cast spent a Spark before failing. Which Technique lifts the cap
    // is a rule — the client mirrors it, never re-derives it.
    const def = allTechniques().find(t => t.id === msg.technique_id);
    const grantsMagic = !!(def && def.magic_granting);
    if (grantsMagic) {
      state.character.magic_technique_active = true;
      if (typeof renderMagicPanel === 'function') renderMagicPanel();
    }
    if (typeof renderBuilderTechniques === 'function') renderBuilderTechniques();
  }
  if (typeof initToolsTab === 'function') initToolsTab();
}

function onSavingThrowResult(msg) {
  const name = (state.allCharacters[msg.player] || {}).name || msg.player;
  const major = majorAttributeName(msg.major_attribute_id);
  state.rollLog.unshift({ player_name: msg.player, character_name: name, ...msg.roll });
  renderPlayRollLog();

  addSystemChat(`${name} makes a ${major} save: ${msg.roll.outcome_label} (${msg.roll.total}).`);

  if (msg.player === state.playerName && state.character) {
    state.character.sparks = msg.sparks_remaining;
    renderPlaySparkCounter();
    showRollResultBox({ player: msg.player, character_name: name }, msg.roll);
  }
  if (typeof checkGracefulFailPrompt === 'function') {
    checkGracefulFailPrompt({ ...msg, character_name: name });
  }
}

function onContestedRollResult(msg) {
  const nameA = (state.allCharacters[msg.player_a] || {}).name || msg.player_a;
  const nameB = (state.allCharacters[msg.player_b] || {}).name || msg.player_b;
  state.rollLog.unshift({ player_name: msg.player_a, character_name: nameA, ...msg.roll_a });
  state.rollLog.unshift({ player_name: msg.player_b, character_name: nameB, ...msg.roll_b });
  renderPlayRollLog();

  const winnerText = msg.winner === 'tie'
    ? 'Tie — neither gains the upper hand.'
    : ((state.allCharacters[msg.winner] || {}).name || msg.winner) + ' wins the contest.';
  const summary = `Contest: ${nameA} ${msg.roll_a.total} vs ${nameB} ${msg.roll_b.total}. ${winnerText}`;
  addSystemChat(summary);
  notify(summary, 'info', { duration: 7000 });

  const box = document.getElementById('play-contested-result');
  if (box) {
    box.classList.remove('hidden');
    box.innerHTML = `
      <div class="contest-side ${msg.winner === msg.player_a ? 'contest-winner' : ''}">
        <div class="contest-name">${escapeHtml(nameA)}</div>
        <div class="contest-total">${msg.roll_a.total}</div>
        <div class="contest-outcome">${escapeHtml(msg.roll_a.outcome_label)}</div>
      </div>
      <div class="contest-vs">vs</div>
      <div class="contest-side ${msg.winner === msg.player_b ? 'contest-winner' : ''}">
        <div class="contest-name">${escapeHtml(nameB)}</div>
        <div class="contest-total">${msg.roll_b.total}</div>
        <div class="contest-outcome">${escapeHtml(msg.roll_b.outcome_label)}</div>
      </div>`;
  }
}

function onActBreakOpened(msg) {
  addSystemChat(msg.message);
  if (state.role === 'player') {
    notify(msg.message, 'gold', {
      sticky: true,
      key: 'act-break',
      action: 'Nominate',
      onAction: () => { switchTab('play'); focusElement('play-peer-spark-player'); },
    });
  } else {
    notify('Act break opened — players are nominating.', 'gold');
  }
}

function onGracefulFailClaimed(msg) {
  addSystemChat(msg.message);
  if (state.role === 'mm') {
    notify(msg.message, 'gold', {
      sticky: true,
      key: 'graceful-fail-claim',
      action: 'Award Spark',
      onAction: () => sendWS({ type: 'spark_earn', player_name: msg.player, reason: 'Graceful failure' }),
    });
  }
}

function onSessionReset() {
  addSystemChat('New session started — Sparks refreshed and once-per-session Techniques reset.');
  notify('New session started. Sparks refreshed.', 'success');
  // Every character's Spark count and technique usage changed server-side; the
  // cheapest correct refresh is to re-read state rather than mirror the rules here.
  sendWS({ type: 'ping' });
  location.reload();
}

// ---------------------------------------------------------------------------
// Small shared lookups
// ---------------------------------------------------------------------------
function majorAttributeName(id) {
  const found = state.ruleset && (state.ruleset.major_attributes || []).find(m => m.id === id);
  return found ? found.name : id;
}

/**
 * Every Technique in one Facet's tree, flattened.
 *
 * The tree the server sends is `ruleset.techniques[facetId].branches[].tiers[]
 * .techniques[]` — three levels of nesting. `ruleset.character_facets[]` carries
 * id/name/description/major_attribute and has never had a `techniques` field, so
 * code that reached for `character_facets[].techniques` always got `undefined`
 * and silently behaved as though the Facet had no Techniques at all.
 *
 * Each entry keeps its branch and tier, because "Requires a Tier 1 in the same
 * branch" is a rule the advancement screen has to be able to show.
 */
function techniquesForFacet(facetId) {
  const tree = state.ruleset && state.ruleset.techniques
    && state.ruleset.techniques[facetId];
  if (!tree) return [];
  const out = [];
  (tree.branches || []).forEach(branch => {
    (branch.tiers || []).forEach(tier => {
      (tier.techniques || []).forEach(technique => {
        out.push(Object.assign({}, technique, {
          branch_id: branch.id,
          branch_name: branch.name,
          tier: tier.tier,
        }));
      });
    });
  });
  return out;
}

/** Every Technique in every Facet's tree, flattened. */
function allTechniques() {
  const trees = (state.ruleset && state.ruleset.techniques) || {};
  return Object.keys(trees).reduce(
    (acc, facetId) => acc.concat(techniquesForFacet(facetId)), []);
}

function techniqueDisplayName(id) {
  const found = allTechniques().find(t => t.id === id);
  if (found && found.name) return found.name;
  return String(id || '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function toggleCollapsible(toggle) {
  const body = toggle.parentElement.querySelector('.collapsible-body');
  if (!body) return;
  const closed = body.classList.toggle('hidden');
  toggle.setAttribute('aria-expanded', String(!closed));
  const arrow = toggle.querySelector('.toggle-arrow');
  if (arrow) arrow.textContent = closed ? '+' : '−';
}

// ---------------------------------------------------------------------------
// Help drawer
//
// Nothing in the app told a first-time MM that enemy attacks are resolved by
// landing a Condition, or where any given task lives. This is that map.
// ---------------------------------------------------------------------------
const HELP_MM = [
  ['Play — Combat', 'Start Combat, Reveal Postures, End Exchange. Enemies never roll: when one attacks, pick the incoming Condition on the target and press Land Hit. Tick "reaction softened it" if their Dodge or Parry got a 7-9 — armour and reactions never stack, and the engine picks the greater reduction.'],
  ['Play — Enemy Tracker', 'Spawn saved enemies, deplete Resolve as Strikes land (10+ takes 2, 7-9 takes 1), and hang Conditions. Mooks have no Resolve — one Strike removes them.'],
  ['Play — Threat Clocks', 'A visible countdown on a hazard. A 7-9 or 6- near it advances a segment; a 10+ never does. Players can spend an action to wind one back.'],
  ['Play — Sparks', 'Open Act Break prompts every player to nominate someone. You confirm each nomination and every Graceful Failure claim. Award directly any time.'],
  ['Play — Contested Roll', 'Two characters pushing against each other. Highest total wins.'],
  ['Play — Table Roller', 'Raw dice for random tables, oracles, and coin flips. It has no outcome tier because it is not a resolution roll — enemies still never roll, and an enemy attack is landed as a Condition in the combat console.'],
  ['Play — Session', 'Invite links (one per player, single use) and Start New Session, which refreshes Sparks and re-arms once-per-session Techniques.'],
  ['Builder — Enemies & Encounters', 'Build enemies, then group them into an Encounter. Run drops the whole encounter into the live tracker in one action.'],
  ['Builder — Advancement', 'Mark skills used so players can spend Skill Points on them, and award marks directly.'],
  ['Builder — Notes', 'Private notes per character, plus campaign notes stored in this browser.'],
  ['Tools', 'Every character sheet, party inventory, rules quick references, and encounter difficulty guidance.'],
];

const HELP_PLAYER = [
  ['Play — Rolling', 'Click an Attribute, or hit Roll on a skill to use both. Stage Sparks on the pips first — each adds a d6 and drops the lowest.'],
  ['Play — Saving Throws', 'When something happens to you rather than something you attempt, roll a Major Attribute save.'],
  ['Play — Combat', 'Declare a Posture each exchange, then Strike, React, Support, or Maneuver. Press spends 1 Endurance for an extra die. At 0 Endurance you can only Absorb.'],
  ['Play — Magic', 'Domain plus Intent plus Scope. Describe what you want; the difficulty comes from your domain type and the scope you reach for.'],
  ['Play — Sparks', 'Nominate another player any time; the MM confirms. On a 6-, narrate how it makes things worse and claim a Graceful Failure Spark.'],
  ['Builder', 'Spend Skill Points on skills you actually used, pick Techniques as Facet levels open them, and keep your own notes.'],
  ['Tools', 'Your sheet, the rest of the party, your inventory, and rules quick references.'],
];

function toggleHelp() {
  const drawer = document.getElementById('help-drawer');
  if (!drawer) return;
  const opening = drawer.classList.contains('hidden');
  if (opening) {
    const rows = state.role === 'mm' ? HELP_MM : HELP_PLAYER;
    document.getElementById('help-content').innerHTML = rows.map(([where, what]) =>
      `<div class="help-row"><div class="help-where">${escapeHtml(where)}</div>
       <div class="help-what">${escapeHtml(what)}</div></div>`).join('');
  }
  drawer.classList.toggle('hidden');
}

function focusElement(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  el.focus();
  el.classList.add('flash-target');
  setTimeout(() => el.classList.remove('flash-target'), 1200);
}

// ---------------------------------------------------------------------------
// Notifications
//
// Everything used to land in the chat log with equal weight — a rules error and
// an idle chat line looked identical. Toasts carry anything the user must not
// miss; the chat log keeps the durable transcript.
// ---------------------------------------------------------------------------
function notify(message, kind, opts) {
  opts = opts || {};
  const host = document.getElementById('toast-host');
  if (!host) return;

  // A keyed toast replaces the previous one with the same key. Sticky prompts
  // ("claim your Graceful Failure") otherwise pile up one per triggering roll
  // and bury the panel behind them.
  if (opts.key) {
    host.querySelectorAll(`[data-toast-key="${CSS.escape(opts.key)}"]`).forEach(el => el.remove());
  }

  const toast = document.createElement('div');
  toast.className = 'toast toast-' + (kind || 'info');
  toast.setAttribute('role', kind === 'error' ? 'alert' : 'status');
  if (opts.key) toast.dataset.toastKey = opts.key;

  const text = document.createElement('span');
  text.className = 'toast-text';
  text.textContent = message;
  toast.appendChild(text);

  if (opts.action && opts.onAction) {
    const btn = document.createElement('button');
    btn.className = 'btn btn-gold btn-sm';
    btn.textContent = opts.action;
    btn.onclick = () => { opts.onAction(); dismiss(); };
    toast.appendChild(btn);
  }

  const close = document.createElement('button');
  close.className = 'toast-close';
  close.textContent = '×';
  close.setAttribute('aria-label', 'Dismiss');
  close.onclick = dismiss;
  toast.appendChild(close);

  host.appendChild(toast);

  // Sticky toasts wait for a decision; the rest clear themselves.
  let timer = null;
  if (!opts.sticky) {
    timer = setTimeout(dismiss, opts.duration || (kind === 'error' ? 8000 : 4500));
  }

  function dismiss() {
    if (timer) clearTimeout(timer);
    toast.classList.add('toast-leaving');
    setTimeout(() => toast.remove(), 200);
  }
  return dismiss;
}

/**
 * Promise-based confirm. Replaces window.confirm so destructive actions read
 * in the app's own voice and can name what is about to be lost.
 */
function confirmDialog(title, body, confirmLabel) {
  return new Promise(resolve => {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
      <div class="modal" role="dialog" aria-modal="true" aria-label="${escapeHtml(title)}">
        <div class="modal-title">${escapeHtml(title)}</div>
        <div class="modal-body">${escapeHtml(body)}</div>
        <div class="btn-row" style="justify-content:flex-end;">
          <button class="btn btn-secondary btn-sm" data-act="cancel">Cancel</button>
          <button class="btn btn-primary btn-sm" data-act="ok">${escapeHtml(confirmLabel || 'Confirm')}</button>
        </div>
      </div>`;

    function close(result) {
      document.removeEventListener('keydown', onKey);
      overlay.remove();
      resolve(result);
    }
    function onKey(e) { if (e.key === 'Escape') close(false); }

    overlay.onclick = (e) => {
      if (e.target === overlay) return close(false);
      const act = e.target.dataset && e.target.dataset.act;
      if (act === 'ok') close(true);
      if (act === 'cancel') close(false);
    };
    document.addEventListener('keydown', onKey);
    document.body.appendChild(overlay);
    const ok = overlay.querySelector('[data-act="ok"]');
    if (ok) ok.focus();
  });
}

/**
 * Prompt for a single line of text. Same reason as confirmDialog — window.prompt
 * is unstyled, blocks the whole page, and is suppressed in some embedded views.
 */
function promptDialog(title, placeholder, initial) {
  return new Promise(resolve => {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
      <div class="modal" role="dialog" aria-modal="true" aria-label="${escapeHtml(title)}">
        <div class="modal-title">${escapeHtml(title)}</div>
        <input type="text" class="modal-input" placeholder="${escapeHtml(placeholder || '')}"
               value="${escapeHtml(initial || '')}">
        <div class="btn-row" style="justify-content:flex-end;">
          <button class="btn btn-secondary btn-sm" data-act="cancel">Cancel</button>
          <button class="btn btn-primary btn-sm" data-act="ok">OK</button>
        </div>
      </div>`;

    const input = overlay.querySelector('.modal-input');
    function close(result) {
      document.removeEventListener('keydown', onKey);
      overlay.remove();
      resolve(result);
    }
    function onKey(e) {
      if (e.key === 'Escape') close(null);
      if (e.key === 'Enter' && document.activeElement === input) close(input.value.trim() || null);
    }
    overlay.onclick = (e) => {
      if (e.target === overlay) return close(null);
      const act = e.target.dataset && e.target.dataset.act;
      if (act === 'ok') close(input.value.trim() || null);
      if (act === 'cancel') close(null);
    };
    document.addEventListener('keydown', onKey);
    document.body.appendChild(overlay);
    input.focus();
    input.select();
  });
}

/**
 * Choose one option from a list. Used where a decision has a fixed legal set —
 * a Technique's domain choice, for instance — so the user picks rather than types.
 * Resolves to the chosen value, or null if cancelled.
 */
function selectDialog(title, body, options) {
  return new Promise(resolve => {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
      <div class="modal" role="dialog" aria-modal="true" aria-label="${escapeHtml(title)}">
        <div class="modal-title">${escapeHtml(title)}</div>
        <div class="modal-body">${escapeHtml(body)}</div>
        <select class="modal-input">
          ${options.map(o => `<option value="${escapeHtml(o.value)}">${escapeHtml(o.label)}</option>`).join('')}
        </select>
        <div class="btn-row" style="justify-content:flex-end;">
          <button class="btn btn-secondary btn-sm" data-act="cancel">Cancel</button>
          <button class="btn btn-primary btn-sm" data-act="ok">Confirm</button>
        </div>
      </div>`;

    const select = overlay.querySelector('.modal-input');
    function close(result) {
      document.removeEventListener('keydown', onKey);
      overlay.remove();
      resolve(result);
    }
    function onKey(e) { if (e.key === 'Escape') close(null); }
    overlay.onclick = (e) => {
      if (e.target === overlay) return close(null);
      const act = e.target.dataset && e.target.dataset.act;
      if (act === 'ok') close(select.value);
      if (act === 'cancel') close(null);
    };
    document.addEventListener('keydown', onKey);
    document.body.appendChild(overlay);
    select.focus();
  });
}

/**
 * Run an async action with the triggering button disabled, so a slow round-trip
 * cannot be double-submitted.
 */
async function withPending(btn, label, fn) {
  if (!btn) return fn();
  const original = btn.textContent;
  btn.disabled = true;
  btn.textContent = label || original;
  try {
    return await fn();
  } finally {
    btn.disabled = false;
    btn.textContent = original;
  }
}

async function copyToClipboard(text, successMessage) {
  try {
    await navigator.clipboard.writeText(text);
    notify(successMessage || 'Copied to clipboard.', 'success');
  } catch (e) {
    notify('Could not copy automatically — select the text and copy it.', 'warn');
  }
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
