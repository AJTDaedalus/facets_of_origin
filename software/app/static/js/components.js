/**
 * Facets of Origin — shared helpers and rendering pieces.
 *
 * Nothing here decides a rule. Numbers shown come from the server (the
 * engine's derived values) or straight from the ruleset data.
 */

// ---------------------------------------------------------------- basics
function esc(v) {
  return String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
const $ = (sel, root) => (root || document).querySelector(sel);
const $$ = (sel, root) => Array.from((root || document).querySelectorAll(sel));
function cap(s) { s = String(s || ''); return s.charAt(0).toUpperCase() + s.slice(1); }
function signed(n) { n = Number(n) || 0; return n >= 0 ? `+${n}` : `${n}`; }
function slugify(s) { return String(s || '').toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '').slice(0, 60); }

const TIER_TEXT = { full_success: 'Full success', partial_success: 'Success with a cost', failure: 'Things go wrong' };

// ---------------------------------------------------------------- ruleset lookups
function R() { return state.ruleset || {}; }
function talentDef(id) { return (R().talents || []).find(t => t.id === id); }
function talentName(id) { const t = talentDef(id); return t ? t.name : cap(String(id || '').replace(/_/g, ' ')); }
function classDef(id) { return (R().classes || []).find(c => c.id === id); }
function domainDef(id) { return (R().magic_domains || []).find(d => d.id === id); }
function domainName(id) { const d = domainDef(id); return d ? d.name : id; }
function itemDef(id) { return (R().items || []).find(i => i.id === id); }
function facetDef(id) { return (R().facets || []).find(f => f.id === id); }
function statName(id) { const s = (R().stats || []).find(x => x.id === id); return s ? s.name : cap(id); }
function difficultyLabels() { return ((R().roll_resolution || {}).difficulty_modifiers || []).map(d => d.label); }
function onMenuOf(t, facet) { return t.facet === facet || (t.shared_with || []).includes(facet); }
function isCastingTalent(t) { return !!(t && t.effects && t.effects.grants_tradition); }

// ---------------------------------------------------------------- dice + rolls
function diceHtml(dice, kept, cls) {
  const keep = (kept || []).slice();
  return `<span class="dice">${(dice || []).map(d => {
    const i = keep.indexOf(d);
    const k = i >= 0; if (k) keep.splice(i, 1);
    return `<span class="die ${cls || ''} ${k ? '' : 'drop'}">${esc(d)}</span>`;
  }).join('')}</span>`;
}

function rollLine(roll) {
  if (!roll) return '';
  const mods = [];
  if (roll.stat) mods.push(`${statName(roll.stat)} ${signed(roll.stat_value)}`);
  if (roll.knack) mods.push('knack +1');
  if (roll.bonus) mods.push(`bonus ${signed(roll.bonus)}`);
  if (roll.difficulty && roll.difficulty !== 'Standard') mods.push(`${roll.difficulty} ${signed(roll.difficulty_modifier)}`);
  const extras = [];
  if (roll.sparks) extras.push(`${roll.sparks} Spark${roll.sparks > 1 ? 's' : ''}`);
  if (roll.help) extras.push('Help');
  if (roll.borrowed_trouble) extras.push('Borrowed Trouble');
  const nat = roll.natural_high ? '<span class="chip gold">Natural 12: name something more</span>'
    : (roll.natural_low ? '<span class="chip bad">Natural 2</span>' : '');
  return `<div class="line">${diceHtml(roll.dice, roll.kept)}
      <span class="total">${esc(roll.total)}</span>
      <span class="tier ${esc(roll.outcome)}">${esc(TIER_TEXT[roll.outcome] || roll.outcome_label)}</span> ${nat}</div>
    <div class="note">${esc(mods.join(' · '))}${extras.length ? ' · extra dice: ' + esc(extras.join(', ')) : ''}${roll.capped ? ' · capped at +4' : ''}</div>
    ${roll.graceful_fail_reason === 'natural_2' ? '<div class="note">The natural 2 confirms the Graceful Fail: a Spark, and the player narrates.</div>' : ''}`;
}

// ---------------------------------------------------------------- bars and pips
function hpBar(cur, max, thin) {
  const pct = max ? Math.max(0, Math.min(100, Math.round(100 * cur / max))) : 0;
  const cls = pct <= 25 ? 'low' : (pct <= 50 ? 'half' : '');
  return `<div class="bar ${thin ? 'thin' : ''} ${cls}"><span style="width:${pct}%"></span></div>`;
}

function sparkPips(n, base) {
  const total = Math.max(n, base || 3);
  let out = '';
  for (let i = 0; i < total; i++) out += `<span class="spark ${i < n ? 'lit' : ''}"></span>`;
  return `<span class="sparks" title="${n} Spark${n === 1 ? '' : 's'}">${out}</span>`;
}

function usePips(left, allowed) {
  if (left === null || left === undefined) return '';
  const total = Math.max(allowed || 1, left);
  let out = '';
  for (let i = 0; i < total; i++) out += `<span class="use-pip ${i < left ? 'full' : ''}"></span>`;
  return `<span class="uses" title="${left} use${left === 1 ? '' : 's'} left">${out}</span>`;
}

function statusChip(status) {
  if (!status || status === 'ok') return '';
  const map = { out: ['cost', 'Out of the fight'], dying: ['bad', 'Dying'], dead: ['bad', 'Dead'] };
  const [cls, text] = map[status] || ['info', status];
  return `<span class="chip ${cls}">${text}</span>`;
}

function useLabel(use) {
  return { passive: 'always on', at_will: 'at will', once_per_scene: 'once a scene', once_per_session: 'once a session', once_per_rest: 'once a rest' }[use] || use;
}

// ---------------------------------------------------------------- slots grid
/** The slots grid: items (a 2-slot item spans two boxes), Wounds, Fatigue, coin, free space. */
function slotsGrid(ch) {
  const d = ch.derived || {};
  const total = d.slots_total || 0;
  const boxes = [];
  (ch.inventory || []).forEach(it => {
    const n = it.slots ?? 1;
    const eq = ch.equipped || {};
    const worn = eq.weapon === it.id || (it.armor && it.armor !== 'shield' && eq.armor === it.armor) || (it.armor === 'shield' && eq.shield);
    for (let i = 0; i < n; i++) {
      boxes.push(`<div class="slot item ${i ? 'cont' : ''}"><span>${i ? '↳ ' : ''}${esc(it.name || it.id)}${worn && !i ? ' <span class="tiny muted">(in hand)</span>' : ''}</span>
        ${it.usage_die && !i ? `<span class="ud">d${esc(it.usage_die)}</span>` : ''}</div>`);
    }
  });
  (ch.wounds || []).forEach(w => boxes.push(`<div class="slot wound"><b>Wound</b><span>${esc(w.name)}</span></div>`));
  for (let i = 0; i < (ch.fatigue || 0); i++) boxes.push('<div class="slot fatigue"><b>Fatigue</b><span class="tiny">clears on a night\'s rest</span></div>');
  const coinSlots = Math.floor((ch.coin || 0) / (((R().slots || {}).coin_per_slot) || 100));
  for (let i = 0; i < coinSlots; i++) boxes.push('<div class="slot coin"><b>Coin</b></div>');
  const out = boxes.map((b, i) => i >= total ? b.replace('class="slot', 'class="slot over') : b);
  for (let i = boxes.length; i < total; i++) out.push('<div class="slot empty">free</div>');
  return `<div class="slots">${out.join('')}</div>`;
}

// ---------------------------------------------------------------- toasts + dialogs
function notify(message, kind, ms) {
  const host = $('#toast-host');
  if (!host) return;
  const el = document.createElement('div');
  el.className = `toast ${kind || ''}`;
  el.textContent = message;
  host.appendChild(el);
  setTimeout(() => el.remove(), ms || 5000);
}

/** A modal. `body` is HTML; `buttons` is [{label, cls, value}]. Resolves with the clicked value (null on Escape). */
function modal(title, body, buttons, onMount) {
  return new Promise(resolve => {
    const host = $('#modal-host');
    const wrap = document.createElement('div');
    wrap.className = 'backdrop';
    wrap.innerHTML = `<div class="modal" role="dialog" aria-modal="true"><h2>${esc(title)}</h2><div class="modal-body">${body}</div>
      <div class="actions">${(buttons || [{ label: 'OK', cls: 'primary', value: true }]).map((b, i) =>
        `<button class="btn ${b.cls || ''}" data-i="${i}">${esc(b.label)}</button>`).join('')}</div></div>`;
    host.appendChild(wrap);
    const close = v => { wrap.remove(); document.removeEventListener('keydown', onKey); resolve(v); };
    const onKey = e => { if (e.key === 'Escape') close(null); };
    document.addEventListener('keydown', onKey);
    $$('.actions button', wrap).forEach(btn => btn.addEventListener('click', () => {
      const b = buttons[Number(btn.dataset.i)];
      close(typeof b.value === 'function' ? b.value(wrap) : b.value);
    }));
    if (onMount) onMount(wrap, close);
    const f = $('input, select, textarea, .btn.primary', wrap);
    if (f) f.focus();
  });
}

async function confirmDialog(title, body, label) {
  return !!(await modal(title, `<p>${esc(body)}</p>`, [{ label: 'Cancel', value: false }, { label: label || 'OK', cls: 'primary', value: true }]));
}

function formatApiError(detail, fallback) {
  if (!detail) return fallback;
  if (typeof detail === 'string') return detail;
  if (detail.errors) return detail.errors.join(' ');
  if (Array.isArray(detail)) return detail.map(d => d.msg || JSON.stringify(d)).join(' ');
  return fallback;
}

async function apiFetch(url, method, body) {
  const opts = { method: method || 'GET', headers: { 'Content-Type': 'application/json' } };
  if (state.token) opts.headers.Authorization = `Bearer ${state.token}`;
  if (body !== undefined) opts.body = JSON.stringify(body);
  return fetch(url, opts);
}

/** Toggle chip markup, wired by the delegated click handler in app.js. */
function toggleChip(key, label, on, extra) {
  return `<span class="toggle ${on ? 'on' : ''}" data-toggle="${esc(key)}" ${extra || ''}>${esc(label)}</span>`;
}

function segmented(key, options, current) {
  return `<span class="seg" data-seg="${esc(key)}">${options.map(o => {
    const v = typeof o === 'string' ? o : o.value; const l = typeof o === 'string' ? o : o.label;
    return `<button type="button" data-v="${esc(v)}" class="${v === current ? 'on' : ''}" ${o.disabled ? 'disabled' : ''}>${esc(l)}</button>`;
  }).join('')}</span>`;
}

function stepper(key, value, max) {
  return `<span class="stepper" data-stepper="${esc(key)}" data-max="${max}"><button type="button" data-d="-1">−</button><span>${value}</span><button type="button" data-d="1">+</button></span>`;
}
