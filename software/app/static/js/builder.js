/**
 * Facets of Origin — the Build tab.
 *
 * Players: the creation wizard (Facet → stats → class → background → kit →
 * magic → review), then the level-up pick screen when the MM calls a level.
 * Mirror Master: the monster-card builder (level + role → the numbers, asked
 * of the engine) and the card library, plus the wizard for building
 * characters on a player's behalf.
 */

const wiz = { step: 'facet' };
const mb = { level: 1, role: 'standard', armor: 0, morale: 7, twists: ['', '', '', '', '', ''] };

function renderBuild() {
  const root = $('#tab-build');
  if (isMM()) { root.innerHTML = mmBuildHtml(); wireMMBuild(root); return; }
  const me = state.me;
  if (me && me.level_up_ready) { root.innerHTML = levelUpHtml(me); wireLevelUp(root, me); return; }
  if (me) { root.innerHTML = builtHtml(me); wireBuilt(root, me); return; }
  root.innerHTML = wizardHtml();
  wireWizard(root);
}

// =====================================================================
// The creation wizard
// =====================================================================
function wizSteps() {
  const s = [['facet', 'Facet'], ['stats', 'Stats'], ['class', 'Class'], ['background', 'Background'], ['kit', 'Kit']];
  if (wizIsCaster()) s.push(['magic', 'Magic']);
  if (wizGiftLineage()) s.push(['lineage', 'Gift']);
  s.push(['review', 'Review']);
  return s;
}

function wizTalents() {
  if (wiz.mode === 'custom') return (wiz.custom && wiz.custom.talents) || [];
  const c = classDef(wiz.classId);
  return c ? c.talents : [];
}
function wizIsCaster() { return wizTalents().some(id => isCastingTalent(talentDef(id))); }
function wizTradition() { const t = wizTalents().map(talentDef).find(isCastingTalent); return t ? t.effects.grants_tradition : null; }
function wizGiftLineage() { const l = (R().lineages || []).find(x => x.id === (wiz.lineage || 'human')); return l && l.gift ? l : null; }
function wizFacet() { return facetDef(wiz.facet); }
function wizStats() {
  const out = {}; const rules = (R().stat_rules || {}).creation || { facet_stat: 2, second: 1, third: 0 };
  (R().stats || []).forEach(s => out[s.id] = rules.third);
  const f = wizFacet(); if (f) out[f.stat] = rules.facet_stat;
  if (wiz.second && wiz.second !== (f && f.stat)) out[wiz.second] = rules.second;
  return out;
}

function wizardHtml() {
  const steps = wizSteps();
  if (!steps.some(s => s[0] === wiz.step)) wiz.step = 'review';
  const idx = steps.findIndex(s => s[0] === wiz.step);
  const body = { facet: stepFacet, stats: stepStats, class: stepClass, background: stepBackground, kit: stepKit,
    magic: stepMagic, lineage: stepLineage, review: stepReview }[wiz.step]();
  return `<div class="wizard">
    <div class="panel"><h2>${isMM() ? 'Build a character' : 'Build your character'}</h2>
      <p class="muted small">Pick a Facet, take a ready-made class or write your own, choose a past. The app keeps the numbers straight.</p>
      <div class="stepper-nav">${steps.map(([k, l], i) => `<button data-wstep="${k}" class="${k === wiz.step ? 'on' : (i < idx ? 'done' : '')}">${i + 1}. ${l}</button>`).join('')}</div>
      ${body}
      <div class="wizard-foot"><button class="btn ghost" data-wprev ${idx === 0 ? 'disabled' : ''}>Back</button>
        <span class="msg error" id="wiz-err"></span>
        ${wiz.step === 'review' ? '<button class="btn primary big" data-wcreate>Create character</button>' : `<button class="btn primary" data-wnext>Next</button>`}</div>
    </div></div>`;
}

function stepFacet() {
  return `<h3>Which Facet are you?</h3><p class="small muted">Your Facet is what you are best at. Its stat starts at +2, and it sets your grit die (HP) and your class menu.</p>
    <div class="choices">${(R().facets || []).map(f => {
      const classes = (R().classes || []).filter(c => c.facet === f.id).map(c => c.name);
      return `<button class="choice big ${wiz.facet === f.id ? 'on' : ''}" data-facet="${esc(f.id)}"><h4>${esc(f.name)}</h4>
        <div class="desc">${esc(f.description)}</div>
        <div class="small mt">Grit die <b>d${f.grit_die}</b> · ${f.tradition ? `can learn <b>${esc(cap(f.tradition))}</b>` : 'no casting'}</div>
        <div class="tiny muted mt">${classes.map(esc).join(' · ')}</div></button>`;
    }).join('')}</div>`;
}

function stepStats() {
  const f = wizFacet();
  if (!f) return '<p class="msg error">Pick a Facet first.</p>';
  const stats = wizStats();
  const others = (R().stats || []).filter(s => s.id !== f.stat);
  const slots = R().slots || {};
  return `<h3>Your stats</h3><p class="small muted">${esc(statName(f.stat))} is your Facet's stat: <b>+2</b>. Choose which of the others is <b>+1</b>; the last is +0.</p>
    <div class="choices">${others.map(s => `<button class="choice ${wiz.second === s.id ? 'on' : ''}" data-second="${esc(s.id)}"><h4>${esc(s.name)} +1</h4><div class="desc">${esc(s.description)}</div></button>`).join('')}</div>
    <div class="stats mt">${(R().stats || []).map(s => `<div class="stat"><div class="v">${signed(stats[s.id])}</div><div class="n">${esc(s.name)}</div></div>`).join('')}</div>
    <div class="subtle small">HP at level 1: your grit die's maximum (${f.grit_die}) + Body (${signed(stats.body)}), before talents. Slots: ${slots.base || 10} + ${esc(statName(slots.plus_stat || 'body'))}.</div>`;
}

function talentChoiceField(id) {
  if (id === 'weapon_master') {
    const kinds = ((R().equipment || {}).weapon_kinds) || [];
    return `<label>Weapon Master: which kind of weapon?</label><select data-wchoice="weapon_master">${kinds.map(k => `<option ${(wiz.talentChoices || {}).weapon_master === k ? 'selected' : ''}>${k}</option>`).join('')}</select>`;
  }
  return '';
}

function stepClass() {
  const f = wizFacet();
  if (!f) return '<p class="msg error">Pick a Facet first.</p>';
  const presets = (R().classes || []).filter(c => c.facet === f.id);
  if (!wiz.mode) wiz.mode = 'preset';
  if (wiz.mode === 'preset' && !presets.some(c => c.id === wiz.classId)) wiz.classId = presets[0] && presets[0].id;
  const tabs = `<div class="subtabs"><button data-wmode="preset" class="${wiz.mode === 'preset' ? 'on' : ''}">Ready-made class</button><button data-wmode="custom" class="${wiz.mode === 'custom' ? 'on' : ''}">Write your own</button></div>`;
  if (wiz.mode === 'preset') {
    const c = classDef(wiz.classId);
    return `${tabs}<div class="choices">${presets.map(p => `<button class="choice ${p.id === wiz.classId ? 'on' : ''}" data-class="${esc(p.id)}"><h4>${esc(p.name)}</h4>
        <div class="desc"><i>${esc(p.concept)}</i></div><div class="small mt">Knack: <b>${esc(p.knack)}</b></div>
        <div class="small">Talents: ${p.talents.map(talentName).map(esc).join(', ')}</div>
        <div class="tiny muted">Signature at level 3: ${esc(talentName(p.signature))}</div></button>`).join('')}</div>
      ${c ? `<div class="panel mt"><h3>${esc(c.name)}'s talents</h3>${c.talents.map(id => { const t = talentDef(id); return t ? `<div class="talent"><div class="talent-top"><span class="talent-name">${esc(t.name)}</span><span class="tiny muted">${esc(useLabel(t.use))}</span></div><div class="talent-text">${esc(t.text)}</div></div>` : ''; }).join('')}
        ${c.talents.map(talentChoiceField).join('')}</div>` : ''}`;
  }
  const cu = wiz.custom = wiz.custom || { name: '', concept: '', knack: '', talents: [], signature: '' };
  const menu = (R().talents || []).filter(t => t.kind === 'talent' && onMenuOf(t, f.id));
  const sigs = (R().talents || []).filter(t => t.kind === 'signature' && onMenuOf(t, f.id));
  return `${tabs}<div class="two-col"><div>
      <label>Class name</label><input type="text" data-wc="name" value="${esc(cu.name)}" maxlength="64" placeholder="e.g. Wandering Disciple">
      <label>Concept (one sentence)</label><input type="text" data-wc="concept" value="${esc(cu.concept)}" maxlength="300" placeholder="I am…">
      <label>Class knack</label><input type="text" data-wc="knack" value="${esc(cu.knack)}" maxlength="64" placeholder="A field you know: e.g. Motion and stillness">
      <label>Signature you're working toward (level 3, optional)</label><select data-wc="signature"><option value="">Decide later</option>
        ${sigs.map(s => `<option value="${esc(s.id)}" ${cu.signature === s.id ? 'selected' : ''}>${esc(s.name)}</option>`).join('')}</select>
      ${cu.talents.map(talentChoiceField).join('')}
    </div><div><div class="label">Two starting talents from the ${esc(f.name)} menu (${cu.talents.length}/2)</div>
      ${menu.map(t => `<div class="talent choice ${cu.talents.includes(t.id) ? 'on' : ''}" data-wtalent="${esc(t.id)}" style="padding:.55rem .7rem">
        <div class="talent-top"><span class="talent-name">${esc(t.name)}</span><span class="tiny muted">${esc(useLabel(t.use))}</span>${isCastingTalent(t) ? '<span class="chip magic">casting</span>' : ''}</div>
        <div class="talent-text">${esc(t.text)}</div></div>`).join('')}</div></div>`;
}

function stepBackground() {
  if (!wiz.bgMode) wiz.bgMode = 'list';
  const tabs = `<div class="subtabs"><button data-wbg="list" class="${wiz.bgMode === 'list' ? 'on' : ''}">Pick one</button><button data-wbg="custom" class="${wiz.bgMode === 'custom' ? 'on' : ''}">Write your own</button></div>`;
  const lin = (R().lineages || []).filter(l => l.playable !== false);
  const lineage = lin.length > 1 ? `<label>Lineage</label><select data-wlineage>${lin.map(l => `<option value="${esc(l.id)}" ${(wiz.lineage || 'human') === l.id ? 'selected' : ''}>${esc(l.name)}</option>`).join('')}</select>` : '';
  if (wiz.bgMode === 'list') {
    const groups = {};
    (R().backgrounds || []).forEach(b => (groups[b.facet] = groups[b.facet] || []).push(b));
    return `${tabs}<p class="small muted">Your past gives you a background knack and a Specialty: one narrow thing where routine tasks just happen and risky ones are Easy. Any background suits any Facet.</p>
      ${Object.entries(groups).map(([fid, list]) => `<div class="label">${esc((facetDef(fid) || {}).name || fid)}</div><div class="choices">${list.map(b =>
        `<button class="choice ${wiz.bgId === b.id ? 'on' : ''}" data-bg="${esc(b.id)}"><h4>${esc(b.name)}</h4><div class="desc">${esc(b.specialty)}</div></button>`).join('')}</div>`).join('')}${lineage}`;
  }
  const cb = wiz.customBg = wiz.customBg || { name: '', knack: '', specialty: '', description: '' };
  return `${tabs}<div class="two-col"><div><label>Background name</label><input type="text" data-wbgf="name" value="${esc(cb.name)}" maxlength="64" placeholder="e.g. Lighthouse keeper's child">
    <label>Background knack</label><input type="text" data-wbgf="knack" value="${esc(cb.knack)}" maxlength="64" placeholder="e.g. Ships and weather">
    <label>Specialty (one narrow thing)</label><input type="text" data-wbgf="specialty" value="${esc(cb.specialty)}" maxlength="300" placeholder="e.g. Reads a coastline's tides and hazards at a glance"></div>
    <div><label>Your history (optional)</label><textarea data-wbgf="description" maxlength="2000">${esc(cb.description)}</textarea>${lineage}</div></div>`;
}

function stepKit() {
  if (!wiz.kit) wiz.kit = wiz.mode === 'preset' && classDef(wiz.classId) ? classDef(wiz.classId).kit.slice() : [];
  const items = R().items || [];
  const stats = wizStats();
  const slots = R().slots || {};
  const total = (slots.base || 10) + (stats[slots.plus_stat || 'body'] || 0);
  const used = wiz.kit.reduce((n, id) => n + ((itemDef(id) || {}).slots ?? 1), 0);
  return `<h3>Your kit</h3><p class="small muted">Everything you carry takes slots (heavy armor and heavy weapons take two). ${wiz.mode === 'preset' ? 'This is your class kit: swap anything you like.' : 'Tap items to pack them.'}
    Leave room: Wounds and Fatigue take slots too.</p>
    <div class="row gap mb"><span class="slot-meter ${used > total ? 'over' : ''}">${used} / ${total} slots</span><span class="small muted">(${slots.base || 10} + ${esc(statName(slots.plus_stat || 'body'))}; talents may add more)</span></div>
    <div class="catalog mb">${wiz.kit.map((id, i) => `<button data-kitrm="${i}" title="Remove">${esc((itemDef(id) || {}).name || id)} ✕</button>`).join('') || '<span class="empty">Nothing packed.</span>'}</div>
    <div class="label">Add</div><div class="catalog">${items.map(it => `<button data-kitadd="${esc(it.id)}">+ ${esc(it.name)}${it.slots !== 1 ? ` (${it.slots})` : ''}${it.weapon ? ` · d${((R().equipment || {}).weapon_categories || {})[it.weapon]?.die || '?'}` : ''}</button>`).join('')}</div>`;
}

function stepMagic() {
  const trad = wizTradition();
  const doms = (R().magic_domains || []).filter(d => d.tradition === trad && !d.prismatic);
  const m = wiz.magic = wiz.magic || { domain: '', workings: ['', ''] };
  const wider = wizTalents().includes('wider_domain');
  return `<h3>${esc(cap(trad))}</h3><p class="small muted">Magic is Domain + Intent + Scope. Pick your domain, then name two <b>signature workings</b>: the things you do so often they are one step Easier.</p>
    <div class="choices">${doms.map(d => `<button class="choice ${m.domain === d.id ? 'on' : ''}" data-domain="${esc(d.id)}"><h4>${esc(d.name)}</h4><div class="desc">${esc(d.description)}</div></button>`).join('')}</div>
    <div class="two-col mt"><div><label>Signature working 1</label><input type="text" data-wwork="0" value="${esc(m.workings[0])}" maxlength="200" placeholder="e.g. A sealing glyph"></div>
      <div><label>Signature working 2</label><input type="text" data-wwork="1" value="${esc(m.workings[1])}" maxlength="200" placeholder="e.g. A warning rune"></div></div>
    ${wider ? `<label>Wider Domain: your second domain</label><select data-wchoice="wider_domain"><option value="">Choose…</option>${doms.filter(d => d.id !== m.domain).map(d => `<option value="${esc(d.id)}" ${(wiz.talentChoices || {}).wider_domain === d.id ? 'selected' : ''}>${esc(d.name)}</option>`).join('')}</select>` : ''}`;
}

function stepLineage() {
  const lin = wizGiftLineage();
  if (!lin) return '';
  if (wiz.gifted === undefined) wiz.gifted = true;
  const doms = (R().magic_domains || []).filter(d => !d.prismatic && (!(lin.gift_domains || []).length || lin.gift_domains.includes(d.id)));
  return `<h3>${esc(lin.name)}</h3><p class="small muted">${esc(lin.description)}</p>
    <label class="row gap" style="text-transform:none;letter-spacing:0"><input type="checkbox" data-wgifted ${wiz.gifted ? 'checked' : ''}> This character carries the gift</label>
    ${wiz.gifted ? `<div class="subtle small mt">${esc(lin.gift)}</div>${lin.gift_domain_scope ? `<label>Gift domain (Minor workings only, cast with Soul)</label>
      <select data-wgiftdom><option value="">Choose…</option>${doms.map(d => `<option value="${esc(d.id)}" ${wiz.giftDomain === d.id ? 'selected' : ''}>${esc(d.name)}</option>`).join('')}</select>` : ''}` : ''}`;
}

function stepReview() {
  const f = wizFacet(); const stats = wizStats();
  const c = wiz.mode === 'custom' ? wiz.custom || {} : classDef(wiz.classId) || {};
  const bg = wiz.bgMode === 'custom' ? wiz.customBg || {} : (R().backgrounds || []).find(b => b.id === wiz.bgId) || {};
  return `<div class="two-col"><div><label>Character name</label><input type="text" data-wname value="${esc(wiz.name || '')}" maxlength="64" placeholder="What does the table call you?">
    ${isMM() ? '<p class="small muted">Built by the MM, the character is filed under its own name.</p>' : ''}</div>
    <div class="summary"><dl>
      <dt>Facet</dt><dd>${esc(f ? f.name : '—')}</dd>
      <dt>Stats</dt><dd>${(R().stats || []).map(s => `${esc(s.name)} ${signed(stats[s.id])}`).join(' · ')}</dd>
      <dt>Class</dt><dd>${esc(c.name || '—')}${wiz.mode === 'custom' ? ' (custom)' : ''}</dd>
      <dt>Knacks</dt><dd>${esc([c.knack, bg.knack].filter(Boolean).join(', ') || '—')}</dd>
      <dt>Talents</dt><dd>${wizTalents().map(talentName).map(esc).join(', ') || '—'}</dd>
      <dt>Background</dt><dd>${esc(bg.name || '—')}</dd>
      <dt>Specialty</dt><dd>${esc(bg.specialty || '—')}</dd>
      <dt>Kit</dt><dd>${(wiz.kit || (c.kit || [])).map(id => esc((itemDef(id) || {}).name || id)).join(', ') || '—'}</dd>
      ${wizIsCaster() ? `<dt>Magic</dt><dd>${esc(domainName((wiz.magic || {}).domain) || '—')}: ${((wiz.magic || {}).workings || []).filter(Boolean).map(esc).join('; ')}</dd>` : ''}
    </dl></div></div>`;
}

function wizCheck(step) {
  if (step === 'facet' && !wiz.facet) return 'Pick a Facet.';
  if (step === 'stats' && !wiz.second) return 'Choose your +1 stat.';
  if (step === 'class') {
    if (wiz.mode === 'custom') {
      const c = wiz.custom || {};
      if (!c.name || !c.concept || !c.knack) return 'A custom class needs a name, a concept and a knack.';
      if ((c.talents || []).length !== 2) return 'Pick exactly two talents.';
    }
  }
  if (step === 'background') {
    if (wiz.bgMode === 'custom') { const b = wiz.customBg || {}; if (!b.name || !b.knack || !b.specialty) return 'A background needs a name, a knack and a Specialty.'; }
    else if (!wiz.bgId) return 'Pick a background.';
  }
  if (step === 'magic') {
    const m = wiz.magic || {};
    if (!m.domain) return 'Pick your domain.';
    if ((m.workings || []).filter(w => w && w.trim()).length !== 2) return 'Name two signature workings.';
  }
  return '';
}

function wireWizard(root) {
  const rerender = () => { root.innerHTML = wizardHtml(); wireWizard(root); };
  const steps = wizSteps().map(s => s[0]);
  const go = dir => {
    const i = steps.indexOf(wiz.step);
    if (dir > 0) { const err = wizCheck(wiz.step); if (err) { $('#wiz-err').textContent = err; return; } }
    wiz.step = steps[Math.max(0, Math.min(steps.length - 1, i + dir))];
    rerender();
  };
  $$('[data-wstep]', root).forEach(b => b.onclick = () => {
    const target = steps.indexOf(b.dataset.wstep), cur = steps.indexOf(wiz.step);
    for (let i = cur; i < target; i++) { const err = wizCheck(steps[i]); if (err) { wiz.step = steps[i]; rerender(); $('#wiz-err').textContent = err; return; } }
    wiz.step = b.dataset.wstep; rerender();
  });
  const n = $('[data-wnext]', root); if (n) n.onclick = () => go(1);
  const p = $('[data-wprev]', root); if (p) p.onclick = () => go(-1);
  $$('[data-facet]', root).forEach(b => b.onclick = () => {
    if (wiz.facet !== b.dataset.facet) { wiz.facet = b.dataset.facet; wiz.second = null; wiz.classId = null; wiz.kit = null; wiz.custom = null; wiz.magic = null; wiz.talentChoices = {}; }
    rerender();
  });
  $$('[data-second]', root).forEach(b => b.onclick = () => { wiz.second = b.dataset.second; wiz.kit = wiz.kit; rerender(); });
  $$('[data-wmode]', root).forEach(b => b.onclick = () => { wiz.mode = b.dataset.wmode; wiz.kit = null; rerender(); });
  $$('[data-class]', root).forEach(b => b.onclick = () => { wiz.classId = b.dataset.class; wiz.kit = null; wiz.magic = null; rerender(); });
  $$('[data-wc]', root).forEach(el => el.oninput = el.onchange = () => { wiz.custom[el.dataset.wc] = el.value; });
  $$('[data-wtalent]', root).forEach(el => el.onclick = () => {
    const t = wiz.custom.talents, id = el.dataset.wtalent;
    if (t.includes(id)) t.splice(t.indexOf(id), 1); else if (t.length < 2) t.push(id); else { t.shift(); t.push(id); }
    rerender();
  });
  $$('[data-wchoice]', root).forEach(el => {
    wiz.talentChoices = wiz.talentChoices || {};
    if (!wiz.talentChoices[el.dataset.wchoice] && el.value) wiz.talentChoices[el.dataset.wchoice] = el.value;
    el.onchange = () => { wiz.talentChoices[el.dataset.wchoice] = el.value; };
  });
  $$('[data-wbg]', root).forEach(b => b.onclick = () => { wiz.bgMode = b.dataset.wbg; rerender(); });
  $$('[data-bg]', root).forEach(b => b.onclick = () => { wiz.bgId = b.dataset.bg; rerender(); });
  $$('[data-wbgf]', root).forEach(el => el.oninput = () => { wiz.customBg[el.dataset.wbgf] = el.value; });
  const lin = $('[data-wlineage]', root); if (lin) lin.onchange = () => { wiz.lineage = lin.value; wiz.gifted = undefined; rerender(); };
  $$('[data-kitrm]', root).forEach(b => b.onclick = () => { wiz.kit.splice(Number(b.dataset.kitrm), 1); rerender(); });
  $$('[data-kitadd]', root).forEach(b => b.onclick = () => { wiz.kit.push(b.dataset.kitadd); rerender(); });
  $$('[data-domain]', root).forEach(b => b.onclick = () => { wiz.magic.domain = b.dataset.domain; rerender(); });
  $$('[data-wwork]', root).forEach(el => el.oninput = () => { wiz.magic.workings[Number(el.dataset.wwork)] = el.value; });
  const gifted = $('[data-wgifted]', root); if (gifted) gifted.onchange = () => { wiz.gifted = gifted.checked; rerender(); };
  const gd = $('[data-wgiftdom]', root); if (gd) gd.onchange = () => { wiz.giftDomain = gd.value; };
  const nm = $('[data-wname]', root); if (nm) nm.oninput = () => { wiz.name = nm.value; };
  const cr = $('[data-wcreate]', root); if (cr) cr.onclick = createCharacter;
}

async function createCharacter() {
  for (const s of wizSteps().map(x => x[0])) { const err = wizCheck(s); if (err) { wiz.step = s; renderBuild(); $('#wiz-err').textContent = err; return; } }
  if (!(wiz.name || '').trim()) { $('#wiz-err').textContent = 'Give your character a name.'; return; }
  const body = { session_id: state.sessionId, character_name: wiz.name.trim(), facet: wiz.facet, second_stat: wiz.second,
    lineage: wiz.lineage || 'human', talent_choices: {}, kit: wiz.kit || null };
  const talents = wizTalents();
  talents.forEach(id => { if ((wiz.talentChoices || {})[id]) body.talent_choices[id] = wiz.talentChoices[id]; });
  if (talents.includes('weapon_master') && !body.talent_choices.weapon_master) body.talent_choices.weapon_master = ((R().equipment || {}).weapon_kinds || [])[0];
  if (wiz.mode === 'custom') body.custom_class = { name: wiz.custom.name, concept: wiz.custom.concept, knack: wiz.custom.knack, talents: wiz.custom.talents, kit: wiz.kit || [], signature: wiz.custom.signature || null };
  else body.class_id = wiz.classId;
  if (wiz.bgMode === 'custom') body.custom_background = wiz.customBg; else body.background_id = wiz.bgId;
  if (wizIsCaster()) body.magic = { domain: wiz.magic.domain, signature_workings: wiz.magic.workings.map(w => w.trim()) };
  if (wizGiftLineage()) { body.gifted = !!wiz.gifted; if (wiz.gifted && wiz.giftDomain) body.gift_domain = wiz.giftDomain; }
  const resp = await apiFetch('/api/characters/', 'POST', body);
  if (!resp.ok) { $('#wiz-err').textContent = formatApiError((await resp.json()).detail, 'The character could not be made.'); return; }
  const d = await resp.json();
  if (isMM()) notify(`${d.character.name} is ready.`, 'success');
  Object.keys(wiz).forEach(k => delete wiz[k]); wiz.step = 'facet';
  if (isMM()) { ui.mmBuild = 'chars'; renderBuild(); }
}

// =====================================================================
// A built character: summary, export, import
// =====================================================================
function builtHtml(me) {
  return `<div class="wizard"><div class="panel"><h2>${esc(me.name)}</h2>
    <p class="muted">Level ${me.level} ${esc((me.class || {}).name || '')}. Your sheet lives on the Play tab; gear and notes live in Tools.</p>
    <p class="small muted">When the Mirror Master calls a level-up at the end of a session, your pick appears here.</p>
    <div class="row gap"><button class="btn primary" data-go-play>Open my sheet</button><button class="btn" data-export>Download .fof</button></div></div>
    <div class="panel"><h3>Level track</h3>${levelTrackHtml(me)}</div></div>`;
}

function levelTrackHtml(me) {
  const adv = R().advancement || {};
  const rows = [];
  for (let l = 2; l <= (adv.max_level || 10); l++) {
    const bits = [l === adv.signature_level ? 'your signature' : 'a talent, or improve one'];
    if ((adv.stat_increase_levels || []).includes(l)) bits.push('+1 to a stat');
    if (me.magic && (adv.signature_working_levels || []).includes(l)) bits.push('another signature working');
    const db = (adv.damage_bonus || []).find(d => d.level === l);
    if (db) bits.push(`+${db.bonus} damage`);
    rows.push(`<tr class="${l <= me.level ? 'muted' : ''}"><td>${l}</td><td>${bits.join(' · ')}</td></tr>`);
  }
  return `<table class="t"><tr><th>Level</th><th>You gain HP, plus</th></tr>${rows.join('')}</table>`;
}

function wireBuilt(root, me) {
  $('[data-go-play]', root).onclick = () => switchTab('play');
  $('[data-export]', root).onclick = () => exportCharacter(me.player_name);
}

async function exportCharacter(player) {
  const resp = await apiFetch(`/api/characters/${state.sessionId}/${encodeURIComponent(player)}/export`);
  if (!resp.ok) return notify('Export failed.', 'error');
  const blob = await resp.blob();
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `${slugify(charName(player)) || 'character'}.fof`;
  a.click();
}

// =====================================================================
// Level up
// =====================================================================
function levelUpHtml(me) {
  const adv = R().advancement || {};
  const next = me.level + 1;
  const f = facetDef(me.facet);
  const sigLevel = next === adv.signature_level;
  const statUp = (adv.stat_increase_levels || []).includes(next);
  const workingUp = me.magic && (adv.signature_working_levels || []).includes(next);
  const held = new Set((me.talents || []).map(t => t.id));
  let pick = '';
  if (sigLevel) {
    const sigs = (R().talents || []).filter(t => t.kind === 'signature' && onMenuOf(t, me.facet));
    const planned = (classDef((me.class || {}).id) || {}).signature;
    if (!ui.lvTalent && planned) ui.lvTalent = planned;
    pick = `<h3>Level ${next}: your signature</h3><p class="small muted">The class commits. From here on, rebuilding is no longer free.</p>
      <div class="choices">${sigs.map(t => `<button class="choice ${ui.lvTalent === t.id ? 'on' : ''}" data-lvt="${esc(t.id)}"><h4>${esc(t.name)}${t.id === planned ? ' <span class="chip gold">your class</span>' : ''}</h4><div class="desc">${esc(t.text)}</div></button>`).join('')}</div>
      ${ui.lvTalent === 'arcane_mastery' && me.magic ? `<label>Arcane Mastery: which signature working?</label><select data-ui="lvChoice">${me.magic.signature_workings.map(w => `<option ${uiv('lvChoice') === w ? 'selected' : ''}>${esc(w)}</option>`).join('')}</select>` : ''}
      ${ui.lvTalent === 'polymath' ? `<label>Polymath: two talents from any menu</label>${[0, 1].map(i => `<select data-ui="poly${i}">${(R().talents || []).filter(t => t.kind === 'talent' && !isCastingTalent(t) && !held.has(t.id)).map(t => `<option value="${esc(t.id)}" ${uiv('poly' + i) === t.id ? 'selected' : ''}>${esc(t.name)} (${esc(t.facet)})</option>`).join('')}</select>`).join('')}` : ''}`;
  } else {
    const kind = uiv('lvKind', 'talent');
    const menu = (R().talents || []).filter(t => t.kind === 'talent' && !held.has(t.id));
    const own = menu.filter(t => onMenuOf(t, me.facet));
    const other = menu.filter(t => !onMenuOf(t, me.facet) && !isCastingTalent(t));
    const improvable = (me.talents || []).filter(t => !t.improved && (talentDef(t.id) || {}).improved);
    const card = (t, attr) => `<button class="choice ${ui.lvTalent === t.id ? 'on' : ''}" ${attr}="${esc(t.id)}"><h4>${esc(t.name)}</h4><div class="desc">${esc(kind === 'improve' ? t.improved : t.text)}</div></button>`;
    pick = `<h3>Level ${next}: your pick</h3>${segmented('lvKind', [{ value: 'talent', label: 'A new talent' }, { value: 'improve', label: 'Improve a talent' }], kind)}
      ${kind === 'talent' ? `<div class="label">${esc(f ? f.name : '')} menu</div><div class="choices">${own.map(t => card(t, 'data-lvt')).join('') || '<div class="empty">You hold every talent on your menu.</div>'}</div>
        <details class="mt"><summary class="small muted">Another Facet's talent (needs a teacher found in play)</summary>
          <label class="row gap" style="text-transform:none;letter-spacing:0"><input type="checkbox" data-ui="lvTeacher" ${uiv('lvTeacher') ? 'checked' : ''}> We found a teacher in play</label>
          <div class="choices mt">${other.map(t => card(t, 'data-lvt')).join('')}</div></details>`
      : `<div class="choices mt">${improvable.map(s => card(talentDef(s.id), 'data-lvt')).join('') || '<div class="empty">Nothing to improve yet.</div>'}</div>`}
      ${ui.lvTalent === 'weapon_master' && kind === 'talent' ? `<label>Weapon kind</label><select data-ui="lvChoice">${((R().equipment || {}).weapon_kinds || []).map(k => `<option ${uiv('lvChoice') === k ? 'selected' : ''}>${k}</option>`).join('')}</select>` : ''}
      ${ui.lvTalent === 'wider_domain' && kind === 'talent' && me.magic ? `<label>Second domain</label><select data-ui="lvChoice">${(R().magic_domains || []).filter(d => d.tradition === me.magic.tradition && !d.prismatic && !me.magic.domains.includes(d.id)).map(d => `<option value="${esc(d.id)}" ${uiv('lvChoice') === d.id ? 'selected' : ''}>${esc(d.name)}</option>`).join('')}</select>` : ''}`;
  }
  const grit = f ? f.grit_die : 6, avg = f ? f.grit_average : 4;
  return `<div class="wizard"><div class="panel"><div class="banner gold"><div class="grow"><h3>Level ${me.level} → ${next}</h3><div class="small">The Mirror Master called it. Choose, then confirm.</div></div></div>
    ${pick}
    ${statUp ? `<div class="label">Level ${next} also raises a stat by 1 (maximum ${(R().stat_rules || {}).maximum || 3})</div>${segmented('lvStat', (R().stats || []).map(s => ({ value: s.id, label: `${s.name} ${signed(me.stats[s.id])}`, disabled: me.stats[s.id] >= ((R().stat_rules || {}).maximum || 3) })), uiv('lvStat'))}` : ''}
    ${workingUp ? `<label>Name another signature working</label><input type="text" data-ui="lvWorking" value="${inputVal('lvWorking')}" maxlength="200">` : ''}
    <div class="label">HP</div>${segmented('lvHp', [{ value: 'average', label: `Take the average (${avg})` }, { value: 'roll', label: `Roll the d${grit}` }], uiv('lvHp', 'average'))}
    <div class="wizard-foot"><span class="msg error" id="lv-err"></span><button class="btn primary big" data-lvgo>Level up</button></div></div></div>`;
}

function wireLevelUp(root, me) {
  $$('[data-lvt]', root).forEach(b => b.onclick = () => { ui.lvTalent = b.dataset.lvt; ui.lvChoice = undefined; renderBuild(); });
  $('[data-lvgo]', root).onclick = () => {
    const adv = R().advancement || {};
    const next = me.level + 1;
    const sig = next === adv.signature_level;
    if (!ui.lvTalent) { $('#lv-err').textContent = 'Choose your pick.'; return; }
    const sel = $('[data-ui="lvChoice"]', root);
    const msg = { type: 'level_pick', kind: sig ? 'signature' : uiv('lvKind', 'talent'), talent_id: ui.lvTalent,
      choice: sel ? sel.value : null, teacher: !!ui.lvTeacher, hp: uiv('lvHp', 'average') };
    if ((adv.stat_increase_levels || []).includes(next)) msg.stat = ui.lvStat || null;
    if (me.magic && (adv.signature_working_levels || []).includes(next)) msg.signature_working = ui.lvWorking || '';
    if (ui.lvTalent === 'polymath') msg.extra_talents = [0, 1].map(i => ($(`[data-ui="poly${i}"]`, root) || {}).value);
    send(msg);
    ['lvTalent', 'lvChoice', 'lvStat', 'lvWorking', 'lvTeacher'].forEach(k => delete ui[k]);
  };
}

function showLevelErrors(errors) {
  const el = $('#lv-err');
  if (el) el.textContent = errors.join(' ');
  else notify(errors.join(' '), 'error');
}

// =====================================================================
// Mirror Master: monster-card builder, library, characters
// =====================================================================
function mmBuildHtml() {
  const sub = uiv('mmBuild', 'monsters');
  const tabs = `<div class="subtabs"><button data-mmsub="monsters" class="${sub === 'monsters' ? 'on' : ''}">Monster cards</button><button data-mmsub="chars" class="${sub === 'chars' ? 'on' : ''}">Characters</button></div>`;
  if (sub === 'chars') {
    const chars = Object.values(state.chars);
    return `${tabs}<div class="panel"><h3>The party</h3>${chars.length ? chars.map(c => `<div class="lib-row"><span class="grow"><b>${esc(c.name)}</b> <span class="muted small">${esc(c.player_name)} · level ${c.level} ${esc((c.class || {}).name || '')}</span></span>
      <button class="btn small" data-exp="${esc(c.player_name)}">Download .fof</button></div>`).join('') : '<div class="empty">No characters yet.</div>'}</div><div id="wiz-root">${wizardHtml()}</div>`;
  }
  return `${tabs}<div class="builder-grid"><div>${monsterFormHtml()}</div><div>${monsterPreviewHtml()}${libraryHtml()}</div></div>`;
}

function monsterFormHtml() {
  const roles = Object.keys((R().monsters || {}).roles || {});
  const num = (k, lo, hi, ph) => `<input type="number" min="${lo}" max="${hi}" data-mb="${k}" value="${esc(mb[k] ?? '')}" placeholder="${esc(ph || '')}">`;
  const txt = (k, ph) => `<input type="text" data-mb="${k}" value="${esc(mb[k] || '')}" placeholder="${esc(ph || '')}" maxlength="500">`;
  return `<div class="panel"><h3>${mb.editing ? 'Edit card' : 'New monster card'}</h3>
    <p class="small muted">One dial and a role. Level and role set HP, damage and attack from the monster table; the card carries the texture.</p>
    <div class="two-col"><div><label>Name</label>${txt('name', 'e.g. Chalk Hound')}</div><div><label>Weapon (flavour)</label>${txt('weapon', 'e.g. Teeth')}</div></div>
    <label>Level: <b>${mb.level}</b></label><input type="range" min="1" max="10" value="${mb.level}" data-mb="level" style="width:100%;accent-color:var(--gold)">
    <label>Role</label>${segmented('mbRole', roles.map(r => ({ value: r, label: cap(r) })), mb.role)}
    <div class="two-col"><div><label>Armor</label>${segmented('mbArmor', ['0', '1', '2'], String(mb.armor))}</div>
      <div><label>Morale (2–12; 12 is fearless)</label>${num('morale', 2, 12)}</div></div>
    <details class="mt"><summary class="small muted">Override a number (the Bestiary marks it with †)</summary>
      <div class="two-col"><div><label>HP</label>${num('hp', 1, 500, 'from the table')}</div><div><label>Damage</label>${num('damage', 0, 50, 'from the table')}</div>
      <div><label>Attack bonus</label>${num('attack', -3, 10, 'from the table')}</div><div><label>Attacks</label>${num('attacks', 1, 4, 'from the role')}</div></div></details>
    <label>Wants</label>${txt('wants', 'What it is after')}
    <label>Special</label>${txt('special', 'One gimmick, stated so you can run it')}
    <label>When bloodied</label>${txt('when_bloodied', 'What changes at half HP (not needed for Mooks)')}
    <label>Tells</label>${txt('tells', 'What the table sees before it acts')}
    <label>Breaks</label>${txt('breaks', 'What it does when its morale breaks')}
    <label>Twists (d6)</label>${mb.twists.map((t, i) => `<input type="text" data-twist="${i}" value="${esc(t)}" placeholder="${i + 1}." maxlength="300" style="margin-bottom:.3rem">`).join('')}
    <label>Nastier (optional)</label>${txt('nastier', 'How to make it worse')}
    <label>Description</label><textarea data-mb="description" maxlength="2000">${esc(mb.description || '')}</textarea>
    <div class="wizard-foot"><button class="btn ghost" data-mbnew>Clear</button><span class="msg error" id="mb-err"></span><button class="btn primary" data-mbsave>Save to library</button></div></div>`;
}

function monsterPreviewHtml() {
  const c = mb.card;
  return `<div class="panel preview-card"><h3>Preview</h3>${c ? `<div class="foe"><div class="foe-top"><span class="foe-name">${esc(mb.name || 'Unnamed')}</span><span class="tiny muted">level ${c.level} ${esc(c.role)}</span>
      ${c.fearless ? '<span class="chip">Fearless</span>' : ''}</div>
      <div class="foe-nums"><span>HP <b>${c.hp === null ? 'drops to any hit' : c.hp}${c.overrides.includes('hp') ? '†' : ''}</b></span><span>Attack <b>${signed(c.attack)}${c.overrides.includes('attack') ? '†' : ''}</b></span>
        <span>Damage <b>${c.damage}${c.overrides.includes('damage') ? '†' : ''}</b></span><span>Attacks <b>${c.attacks}${c.overrides.includes('attacks') ? '†' : ''}</b></span><span>Armor <b>${c.armor}</b></span><span>Morale <b>${c.morale}</b></span></div>
      ${c.mob ? `<div class="small muted">Mooks attack as one mob: +${c.mob_damage_per_extra} damage per extra, max +${c.mob_damage_cap}.</div>` : ''}
      ${c.bloodied_phase ? '<div class="small muted">Bloodied: the card changes phase.</div>' : ''}
      <dl class="foe-card">${mb.wants ? `<dt>Wants</dt><dd>${esc(mb.wants)}</dd>` : ''}${mb.special ? `<dt>Special</dt><dd>${esc(mb.special)}</dd>` : ''}
        ${mb.when_bloodied ? `<dt>When bloodied</dt><dd>${esc(mb.when_bloodied)}</dd>` : ''}${mb.tells ? `<dt>Tells</dt><dd>${esc(mb.tells)}</dd>` : ''}
        ${mb.breaks ? `<dt>Breaks</dt><dd>${esc(mb.breaks)}</dd>` : ''}${mb.twists.some(Boolean) ? `<dt>Twists</dt><dd>${mb.twists.map((t, i) => `${i + 1}. ${esc(t)}`).join('<br>')}</dd>` : ''}</dl></div>`
    : '<div class="empty">Working out the numbers…</div>'}</div>`;
}

function libraryHtml() {
  const lib = Object.values(state.library).sort((a, b) => a.level - b.level || a.name.localeCompare(b.name));
  return `<div class="panel"><div class="panel-head"><h3>Library</h3><button class="btn small ghost right" data-bestiary>Load the Bestiary</button></div>
    ${lib.length ? lib.map(e => `<div class="lib-row"><span class="grow"><b>${esc(e.name)}</b> <span class="tiny muted">L${e.level} ${esc(e.role)} · HP ${e.card ? (e.card.hp ?? '—') : '?'} · dmg ${e.card ? e.card.damage : '?'}</span></span>
      ${e.role === 'mook' ? `<input type="number" min="1" max="30" value="4" data-libcount="${esc(e.id)}">` : ''}
      <button class="btn small primary" data-libspawn="${esc(e.id)}">Spawn</button><button class="btn small" data-libedit="${esc(e.id)}">Edit</button>
      <button class="btn small danger" data-libdel="${esc(e.id)}">×</button></div>`).join('') : '<div class="empty">No cards yet.</div>'}</div>`;
}

let _mbTimer = null;
function requestCardPreview() {
  clearTimeout(_mbTimer);
  _mbTimer = setTimeout(async () => {
    const body = { session_id: state.sessionId, level: Number(mb.level), role: mb.role, armor: Number(mb.armor), morale: Number(mb.morale) || 7 };
    ['hp', 'damage', 'attack', 'attacks'].forEach(k => { if (mb[k] !== undefined && mb[k] !== '' && mb[k] !== null) body[k] = Number(mb[k]); });
    const resp = await apiFetch('/api/enemies/preview-card', 'POST', body);
    if (!resp.ok) { mb.card = null; }
    else mb.card = (await resp.json()).card;
    if (state.tab === 'build' && isMM() && uiv('mmBuild', 'monsters') === 'monsters') {
      const box = $('.preview-card');
      if (box) box.outerHTML = monsterPreviewHtml();
    }
  }, 150);
}

function wireMMBuild(root) {
  $$('[data-mmsub]', root).forEach(b => b.onclick = () => { ui.mmBuild = b.dataset.mmsub; renderBuild(); });
  if (uiv('mmBuild', 'monsters') === 'chars') {
    $$('[data-exp]', root).forEach(b => b.onclick = () => exportCharacter(b.dataset.exp));
    wireWizard($('#wiz-root', root));
    return;
  }
  $$('[data-mb]', root).forEach(el => el.oninput = () => {
    mb[el.dataset.mb] = el.value;
    if (el.dataset.mb === 'level') { const b = el.previousElementSibling && $('b', el.previousElementSibling); if (b) b.textContent = el.value; }
    if (['level', 'morale', 'hp', 'damage', 'attack', 'attacks'].includes(el.dataset.mb)) requestCardPreview();
    else { const box = $('.preview-card'); if (box) box.outerHTML = monsterPreviewHtml(); }
  });
  $$('[data-twist]', root).forEach(el => el.oninput = () => { mb.twists[Number(el.dataset.twist)] = el.value; });
  $('[data-mbnew]', root).onclick = () => { Object.keys(mb).forEach(k => delete mb[k]); Object.assign(mb, { level: 1, role: 'standard', armor: 0, morale: 7, twists: ['', '', '', '', '', ''] }); renderBuild(); requestCardPreview(); };
  $('[data-mbsave]', root).onclick = saveCard;
  $('[data-bestiary]', root).onclick = () => send({ type: 'bestiary_load' });
  $$('[data-libspawn]', root).forEach(b => b.onclick = () => {
    const cnt = $(`[data-libcount="${b.dataset.libspawn}"]`, root);
    send({ type: 'enemy_spawn', enemy_id: b.dataset.libspawn, count: cnt ? Number(cnt.value) || 1 : 1 });
    notify('Added to the tracker (Play tab).', 'success');
  });
  $$('[data-libedit]', root).forEach(b => b.onclick = () => {
    const e = state.library[b.dataset.libedit];
    Object.keys(mb).forEach(k => delete mb[k]);
    Object.assign(mb, { editing: e.id, id: e.id, name: e.name, level: e.level, role: e.role, armor: e.armor, morale: e.morale, weapon: e.weapon,
      wants: e.wants, special: e.special, when_bloodied: e.when_bloodied || '', tells: e.tells, breaks: e.breaks, nastier: e.nastier || '',
      description: e.description, twists: (e.twists || []).concat(['', '', '', '', '', '']).slice(0, 6), ...(e.overrides || {}) });
    renderBuild(); requestCardPreview(); window.scrollTo(0, 0);
  });
  $$('[data-libdel]', root).forEach(b => b.onclick = async () => {
    if (!await confirmDialog('Delete this card?', 'It leaves the library; foes already on the tracker stay.', 'Delete')) return;
    const resp = await apiFetch(`/api/enemies/${state.sessionId}/${encodeURIComponent(b.dataset.libdel)}`, 'DELETE');
    if (resp.ok) { delete state.library[b.dataset.libdel]; renderBuild(); }
  });
  if (!mb.card) requestCardPreview();
}

/** Segmented controls in the builder map onto the card being built. */
const _prevUiChange = onUiChange;
onUiChange = function (key) {
  if (isMM() && state.tab === 'build') {
    if (key === 'mbRole') { mb.role = ui.mbRole; requestCardPreview(); return; }
    if (key === 'mbArmor') { mb.armor = Number(ui.mbArmor); requestCardPreview(); return; }
  }
  if (state.tab === 'build' && ['lvKind', 'lvStat', 'lvHp'].includes(key)) { if (key === 'lvKind') { delete ui.lvTalent; renderBuild(); } return; }
  _prevUiChange(key);
};

async function saveCard() {
  const err = $('#mb-err');
  if (!(mb.name || '').trim()) { err.textContent = 'Name the card.'; return; }
  const body = { session_id: state.sessionId, id: mb.editing || slugify(mb.name), name: mb.name.trim(), level: Number(mb.level), role: mb.role,
    armor: Number(mb.armor), morale: Number(mb.morale) || 7, weapon: mb.weapon || '', wants: mb.wants || '', special: mb.special || '',
    when_bloodied: mb.when_bloodied || null, tells: mb.tells || '', breaks: mb.breaks || '', twists: mb.twists.map(t => t.trim()).filter(Boolean),
    nastier: mb.nastier || null, description: mb.description || '' };
  ['hp', 'damage', 'attack', 'attacks'].forEach(k => { if (mb[k] !== undefined && mb[k] !== '' && mb[k] !== null) body[k] = Number(mb[k]); });
  const resp = await apiFetch('/api/enemies/', 'POST', body);
  if (!resp.ok) { err.textContent = formatApiError((await resp.json()).detail, 'The card is not complete.'); return; }
  const e = (await resp.json()).enemy;
  state.library[e.id] = e;
  mb.editing = e.id;
  notify(`${e.name} saved to the library.`, 'success');
  renderBuild();
}
