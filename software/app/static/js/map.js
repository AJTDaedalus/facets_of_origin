// Map board (mapgen Phase 3 v1, docs/BRIEF_mapgen_phase3.md).
// Plumbing only: the MM puts a rendered map up; tokens for characters and active enemies
// are dragged on it; the server keeps positions in grid squares and tells the table.
//
// The board is one persistent DOM node per map (image, fog layer, token layer), built with
// DOM properties rather than HTML strings, so server data is never parsed as markup and the
// multi-MB image is decoded once. Token moves patch the token layer only; a drag in progress
// is never interrupted by an incoming update.

const MAPUI = { id: null, src: null, el: null, fog: null, layer: null, dragging: false, pendingRefresh: false };
const SVGNS = 'http://www.w3.org/2000/svg';

function mapTokens() {
  const out = [];
  Object.entries(state.chars || {}).forEach(([pn, c]) => out.push({ id: `pc:${pn}`, label: c.name || pn, kind: 'pc', mine: pn === myName() }));
  Object.values(state.enemies || {}).forEach(e => { if (!e.defeated) out.push({ id: `foe:${e.key}`, label: e.name, kind: 'foe', mine: false }); });
  return out;
}

function initials(name) { return String(name || '?').split(/\s+/).map(w => w[0]).join('').slice(0, 2).toUpperCase(); }

function mapBoardHtml() {
  const m = state.map;
  const mm = isMM();
  const picks = (state.mapList || []).map(x =>
    `<option value="${esc(x.id)}" ${uiv('map_pick', '') === x.id ? 'selected' : ''}>${esc(x.title)} (${Number(x.squares.x)}×${Number(x.squares.y)})</option>`).join('');
  const controls = mm ? `<div class="row gap map-controls">
      <button class="btn small" data-map="list">Maps…</button>
      ${picks ? `<select data-ui="map_pick">${picks}</select><button class="btn small primary" data-map="set">Show to the table</button>` : ''}
      ${m ? '<button class="btn small danger" data-map="clear">Take down</button>' : ''}</div>` : '';
  if (!m) {
    return mm ? `<div class="panel"><h3>Map</h3>${controls}<div class="small muted">No map up. Render one with <code>python -m mapgen render</code>, then pick it here.</div></div>` : '';
  }
  const fog = m.fog || { enabled: false, revealed: [], areas: {} };
  const placed = m.tokens || {};
  const tray = mapTokens().filter(t => !placed[t.id] && (mm || t.mine)).map(t =>
    `<button class="btn small" data-place="${esc(t.id)}">Place ${esc(t.label)}</button>`).join('');
  const areaNames = Object.keys(fog.areas || {});
  const fogControls = mm ? `<div class="row gap wrap map-fog-controls">
      <button class="btn small ${fog.enabled ? 'on' : ''}" data-fog="toggle">Fog: ${fog.enabled ? 'on' : 'off'}</button>
      ${fog.enabled ? areaNames.map(a => `<label class="chip"><input type="checkbox" data-fog-area="${esc(a)}" ${fog.revealed.includes(a) ? 'checked' : ''}> ${esc(a.replace(/_/g, ' '))}</label>`).join('') : ''}
      ${fog.enabled && !areaNames.length ? '<span class="small muted">No areas to reveal: list them under <code>fog_areas</code> in the recipe.</span>' : ''}
      ${fog.enabled ? '<span class="small muted">Fog hides areas and foes from players; the picture itself still reaches their browsers.</span>' : ''}
    </div>` : '';
  const hint = mm ? 'Drag tokens. Shift-click a token to take it off the board.' : 'Drag your own token.';
  return `<div class="panel map-panel"><h3>${esc(m.title)}</h3>${controls}${fogControls}
    <div class="map-scroll" data-board-slot></div>
    ${tray ? `<div class="row gap wrap map-tray">${tray}</div>` : ''}
    <div class="small muted">${hint}</div></div>`;
}

function ensureBoard(m) {
  if (MAPUI.el && MAPUI.id === m.id && MAPUI.src === m.image) return;
  const el = document.createElement('div');
  el.className = 'map-canvas';
  const img = document.createElement('img');
  img.draggable = false;
  img.alt = String(m.title || 'map');
  img.src = String(m.image || '');          // a property, never markup
  const fog = document.createElement('div');
  fog.className = 'map-fog-wrap';
  const layer = document.createElement('div');
  layer.className = 'map-tokens';
  el.append(img, fog, layer);
  Object.assign(MAPUI, { id: m.id, src: m.image, el, fog, layer, dragging: false });
  layer.addEventListener('pointerdown', onTokenDown);
}

function svgRect(attrs) {
  const r = document.createElementNS(SVGNS, 'rect');
  Object.entries(attrs).forEach(([k, v]) => r.setAttribute(k, String(v)));
  return r;
}

function updateBoard() {
  const m = state.map;
  if (!m || !MAPUI.el) return;
  const sx = Number(m.squares.x) || 1, sy = Number(m.squares.y) || 1;
  MAPUI.fog.replaceChildren();
  const fog = m.fog || {};
  if (fog.enabled) {
    const svg = document.createElementNS(SVGNS, 'svg');
    svg.setAttribute('class', 'map-fog');
    svg.setAttribute('viewBox', `0 0 ${sx} ${sy}`);
    svg.setAttribute('preserveAspectRatio', 'none');
    const mask = document.createElementNS(SVGNS, 'mask');
    mask.setAttribute('id', 'fogmask');
    mask.append(svgRect({ width: sx, height: sy, fill: 'white' }));
    (fog.revealed || []).forEach(a => {
      const b = (fog.areas || {})[a];
      if (!b) return;
      mask.append(svgRect({ x: Number(b[0]), y: Number(b[1]), width: Math.max(0, Number(b[2]) - Number(b[0])),
        height: Math.max(0, Number(b[3]) - Number(b[1])), fill: 'black' }));
    });
    const defs = document.createElementNS(SVGNS, 'defs');
    defs.append(mask);
    svg.append(defs, svgRect({ width: sx, height: sy, fill: '#0b0c10', opacity: isMM() ? 0.45 : 0.96, mask: 'url(#fogmask)' }));
    MAPUI.fog.append(svg);
  }
  if (MAPUI.dragging) return;              // never yank a token out from under a drag
  MAPUI.layer.replaceChildren();
  const placed = m.tokens || {};
  mapTokens().forEach(t => {
    const p = placed[t.id];
    if (!p) return;
    const d = document.createElement('div');
    d.className = `map-token ${t.kind}${isMM() || t.mine ? ' can' : ''}`;
    d.dataset.token = t.id;
    d.title = t.label;
    d.textContent = initials(t.label);
    d.style.left = `${(Number(p.x) / sx) * 100}%`;
    d.style.top = `${(Number(p.y) / sy) * 100}%`;
    d.style.width = `${100 / sx}%`;
    MAPUI.layer.append(d);
  });
}

function onTokenDown(ev) {
  const el = ev.target.closest('.map-token.can');
  const m = state.map;
  if (!el || !m) return;
  if (ev.shiftKey && isMM()) { send({ type: 'token_remove', token: el.dataset.token }); return; }
  ev.preventDefault();
  el.setPointerCapture(ev.pointerId);
  MAPUI.dragging = true;
  const mapAtStart = m.id;
  const box = () => MAPUI.el.getBoundingClientRect();   // the image's own box, so scrolling can't skew it
  let last = { x: ev.clientX, y: ev.clientY }, moved = false;
  el.onpointermove = e => {
    last = { x: e.clientX, y: e.clientY };
    moved = true;
    const r = box();
    el.style.left = `${Math.max(0, Math.min(100, (e.clientX - r.left) / r.width * 100))}%`;
    el.style.top = `${Math.max(0, Math.min(100, (e.clientY - r.top) / r.height * 100))}%`;
  };
  let done = false;
  const finish = e => {
    if (done) return;
    done = true;
    el.onpointermove = null; el.onpointerup = null; el.onpointercancel = null; el.onlostpointercapture = null;
    MAPUI.dragging = false;
    // pointerup commits where the pointer is; a lost capture (e.g. the board was re-rendered
    // under the drag) commits the last position seen; only an explicit cancel discards it
    // a drop onto a map that has since been swapped or taken down is discarded
    const sameMap = state.map && state.map.id === mapAtStart;
    const commit = sameMap && (e.type === 'pointerup' || (e.type === 'lostpointercapture' && moved));
    if (commit) {
      const px = e.type === 'pointerup' ? e.clientX : last.x;
      const py = e.type === 'pointerup' ? e.clientY : last.y;
      const r = box();
      const sq = r.width / Number(m.squares.x);
      const x = Math.max(0.5, Math.min(Number(m.squares.x) - 0.5, Math.floor((px - r.left) / sq) + 0.5));
      const y = Math.max(0.5, Math.min(Number(m.squares.y) - 0.5, Math.floor((py - r.top) / sq) + 0.5));
      send({ type: 'token_move', token: el.dataset.token, x, y });
    }
    if (MAPUI.pendingRefresh) { MAPUI.pendingRefresh = false; refresh(['play']); }
    else if (!commit) updateBoard();
  };
  el.onpointerup = finish;
  el.onpointercancel = finish;
  el.onlostpointercapture = finish;
}

/** Patch the board in place (token moves, fog) without rebuilding the play tab. */
function mapRefresh(trayChanged) {
  if (!trayChanged && state.tab === 'play' && MAPUI.el && MAPUI.el.isConnected) updateBoard();
  else refresh(['play']);
}

function wireMapBoard(root) {
  $$('[data-map]', root).forEach(b => b.onclick = () => {
    const a = b.dataset.map;
    if (a === 'list') send({ type: 'map_list' });
    if (a === 'set') { const sel = $('[data-ui="map_pick"]', root); if (sel) send({ type: 'map_set', id: sel.value }); }
    if (a === 'clear') send({ type: 'map_clear' });
  });
  $$('[data-ui="map_pick"]', root).forEach(s => s.onchange = () => { ui.map_pick = s.value; });
  const m = state.map;
  if (!m) return;
  $$('[data-fog]', root).forEach(b => b.onclick = () =>
    send({ type: 'fog_set', enabled: !(m.fog && m.fog.enabled) }));
  $$('[data-fog-area]', root).forEach(c => c.onchange = () =>
    send({ type: 'fog_reveal', area: c.dataset.fogArea, revealed: c.checked }));
  $$('[data-place]', root).forEach(b => b.onclick = () =>
    send({ type: 'token_move', token: b.dataset.place, x: Number(m.squares.x) / 2, y: Number(m.squares.y) / 2 }));
  const slot = $('[data-board-slot]', root);
  if (!slot) return;
  ensureBoard(m);
  slot.appendChild(MAPUI.el);          // the same node every render: the image is not re-decoded
  updateBoard();
}
