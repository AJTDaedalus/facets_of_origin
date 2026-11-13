// Map board (mapgen Phase 3 v1, docs/BRIEF_mapgen_phase3.md).
// Plumbing only: the MM puts a rendered map up; tokens for characters and active enemies
// are dragged on it; the server keeps positions in grid squares and tells the table.

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
    `<option value="${esc(x.id)}" ${uiv('map_pick', '') === x.id ? 'selected' : ''}>${esc(x.title)} (${x.squares.x}×${x.squares.y})</option>`).join('');
  const controls = mm ? `<div class="row gap map-controls">
      <button class="btn small" data-map="list">Maps…</button>
      ${picks ? `<select data-ui="map_pick">${picks}</select><button class="btn small primary" data-map="set">Show to the table</button>` : ''}
      ${m ? '<button class="btn small danger" data-map="clear">Take down</button>' : ''}</div>` : '';
  if (!m) {
    return mm ? `<div class="panel"><h3>Map</h3>${controls}<div class="small muted">No map up. Render one with <code>python -m mapgen render</code>, then pick it here.</div></div>` : '';
  }
  const placed = m.tokens || {};
  const toks = mapTokens();
  const onBoard = toks.filter(t => placed[t.id]).map(t => {
    const p = placed[t.id];
    const left = (p.x / m.squares.x) * 100;
    const top = (p.y / m.squares.y) * 100;
    const size = 100 / m.squares.x;
    const can = mm || t.mine;
    return `<div class="map-token ${t.kind} ${can ? 'can' : ''}" data-token="${esc(t.id)}" title="${esc(t.label)}"
      style="left:${left}%;top:${top}%;width:${size}%;">${esc(initials(t.label))}</div>`;
  }).join('');
  const tray = toks.filter(t => !placed[t.id] && (mm || t.mine)).map(t =>
    `<button class="btn small" data-place="${esc(t.id)}">Place ${esc(t.label)}</button>`).join('');
  const hint = mm ? 'Drag tokens. Shift-click a token to take it off the board.' : 'Drag your own token.';
  return `<div class="panel map-panel"><h3>${esc(m.title)}</h3>${controls}
    <div class="map-board" data-board><img src="${m.image}" alt="${esc(m.title)}" draggable="false">${onBoard}</div>
    ${tray ? `<div class="row gap wrap map-tray">${tray}</div>` : ''}
    <div class="small muted">${hint}</div></div>`;
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
  $$('[data-place]', root).forEach(b => b.onclick = () =>
    send({ type: 'token_move', token: b.dataset.place, x: m.squares.x / 2, y: m.squares.y / 2 }));
  const board = $('[data-board]', root);
  if (!board) return;
  $$('.map-token.can', board).forEach(el => {
    el.onpointerdown = ev => {
      if (ev.shiftKey && isMM()) { send({ type: 'token_remove', token: el.dataset.token }); return; }
      ev.preventDefault();
      el.setPointerCapture(ev.pointerId);
      const rect = board.getBoundingClientRect();
      el.onpointermove = e => {
        el.style.left = `${Math.max(0, Math.min(100, (e.clientX - rect.left) / rect.width * 100))}%`;
        el.style.top = `${Math.max(0, Math.min(100, (e.clientY - rect.top) / rect.height * 100))}%`;
      };
      el.onpointerup = e => {
        el.onpointermove = null;
        el.onpointerup = null;
        const sq = rect.width / m.squares.x;
        // snap the token's centre to the middle of a square
        const x = Math.floor((e.clientX - rect.left) / sq) + 0.5;
        const y = Math.floor((e.clientY - rect.top) / sq) + 0.5;
        send({ type: 'token_move', token: el.dataset.token, x, y });
      };
    };
  });
}
