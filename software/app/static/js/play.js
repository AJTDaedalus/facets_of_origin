/**
 * Facets of Origin — the Play tab.
 *
 * Players: the character sheet and the action panel (roll, attack, cast,
 * defend, avoid) with Spark / Help / Borrowed Trouble dice.
 * Mirror Master: the exchange bar, the combat tracker (foes roll in the open),
 * the party, threat clocks, the Toolbox and the session controls.
 *
 * Every button sends an event; the server's engine decides what happens.
 */

function uiv(key, dflt) { return ui[key] === undefined ? dflt : ui[key]; }
function inputVal(key) { return esc(uiv(key, '')); }

function renderPlay() {
  const root = $('#play-main');
  if (isMM()) { root.innerHTML = mmPlayHtml(); wireMMPlay(root); return; }
  const me = state.me;
  if (!me) {
    root.innerHTML = `<div class="panel center"><h2>No character yet</h2><p class="muted">Build one to take your seat.</p>
      <button class="btn primary" data-go-build>Open Build</button></div>${clocksPublicHtml()}`;
    $('[data-go-build]', root).onclick = () => switchTab('build');
    return;
  }
  root.innerHTML = `${bannersHtml(me)}<div class="sheet-grid"><div>${sheetHtml(me)}</div>
    <div>${actionsHtml(me)}${partyHtml(me)}${foesPublicHtml()}${clocksPublicHtml()}</div></div>`;
  wirePlayer(root, me);
}

// =====================================================================
// Player: banners
// =====================================================================
function bannersHtml(me) {
  const out = [];
  if (me.must_hold_on) out.push(`<div class="banner bad"><div class="grow"><h3>You're at 0 HP</h3>
    <div class="small">You took a Wound. Roll Hold On (2d6 + Body): 10+ stand at 1 HP · 7–9 out of the fight · 6− dying.</div></div>
    ${stepper('holdSparks', uiv('holdSparks', 0), me.sparks)}<button class="btn primary" data-act="hold_on">Roll Hold On</button></div>`);
  if (me.status === 'dying') out.push(`<div class="banner bad"><div class="grow"><h3>You are dying</h3>
    <div class="small">An ally who tends you before the scene ends saves you. If no one does: live with a permanent Scar, or make a heroic final action that succeeds.</div></div>
    <button class="btn" data-act="death_scar">Live, with a Scar</button><button class="btn danger" data-act="death_heroic">Heroic final action</button></div>`);
  if (me.status === 'out') out.push('<div class="banner gold"><div class="grow"><h3>Out of the fight</h3><div class="small">Conscious, but done for this fight. A breather or healing brings you back.</div></div></div>');
  if (me.level_up_ready) out.push('<div class="banner gold"><div class="grow"><h3>Level up!</h3><div class="small">The Mirror Master called it. Choose your pick in Build.</div></div><button class="btn primary" data-go-build>Choose my pick</button></div>');
  if (state.pendingAttack) out.push('<div class="banner gold"><div class="grow"><h3>You rolled 10+</h3><div class="small">Pick your option to finish the attack.</div></div><button class="btn primary" data-act="reopen_pick">Pick</button></div>');
  if (state.pendingCost) out.push('<div class="banner magic"><div class="grow"><h3>The working has a cost</h3><div class="small">Choose which one you pay.</div></div><button class="btn magic" data-act="reopen_cost">Choose</button></div>');
  if (state.lastFailed) out.push(`<div class="banner gold"><div class="grow"><h3>Things went wrong</h3><div class="small">Make it worse or richer for the story, and claim a Spark. The MM confirms.</div></div>
    <button class="btn" data-act="graceful_fail">Claim a Graceful Fail</button></div>`);
  return out.join('');
}

// =====================================================================
// Player: the sheet
// =====================================================================
function sheetHtml(me) {
  const d = me.derived || {};
  const cls = me.class || {};
  const facet = facetDef(me.facet);
  const bg = me.background || {};
  const selStat = uiv('stat', facet ? facet.stat : 'body');
  const talents = (me.talents || []).map(t => talentCard(me, t.id, t)).join('');
  const sig = me.signature ? talentCard(me, me.signature, { id: me.signature, signature: true }) : '';
  return `<div class="panel">
    <div class="sheet-head"><div class="grow"><h2>${esc(me.name)}</h2>
      <div class="sheet-sub">Level ${me.level} ${esc(cls.name || '')}${cls.custom ? ' <span class="chip">custom</span>' : ''} · ${esc(facet ? facet.name : me.facet)}${me.lineage && me.lineage.id && me.lineage.id !== 'human' ? ' · ' + esc(me.lineage.id) : ''}</div>
      ${cls.concept ? `<div class="small muted"><i>${esc(cls.concept)}</i></div>` : ''}</div>
      <div class="center">${sparkPips(me.sparks, ((R().spark || {}).base_sparks_per_session) || 3)}<div class="tiny muted">Sparks</div></div></div>
    <div class="hp"><div class="hp-top"><span>HP <b>${me.hp ? me.hp.current : 0}</b> / ${d.hp_max}</span> ${statusChip(me.status)}
      <span>Armor ${d.armor} · weapon d${d.weapon_die}${d.damage_bonus ? ` +${d.damage_bonus}` : ''}</span></div>${hpBar(me.hp ? me.hp.current : 0, d.hp_max)}</div>
    <div class="stats">${(R().stats || []).map(s => `<div class="stat ${selStat === s.id ? 'on' : ''}" data-stat="${esc(s.id)}" title="${esc(s.description)}">
      <div class="v">${signed(me.stats[s.id])}</div><div class="n">${esc(s.name)}</div></div>`).join('')}</div>
    <div class="label">Knacks <span class="dim">(+1 when one applies; they never stack)</span></div>
    <div class="knacks">${(me.knacks || []).map(k => `<span class="chip gold">${esc(k)}</span>`).join('')}</div>
    ${me.specialty ? `<div class="label">Specialty</div><div class="small">${esc(me.specialty)}</div>` : ''}
    ${bg.name ? `<div class="small muted mt">Background: ${esc(bg.name)}</div>` : ''}
  </div>
  <div class="panel"><h3>Talents</h3>${talents || '<div class="empty">None yet.</div>'}${sig}</div>
  ${me.magic ? magicPanel(me) : ''}
  ${me.gifted && me.gift_domain ? `<div class="panel"><h3>Lineage gift</h3><div class="small">Minor workings in ${esc(domainName(me.gift_domain))}, cast with Soul, free.</div></div>` : ''}
  <div class="panel"><div class="panel-head"><h3>Slots</h3><span class="right small muted">${d.slots_used} / ${d.slots_total} used · ${me.coin} coin</span></div>
    ${d.items_to_drop ? `<div class="banner bad small">Over by ${d.items_to_drop}: drop ${d.items_to_drop} item${d.items_to_drop > 1 ? 's' : ''} (Tools → Inventory).</div>` : ''}
    ${slotsGrid(me)}
    ${usageButtons(me)}
    ${(me.scars || []).length ? `<div class="label">Scars</div>${me.scars.map(s => `<span class="chip bad">${esc(s.name)}</span>`).join(' ')}` : ''}
    ${(me.wounds || []).length ? `<div class="small muted mt">Rolls that strain a Wound are Hard. A night's rest heals one.</div>` : ''}
  </div>`;
}

function talentCard(me, id, st) {
  const t = talentDef(id);
  if (!t) return '';
  const left = (me.talent_uses_left || {})[id];
  const tracked = left !== undefined && left !== null;
  return `<div class="talent"><div class="talent-top"><span class="talent-name">${esc(t.name)}</span>
    ${st.signature ? '<span class="chip gold">signature</span>' : ''}${st.improved ? '<span class="chip good">improved</span>' : ''}
    ${st.choice ? `<span class="chip">${esc(domainDef(st.choice) ? domainName(st.choice) : st.choice)}</span>` : ''}
    <span class="tiny muted">${esc(useLabel(t.use))}</span>
    <span class="right row gap">${tracked ? usePips(left, 1) : ''}${tracked ? `<button class="btn small" data-use="${esc(id)}" ${left < 1 ? 'disabled' : ''}>Use</button>` : ''}</span></div>
    <div class="talent-text">${esc(st.improved && t.improved ? t.improved : t.text)}</div></div>`;
}

function magicPanel(me) {
  const m = me.magic;
  return `<div class="panel"><h3>Magic <span class="chip magic">${esc(cap(m.tradition))}</span></h3>
    <div class="small">Domain${m.domains.length > 1 ? 's' : ''}: ${m.domains.map(d => `<b>${esc(domainName(d))}</b>`).join(', ')} · cast with ${esc(statName(((R().magic || {}).traditions || {})[m.tradition]?.stat || 'mind'))}</div>
    <div class="label">Signature workings <span class="dim">(one step Easier)</span></div>
    <div class="knacks">${(m.signature_workings || []).map(w => `<span class="chip magic">${esc(w)}</span>`).join('')}</div>
    <div class="small muted mt">Fatigue: <b>${me.fatigue}</b>. Each fills a slot until a night's rest. No free slot, no full working.</div></div>`;
}

function usageButtons(me) {
  const items = (me.inventory || []).filter(i => i.usage_die);
  if (!items.length) return '';
  return `<div class="label">Usage dice <span class="dim">(roll after a scene of use; 1–2 steps it down)</span></div>
    <div class="row gap">${items.map(i => `<button class="btn small" data-usage="${esc(i.id)}">${esc(i.name)} d${i.usage_die}</button>`).join('')}</div>`;
}

// =====================================================================
// Player: actions
// =====================================================================
function actionsHtml(me) {
  const act = uiv('act', 'roll');
  const canAct = me.status === 'ok' && !(me.hp && me.hp.current === 0);
  const tabs = [['roll', 'Roll'], ['attack', 'Attack'], ['cast', 'Cast'], ['defend', 'Defend'], ['avoid', 'Avoid']]
    .filter(([k]) => k !== 'cast' || me.magic || (me.gifted && me.gift_domain));
  let body = '';
  if (act === 'roll') body = rollForm(me);
  else if (act === 'attack') body = attackForm(me);
  else if (act === 'cast') body = castForm(me);
  else if (act === 'defend') body = defendForm(me);
  else body = avoidForm(me);
  return `<div class="panel"><div class="action-tabs">${tabs.map(([k, l]) => `<button class="btn small ${act === k ? 'on' : ''}" data-actab="${k}">${l}</button>`).join('')}</div>
    ${!canAct ? '<div class="small muted mb">You are down: only Hold On, the death choice, or Avoid are open to you.</div>' : ''}${body}</div>`;
}

function diceOpts(me, withDiff) {
  return `${withDiff ? `<div class="label">Difficulty</div>${segmented('diff', difficultyLabels(), uiv('diff', 'Standard'))}` : ''}
    <div class="label">Extra dice <span class="dim">(each adds a d6; keep the best two)</span></div>
    <div class="dice-opts">${toggleChip('knack', 'A knack applies (+1)', uiv('knack', false))}
      <span class="toggle ${uiv('sparks', 0) ? 'on' : ''}">Sparks ${stepper('sparks', Math.min(uiv('sparks', 0), me.sparks), me.sparks)}</span>
      ${toggleChip('help', 'Help', uiv('help', false))}${toggleChip('bt', 'Borrowed Trouble', uiv('bt', false))}</div>
    ${uiv('help', false) ? `<select data-ui="helper">${Object.values(state.chars).filter(c => c.player_name !== myName()).map(c =>
      `<option value="${esc(c.name)}" ${uiv('helper') === c.name ? 'selected' : ''}>${esc(c.name)} helps (and shares the cost)</option>`).join('')}</select>` : ''}`;
}

function statSeg() {
  return segmented('stat', (R().stats || []).map(s => ({ value: s.id, label: s.name })), uiv('stat', facetDef(state.me.facet)?.stat || 'body'));
}

function rollForm(me) {
  return `<div class="label">Stat</div>${statSeg()}${diceOpts(me, true)}
    <div class="label">What are you trying?</div><input type="text" data-ui="desc" value="${inputVal('desc')}" maxlength="200" placeholder="e.g. climb the chapel wall">
    <button class="btn primary block go" data-act="roll">Roll 2d6 + ${esc(statName(uiv('stat', facetDef(me.facet)?.stat || 'body')))}</button>`;
}

function foeOptions(selected, includeNone) {
  const foes = Object.values(state.enemies).filter(e => !e.defeated && !e.broken);
  return `${includeNone ? `<option value="">No listed foe</option>` : ''}${foes.map(e =>
    `<option value="${esc(e.key)}" ${selected === e.key ? 'selected' : ''}>${esc(e.name)} (level ${e.level} ${esc(e.role)}${e.role === 'mook' && e.count > 1 ? ' ×' + e.count : ''})</option>`).join('')}`;
}

function attackForm(me) {
  const opts = ((R().combat || {}).options) || {};
  const pre = uiv('preopt', '');
  const hasBrawler = (me.talents || []).some(t => t.id === 'brawler');
  const ranged = me.derived && me.derived.ranged;
  const foes = Object.values(state.enemies).filter(e => !e.defeated && !e.broken);
  if (!uiv('target') && foes.length) ui.target = foes[0].key;
  return `<div class="label">Target</div><select data-ui="target">${foeOptions(uiv('target', ''), true)}</select>
    <div class="small muted mt">2d6 + Body. 10+ weapon die and pick one · 7–9 weapon die, but you're exposed · 6− a miss, and the MM makes a move.</div>
    ${diceOpts(me, true)}
    <div class="label">On a 10+</div>${segmented('preopt', [{ value: '', label: 'Decide after' }, ...Object.entries(opts).map(([k, o]) => ({ value: k, label: o.label }))], pre)}
    ${pre === 'cover' ? `<select data-ui="coverAlly" class="mt">${allyOptions(uiv('coverAlly'))}</select>` : ''}
    <div class="dice-opts">${hasBrawler ? toggleChip('brawling', 'Brawling (bare hands)', uiv('brawling', false)) : ''}
      ${ranged ? toggleChip('inCover', 'Target is in cover', uiv('inCover', false)) : ''}</div>
    <button class="btn primary block go" data-act="attack">Attack</button>`;
}

function allyOptions(sel) {
  return Object.values(state.chars).filter(c => c.player_name !== myName()).map(c =>
    `<option value="${esc(c.name)}" ${sel === c.name ? 'selected' : ''}>${esc(c.name)}</option>`).join('');
}

function castDomains(me) {
  const doms = (me.magic ? me.magic.domains : []).slice();
  if (me.gifted && me.gift_domain && !doms.includes(me.gift_domain)) doms.push(me.gift_domain);
  return doms;
}

function castForm(me) {
  const doms = castDomains(me);
  if (!uiv('domain') || !doms.includes(ui.domain)) ui.domain = doms[0];
  const scopes = ((R().magic || {}).scopes) || [];
  const scope = uiv('scope', 'minor');
  const sc = scopes.find(s => s.id === scope) || {};
  const workings = me.magic ? me.magic.signature_workings : [];
  const improvedCaster = (me.talents || []).some(t => isCastingTalent(talentDef(t.id)) && t.improved);
  const foes = Object.values(state.enemies).filter(e => !e.defeated && !e.broken);
  const harm = uiv('harm', false);
  return `<div class="label">Domain</div>${segmented('domain', doms.map(d => ({ value: d, label: domainName(d) })), ui.domain)}
    <div class="label">Scope</div>${segmented('scope', scopes.map(s => ({ value: s.id, label: `${s.label} · ${s.fatigue} Fatigue`, disabled: me.level < s.min_level })), scope)}
    <div class="small muted mt">${esc(sc.description || '')}</div>
    <div class="label">Working</div><select data-ui="working"><option value="">Something new (not a signature working)</option>
      ${workings.map(w => `<option ${uiv('working') === w ? 'selected' : ''}>${esc(w)}</option>`).join('')}</select>
    <div class="label">Intent</div><input type="text" data-ui="intent" value="${inputVal('intent')}" maxlength="300" placeholder="What should it do?">
    <div class="dice-opts">${sc.damage ? toggleChip('harm', `Harm (${sc.damage}${sc.targets === 'group' ? ' to a group' : ''})`, harm) : ''}
      ${improvedCaster ? toggleChip('reduceFatigue', '−1 Fatigue (once a scene)', uiv('reduceFatigue', false)) : ''}
      ${me.signature === 'miracle' && scope === 'major' ? toggleChip('miracle', 'Miracle: no Fatigue', uiv('miracle', false)) : ''}</div>
    ${harm && sc.damage ? (sc.targets === 'group'
      ? `<div class="label">Foes caught in it</div>${foes.map(e => `<label class="row gap" style="text-transform:none;letter-spacing:0"><input type="checkbox" data-group="${esc(e.key)}" ${(ui.group || []).includes(e.key) ? 'checked' : ''}> ${esc(e.name)}</label>`).join('') || '<div class="empty">No foes on the tracker.</div>'}`
      : `<div class="label">Target</div><select data-ui="castTarget">${foeOptions(uiv('castTarget', ''), true)}</select>`) : ''}
    ${diceOpts(me, false)}
    <div id="cast-plan" class="plan subtle">${ui.lastPlan ? castPlanHtml(ui.lastPlan) : 'Working out the cost…'}</div>
    <button class="btn magic block go" data-act="cast" ${ui.lastPlan && !ui.lastPlan.ok ? 'disabled' : ''}>Cast</button>`;
}

function castPayload(me) {
  const sig = ui.working ? true : null;
  const intentText = (ui.intent || '').trim();
  const harm = uiv('harm', false);
  const p = { domain: ui.domain, scope: uiv('scope', 'minor'), working: ui.working || null, signature: sig,
    intent: harm && !/^harm/i.test(intentText) ? `harm: ${intentText}` : intentText,
    reduce_fatigue: !!ui.reduceFatigue, miracle: !!ui.miracle };
  const sc = (((R().magic || {}).scopes) || []).find(s => s.id === p.scope) || {};
  if (harm && sc.damage) {
    if (sc.targets === 'group') p.targets = (ui.group || []).filter(k => state.enemies[k]);
    else if (ui.castTarget) p.target = ui.castTarget;
  }
  return p;
}

let _previewTimer = null;
function requestCastPreview() {
  clearTimeout(_previewTimer);
  _previewTimer = setTimeout(() => {
    if (!state.me || uiv('act') !== 'cast' || !ui.domain) return;
    const p = castPayload(state.me);
    send({ type: 'cast_preview', domain: p.domain, scope: p.scope, working: p.working, signature: p.signature,
      reduce_fatigue: p.reduce_fatigue, miracle: p.miracle });
  }, 120);
}

function castPlanHtml(plan) {
  return plan.ok
    ? `Rolls <b>2d6 + ${esc(statName(plan.stat))}</b> at <b>${esc(plan.difficulty)}</b> · costs <b>${plan.fatigue} Fatigue</b>${plan.gift ? ' · lineage gift' : ''}${plan.steps.length ? `<div class="tiny muted">${plan.steps.map(esc).join(' · ')}</div>` : ''}`
    : `<span class="msg error">${plan.errors.map(esc).join(' ')}</span>`;
}

function showCastPlan(plan) {
  ui.lastPlan = plan;
  const el = $('#cast-plan');
  if (!el) return;
  el.innerHTML = castPlanHtml(plan);
  const btn = $('[data-act="cast"]');
  if (btn) btn.disabled = !plan.ok;
}

function defendForm(me) {
  const sentinel = (me.talents || []).some(t => t.id === 'sentinel') || me.signature === 'sentinel';
  const allies = Object.values(state.chars).filter(c => c.player_name !== myName());
  const inFight = !!state.combat;
  return `<div class="small muted">No attack this exchange: attacks on you are Hard.
      <b>Intercept</b> also pulls attacks aimed at an ally within reach onto you${sentinel ? ' (Sentinel: every ally in reach)' : ''}.</div>
    ${allies.length ? `<div class="label">Intercept for</div>${allies.map(c => `<label class="row gap" style="text-transform:none;letter-spacing:0">
      <input type="checkbox" data-intercept="${esc(c.name)}" ${(ui.intercept || []).includes(c.name) ? 'checked' : ''}> ${esc(c.name)}</label>`).join('')}` : ''}
    ${!inFight ? '<div class="small msg error">No fight is running.</div>' : ''}
    <button class="btn primary block go" data-act="defend" ${inFight ? '' : 'disabled'}>${(ui.intercept || []).length ? 'Intercept' : 'Defend'}</button>`;
}

function avoidForm(me) {
  return `<div class="small muted">The avoid roll: 2d6 + the stat that fits what is acting on you. 10+ avoid it · 7–9 the worst of it · 6− it takes hold.</div>
    <div class="label">Stat</div>${statSeg()}${diceOpts(me, true)}
    <div class="label">What are you avoiding?</div><input type="text" data-ui="avoidDesc" value="${inputVal('avoidDesc')}" maxlength="200" placeholder="e.g. the collapsing floor">
    <button class="btn primary block go" data-act="avoid">Avoid</button>`;
}

function extraDice(me) {
  const d = { sparks: Math.min(uiv('sparks', 0), me.sparks), help: ui.help ? 1 : 0, borrowed_trouble: !!ui.bt, knack: !!ui.knack };
  if (ui.help) d.helper = ui.helper || (Object.values(state.chars).find(c => c.player_name !== myName()) || {}).name;
  return d;
}

function resetExtra() { ui.sparks = 0; ui.help = false; ui.bt = false; ui.knack = false; }

// =====================================================================
// Player: party, foes, clocks
// =====================================================================
function partyHtml(me) {
  const others = Object.values(state.chars).filter(c => c.player_name !== myName());
  if (!others.length) return '';
  return `<div class="panel"><h3>The party</h3><div class="party">${others.map(c => `<div class="pc ${c.status === 'dying' ? 'dying' : ''}">
    <div class="pc-top"><span class="pc-name">${esc(c.name)}</span><span class="tiny muted">L${c.level} ${esc((c.class || {}).name || '')}</span>${statusChip(c.status)}</div>
    <div class="hp-top tiny"><span>HP ${c.hp.current}/${c.derived.hp_max}</span>${sparkPips(c.sparks, 3)}</div>${hpBar(c.hp.current, c.derived.hp_max, true)}
    <div class="row gap mt"><button class="btn small" data-peer="${esc(c.player_name)}">Spark?</button>
      <button class="btn small ghost" data-nominate="${esc(c.player_name)}" title="Act break nomination">Nominate</button>
      ${c.status === 'dying' ? `<button class="btn small good" data-tend="${esc(c.player_name)}">Tend</button>` : ''}</div></div>`).join('')}</div></div>`;
}

function foesPublicHtml() {
  const foes = Object.values(state.enemies);
  if (!foes.length && !state.combat) return '';
  const tg = (state.combat || {}).telegraphs || {};
  return `<div class="panel"><div class="panel-head"><h3>Foes</h3>${state.combat ? `<span class="chip gold right">Exchange ${state.combat.exchange}</span>` : ''}</div>
    ${foes.length ? foes.map(e => `<div class="lib-row"><span class="grow"><b>${esc(e.name)}</b> <span class="tiny muted">level ${e.level} ${esc(e.role)}${e.role === 'mook' ? ` · ${e.count} standing` : ''}</span>
      ${tg[e.key] ? `<div class="small">About to: <i>${esc(tg[e.key])}</i></div>` : ''}</span>
      ${e.bloodied && !e.defeated ? '<span class="chip bad">Bloodied</span>' : ''}${e.broken ? '<span class="chip cost">Broken</span>' : ''}${e.defeated ? '<span class="chip good">Down</span>' : ''}</div>`).join('')
    : '<div class="empty">No foes in sight.</div>'}</div>`;
}

function clocksPublicHtml() {
  const clocks = Object.values(state.clocks);
  if (!clocks.length) return '';
  return `<div class="panel"><h3>Threat clocks</h3><div class="clocks">${clocks.map(clockHtml).join('')}</div></div>`;
}

function clockHtml(c, mm) {
  let segs = '';
  for (let i = 0; i < c.segments; i++) segs += `<span class="clock-seg ${i < c.filled_segments ? 'on' : ''}"></span>`;
  return `<div class="clock ${c.is_full ? 'full' : ''}"><b>${esc(c.name)}</b> <span class="tiny muted">${c.filled_segments}/${c.segments}</span>
    <div class="clock-segs">${segs}</div>
    ${mm ? `<div class="row gap"><button class="btn small" data-clock-adv="${esc(c.id)}">Tick</button><button class="btn small ghost" data-clock-back="${esc(c.id)}">Wind back</button>
      <button class="btn small danger" data-clock-del="${esc(c.id)}">×</button></div>` : ''}</div>`;
}

// =====================================================================
// Player: wiring
// =====================================================================
function wirePlayer(root, me) {
  $$('[data-go-build]', root).forEach(b => b.onclick = () => switchTab('build'));
  $$('[data-stat]', root).forEach(el => el.onclick = () => { ui.stat = el.dataset.stat; renderPlay(); });
  $$('[data-actab]', root).forEach(b => b.onclick = () => { ui.act = b.dataset.actab; renderPlay(); if (ui.act === 'cast') requestCastPreview(); });
  $$('[data-use]', root).forEach(b => b.onclick = () => send({ type: 'talent_use', talent_id: b.dataset.use }));
  $$('[data-usage]', root).forEach(b => b.onclick = () => send({ type: 'usage_roll', item: b.dataset.usage }));
  $$('[data-peer]', root).forEach(b => b.onclick = () => { send({ type: 'peer_call', player: b.dataset.peer }); notify('Called "Spark?". The MM decides.', 'spk'); });
  $$('[data-nominate]', root).forEach(b => b.onclick = () => send({ type: 'act_break_nominate', player: b.dataset.nominate }));
  $$('[data-tend]', root).forEach(b => b.onclick = () => send({ type: 'tend', target: b.dataset.tend }));
  $$('[data-group]', root).forEach(cb => cb.onchange = () => {
    ui.group = $$('[data-group]', root).filter(x => x.checked).map(x => x.dataset.group);
  });
  $$('[data-intercept]', root).forEach(cb => cb.onchange = () => {
    ui.intercept = $$('[data-intercept]', root).filter(x => x.checked).map(x => x.dataset.intercept);
    const btn = $('[data-act="defend"]', root);
    if (btn) btn.textContent = ui.intercept.length ? 'Intercept' : 'Defend';
  });
  $$('[data-act]', root).forEach(b => b.onclick = () => playerAction(b.dataset.act, me));
  if (uiv('act') === 'cast') requestCastPreview();
}

function playUiChanged(key) {
  if (!state.me || isMM()) return;
  if (['preopt', 'help', 'harm', 'scope', 'domain', 'stat'].includes(key)) { renderPlay(); }
  if (['scope', 'domain', 'working', 'reduceFatigue', 'miracle', 'harm'].includes(key)) requestCastPreview();
}

async function playerAction(act, me) {
  if (act === 'roll') {
    send({ type: 'roll', stat: uiv('stat', facetDef(me.facet)?.stat), difficulty: uiv('diff', 'Standard'), description: ui.desc || '', ...extraDice(me) });
    resetExtra(); ui.desc = ''; renderPlay();
  } else if (act === 'avoid') {
    send({ type: 'avoid', stat: uiv('stat', facetDef(me.facet)?.stat), difficulty: uiv('diff', 'Standard'), description: ui.avoidDesc || '', ...extraDice(me) });
    resetExtra(); ui.avoidDesc = ''; renderPlay();
  } else if (act === 'attack') {
    const msg = { type: 'attack', target: ui.target || null, difficulty: uiv('diff', 'Standard'), brawling: !!ui.brawling, in_cover: !!ui.inCover, ...extraDice(me) };
    if (ui.preopt) { msg.options = [ui.preopt]; if (ui.preopt === 'cover') msg.cover_ally = ui.coverAlly || (Object.values(state.chars).find(c => c.player_name !== myName()) || {}).name; }
    send(msg); resetExtra(); renderPlay();
  } else if (act === 'cast') {
    send({ type: 'cast', ...castPayload(me), ...extraDice(me) }); resetExtra(); ui.intent = ''; renderPlay();
  } else if (act === 'defend') {
    send({ type: 'defend', intercept_for: ui.intercept || [] });
  } else if (act === 'hold_on') {
    send({ type: 'hold_on', sparks: uiv('holdSparks', 0) }); ui.holdSparks = 0;
  } else if (act === 'death_scar' || act === 'death_heroic') {
    const heroic = act === 'death_heroic';
    if (await confirmDialog(heroic ? 'A heroic final action' : 'Live, with a Scar', heroic
      ? 'Your character dies, and their final action succeeds. Describe it to the table.'
      : 'You survive with a permanent Scar (rolled on the table), out of the fight.', heroic ? 'Go out a hero' : 'Take the Scar'))
      send({ type: 'death_choice', choice: heroic ? 'heroic' : 'scar' });
  } else if (act === 'graceful_fail') {
    const text = await modal('Graceful Fail', `<p class="small muted">How do you make this failure worse, or richer, for the story?</p><textarea id="gf-text" maxlength="500"></textarea>`,
      [{ label: 'Cancel', value: null }, { label: 'Claim the Spark', cls: 'primary', value: w => $('#gf-text', w).value }]);
    if (text !== null) { send({ type: 'graceful_fail', narration: text || '' }); state.lastFailed = false; renderPlay(); }
  } else if (act === 'reopen_pick' && state.pendingAttack) pickOption(state.pendingAttack);
  else if (act === 'reopen_cost' && state.pendingCost) pickCost(state.pendingCost);
}

/** The 10+ picker: +1d6 damage, a stunt, or cover. */
async function pickOption(m) {
  const allowed = m.options_allowed || 1;
  const body = `<p>You rolled <b>${m.roll.total}</b>${m.target_name ? ` against ${esc(m.target_name)}` : ''}. Pick ${allowed === 1 ? 'one' : 'two'}:</p>
    ${m.choices.map(c => `<label class="row gap" style="text-transform:none;letter-spacing:0;font-size:1rem;color:var(--text)">
      <input type="${allowed === 1 ? 'radio' : 'checkbox'}" name="opt" value="${esc(c.id)}"> <b>${esc(c.label)}</b></label>
      ${c.description ? `<div class="small muted" style="margin:0 0 .4rem 1.6rem">${esc(c.description)}</div>` : ''}`).join('')}
    <div id="cover-row" class="hidden"><label>Cover which ally?</label><select id="cover-ally">${allyOptions()}</select></div>`;
  const picked = await modal('10+: pick your option', body, [{ label: 'Later', value: null },
    { label: 'Finish the attack', cls: 'primary', value: w => ({ opts: $$('input[name=opt]:checked', w).map(i => i.value), ally: ($('#cover-ally', w) || {}).value }) }],
    w => $$('input[name=opt]', w).forEach(i => i.onchange = () => $('#cover-row', w).classList.toggle('hidden', !$$('input[name=opt]:checked', w).some(x => x.value === 'cover'))));
  if (!picked) { renderPlay(); return; }
  if (!picked.opts.length) { notify('Pick an option.', 'warn'); return pickOption(m); }
  if (picked.opts.length > allowed) { notify(`Pick at most ${allowed}.`, 'warn'); return pickOption(m); }
  send({ type: 'choose_option', options: picked.opts, cover_ally: picked.ally || null });
}

async function pickCost(options) {
  const i = await modal('It works, at a cost', `<p class="small muted">Choose which cost you pay.</p>
    ${options.map((c, i) => `<label class="row gap" style="text-transform:none;letter-spacing:0;font-size:1rem;color:var(--text)"><input type="radio" name="cost" value="${i}" ${i === 0 ? 'checked' : ''}> ${esc(c.text)}</label>`).join('')}`,
    [{ label: 'Later', value: null }, { label: 'Pay this one', cls: 'magic', value: w => Number(($('input[name=cost]:checked', w) || {}).value || 0) }]);
  if (i === null) { renderPlay(); return; }
  send({ type: 'choose_complication', index: i });
  state.pendingCost = null;
  renderPlay();
}

// =====================================================================
// Mirror Master
// =====================================================================
function mmPlayHtml() {
  return `<div class="mm-grid"><div>${exchangeHtml()}${trackerHtml()}${mmPartyHtml()}</div>
    <div>${nominationsHtml()}${toolboxHtml()}${mmClocksHtml()}${sessionHtml()}${invitePanelHtml()}</div></div>`;
}

function exchangeHtml() {
  const c = state.combat;
  const dg = state.danger;
  const danger = dg ? `<span class="chip ${{ skirmish: 'good', fight: 'info', hard: 'cost', deadly: 'bad' }[dg.read] || ''}" title="${esc(dg.text)}">Danger: ${esc(cap(dg.read))}</span>` : '';
  return `<div class="panel"><div class="exchange-bar">
    ${c ? `<span class="exchange-n">Exchange ${c.exchange}</span>
      <button class="btn primary" data-mm="end_exchange">End exchange</button><button class="btn ghost" data-mm="end_combat">End the fight</button>`
    : `<span class="muted">No fight running.</span><button class="btn primary" data-mm="start_combat">Start a fight</button>`}
    <span class="right">${danger}</span></div>
    ${c ? `<div class="small muted mt">1 Telegraph each foe · 2 Players act, any order · 3 Foes roll in the open · 4 Narrate · 5 End the exchange</div>` : ''}
    ${dg && dg.text ? `<div class="small muted">${esc(dg.text)}</div>` : ''}</div>`;
}

function trackerHtml() {
  const lib = Object.values(state.library).sort((a, b) => a.level - b.level || a.name.localeCompare(b.name));
  const foes = Object.values(state.enemies);
  return `<div class="panel"><div class="panel-head"><h3>Combat tracker</h3></div>
    <div class="row gap mb"><select data-ui="spawnId" style="max-width:340px">${lib.map(e => `<option value="${esc(e.id)}" ${uiv('spawnId') === e.id ? 'selected' : ''}>L${e.level} ${esc(e.name)} (${esc(e.role)})</option>`).join('') || '<option value="">Library is empty</option>'}</select>
      <input type="number" min="1" max="30" value="${esc(uiv('spawnCount', 1))}" data-ui="spawnCount" style="width:70px" title="How many (Mooks come as a mob)">
      <button class="btn primary" data-mm="spawn">Add to the fight</button>
      <button class="btn ghost small" data-go-build>Card builder</button></div>
    ${foes.length ? `<div class="foes">${foes.map(foeCardHtml).join('')}</div>` : '<div class="empty">No foes on the tracker. Pick a card above.</div>'}</div>`;
}

function foeCardHtml(e) {
  const c = e.card || {};
  const mook = e.role === 'mook';
  const tg = (state.combat || {}).telegraphs || {};
  let life = '';
  if (mook) {
    let pips = '';
    const start = Math.max(e.count, uiv('mob_' + e.key, e.count));
    ui['mob_' + e.key] = start;
    for (let i = 0; i < start; i++) pips += `<span class="mook-pip ${i < e.count ? '' : 'down'}"></span>`;
    life = `<div class="small">${e.count} standing · drop to any hit</div><div class="mook-pips">${pips}</div>`;
  } else {
    life = `<div class="hp-top"><span>HP <b>${e.hp_current}</b> / ${c.hp}</span><span>Bloodied at ${Math.floor(c.hp / 2)}</span></div>${hpBar(e.hp_current, c.hp)}`;
  }
  const targets = Object.values(state.chars).filter(ch => ch.status !== 'dead');
  const dmgNote = mook && e.count > 1 ? ` (+${Math.min((e.count - 1) * (c.mob_damage_per_extra || 1), c.mob_damage_cap || 4)} mob)` : '';
  return `<div class="foe ${e.bloodied && !e.defeated ? 'bloodied' : ''} ${e.defeated ? 'defeated' : ''} ${e.broken ? 'broken' : ''}">
    <div class="foe-top"><span class="foe-name">${esc(e.name)}</span><span class="tiny muted">level ${e.level} ${esc(e.role)}</span>
      <span class="right row gap">${e.bloodied && !e.defeated ? '<span class="chip bad">Bloodied</span>' : ''}${e.phase > 1 ? `<span class="chip bad">Phase ${e.phase}</span>` : ''}
      ${e.broken ? '<span class="chip cost">Broken</span>' : ''}${e.defeated ? '<span class="chip good">Down</span>' : ''}${c.fearless ? '<span class="chip">Fearless</span>' : ''}</span></div>
    ${life}
    <div class="foe-nums"><span>Attack <b>${signed(c.attack)}</b></span><span>Damage <b>${c.damage}${dmgNote}</b></span><span>Attacks <b>${c.attacks}</b></span>
      <span>Armor <b>${e.armor}</b></span><span>Morale <b>${e.morale}</b></span></div>
    ${(e.openings || []).length ? `<div class="small"><span class="chip info">Opening</span> ${e.openings.map(o => o === '*' ? 'the next attack' : esc(o)).join(', ')}: Easy</div>` : ''}
    ${state.combat && !e.defeated ? `<div class="foe-actions"><input type="text" placeholder="Telegraph: about to…" data-ui="tg_${esc(e.key)}" value="${inputVal('tg_' + e.key)}" style="flex:1;min-width:140px">
      <button class="btn small" data-tg="${esc(e.key)}">Telegraph</button></div>${tg[e.key] ? `<div class="small muted">Telegraphed: <i>${esc(tg[e.key])}</i></div>` : ''}` : ''}
    ${!e.defeated && !e.broken ? `<div class="foe-actions"><select data-ui="tgt_${esc(e.key)}">${targets.map(ch => `<option value="${esc(ch.player_name)}" ${uiv('tgt_' + e.key) === ch.player_name ? 'selected' : ''}>${esc(ch.name)}</option>`).join('')}</select>
      <button class="btn small danger" data-eatk="${esc(e.key)}" ${targets.length ? '' : 'disabled'}>Attack (rolls in the open)</button>
      <button class="btn small" data-morale="${esc(e.key)}">Morale</button></div>` : ''}
    <div class="foe-actions"><input type="number" min="0" max="500" placeholder="0" data-ui="dmg_${esc(e.key)}" value="${inputVal('dmg_' + e.key)}" style="width:70px">
      <button class="btn small" data-edmg="${esc(e.key)}">Damage</button>${mook ? '' : `<button class="btn small ghost" data-eheal="${esc(e.key)}">Heal</button>`}
      <button class="btn small ghost" data-ebroken="${esc(e.key)}">${e.broken ? 'Rally' : 'Mark broken'}</button>
      <button class="btn small danger right" data-eremove="${esc(e.key)}" title="Remove from the tracker">×</button></div>
    <details class="foe-card"><summary class="small muted">The card</summary><dl>
      ${e.wants ? `<dt>Wants</dt><dd>${esc(e.wants)}</dd>` : ''}${e.special ? `<dt>Special</dt><dd>${esc(e.special)}</dd>` : ''}
      ${e.when_bloodied ? `<dt>When bloodied</dt><dd class="${e.bloodied ? 'hot' : ''}">${esc(e.when_bloodied)}</dd>` : ''}
      ${e.tells ? `<dt>Tells</dt><dd>${esc(e.tells)}</dd>` : ''}${e.breaks ? `<dt>Breaks</dt><dd>${esc(e.breaks)}</dd>` : ''}
      ${(e.twists || []).length ? `<dt>Twists (d6)</dt><dd>${e.twists.map((t, i) => `${i + 1}. ${esc(t)}`).join('<br>')}</dd>` : ''}
      ${e.nastier ? `<dt>Nastier</dt><dd>${esc(e.nastier)}</dd>` : ''}</dl></details></div>`;
}

function mmPartyHtml() {
  const chars = Object.values(state.chars);
  return `<div class="panel"><h3>The party</h3>${chars.length ? `<div class="party">${chars.map(c => {
    const d = c.derived || {};
    return `<div class="pc ${c.status === 'dying' ? 'dying' : ''}"><div class="pc-top"><span class="pc-name">${esc(c.name)}</span>
      <span class="tiny muted">${esc(c.player_name)} · L${c.level} ${esc((c.class || {}).name || '')}</span>${statusChip(c.status)}
      ${c.level_up_ready ? '<span class="chip gold">picking a level</span>' : ''}${c.must_hold_on ? '<span class="chip bad">must Hold On</span>' : ''}</div>
      <div class="hp-top tiny"><span>HP <b>${c.hp.current}</b>/${d.hp_max} · armor ${d.armor}</span>${sparkPips(c.sparks, 3)}</div>${hpBar(c.hp.current, d.hp_max, true)}
      <div class="tiny muted mt">Slots ${d.slots_used}/${d.slots_total} · Fatigue ${c.fatigue} · Wounds ${(c.wounds || []).length}${(c.wounds || []).length ? ': ' + c.wounds.map(w => esc(w.name)).join(', ') : ''}</div>
      <div class="row gap mt"><button class="btn small" data-award="${esc(c.player_name)}">+ Spark</button>
        <input type="number" min="1" max="200" placeholder="HP" data-ui="hp_${esc(c.player_name)}" value="${inputVal('hp_' + c.player_name)}" style="width:62px;padding:.25rem .4rem">
        <button class="btn small danger" data-hurt="${esc(c.player_name)}">Hurt</button><button class="btn small good" data-heal="${esc(c.player_name)}">Heal</button>
        <button class="btn small ghost" data-wound="${esc(c.player_name)}">Wound</button>
        ${(c.wounds || []).length ? `<button class="btn small ghost" data-unwound="${esc(c.player_name)}">Heal a Wound</button>` : ''}
        ${c.status === 'dying' ? `<button class="btn small good" data-tend="${esc(c.player_name)}">Tend</button>` : ''}</div></div>`;
  }).join('')}</div>` : '<div class="empty">No characters yet. Invite players, or build one in Build.</div>'}</div>`;
}

function nominationsHtml() {
  if (!state.nominations.length) return '';
  return `<div class="panel nominations"><h3>Spark calls</h3>${state.nominations.map((n, i) => `<div class="result">
    <div class="result-head"><span class="kind">${esc(n.reason)}</span><span class="right tiny muted">${n.by ? 'from ' + esc(n.by) : ''}</span></div>
    <div>${esc(charName(n.player))}</div><div class="row gap mt"><button class="btn small primary" data-nom-yes="${i}">Award a Spark</button>
    <button class="btn small ghost" data-nom-no="${i}">Not this time</button></div></div>`).join('')}</div>`;
}

function toolboxHtml() {
  const tables = Object.values(R().tables || {});
  const res = state.toolResults;
  return `<div class="panel"><div class="panel-head"><h3>Toolbox</h3><span class="right tiny muted">Private to you until you reveal it</span></div>
    <button class="btn block stuck-btn mb" data-tb="stuck">Stuck? Give me three ways forward</button>
    <div class="toolbox-grid">
      <button class="btn small" data-tb="reaction">Reaction roll</button>
      <select data-ui="reactMod">${[-2, -1, 0, 1, 2].map(n => `<option value="${n}" ${String(uiv('reactMod', 0)) === String(n) ? 'selected' : ''}>modifier ${signed(n)}</option>`).join('')}</select>
      <button class="btn small" data-tb="pressure">Pressure die</button>
      <select data-ui="pressureVariant">${['generic', 'underground', 'wild', 'settlement', 'occasion'].map(v => `<option ${uiv('pressureVariant', 'generic') === v ? 'selected' : ''}>${v}</option>`).join('')}</select>
      <button class="btn small" data-table="complications_fight">Fight cost</button>
      <button class="btn small" data-table="complications_explore">Explore cost</button>
      <button class="btn small" data-table="complications_social">Social cost</button>
      <button class="btn small" data-table="trouble">MM move</button>
      <button class="btn small" data-tb="npc">NPC on the spot</button>
      <button class="btn small" data-table="trinkets">Trinket</button>
      <button class="btn small" data-table="curios">Curio</button>
      <button class="btn small" data-table="relics">Relic</button>
      <button class="btn small" data-tb="hoard">Hoard</button>
      <select data-ui="hoardLevel">${Array.from({ length: 10 }, (_, i) => `<option value="${i + 1}" ${String(uiv('hoardLevel', 1)) === String(i + 1) ? 'selected' : ''}>site level ${i + 1}</option>`).join('')}</select>
    </div>
    <div class="label">Oracle</div><div class="row gap"><input type="text" class="grow" style="width:auto" data-ui="oracleQ" value="${inputVal('oracleQ')}" placeholder="A yes/no question">
      <select data-ui="oracleOdds" style="width:auto">${['likely', 'even', 'unlikely', 'very_unlikely'].map(o => `<option value="${o}" ${uiv('oracleOdds', 'even') === o ? 'selected' : ''}>${o.replace('_', ' ')}</option>`).join('')}</select>
      <button class="btn small" data-tb="oracle">Ask</button></div>
    <div class="label">Any table</div><div class="row gap"><select data-ui="anyTable" class="grow" style="width:auto">${tables.map(t => `<option value="${esc(t.id)}" ${uiv('anyTable') === t.id ? 'selected' : ''}>${esc(t.name)} (${esc(t.die)})</option>`).join('')}</select>
      <button class="btn small" data-tb="any">Roll</button></div>
    ${toggleChip('revealNow', 'Show the table at once', uiv('revealNow', false), 'style="margin-top:.6rem"')}
    <div class="mt">${res.length ? res.map((r, i) => `<div class="result"><div class="result-head"><span class="kind">${esc(r.kind)}</span>
      ${r.result_id ? `<button class="btn small right" data-reveal="${i}">Reveal</button>` : '<span class="right chip good">shown</span>'}</div>${toolboxText(r.kind, r.result)}</div>`).join('') : '<div class="empty">Results appear here.</div>'}</div></div>`;
}

function mmClocksHtml() {
  return `<div class="panel"><h3>Threat clocks</h3><div class="row gap mb"><input type="text" data-ui="clockName" value="${inputVal('clockName')}" placeholder="What is coming?" class="grow" style="width:auto">
    <select data-ui="clockSegs" style="width:auto">${[4, 6, 8].map(n => `<option value="${n}" ${String(uiv('clockSegs', 4)) === String(n) ? 'selected' : ''}>${n}</option>`).join('')}</select>
    <button class="btn small" data-mm="clock_create">Add</button></div>
    <div class="clocks">${Object.values(state.clocks).map(c => clockHtml(c, true)).join('') || '<div class="empty">No clocks ticking.</div>'}</div></div>`;
}

function sessionHtml() {
  return `<div class="panel"><h3>Session ${state.sessionNumber}</h3><div class="toolbox-grid">
    <button class="btn small" data-mm="scene_end">New scene</button>
    <button class="btn small" data-mm="act_break">Act break</button>
    <button class="btn small" data-mm="breather">Breather (all)</button>
    <button class="btn small" data-mm="night">Night's rest (all)</button>
    <button class="btn small primary" data-mm="session_end">End of session</button>
    <button class="btn small ghost" data-mm="next_session">Start next session</button></div></div>`;
}

function invitePanelHtml() {
  return `<div class="panel"><h3>Invite a player</h3><div class="row gap"><input type="text" id="mm-invite-name" placeholder="Player name" class="grow" style="width:auto">
    <button class="btn small" id="mm-invite-btn">Make link</button></div><div id="mm-invite-out" class="invite hidden"></div></div>`;
}

function wireMMPlay(root) {
  $$('[data-go-build]', root).forEach(b => b.onclick = () => switchTab('build'));
  $('#mm-invite-btn', root).onclick = () => makeInvite(state.sessionId, $('#mm-invite-name').value, '#mm-invite-out');
  $$('[data-mm]', root).forEach(b => b.onclick = () => mmAction(b.dataset.mm));
  $$('[data-tg]', root).forEach(b => b.onclick = () => { send({ type: 'telegraph', enemy: b.dataset.tg, text: ui['tg_' + b.dataset.tg] || '' }); ui['tg_' + b.dataset.tg] = ''; });
  $$('[data-eatk]', root).forEach(b => b.onclick = () => {
    const k = b.dataset.eatk;
    const target = ui['tgt_' + k] || (Object.values(state.chars).find(c => c.status !== 'dead') || {}).player_name;
    send({ type: 'enemy_attack', enemy: k, target });
  });
  $$('[data-morale]', root).forEach(b => b.onclick = () => send({ type: 'morale_check', enemy: b.dataset.morale }));
  $$('[data-edmg]', root).forEach(b => b.onclick = () => { const k = b.dataset.edmg; const n = Number(ui['dmg_' + k] || 0); if (n > 0) send({ type: 'enemy_update', key: k, damage: n }); ui['dmg_' + k] = ''; });
  $$('[data-eheal]', root).forEach(b => b.onclick = () => { const k = b.dataset.eheal; const n = Number(ui['dmg_' + k] || 0); if (n > 0) send({ type: 'enemy_update', key: k, heal: n }); ui['dmg_' + k] = ''; });
  $$('[data-ebroken]', root).forEach(b => b.onclick = () => { const e = state.enemies[b.dataset.ebroken]; send({ type: 'enemy_update', key: e.key, broken: !e.broken }); });
  $$('[data-eremove]', root).forEach(b => b.onclick = () => send({ type: 'enemy_remove', key: b.dataset.eremove }));
  $$('[data-award]', root).forEach(b => b.onclick = () => send({ type: 'award_spark', player: b.dataset.award, reason: 'MM award' }));
  $$('[data-hurt]', root).forEach(b => b.onclick = () => { const n = Number(ui['hp_' + b.dataset.hurt] || 0); if (n > 0) send({ type: 'hp_adjust', player: b.dataset.hurt, delta: -n }); ui['hp_' + b.dataset.hurt] = ''; });
  $$('[data-heal]', root).forEach(b => b.onclick = () => { const n = Number(ui['hp_' + b.dataset.heal] || 0); if (n > 0) send({ type: 'hp_adjust', player: b.dataset.heal, delta: n }); ui['hp_' + b.dataset.heal] = ''; });
  $$('[data-wound]', root).forEach(b => b.onclick = () => send({ type: 'wound_add', player: b.dataset.wound }));
  $$('[data-unwound]', root).forEach(b => b.onclick = () => send({ type: 'wound_remove', player: b.dataset.unwound, index: 0 }));
  $$('[data-tend]', root).forEach(b => b.onclick = () => send({ type: 'tend', target: b.dataset.tend }));
  $$('[data-nom-yes]', root).forEach(b => b.onclick = () => {
    const n = state.nominations[Number(b.dataset.nomYes)];
    state.nominations.splice(Number(b.dataset.nomYes), 1);
    send(n.graceful ? { type: 'graceful_fail_confirm', player: n.player } : { type: 'award_spark', player: n.player, reason: n.reason });
  });
  $$('[data-nom-no]', root).forEach(b => b.onclick = () => { state.nominations.splice(Number(b.dataset.nomNo), 1); renderPlay(); });
  $$('[data-clock-adv]', root).forEach(b => b.onclick = () => send({ type: 'threat_clock_advance', clock_id: b.dataset.clockAdv }));
  $$('[data-clock-back]', root).forEach(b => b.onclick = () => send({ type: 'threat_clock_wind_back', clock_id: b.dataset.clockBack }));
  $$('[data-clock-del]', root).forEach(b => b.onclick = () => send({ type: 'threat_clock_delete', clock_id: b.dataset.clockDel }));
  const reveal = !!ui.revealNow;
  $$('[data-table]', root).forEach(b => b.onclick = () => send({ type: 'toolbox_roll', table: b.dataset.table, reveal }));
  $$('[data-tb]', root).forEach(b => b.onclick = () => {
    const k = b.dataset.tb, rv = !!ui.revealNow;
    if (k === 'stuck') send({ type: 'stuck' });
    else if (k === 'reaction') send({ type: 'reaction_roll', modifier: Number(uiv('reactMod', 0)), reveal: rv });
    else if (k === 'pressure') send({ type: 'pressure_roll', variant: uiv('pressureVariant', 'generic'), reveal: rv });
    else if (k === 'npc') send({ type: 'npc', reveal: rv });
    else if (k === 'hoard') send({ type: 'hoard', site_level: Number(uiv('hoardLevel', 1)), reveal: rv });
    else if (k === 'oracle') send({ type: 'oracle', odds: uiv('oracleOdds', 'even'), question: ui.oracleQ || '', reveal: rv });
    else if (k === 'any') send({ type: 'toolbox_roll', table: uiv('anyTable') || Object.keys(R().tables || {})[0], reveal: rv });
  });
  $$('[data-reveal]', root).forEach(b => b.onclick = () => {
    const r = state.toolResults[Number(b.dataset.reveal)];
    send({ type: 'toolbox_reveal', result_id: r.result_id });
    r.result_id = null;
    renderPlay();
  });
}

async function mmAction(a) {
  if (a === 'spawn') {
    const id = uiv('spawnId') || Object.keys(state.library)[0];
    if (!id) return notify('The library is empty: build a card first.', 'warn');
    ui.spawnId = id;
    send({ type: 'enemy_spawn', enemy_id: id, count: Number(uiv('spawnCount', 1)) || 1 });
  } else if (a === 'clock_create') {
    send({ type: 'threat_clock_create', name: ui.clockName || 'Threat', segments: Number(uiv('clockSegs', 4)) });
    ui.clockName = '';
  } else if (a === 'breather') send({ type: 'rest', kind: 'breather' });
  else if (a === 'night') { if (await confirmDialog("A night's rest", 'Everyone recovers full HP, clears all Fatigue and heals one Wound.', 'Rest')) send({ type: 'rest', kind: 'night' }); }
  else if (a === 'next_session') { if (await confirmDialog('Start the next session?', 'Sparks go back to three (unspent ones are lost) and once-a-session talents refresh.', 'Start it')) send({ type: 'next_session' }); }
  else send({ type: a });
}

/** Session end: the five prompts and the Grant Level buttons. */
async function showSessionEnd(m) {
  const body = `<p class="small muted">Talk these through with the table. When it feels earned, call the level-up.</p>
    ${m.prompts.map(p => `<label class="row gap" style="text-transform:none;letter-spacing:0;font-size:.95rem;color:var(--text)"><input type="checkbox"> ${esc(p.text)}</label>`).join('')}
    ${m.pacing_suggests_level ? `<p class="mt"><span class="chip gold">Default pacing: level ${m.pacing_suggests_level} after session ${m.session_number}</span></p>` : ''}
    <div class="label">Characters</div>${m.characters.map(c => `<div class="lib-row"><span class="grow">${esc(c.name)} <span class="muted small">level ${c.level}</span></span>
      ${c.ready ? '<span class="chip gold">already granted</span>' : `<button class="btn small primary" data-grant="${esc(c.player)}">Grant level</button>`}</div>`).join('')}`;
  await modal(`End of session ${m.session_number}`, body, [{ label: 'Close', value: null }, { label: 'Grant everyone a level', cls: 'primary', value: 'all' }],
    (w, close) => $$('[data-grant]', w).forEach(b => b.onclick = () => { send({ type: 'level_up', players: [b.dataset.grant] }); b.replaceWith(Object.assign(document.createElement('span'), { className: 'chip gold', textContent: 'granted' })); }))
    .then(v => { if (v === 'all') send({ type: 'level_up' }); });
}
