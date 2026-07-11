/**
 * Shared rendering components used across tabs.
 * Depends on: state, escapeHtml from app.js
 */

// ---------------------------------------------------------------------------
// Character sheet (read-only, used in Tools tab and player list)
// ---------------------------------------------------------------------------
function renderCharacterSheetReadOnly(char, ruleset, containerId) {
  const container = document.getElementById(containerId);
  if (!container || !char || !ruleset) return;

  const facetDef = ruleset.character_facets.find(cf => cf.id === char.primary_facet);
  const facetName = facetDef ? facetDef.name : char.primary_facet;

  let html = `
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
      <h3 style="font-size:1.1rem;margin:0;">${escapeHtml(char.name)}</h3>
      <span class="facet-badge facet-${char.primary_facet}">${facetName}</span>
      <span style="font-size:0.8rem;color:var(--text-dim);">Level ${char.facet_level}</span>
    </div>
  `;

  // Attributes grid
  html += '<div class="card-title">Attributes</div>';
  ruleset.major_attributes.forEach(major => {
    html += `<div class="major-group"><div class="major-label">${major.name}</div><div class="attr-grid">`;
    major.minor_attributes.forEach(minorId => {
      const minor = ruleset.minor_attributes.find(m => m.id === minorId);
      if (!minor) return;
      const rating = char.attributes[minorId] || 2;
      const ratingDef = ruleset.attribute_ratings.find(r => r.rating === rating);
      const mod = ratingDef ? ratingDef.modifier : 0;
      const modStr = mod > 0 ? `+${mod}` : `${mod}`;
      html += `
        <div class="attr-block" style="cursor:default;">
          <div class="attr-name">${minor.name}</div>
          <div class="attr-rating">${rating}</div>
          <div class="attr-modifier">${modStr}</div>
          <div class="attr-label">${ratingDef ? ratingDef.label : ''}</div>
        </div>`;
    });
    html += '</div></div>';
  });

  // Skills table
  html += '<div class="card-title" style="margin-top:16px;">Skills</div>';
  html += '<table class="skills-table"><thead><tr><th>Skill</th><th>Rank</th><th>Progress</th></tr></thead><tbody>';
  ruleset.skills.forEach(skill => {
    if (skill.status === 'stub') return;
    const ss = char.skills[skill.id] || { rank: 'novice', marks: 0 };
    const marksNeeded = ruleset.advancement ? ruleset.advancement.marks_per_rank : 3;
    const dots = String.fromCodePoint(0x25CF).repeat(ss.marks) + String.fromCodePoint(0x25CB).repeat(Math.max(0, marksNeeded - ss.marks));
    const isPrimary = skill.facet === char.primary_facet;
    html += `<tr>
      <td>${skill.name}${isPrimary ? '' : ' <span style="color:var(--text-dim);font-size:10px">' + String.fromCodePoint(0x25CF) + '</span>'}</td>
      <td><span class="rank-badge rank-${ss.rank}">${ss.rank}</span></td>
      <td class="marks-dots">${dots}</td>
    </tr>`;
  });
  html += '</tbody></table>';

  // Techniques
  if (char.techniques && char.techniques.length > 0) {
    html += '<div class="card-title" style="margin-top:16px;">Techniques</div>';
    html += '<ul style="list-style:none;font-size:13px;">';
    char.techniques.forEach(t => {
      const choice = char.technique_choices && char.technique_choices[t];
      html += `<li style="padding:3px 0;border-bottom:1px solid rgba(255,255,255,0.04);">${t}${choice ? ' (' + escapeHtml(choice) + ')' : ''}</li>`;
    });
    html += '</ul>';
  }

  // Background & specialty
  if (char.background_id || char.specialty) {
    html += '<div class="card-title" style="margin-top:16px;">Background</div>';
    if (char.background_id) html += `<div style="font-size:13px;margin-bottom:4px;">${escapeHtml(char.background_id)}</div>`;
    if (char.specialty) html += `<div style="font-size:12px;color:var(--text-dim);font-style:italic;">${escapeHtml(char.specialty)}</div>`;
  }

  // Magic
  if (char.magic_domain) {
    html += '<div class="card-title" style="margin-top:16px;">Magic</div>';
    html += `<div style="font-size:13px;">Domain: ${escapeHtml(char.magic_domain)}${char.magic_technique_active ? '' : ' (pre-technique)'}</div>`;
    if (char.secondary_magic_domain) {
      html += `<div style="font-size:13px;">Secondary: ${escapeHtml(char.secondary_magic_domain)}</div>`;
    }
  }

  // Career stats
  html += `<div style="margin-top:16px;font-size:12px;color:var(--text-dim);">
    Career Advances: ${char.career_advances} | Total Facet Levels: ${char.total_facet_levels} | SP Remaining: ${char.session_skill_points_remaining}
  </div>`;

  container.innerHTML = html;
}

// ---------------------------------------------------------------------------
// Compact character card (used in player list)
// ---------------------------------------------------------------------------
function renderCharacterCompact(char, ruleset) {
  if (!char) return '';
  const facetDef = ruleset ? ruleset.character_facets.find(cf => cf.id === char.primary_facet) : null;
  const facetName = facetDef ? facetDef.name : char.primary_facet;
  return `
    <span>${escapeHtml(char.player_name)}${char.name !== char.player_name ? ' (' + escapeHtml(char.name) + ')' : ''}</span>
    <span class="facet-badge facet-${char.primary_facet}">${facetName}</span>
  `;
}

// ---------------------------------------------------------------------------
// Combat state rendering (shared between Play and Tools)
// ---------------------------------------------------------------------------
function renderCombatStateCompact(char) {
  if (!char || char.endurance_current === null || char.endurance_current === undefined) return '';
  const condStr = char.conditions && char.conditions.length > 0 ? char.conditions.join(', ') : 'none';
  return `<span style="font-size:11px;color:var(--text-dim);">End: ${char.endurance_current} | ${char.posture || 'measured'} | ${condStr}</span>`;
}

// ---------------------------------------------------------------------------
// Enemy card rendering (shared between MM tracker and player view)
// ---------------------------------------------------------------------------
// Mooks have no Resolve pool — they fall to one Strike. Returns null for mooks,
// otherwise {current, max} where current falls back to max before combat starts.
function enemyResolveDisplay(enemy) {
  if (enemy.tier === 'mook') return null;
  const max = enemy.resolve || 0;
  const current = (enemy.resolve_current !== null && enemy.resolve_current !== undefined)
    ? enemy.resolve_current : max;
  return { current: current, max: max };
}

function renderEnemyCard(key, enemy, opts) {
  opts = opts || {};
  const condStr = enemy.conditions && enemy.conditions.length > 0
    ? enemy.conditions.join(', ') : 'none';
  const res = enemyResolveDisplay(enemy);
  const hasPhases = opts.showPhases && enemy.phases && enemy.phases.length > 0;

  let resolveBlock;
  if (res) {
    const denom = res.max || res.current || 1;
    const pct = Math.round((res.current / denom) * 100);
    const fillClass = 'resolve-fill' + (pct <= 25 ? ' critical' : pct <= 50 ? ' low' : '');
    let markers = '';
    if (hasPhases) {
      markers = enemy.phases.map(function (p) {
        const left = Math.max(0, Math.min(100, Math.round((p.resolve_threshold / denom) * 100)));
        return '<span class="resolve-phase-marker" style="left:' + left + '%;"'
          + ' title="Phase at ' + p.resolve_threshold + ': ' + escapeHtml(p.description || '') + '"></span>';
      }).join('');
    }
    resolveBlock =
      '<div class="resolve-bar"><div class="' + fillClass + '" style="width:' + pct + '%;"></div>' + markers + '</div>'
      + '<div style="font-size:11px;color:var(--text-dim);">Resolve <span class="enemy-resolve">'
      + res.current + '</span>/' + res.max + '</div>';
  } else {
    resolveBlock = '<div style="font-size:12px;color:var(--text-dim);">Mook &mdash; falls to one Strike</div>';
  }

  let phaseNote = '';
  if (hasPhases) {
    phaseNote = '<div style="font-size:11px;color:var(--text-dim);margin-top:2px;">Phases at Resolve: '
      + enemy.phases.map(function (p) { return escapeHtml(String(p.resolve_threshold)); }).join(', ')
      + '</div>';
  }

  let controls = '';
  if (opts.mmControls) {
    controls =
      '<div class="btn-row" style="margin-top:4px;">'
      + (res ? '<button class="btn btn-secondary btn-sm" onclick="enemyTakeDamage(\'' + escapeHtml(key) + '\')">-1 Resolve</button>' : '')
      + '<button class="btn btn-secondary btn-sm" onclick="enemyAddCondition(\'' + escapeHtml(key) + '\')">+Cond</button>'
      + '<button class="btn btn-secondary btn-sm" onclick="removeEnemy(\'' + escapeHtml(key) + '\')">Remove</button>'
      + '</div>';
  }

  return ''
    + '<div class="enemy-tracker-entry">'
    + '<div style="display:flex;justify-content:space-between;align-items:center;">'
    + '<strong>' + escapeHtml(enemy.name) + '</strong>'
    + '<span style="font-size:11px;color:var(--text-dim);">' + escapeHtml(enemy.tier) + ' | TR ' + (enemy.tr || '?') + '</span>'
    + '</div>'
    + '<div style="margin-top:4px;">' + resolveBlock + '</div>'
    + '<div style="font-size:12px;margin-top:2px;">Cond: ' + escapeHtml(condStr) + '</div>'
    + phaseNote
    + controls
    + '</div>';
}

// ---------------------------------------------------------------------------
// Threat Clock card (PHB III.2, D4) — visible to the whole table
// ---------------------------------------------------------------------------
function renderThreatClockCard(clock, opts) {
  opts = opts || {};
  const segments = [];
  for (let i = 0; i < clock.segments; i++) {
    segments.push('<span class="clock-segment' + (i < clock.filled_segments ? ' filled' : '') + '"></span>');
  }

  let controls = '';
  if (opts.mmControls) {
    controls =
      '<div class="btn-row" style="margin-top:4px;">'
      + '<button class="btn btn-secondary btn-sm" onclick="clockAdvance(\'' + escapeHtml(clock.id) + '\', \'partial_success\')">Advance (7-9)</button>'
      + '<button class="btn btn-secondary btn-sm" onclick="clockAdvance(\'' + escapeHtml(clock.id) + '\', \'failure\')">Advance (6-)</button>'
      + '<button class="btn btn-secondary btn-sm" onclick="clockWindBack(\'' + escapeHtml(clock.id) + '\')">Wind Back</button>'
      + '</div>';
  }

  return ''
    + '<div class="threat-clock-entry' + (clock.is_full ? ' clock-full' : '') + '">'
    + '<div style="display:flex;justify-content:space-between;align-items:center;">'
    + '<strong>' + escapeHtml(clock.name) + '</strong>'
    + '<span style="font-size:11px;color:var(--text-dim);">' + clock.filled_segments + '/' + clock.segments
    + (clock.is_full ? ' — STRIKES' : '') + '</span>'
    + '</div>'
    + '<div class="clock-segments">' + segments.join('') + '</div>'
    + controls
    + '</div>';
}

// ---------------------------------------------------------------------------
// Rule summary card (collapsible, used in Tools tab)
// ---------------------------------------------------------------------------
function renderRuleSummaryCard(title, content) {
  return `
    <div class="card rule-summary-card">
      <div class="card-title rule-summary-toggle" onclick="this.parentElement.classList.toggle('expanded')" style="cursor:pointer;">
        ${escapeHtml(title)} <span class="toggle-arrow">+</span>
      </div>
      <div class="rule-summary-content">${content}</div>
    </div>
  `;
}
