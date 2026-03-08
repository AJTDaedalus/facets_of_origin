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
