/**
 * Facets of Origin — the Tools tab: the rules reference (rendered from the
 * ruleset the server loaded, so it always matches the engine), inventory and
 * notes.
 */

function renderTools() {
  const root = $('#tab-tools');
  const sub = uiv('toolsSub', 'rules');
  const tabs = `<div class="subtabs"><button data-tsub="rules" class="${sub === 'rules' ? 'on' : ''}">Rules reference</button>
    <button data-tsub="inventory" class="${sub === 'inventory' ? 'on' : ''}">Inventory</button><button data-tsub="notes" class="${sub === 'notes' ? 'on' : ''}">Notes</button></div>`;
  let body = '';
  if (sub === 'rules') body = rulesHtml();
  else if (sub === 'inventory') body = inventoryHtml();
  else body = notesHtml();
  root.innerHTML = tabs + body;
  $$('[data-tsub]', root).forEach(b => b.onclick = () => { ui.toolsSub = b.dataset.tsub; renderTools(); });
  if (sub === 'rules') wireRules(root);
  else if (sub === 'inventory') wireInventory(root);
  else wireNotes(root);
}

// =====================================================================
// Rules reference
// =====================================================================
const REF_SECTIONS = [
  ['rolling', 'Rolling the dice'], ['sparks', 'Sparks'], ['combat', 'Combat'], ['harm', 'Harm, 0 HP and rest'],
  ['magic', 'Magic'], ['levels', 'Levels'], ['talents', 'Talents'], ['classes', 'Classes'], ['backgrounds', 'Backgrounds'],
  ['gear', 'Gear'], ['monsters', 'Monsters', true], ['tables', 'MM tables', true],
];

function rulesHtml() {
  const sec = uiv('refSec', 'rolling');
  const nav = REF_SECTIONS.filter(s => !s[2] || isMM()).map(([k, l]) => `<button data-ref="${k}" class="${sec === k ? 'on' : ''}">${esc(l)}</button>`).join('');
  const fn = { rolling: refRolling, sparks: refSparks, combat: refCombat, harm: refHarm, magic: refMagic, levels: refLevels,
    talents: refTalents, classes: refClasses, backgrounds: refBackgrounds, gear: refGear, monsters: refMonsters, tables: refTables }[sec] || refRolling;
  return `<div class="ref"><nav class="ref-nav">${nav}</nav><div class="panel">${fn()}</div></div>`;
}

function wireRules(root) {
  $$('[data-ref]', root).forEach(b => b.onclick = () => { ui.refSec = b.dataset.ref; renderTools(); });
  const s = $('[data-refsearch]', root);
  if (s) s.oninput = () => {
    ui.refSearch = s.value;
    const q = s.value.toLowerCase();
    $$('.ref-entry', root).forEach(el => el.classList.toggle('hidden', q && !el.textContent.toLowerCase().includes(q)));
  };
}

function table(head, rows) {
  return `<table class="t"><tr>${head.map(h => `<th>${esc(h)}</th>`).join('')}</tr>${rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join('')}</tr>`).join('')}</table>`;
}

function refRolling() {
  const rr = R().roll_resolution || {};
  const th = rr.thresholds || {};
  return `<h2>Rolling the dice</h2>
    <p>Roll <b>2d6 + a stat</b> (+${rr.knack_bonus} if one of your knacks applies; knacks never stack), adjusted by difficulty. Stat, knack and talent bonuses together never exceed <b>+${rr.bonus_cap}</b>.</p>
    ${table(['Result', 'Outcome'], (rr.outcome_tiers || []).map(t => [t.threshold ? `${t.threshold}${t.id === 'full_success' ? '+' : '–' + (th.full_success - 1)}` : `${th.partial_success - 1} or less`, `<b>${esc(t.label)}</b>: ${esc(t.description)}`]))}
    <h3>Difficulty</h3>${table(['Difficulty', 'Modifier', 'When'], (rr.difficulty_modifiers || []).map(d => [esc(d.label), signed(d.modifier), esc(d.description)]))}
    <h3>Extra dice</h3><p>Each adds a d6; you keep the best two. They stack.</p>
    ${table(['Source', 'How'], [['Spark', esc((R().spark || {}).mechanic?.description || '')], ['Help', `An ally's action adds ${rr.help?.extra_dice} die (max ${rr.help?.max_per_roll}). They share your cost.`],
      ['Borrowed Trouble', `Accept a complication that happens whatever the roll, for ${rr.borrowed_trouble?.extra_dice} die (max ${rr.borrowed_trouble?.max_per_roll} per roll).`]])}
    <h3>Naturals</h3><p><b>${esc(rr.critical?.label)}:</b> ${esc(rr.critical?.description)}</p><p><b>${esc(rr.fumble?.label)}:</b> ${esc(rr.fumble?.description)}</p>
    <h3>Avoid</h3><p>The old saving throw: 2d6 + the stat that fits what is acting on you.</p>
    ${table(['Result', ''], Object.entries(rr.avoid?.outcomes || {}).map(([k, v]) => [esc(TIER_TEXT[k] || k), esc(v)]))}`;
}

function refSparks() {
  const sp = R().spark || {};
  return `<h2>Sparks</h2><p>Everyone starts each session with <b>${sp.base_sparks_per_session}</b>. Unspent Sparks do not carry over.</p>
    <p>${esc(sp.mechanic?.description || '')}</p><h3>Earning Sparks</h3>
    ${(sp.earn_methods || []).map(m => `<div class="ref-entry"><h4>${esc(m.label)}</h4><div class="small">${esc(m.description)}</div></div>`).join('')}`;
}

function refCombat() {
  const c = R().combat || {};
  const eq = R().equipment || {};
  const opts = c.options || {};
  const ea = c.enemy_attack || {};
  return `<h2>Combat</h2><p>A fight runs in <b>exchanges</b>: the MM telegraphs what each foe is about to do · players act, in any order · foes roll their attacks in the open · the MM narrates · exchange effects expire.</p>
    <h3>Attacking (2d6 + Body)</h3>
    ${table(['Result', ''], [['10+', `Deal your weapon die and pick one: ${Object.values(opts).map(o => `<b>${esc(o.label)}</b>${o.description ? ' (' + esc(o.description) + ')' : ''}`).join(' · ')}`],
      ['7–9', "Deal your weapon die, but you're <b>exposed</b>: if a foe can reach you, its next attack on you this exchange rolls an extra die (keep the best two)."],
      ['6−', 'You miss, and the MM makes a move.']])}
    <h3>When foes attack</h3><p>The app rolls in the open: ${esc(ea.dice)} + the foe's attack bonus.</p>
    ${table(['Result', ''], [['10+', `${esc(ea.full_success?.label)}: damage +${ea.full_success?.damage_bonus}`], ['7–9', esc(ea.partial_success?.label)], ['6−', esc(ea.failure?.label)],
      ['Natural 12', esc(ea.natural_high)], ['Natural 2', esc(ea.natural_low)]])}
    <p><b>Defend:</b> you don't attack; attacks on you are ${esc(c.defend?.enemy_difficulty)}. <b>Intercept:</b> Defend, and attacks aimed at an ally within reach come to you.</p>
    <p><b>Armor</b> subtracts from damage (never below ${c.armor?.minimum_damage}; at most ${c.armor?.cap}).
      <b>Level gap:</b> ${(c.level_gap || []).map(g => `a foe ${g.gap}+ levels above you is ${esc(g.difficulty)}`).join('; ')}.</p>
    <h3>Weapons</h3>${table(['Category', 'Die', 'Slots', 'Examples'], Object.entries(eq.weapon_categories || {}).map(([k, w]) => [esc(cap(k)), `d${w.die}`, w.slots, esc(w.examples) + (w.notes ? ` <span class="muted">${esc(w.notes)}</span>` : '')]))}
    <h3>Armor</h3>${table(['Armor', 'Value', 'Slots', ''], Object.entries(eq.armor || {}).map(([k, a]) => [esc(cap(k)), a.armor, a.slots, esc(a.notes || '')]))}
    <h3>Damage bonus by level</h3><p>${((R().advancement || {}).damage_bonus || []).map(d => `+${d.bonus} at level ${d.level}`).join(' · ')}, on every damage roll.</p>`;
}

function refHarm() {
  const ho = R().hold_on || {};
  const rec = R().recovery || {};
  return `<h2>Harm, 0 HP and rest</h2>
    <p>At 0 HP you take a <b>Wound</b> (it fills a slot; ${esc((R().wounds || {}).effect || '')}) and roll <b>Hold On</b>: 2d6 + ${esc(statName(ho.stat))}.</p>
    ${table(['Result', ''], Object.entries(ho.outcomes || {}).map(([k, v]) => [esc(TIER_TEXT[k] || k), esc(v)]))}
    <p><b>The death choice:</b> if no one tends you before the scene ends, choose a heroic final action that succeeds, or live with a permanent Scar.</p>
    <h3>Recovery</h3>${table(['Rest', 'What it restores'], [['Breather', 'A few quiet minutes: half your maximum HP. In danger, the MM rolls the Pressure die.'],
      ["Night's rest", `Somewhere safe: full HP, all Fatigue cleared, ${rec.night_rest?.clears_wounds} Wound healed.`]])}`;
}

function refMagic() {
  const m = R().magic || {};
  const doms = R().magic_domains || [];
  return `<h2>Magic</h2><p>A working is <b>Domain + Intent + Scope</b>, cast with ${Object.entries(m.traditions || {}).map(([k, t]) => `${esc(statName(t.stat))} (${esc(cap(k))})`).join(' or ')}. A knack that applies adds +1.</p>
    ${table(['Scope', 'Difficulty', 'Fatigue', 'From level', 'Harm', ''], (m.scopes || []).map(s => [`<b>${esc(s.label)}</b>`, esc(s.difficulty), s.fatigue, s.min_level, esc(s.damage || '—'), esc(s.description)]))}
    <p>Fatigue fills a slot until a night's rest. No free slot, no full working. <b>Signature workings</b> are one step Easier. Heavy armor adds ${m.heavy_armor_extra_fatigue} Fatigue to a full working.
      On a 7–9 it works and you choose one of two costs; on a 6− a mishap, and the Graceful Fail applies.</p>
    <h3>Domains</h3><input type="text" data-refsearch placeholder="Search domains…" value="${inputVal('refSearch')}">
    ${doms.map(d => `<div class="ref-entry"><h4>${esc(d.name)} <span class="chip ${d.tradition === 'thaumaturgy' ? 'info' : 'magic'}">${esc(cap(d.tradition))}</span>${d.prismatic ? ' <span class="chip gold">prismatic</span>' : ''}</h4><div class="small">${esc(d.description)}</div></div>`).join('')}`;
}

function refLevels() {
  const a = R().advancement || {};
  const rows = [];
  for (let l = 2; l <= a.max_level; l++) {
    const bits = [l === a.signature_level ? 'your signature' : 'a talent, or improve one you have held a level'];
    if ((a.stat_increase_levels || []).includes(l)) bits.push('+1 to a stat');
    if ((a.signature_working_levels || []).includes(l)) bits.push('casters: another signature working');
    const db = (a.damage_bonus || []).find(d => d.level === l); if (db) bits.push(`damage +${db.bonus}`);
    const pace = (a.pacing || []).find(p => p.level === l);
    rows.push([l, bits.join(' · '), pace ? `after session ${pace.after_session}` : '']);
  }
  return `<h2>Levels</h2><p>Levels 1–${a.max_level}, called by the Mirror Master at the end of a session. Each level: HP (your grit die, or its average) plus one pick.</p>
    ${table(['Level', 'Pick', 'Default pacing'], rows)}
    <h3>The five prompts</h3><ol>${(a.prompts || []).map(p => `<li>${esc(p.text)}</li>`).join('')}</ol>`;
}

function refTalents() {
  const facets = R().facets || [];
  return `<h2>Talents</h2><p class="small muted">Options and permissions, not bonuses. Take new ones from your Facet's menu; another Facet's needs a teacher found in play.</p>
    <input type="text" data-refsearch placeholder="Search talents…" value="${inputVal('refSearch')}">
    ${facets.map(f => `<h3 class="mt">${esc(f.name)}</h3>${(R().talents || []).filter(t => t.facet === f.id).map(t => `<div class="ref-entry">
      <h4>${esc(t.name)} ${t.kind === 'signature' ? '<span class="chip gold">signature</span>' : ''} <span class="tiny muted">${esc(useLabel(t.use))}</span>${(t.shared_with || []).length ? ` <span class="chip">also ${t.shared_with.map(s => esc((facetDef(s) || {}).name || s)).join(', ')}</span>` : ''}</h4>
      <div class="small">${esc(t.text)}</div>${t.improved ? `<div class="small"><b>Improved:</b> ${esc(t.improved)}</div>` : ''}
      ${t.choose ? `<div class="tiny muted">Choose: ${esc(t.choose)}</div>` : ''}<div class="tiny muted">Normally: ${esc(t.normal)}</div></div>`).join('')}`).join('')}`;
}

function refClasses() {
  return `<h2>Classes</h2><p class="small muted">A class is a name, a one-sentence concept, a class knack, two starting talents, a kit, and at level 3 a signature. Take one of these, or write your own from your Facet's menu.</p>
    ${(R().facets || []).map(f => `<h3 class="mt">${esc(f.name)}</h3>${(R().classes || []).filter(c => c.facet === f.id).map(c => `<div class="ref-entry"><h4>${esc(c.name)}</h4>
      <div class="small"><i>${esc(c.concept)}</i></div><div class="small">Knack: <b>${esc(c.knack)}</b> · Talents: ${c.talents.map(talentName).map(esc).join(', ')} · Signature: ${esc(talentName(c.signature))}</div>
      <div class="tiny muted">Kit: ${c.kit.map(i => esc((itemDef(i) || {}).name || i)).join(', ')}</div></div>`).join('')}`).join('')}`;
}

function refBackgrounds() {
  return `<h2>Backgrounds</h2><p class="small muted">A history, a background knack and a Specialty: one narrow thing where routine or informational tasks just happen, and risky ones are Easy.</p>
    <input type="text" data-refsearch placeholder="Search backgrounds…" value="${inputVal('refSearch')}">
    ${(R().backgrounds || []).map(b => `<div class="ref-entry"><h4>${esc(b.name)}</h4><div class="small">Knack: <b>${esc(b.knack)}</b></div><div class="small">Specialty: ${esc(b.specialty)}</div></div>`).join('')}`;
}

function refGear() {
  const eq = R().equipment || {};
  const ud = (R().exploration || {}).usage_die || {};
  const sl = R().slots || {};
  return `<h2>Gear</h2><p>You carry ${sl.base} + ${esc(statName(sl.plus_stat))} slots. Most items take 1 (heavy armor and heavy weapons 2); Wounds and Fatigue take slots too; ${sl.coin_per_slot} coin fills a slot. Carry at most ${sl.curio_limit} curios.</p>
    <p><b>Usage die:</b> ${(ud.steps || []).map(s => 'd' + s).join(' → ')} → gone. Roll it after a scene of use; a ${(ud.steps_down_on || []).join(' or ')} steps it down.</p>
    ${table(['Item', 'Slots', ''], (R().items || []).map(i => [esc(i.name), i.slots, [i.weapon ? `${i.weapon} weapon, d${(eq.weapon_categories || {})[i.weapon]?.die}` : '', i.armor ? `${i.armor} armor` : '', i.usage_die ? `usage d${i.usage_die}` : '', i.curio ? 'curio' : ''].filter(Boolean).map(esc).join(' · ')]))}
    <h3>Prices</h3>${table(['', 'Coin', 'For example'], (eq.price_guide || []).map(p => [esc(p.label), p.coin, esc(p.examples)]))}`;
}

function refMonsters() {
  const m = R().monsters || {};
  return `<h2>Monsters</h2><p>One dial and a role. Level sets HP, damage and attack; the role adjusts them.</p>
    ${table(['Level', 'HP', 'Damage', 'Attack'], (m.level_table || []).map(r => [r.level, r.hp, r.damage, signed(r.attack)]))}
    ${table(['Role', 'HP', 'Damage', 'Attack', 'Attacks', ''], Object.entries(m.roles || {}).map(([k, r]) => [esc(cap(k)), r.hp_mult ? `×${r.hp_mult}` : 'drops to any hit',
      signed(r.damage_mod), signed(r.attack_mod), r.attacks, [r.mob ? `mob: +${r.mob_damage_per_extra} damage per extra (max +${r.mob_damage_cap})` : '', r.bloodied_phase ? 'changes phase when Bloodied' : ''].filter(Boolean).join(' · ')]))}
    <p><b>Morale:</b> at a trigger (${(m.morale?.triggers || []).map(t => t.replace(/_/g, ' ')).join(', ')}) roll 2d6; over the foe's morale it breaks. Default ${m.morale?.default}; ${m.morale?.fearless} is fearless.</p>`;
}

function refTables() {
  const tables = Object.values(R().tables || {});
  return `<h2>MM tables</h2><input type="text" data-refsearch placeholder="Search tables…" value="${inputVal('refSearch')}">
    ${tables.map(t => `<div class="ref-entry"><h4>${esc(t.name)} <span class="chip">${esc(t.die)}</span></h4><div class="small muted">${esc(t.use || '')}</div>
      <details><summary class="small">Entries</summary>${table([t.die, 'Result'], (t.entries || []).map(e => [esc(e.roll), esc(e.text)]))}</details></div>`).join('')}`;
}

// =====================================================================
// Inventory
// =====================================================================
function invTarget() {
  if (!isMM()) return state.me;
  const p = uiv('invPlayer') || Object.keys(state.chars)[0];
  return state.chars[p] || null;
}

function inventoryHtml() {
  const ch = invTarget();
  const picker = isMM() ? `<div class="row gap mb"><span class="label" style="margin:0">Character</span><select data-invplayer style="width:auto">${Object.values(state.chars).map(c => `<option value="${esc(c.player_name)}" ${ch && ch.player_name === c.player_name ? 'selected' : ''}>${esc(c.name)}</option>`).join('')}</select></div>` : '';
  if (!ch) return `<div class="panel">${picker}<div class="empty">No character yet.</div></div>`;
  if (!ui.invDraft || ui.invDraftFor !== ch.player_name) {
    ui.invDraft = (ch.inventory || []).map(i => ({ ...i }));
    ui.invEquip = { ...(ch.equipped || {}) };
    ui.invDraftFor = ch.player_name;
  }
  const items = ui.invDraft;
  const d = ch.derived || {};
  const weapons = items.filter(i => i.weapon);
  return `<div class="two-col"><div class="panel">${picker}<div class="panel-head"><h3>${esc(ch.name)}'s gear</h3><span class="right small muted">${d.slots_used}/${d.slots_total} slots · ${ch.coin} coin</span></div>
    ${items.map((it, i) => `<div class="inv-row"><input type="text" data-invname="${i}" value="${esc(it.name || it.id)}" maxlength="200">
      <input type="number" min="0" max="4" data-invslots="${i}" value="${esc(it.slots ?? 1)}" title="Slots">
      <select data-invud="${i}" title="Usage die"><option value="">no die</option>${[8, 6, 4].map(n => `<option value="${n}" ${it.usage_die === n ? 'selected' : ''}>d${n}</option>`).join('')}</select>
      <button class="btn small danger" data-invrm="${i}">×</button></div>`).join('') || '<div class="empty">Nothing carried.</div>'}
    <div class="label">In hand</div><div class="row gap">
      <select data-invweapon style="width:auto"><option value="">Unarmed</option>${weapons.map(w => `<option value="${esc(w.id)}" ${ui.invEquip.weapon === w.id ? 'selected' : ''}>${esc(w.name || w.id)}</option>`).join('')}</select>
      <select data-invarmor style="width:auto">${['none', 'light', 'heavy'].map(a => `<option value="${a}" ${ui.invEquip.armor === a ? 'selected' : ''}>${a === 'none' ? 'No armor' : cap(a) + ' armor'}</option>`).join('')}</select>
      <label class="row gap" style="text-transform:none;letter-spacing:0;margin:0"><input type="checkbox" data-invshield ${ui.invEquip.shield ? 'checked' : ''}> Shield</label></div>
    <div class="wizard-foot"><button class="btn ghost" data-invreset>Undo changes</button><span class="msg error" id="inv-err"></span><button class="btn primary" data-invsave>Save gear</button></div></div>
    <div class="panel"><h3>Add an item</h3><div class="catalog">${(R().items || []).map(it => `<button data-invadd="${esc(it.id)}">+ ${esc(it.name)}</button>`).join('')}</div>
      <div class="label">Something else</div><div class="row gap"><input type="text" data-ui="invCustom" value="${inputVal('invCustom')}" placeholder="e.g. A silver locket" class="grow" style="width:auto">
      <button class="btn small" data-invcustom>Add</button></div>
      <p class="small muted mt">Wounds and Fatigue take slots of their own; they are not listed here.</p>
      <button class="btn" data-export-inv>Download .fof</button></div></div>`;
}

function wireInventory(root) {
  const ch = invTarget();
  const sel = $('[data-invplayer]', root);
  if (sel) sel.onchange = () => { ui.invPlayer = sel.value; ui.invDraftFor = null; renderTools(); };
  if (!ch) return;
  const items = ui.invDraft;
  $$('[data-invname]', root).forEach(el => el.oninput = () => { items[Number(el.dataset.invname)].name = el.value; });
  $$('[data-invslots]', root).forEach(el => el.oninput = () => { items[Number(el.dataset.invslots)].slots = Number(el.value); });
  $$('[data-invud]', root).forEach(el => el.onchange = () => { items[Number(el.dataset.invud)].usage_die = el.value ? Number(el.value) : null; });
  $$('[data-invrm]', root).forEach(b => b.onclick = () => { items.splice(Number(b.dataset.invrm), 1); renderTools(); });
  $$('[data-invadd]', root).forEach(b => b.onclick = () => { const d = itemDef(b.dataset.invadd); items.push({ ...d }); renderTools(); });
  $('[data-invcustom]', root).onclick = () => {
    const name = (ui.invCustom || '').trim(); if (!name) return;
    items.push({ id: `${slugify(name) || 'item'}_${Date.now().toString(36).slice(-4)}`, name, slots: 1 });
    ui.invCustom = ''; renderTools();
  };
  $('[data-invweapon]', root).onchange = e => { ui.invEquip.weapon = e.target.value || null; };
  $('[data-invarmor]', root).onchange = e => { ui.invEquip.armor = e.target.value; };
  $('[data-invshield]', root).onchange = e => { ui.invEquip.shield = e.target.checked; };
  $('[data-invreset]', root).onclick = () => { ui.invDraftFor = null; renderTools(); };
  $('[data-export-inv]', root).onclick = () => exportCharacter(ch.player_name);
  $('[data-invsave]', root).onclick = async () => {
    const body = { inventory: items.map(i => ({ id: i.id, name: i.name || '', slots: i.slots ?? 1, kind: i.kind || null, usage_die: i.usage_die || null })), equipped: ui.invEquip };
    const resp = await apiFetch(`/api/characters/${state.sessionId}/${encodeURIComponent(ch.player_name)}/inventory`, 'PUT', body);
    if (!resp.ok) { $('#inv-err').textContent = formatApiError((await resp.json()).detail, 'That did not fit.'); return; }
    notify('Gear saved.', 'success');
    ui.invDraftFor = null;
    send({ type: 'character_sync', player: ch.player_name });
  };
}

// =====================================================================
// Notes
// =====================================================================
function notesHtml() {
  const ch = invTarget();
  const picker = isMM() ? `<div class="row gap mb"><span class="label" style="margin:0">Character</span><select data-invplayer style="width:auto">${Object.values(state.chars).map(c => `<option value="${esc(c.player_name)}" ${ch && ch.player_name === c.player_name ? 'selected' : ''}>${esc(c.name)}</option>`).join('')}</select></div>` : '';
  if (!ch) return `<div class="panel">${picker}<div class="empty">No character yet.</div></div>`;
  return `<div class="panel" style="max-width:800px">${picker}<h3>${esc(ch.name)}</h3>
    <label>Player notes</label><textarea data-notes-player style="min-height:12rem" maxlength="2000">${esc(ch.notes_player || '')}</textarea>
    ${isMM() ? `<label>Mirror Master notes (only you see these)</label><textarea data-notes-mm style="min-height:8rem" maxlength="2000">${esc(ch.notes_mm || '')}</textarea>` : ''}
    <div class="wizard-foot"><span></span><button class="btn primary" data-notes-save>Save notes</button></div></div>`;
}

function wireNotes(root) {
  const ch = invTarget();
  const sel = $('[data-invplayer]', root);
  if (sel) sel.onchange = () => { ui.invPlayer = sel.value; renderTools(); };
  if (!ch) return;
  $('[data-notes-save]', root).onclick = async () => {
    const body = { notes_player: $('[data-notes-player]', root).value };
    const mm = $('[data-notes-mm]', root); if (mm) body.notes_mm = mm.value;
    const resp = await apiFetch(`/api/characters/${state.sessionId}/${encodeURIComponent(ch.player_name)}/notes`, 'PUT', body);
    if (!resp.ok) return notify(formatApiError((await resp.json()).detail, 'Could not save.'), 'error');
    notify('Notes saved.', 'success');
    send({ type: 'character_sync', player: ch.player_name });
  };
}
