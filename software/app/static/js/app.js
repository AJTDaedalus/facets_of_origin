/**
 * Facets of Origin — application shell: auth, the MM dashboard, the socket,
 * table state, tabs and the shared feed. Tab pages live in builder.js
 * (Build), play.js (Play) and tools.js (Tools).
 */

const state = {
  token: null, role: null, playerName: null, sessionId: null, sessionName: null,
  ws: null, connected: false,
  ruleset: null,
  me: null,               // own character (players)
  chars: {},              // player_name -> character view
  enemies: {},            // tracker key -> foe (MM: full card; players: public view)
  library: {},            // MM: enemy card library
  clocks: {},
  combat: null,
  danger: null,
  sessionNumber: 1,
  feed: [],
  toolResults: [],        // MM: private toolbox results
  nominations: [],        // MM: Spark calls waiting for a ruling
  pendingAttack: null,    // my 10+ attack waiting for its option
  pendingCost: null,      // my 7-9 casting costs to choose from
  lastFailed: false,      // my last roll was a 6- (Graceful Fail can be claimed)
  tab: 'play',
};

/** UI-only memory (selected controls) so re-renders keep what the user set. */
const ui = {};

// ---------------------------------------------------------------- boot
window.addEventListener('DOMContentLoaded', () => {
  wireStatic();
  const invite = new URLSearchParams(location.search).get('token');
  if (invite) return show('join-screen', { invite });
  const tok = sessionStorage.getItem('facets_token');
  if (tok) {
    Object.assign(state, {
      token: tok, role: sessionStorage.getItem('facets_role'),
      playerName: sessionStorage.getItem('facets_player_name'),
      sessionId: sessionStorage.getItem('facets_session_id') || null,
      sessionName: sessionStorage.getItem('facets_session_name') || '',
    });
    if (state.role === 'mm' && !state.sessionId) return showDashboard();
    return enterGame();
  }
  show('auth-screen');
});

function show(id, data) {
  ['auth-screen', 'setup-screen', 'join-screen', 'mm-dashboard', 'game-screen'].forEach(s => $('#' + s).classList.toggle('hidden', s !== id));
  if (data && data.invite) $('#join-screen').dataset.invite = data.invite;
}

function wireStatic() {
  $('#btn-login').onclick = mmLogin;
  $('#mm-password').addEventListener('keydown', e => { if (e.key === 'Enter') mmLogin(); });
  $('#btn-show-setup').onclick = () => show('setup-screen');
  $('#btn-setup').onclick = setupPassword;
  $('#btn-join').onclick = redeemInvite;
  $('#btn-logout-dash').onclick = logout;
  $('#btn-create-session').onclick = createSession;
  $('#btn-invite').onclick = () => makeInvite($('#invite-session-id').value, $('#invite-player-name').value, '#invite-result');
  $('#btn-leave').onclick = leaveGame;
  $$('.tab').forEach(t => t.onclick = () => switchTab(t.dataset.tab));
  $('#chat-form').addEventListener('submit', e => {
    e.preventDefault();
    const text = $('#chat-input').value.trim();
    if (text) send({ type: 'chat', text });
    $('#chat-input').value = '';
  });
  // Free-text fields remember what was typed across re-renders.
  document.addEventListener('input', e => { const k = e.target.dataset && e.target.dataset.ui; if (k) ui[k] = e.target.type === 'checkbox' ? e.target.checked : e.target.value; });
  document.addEventListener('change', e => { const k = e.target.dataset && e.target.dataset.ui; if (k) { ui[k] = e.target.type === 'checkbox' ? e.target.checked : e.target.value; onUiChange(k); } });
  // Delegated controls: toggles, segmented buttons, steppers anywhere in the game.
  document.addEventListener('click', e => {
    const tg = e.target.closest('[data-toggle]');
    if (tg) { ui[tg.dataset.toggle] = !ui[tg.dataset.toggle]; tg.classList.toggle('on', !!ui[tg.dataset.toggle]); onUiChange(tg.dataset.toggle); return; }
    const sb = e.target.closest('[data-seg] button');
    if (sb && !sb.disabled) {
      const seg = sb.closest('[data-seg]');
      ui[seg.dataset.seg] = sb.dataset.v;
      $$('button', seg).forEach(b => b.classList.toggle('on', b === sb));
      onUiChange(seg.dataset.seg); return;
    }
    const st = e.target.closest('[data-stepper] button');
    if (st) {
      const box = st.closest('[data-stepper]');
      const k = box.dataset.stepper; const max = Number(box.dataset.max);
      ui[k] = Math.max(0, Math.min(max, (ui[k] || 0) + Number(st.dataset.d)));
      $('span', box).textContent = ui[k];
      onUiChange(k);
    }
  });
}

/** Hook for pages that react to a control change (e.g. the cast preview). */
function onUiChange(key) { if (typeof playUiChanged === 'function') playUiChanged(key); }

// ---------------------------------------------------------------- auth
async function mmLogin() {
  $('#auth-error').textContent = '';
  const resp = await apiFetch('/api/sessions/auth/mm-login', 'POST', { password: $('#mm-password').value });
  if (!resp.ok) { $('#auth-error').textContent = formatApiError((await resp.json()).detail, 'Sign-in failed.'); return; }
  storeAuth((await resp.json()).access_token, 'mm', 'MM', null, null);
  showDashboard();
}

async function setupPassword() {
  const pw = $('#setup-password').value, again = $('#setup-confirm').value;
  const err = $('#setup-error');
  if (pw !== again) { err.textContent = 'The passwords do not match.'; return; }
  if (pw.length < 8) { err.textContent = 'Use at least 8 characters.'; return; }
  const resp = await apiFetch('/api/sessions/auth/setup', 'POST', { password: pw });
  if (!resp.ok) { err.textContent = formatApiError((await resp.json()).detail, 'Setup failed.'); return; }
  show('auth-screen');
  $('#auth-ok').textContent = 'Password set. Sign in above.';
}

async function redeemInvite() {
  const resp = await apiFetch('/api/sessions/join', 'POST', { invite_token: $('#join-screen').dataset.invite });
  if (!resp.ok) { $('#join-error').textContent = formatApiError((await resp.json()).detail, 'That invite did not work.'); return; }
  const d = await resp.json();
  storeAuth(d.access_token, 'player', d.player_name, d.session_id, d.session_name);
  history.replaceState(null, '', '/');
  enterGame();
}

function storeAuth(token, role, playerName, sessionId, sessionName) {
  Object.assign(state, { token, role, playerName, sessionId, sessionName });
  sessionStorage.setItem('facets_token', token);
  sessionStorage.setItem('facets_role', role);
  sessionStorage.setItem('facets_player_name', playerName || '');
  sessionStorage.setItem('facets_session_id', sessionId || '');
  sessionStorage.setItem('facets_session_name', sessionName || '');
}

function logout() { sessionStorage.clear(); location.href = '/'; }

function leaveGame() {
  if (state.ws) { state.ws.onclose = null; state.ws.close(); }
  if (state.role === 'mm') {
    storeAuth(state.token, 'mm', 'MM', null, null);
    showDashboard();
  } else logout();
}

// ---------------------------------------------------------------- dashboard
async function showDashboard() {
  show('mm-dashboard');
  await loadSessions();
  const resp = await apiFetch('/api/facets/available');
  if (resp.status === 401) return logout();
  if (resp.ok) {
    const data = await resp.json();
    $('#facet-list').innerHTML = (data.facets || []).map(f => f.error
      ? `<div class="msg error">${esc(f.path)}: ${esc(f.error)}</div>`
      : `<label><input type="checkbox" value="${esc(f.id)}" ${f.id === 'base' ? 'checked disabled' : ''}> ${esc(f.name)} <span class="dim">v${esc(f.version)}</span></label>`).join('');
  }
}

async function loadSessions() {
  const resp = await apiFetch('/api/sessions/');
  if (resp.status === 401) return logout();
  if (!resp.ok) return;
  const sessions = (await resp.json()).sessions || [];
  $('#session-list').innerHTML = sessions.length ? sessions.map(s => `
    <li><span class="grow"><b>${esc(s.name)}</b> <span class="muted small">${s.player_count} character${s.player_count === 1 ? '' : 's'}</span></span>
      <button class="btn primary small" data-open="${esc(s.id)}" data-name="${esc(s.name)}">Open</button>
      <button class="btn danger small" data-del="${esc(s.id)}" data-name="${esc(s.name)}">Delete</button></li>`).join('')
    : '<li class="empty">No sessions yet. Make one, then invite your players.</li>';
  $$('[data-open]', $('#session-list')).forEach(b => b.onclick = () => {
    storeAuth(state.token, 'mm', 'MM', b.dataset.open, b.dataset.name); enterGame();
  });
  $$('[data-del]', $('#session-list')).forEach(b => b.onclick = async () => {
    if (!await confirmDialog(`Delete "${b.dataset.name}"?`, 'Its characters and invite links go with it.', 'Delete')) return;
    await apiFetch(`/api/sessions/${b.dataset.del}`, 'DELETE');
    loadSessions();
  });
  $('#invite-session-id').innerHTML = sessions.map(s => `<option value="${esc(s.id)}">${esc(s.name)}</option>`).join('')
    || '<option value="">Make a session first</option>';
}

async function createSession() {
  const name = $('#new-session-name').value.trim();
  if (!name) return notify('Name the session first.', 'warn');
  const ids = $$('#facet-list input:checked:not(:disabled)').map(i => i.value);
  const resp = await apiFetch('/api/sessions/', 'POST', { name, active_facet_ids: ids });
  if (!resp.ok) return notify(formatApiError((await resp.json()).detail, 'Could not create it.'), 'error');
  $('#new-session-name').value = '';
  notify(`"${name}" is ready. Invite your players.`, 'success');
  loadSessions();
}

async function makeInvite(sessionId, playerName, target) {
  playerName = (playerName || '').trim();
  if (!sessionId) return notify('Make a session first.', 'warn');
  if (!playerName) return notify("Enter the player's name.", 'warn');
  const resp = await apiFetch('/api/sessions/invite', 'POST', { session_id: sessionId, player_name: playerName });
  if (!resp.ok) return notify(formatApiError((await resp.json()).detail, 'Could not make the invite.'), 'error');
  const d = await resp.json();
  const box = $(target);
  box.classList.remove('hidden');
  box.innerHTML = `<div class="small">Single-use link for <b>${esc(playerName)}</b>:</div><code>${esc(d.invite_url)}</code>
    <button class="btn small primary">Copy link</button>`;
  $('button', box).onclick = () => navigator.clipboard.writeText(d.invite_url).then(() => notify('Copied.', 'success'));
}

// ---------------------------------------------------------------- game + socket
function enterGame() {
  show('game-screen');
  $('#hdr-session').textContent = state.sessionName || '';
  $('#hdr-who').textContent = state.role === 'mm' ? 'Mirror Master' : state.playerName;
  connect();
}

function connect() {
  const ws = new WebSocket(`${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws`);
  state.ws = ws;
  setConn('connecting');
  ws.onopen = () => ws.send(JSON.stringify({ token: state.token, session_id: state.sessionId }));
  ws.onmessage = ev => { try { handle(JSON.parse(ev.data)); } catch (err) { console.error(err); } };
  ws.onclose = () => { setConn('offline'); if (state.ws === ws) setTimeout(connect, 3000); };
}

function setConn(s) {
  state.connected = s === 'online';
  const el = $('#hdr-conn');
  el.className = `conn ${s}`;
  el.title = { online: 'Connected', connecting: 'Connecting…', offline: 'Offline: reconnecting' }[s];
}

function send(msg) {
  if (state.ws && state.ws.readyState === WebSocket.OPEN) state.ws.send(JSON.stringify(msg));
  else notify('Not connected yet: try again in a moment.', 'warn');
}

function isMM() { return state.role === 'mm'; }
function myName() { return state.playerName; }
function charName(player) { const c = state.chars[player]; return c ? c.name : player; }

function switchTab(tab) {
  state.tab = tab;
  $$('.tab').forEach(t => t.classList.toggle('on', t.dataset.tab === tab));
  ['build', 'play', 'tools'].forEach(t => $('#tab-' + t).classList.toggle('hidden', t !== tab));
  renderTab();
}

function renderTab() {
  if (!state.ruleset) return;
  // Keep focus (and the caret) in a field the user is typing in across re-renders.
  const act = document.activeElement;
  const key = act && act.dataset && act.dataset.ui;
  const caret = key && typeof act.selectionStart === 'number' ? act.selectionStart : null;
  if (state.tab === 'build') renderBuild();
  else if (state.tab === 'play') renderPlay();
  else renderTools();
  if (key) {
    const el = document.querySelector(`[data-ui="${CSS.escape(key)}"]`);
    if (el && el !== act) { el.focus(); if (caret !== null && el.setSelectionRange) try { el.setSelectionRange(caret, caret); } catch (e) { /* not a text field */ } }
  }
  const me = state.me;
  $('#build-dot').classList.toggle('hidden', !(me && me.level_up_ready));
}

/** Re-render only if the page shown depends on what changed. */
function refresh(parts) {
  if (!parts || parts.includes(state.tab)) renderTab();
  const me = state.me;
  $('#build-dot').classList.toggle('hidden', !(me && me.level_up_ready));
}

// ---------------------------------------------------------------- server messages
function handle(msg) {
  const h = HANDLE[msg.type];
  if (h) h(msg);
}

function setChar(player, ch) {
  state.chars[player] = ch;
  if (player === myName()) state.me = ch;
}

const HANDLE = {
  state(m) {
    const d = m.data;
    setConn('online');
    Object.assign(state, {
      ruleset: d.ruleset, chars: d.all_characters || {}, enemies: d.active_enemies || {},
      library: d.enemy_library || {}, clocks: d.threat_clocks || {}, combat: d.combat,
      danger: d.danger || null, sessionNumber: d.session_number || state.sessionNumber,
      sessionName: d.session_name || state.sessionName,
    });
    state.me = isMM() ? null : (d.your_character || null);
    $('#hdr-session').textContent = state.sessionName || '';
    if (!state.feed.length) (d.roll_log || []).slice(-20).forEach(r => feedRoll(r.player_name, r, true));
    const first = !$('.tab.on');
    if (first) switchTab(isMM() ? 'play' : (state.me ? 'play' : 'build'));
    else renderTab();
  },
  error(m) { notify(m.message, 'error', 7000); },
  pong() {},
  player_joined(m) { if (m.player !== myName() && m.player !== 'mm') feedSys(`${m.player} joined.`); },
  player_left(m) { if (m.player !== 'mm') feedSys(`${m.player} left.`); },
  chat(m) { feedPush('chat', `<span class="who">${esc(m.from === 'mm' ? 'MM' : m.from)}</span> ${esc(m.text)}`); },

  character_created(m) { setChar(m.player, m.character); feedSys(`${m.character.name} joins the party.`); if (m.player === myName()) { notify('Your character is ready.', 'success'); switchTab('play'); } else refresh(); },
  character_updated(m) { setChar(m.player, m.character); refresh(); },
  character_removed(m) { delete state.chars[m.player]; if (m.player === myName()) state.me = null; refresh(); },

  roll_result(m) { feedRoll(m.player, m.roll); },
  avoid_result(m) { feedRoll(m.player, m.roll, false, `avoids`, m.roll.extra && m.roll.extra.text); },
  attack_choose(m) {
    if (m.player === myName()) { state.pendingAttack = m; pickOption(m); }
    else feedPush('full_success', `<span class="who">${esc(m.character)}</span> rolls 10+ on ${esc(m.target_name || 'the attack')} and is choosing…`);
  },
  attack_result(m) { state.pendingAttack = m.player === myName() ? null : state.pendingAttack; feedAttack(m); state.combat = m.combat || state.combat; },
  enemy_attack_result(m) { feedEnemyAttack(m); if (m.combat) state.combat = m.combat; },
  cast_result(m) { feedCast(m); },
  cast_plan(m) { if (typeof showCastPlan === 'function') showCastPlan(m.plan); },
  complication_chosen(m) { feedPush('magic', `<span class="who">${esc(m.character)}</span> pays the cost: ${esc(m.complication.text)}`); },
  hold_on_result(m) { feedRoll(m.player, m.roll, false, 'holds on', m.text); },
  tended(m) { feedPush('sys', `${esc(charName(m.by))} tends ${esc(charName(m.player))}${m.field_surgeon ? ' (Field Surgeon: back on their feet at 1 HP)' : ': saved, out of the fight'}.`); },
  death_choice_made(m) {
    feedPush('failure', m.choice === 'scar'
      ? `<span class="who">${esc(m.character)}</span> lives, with a Scar: ${esc(m.scar.name)}`
      : `<span class="who">${esc(m.character)}</span> chooses a heroic final action. It succeeds.`);
  },
  rest_result(m) { feedSys(m.kind === 'night' ? "A night's rest: HP restored, Fatigue cleared, a Wound mends." : 'A breather: half HP back.'); },
  hp_adjusted(m) { feedSys(`${esc(charName(m.player))} ${m.delta < 0 ? 'takes ' + (-m.delta) + ' damage' : 'heals ' + m.delta} (HP ${m.hp}).${m.fall ? ' Down: a Wound (' + esc(m.fall.wound.name) + '), and Hold On.' : ''}`); },
  wound_added(m) { feedPush('failure', `${esc(charName(m.player))} takes a Wound: <b>${esc(m.wound.name)}</b>${m.items_to_drop ? ` (no room: drop ${m.items_to_drop} item${m.items_to_drop > 1 ? 's' : ''})` : ''}`); },
  wound_removed(m) { feedSys(`${esc(charName(m.player))}'s Wound heals: ${esc(m.wound.name)}.`); },
  usage_result(m) {
    const r = m.result;
    feedPush(r.stepped_down ? 'partial_success' : 'full_success', `<span class="who">${esc(m.character)}</span> rolls the usage die for ${esc(r.item)}:
      ${diceHtml([r.roll], [r.roll])} ${r.gone ? '<b>used up</b>' : (r.stepped_down ? `steps down to d${r.usage_die}` : 'holds')}`);
  },
  talent_used(m) { feedSys(`${esc(m.character)} uses ${esc(m.talent)}${m.uses_left !== null && m.uses_left !== undefined ? ` (${m.uses_left} left)` : ''}.`); },
  scene_ended() { feedSys('New scene: once-a-scene talents refresh.'); },

  combat_started(m) { state.combat = m.combat; feedSys('The fight begins. Exchange 1.'); refresh(); },
  exchange_ended(m) { state.combat = m.combat; feedSys(`Exchange ${m.exchange}. Exposure, Defend and cover have expired.`); refresh(); },
  combat_ended() { state.combat = null; feedSys('The fight is over.'); refresh(); },
  combat_state(m) { state.combat = m.combat; refresh(['play']); },
  telegraph(m) { state.combat = m.combat; feedPush('foe', `<b>${esc(m.name)}</b> is about to: ${esc(m.text)}`); refresh(['play']); },
  defend_declared(m) {
    state.combat = m.combat;
    feedSys(`${esc(m.defender)} ${m.intercept_for && m.intercept_for.length ? 'intercepts for ' + esc(m.intercept_for.join(', ')) : 'defends'}: attacks on them are Hard.`);
    refresh(['play']);
  },

  enemy_spawned(m) { state.enemies[m.enemy.key] = m.enemy; feedPush('foe', `<b>${esc(m.enemy.name)}</b> enters the fight.`); refresh(['play']); },
  enemy_updated(m) { state.enemies[m.enemy.key] = m.enemy; refresh(['play']); },
  enemy_removed(m) { delete state.enemies[m.key]; refresh(['play']); },
  enemy_library(m) { state.library = m.library; notify(m.loaded.length ? `Loaded ${m.loaded.length} Bestiary cards.` : 'The library already holds the Bestiary.', 'success'); refresh(); },
  enemy_damage(m) { if (m.result.bloodied_now) notify(`${m.name} is Bloodied.`, 'warn'); },
  danger(m) { state.danger = m.danger; refresh(['play']); },
  morale_result(m) {
    const r = m.result;
    feedPush(r.breaks ? 'full_success' : 'foe', `Morale: <b>${esc(m.name)}</b> ${diceHtml(r.dice, r.dice, 'die-foe')} ${r.total} vs ${r.morale}
      — ${r.fearless ? 'fearless: it never breaks' : (r.breaks ? `<b>it breaks.</b> ${esc(r.breaks_text)}` : 'it holds')}`);
  },

  toolbox_result(m) {
    if (m.revealed) { feedPush('sys', `<span class="who">MM reveals</span> ${toolboxText(m.kind, m.result)}`); }
    if (isMM() && !m.revealed) { state.toolResults.unshift(m); state.toolResults = state.toolResults.slice(0, 30); refresh(['play']); }
  },
  clock_updated(m) {
    state.clocks[m.clock.id] = m.clock;
    if (m.filled) { feedPush('failure', `The <b>${esc(m.clock.name)}</b> clock is full. It strikes.`); notify(`${m.clock.name}: the clock is full.`, 'warn'); }
    refresh(['play']);
  },
  clock_deleted(m) { delete state.clocks[m.clock_id]; refresh(['play']); },

  spark_earned(m) { feedPush('spk', `✦ <span class="who">${esc(charName(m.player))}</span> earns a Spark (${esc(m.reason)}). Now ${m.sparks_now}.`); if (m.player === myName()) notify(`You earned a Spark: ${m.reason}.`, 'spk'); state.nominations = state.nominations.filter(n => n.player !== m.player); refresh(['play']); },
  spark_spent(m) { feedSys(`${esc(charName(m.player))} spends a Spark${m.reason ? ': ' + esc(m.reason) : ''}.`); },
  spark_nomination(m) { feedPush('spk', esc(m.message)); if (isMM()) { state.nominations.push({ player: m.player, reason: m.kind === 'act_break' ? 'Act break nomination' : 'Peer call', by: m.nominated_by }); refresh(['play']); } },
  act_break_opened(m) { feedPush('spk', esc(m.message)); if (!isMM()) notify('Act break: nominate someone for a Spark (their card, "Spark?").', 'spk', 8000); },
  graceful_fail_claimed(m) {
    feedPush('spk', `<span class="who">${esc(charName(m.player))}</span> claims a Graceful Fail${m.narration ? ': “' + esc(m.narration) + '”' : ''}. MM to confirm.`);
    if (isMM()) { state.nominations.push({ player: m.player, reason: 'Graceful Fail', graceful: true }); refresh(['play']); }
  },

  level_up_ready(m) {
    feedPush('spk', `Level up! ${m.players.map(p => esc(charName(p))).join(', ')} may choose their pick.`);
    if (m.players.includes(myName())) notify('The MM called a level-up. Open Build to choose your pick.', 'spk', 9000);
  },
  level_up_done(m) { feedPush('spk', `<span class="who">${esc(m.character)}</span> reaches level ${m.level}${m.hp_roll ? ` (HP die: ${m.hp_roll})` : ''}.`); if (m.player === myName()) { notify(`Level ${m.level}!`, 'success'); } },
  level_pick_error(m) { if (typeof showLevelErrors === 'function') showLevelErrors(m.errors); else notify(m.errors.join(' '), 'error'); },
  session_end_prompts(m) { if (typeof showSessionEnd === 'function') showSessionEnd(m); },
  session_started(m) { state.sessionNumber = m.session_number; feedSys(`Session ${m.session_number} begins. Sparks are back to three.`); },
  spark_flow_nudge(m) { if (isMM()) notify(m.message, 'spk', 9000); },
};

// ---------------------------------------------------------------- the feed
function feedPush(cls, html) {
  state.feed.push({ cls, html });
  if (state.feed.length > 150) state.feed.shift();
  const el = document.createElement('div');
  el.className = `entry ${cls}`;
  el.innerHTML = html;
  const feed = $('#feed');
  if (!feed) return;
  feed.appendChild(el);
  while (feed.children.length > 150) feed.firstChild.remove();
  feed.scrollTop = feed.scrollHeight;
}
function feedSys(text) { feedPush('sys', text); }

function feedRoll(player, roll, quiet, verb, text) {
  if (!roll) return;
  const who = charName(player);
  feedPush(roll.outcome, `<span class="who">${esc(who)}</span> ${esc(verb || (roll.kind === 'roll' ? 'rolls' : roll.kind.replace('_', ' ')))}${roll.description ? ': ' + esc(roll.description) : ''}${rollLine(roll)}${text ? `<div class="note">${esc(text)}</div>` : ''}`);
  if (!quiet && player === myName()) {
    state.lastFailed = roll.outcome === 'failure' && !roll.graceful_fail_claimed;
    refresh(['play']);
  }
}

function feedAttack(m) {
  const r = m.result;
  const parts = [];
  if (r.hit) {
    parts.push(`Damage ${diceHtml(r.damage_dice, r.damage_dice, 'die-dmg')}${r.extra_damage_dice.length ? ' + ' + diceHtml(r.extra_damage_dice, r.extra_damage_dice, 'die-dmg') : ''}${r.damage_bonus ? ' + ' + r.damage_bonus : ''}
      = <b>${r.raw_damage}</b>${r.damage !== r.raw_damage ? `, <b>${r.damage}</b> through armor` : ''}`);
    if (r.options.length) parts.push(`Picks: ${r.options.map(o => ((R().combat || {}).options || {})[o]?.label || o).map(esc).join(', ')}${r.cover_for ? ` (covering ${esc(r.cover_for)})` : ''}`);
    if (r.exposed) parts.push('<span class="chip cost">Exposed: the foe\'s next attack on them rolls an extra die</span>');
  } else parts.push('<span class="chip bad">Miss: the MM makes a move</span>');
  const er = r.enemy_result;
  if (er) {
    if (er.mooks_dropped) parts.push(`${er.mooks_dropped} down`);
    if (er.bloodied_now) parts.push(`<span class="chip bad">Bloodied</span>${er.when_bloodied ? ' ' + esc(er.when_bloodied) : ''}`);
    if (er.defeated) parts.push('<span class="chip good">Defeated</span>');
  }
  if (r.opening_used) parts.push('<span class="chip info">Used an opening: one step Easier</span>');
  (r.notes || []).forEach(n => parts.push(esc(n)));
  feedPush(r.tier, `<span class="who">${esc(m.character)}</span> attacks ${esc(r.target_name || '')}${rollLine(r.roll)}<div class="note">${parts.join(' · ')}</div>`);
  if (m.player === myName()) state.lastFailed = r.tier === 'failure' && !r.roll.graceful_fail_claimed;
}

function feedEnemyAttack(m) {
  const r = m.result;
  const tier = r.hit ? (r.tier === 'full_success' ? 'failure' : 'partial_success') : 'full_success';
  const bits = [`2d6${signed(r.attack_bonus)}${r.difficulty !== 'Standard' ? ` (${r.difficulty})` : ''}`];
  if (r.exposure_die) bits.push('exposed: an extra die');
  if (r.hit) bits.push(`damage ${r.raw_damage}${r.armor ? ` − armor ${r.armor}` : ''} = <b>${r.damage}</b>`);
  (r.notes || []).forEach(n => bits.push(esc(n)));
  let fall = '';
  if (m.fall) fall = `<div class="note"><b>${esc(r.target)} drops to 0 HP.</b> Wound: ${esc(m.fall.wound.name)}. Roll Hold On.</div>`;
  feedPush('foe', `<b>${esc(r.enemy_name)}</b> attacks <span class="who">${esc(r.target)}</span>${r.original_target !== r.target ? ` (aimed at ${esc(r.original_target)})` : ''}
    <div class="line">${diceHtml(r.dice, r.kept, 'die-foe')} <span class="total">${r.total}</span> <span class="tier ${tier}">${esc(r.label)}</span>
    ${r.natural_high ? '<span class="chip bad">Natural 12: something more</span>' : ''}${r.natural_low ? '<span class="chip good">Natural 2: an opening</span>' : ''}</div>
    <div class="note">${bits.join(' · ')}</div>${fall}`);
}

function feedCast(m) {
  const r = m.result, p = r.plan;
  const bits = [`${esc(domainName(p.domain))}, ${esc(cap(p.scope))}${p.signature ? ', signature working' : ''}`, `${p.difficulty}`, `Fatigue ${r.fatigue_paid}`];
  if (r.damage_dice.length) bits.push(`harm ${diceHtml(r.damage_dice, r.damage_dice, 'die-dmg')}${r.damage_bonus ? ' + ' + r.damage_bonus : ''} = <b>${r.damage}</b>`);
  let extra = '';
  if (r.complication_options.length) extra += `<div class="note">It works, at a cost (${esc(m.character)} picks one): ${r.complication_options.map(c => '“' + esc(c.text) + '”').join(' or ')}</div>`;
  if (r.mishap) extra += `<div class="note"><b>Mishap:</b> ${esc(r.mishap.text)} · the Graceful Fail applies.</div>`;
  if (r.enemy_result && r.enemy_result.bloodied_now) extra += '<div class="note"><span class="chip bad">Bloodied</span></div>';
  feedPush('magic', `<span class="who">${esc(m.character)}</span> casts${r.intent ? ': ' + esc(r.intent) : ''}${rollLine(r.roll)}<div class="note">${bits.join(' · ')}</div>${extra}`);
  if (m.player === myName()) {
    state.lastFailed = r.outcome === 'failure' && !r.roll.graceful_fail_claimed;
    if (r.complication_options.length) { state.pendingCost = r.complication_options; pickCost(r.complication_options); }
  }
}

function toolboxText(kind, r) {
  if (kind === 'table' || kind === 'pressure') return `<b>${esc(r.name)}</b> (${esc(r.die)}: ${esc(r.roll)}): ${esc(r.text)}`;
  if (kind === 'reaction') return `<b>Reaction</b> ${diceHtml(r.dice, r.dice)} ${r.total}: ${esc(r.text)}`;
  if (kind === 'oracle') return `<b>Oracle</b>${r.question ? ' “' + esc(r.question) + '”' : ''} ${diceHtml(r.dice, r.dice)} <b>${esc(r.answer)}</b>${r.action ? ` · ${esc(r.action)} / ${esc(r.theme)}` : ''}`;
  if (kind === 'npc') return `<b>${esc(r.name)}</b>: ${esc(r.trait)}. Wants ${esc(r.want)}. Secret: ${esc(r.secret)}`;
  if (kind === 'hoard') return `<b>Hoard</b> (site level ${r.site_level}): ${r.coin} coin${r.curio ? `; curio: ${esc(r.curio.text)}` : ''}${r.relic ? `; relic: ${esc(r.relic.text)}` : ''}${r.trinket ? `; trinket: ${esc(r.trinket.text)}` : ''}`;
  if (kind === 'stuck') return r.map((o, i) => `<div><b>${i + 1}. ${esc(cap(o.kind))}:</b> ${esc(o.text)}${o.detail ? ` <span class="muted">(${esc(o.detail)})</span>` : ''}${o.reaction ? ` <span class="muted">Reaction: ${esc(o.reaction)}</span>` : ''}</div>`).join('');
  return esc(JSON.stringify(r));
}
