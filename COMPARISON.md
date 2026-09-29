# Rulesets and Editions, Side by Side

Facets of Origin currently carries three rulesets and two editions of its first adventure,
all in this one tree, so they can be compared before the owner chooses. Nothing here is
final until that choice is made.

## The three rulesets

| | **v0.3** | **Lean Facets** | **Facets d20** |
|---|---|---|---|
| Where | `rulesets/v0.3/` (read-only snapshot) | `player_handbook/`, `mm_manual/`, `bestiary/` | `facets_d20/` |
| Dice | 2d6 + attribute + skill, three-tier results | 2d6 + stat (+ a knack), three-tier results | d20 + modifier vs DC (SRD 5.2.1) |
| Harm | Conditions, no HP; enemies have Resolve | HP and Wounds; damage dice | HP, AC, damage (5e) |
| Character shape | Facet + skills advanced by marks; Techniques | Facet owns the numbers; preset or custom class; talents | Facet + five talents on Steel/Spell tracks; edges at even levels; knacks for roleplay |
| Magic | Domain + intent + scope; readied intents | Workings, Fatigue in slots | SRD spells: a shared Common list + one domain; no preparation |
| Combat | Simultaneous exchanges, postures, reactions | Players roll to act; foes roll in the open | Side initiative, morale at Bloodied, fixed monster damage, boss turns |
| Software engine | none (superseded) | `software/app/` — the running app | `software/facets_d20/` — rules engine + simulator (no app yet) |
| Status | Frozen at tag `pre-lean-facets` | v1.0 built; v1.1 plan awaiting owner | v0.2 complete: books rewritten, balanced by simulation, fresh-eyes playtested, edges added; awaiting a human table |
| Licence base | original | original | SRD 5.2.1, CC BY 4.0 (attributed) |
| Key docs | the tag's `docs/` | `docs/BRIEF_lean_facets*.md`, `docs/REVIEW_lean_facets.md` | `docs/BRIEF_facets_d20.md` (+ Amendments 1–3), `docs/AUDIT_facets_d20.md`, `docs/RESEARCH_facets_d20_*.md` |

## The two editions of Oraga Night

| | **Facets edition** | **Fifth-edition (SRD 5.2.1)** |
|---|---|---|
| Where | `adventures/oraga_night/` | `conversions/dnd5e/oraga_night/` |
| Rules | Lean Facets | fifth-edition rules, SRD 5.2.1 |
| Party | 3–5 characters, starting at level 1 | four 4th-level characters; ends at 5th |
| Length | one session + optional aftermath wing | one session, the night only, starting in the street |
| Combat | three fights, all optional | the snakes: 14 fight cards, one per invited enemy and more, plus the Attendant as the midnight boss |
| Visual | — | `conversions/dnd5e/oraga_night/flow/` (generated page) |
| Owner review | `references/oraga_night/` (private, not in the repo) | `conversions/dnd5e/oraga_night/INVENTIONS_5e.md` |

## How to compare

- Read each ruleset's character-creation chapter and build the same concept in all three.
- Run the same fight in each: the 5e edition's snake cards are a good test bed.
- For Facets d20, `software/tools/d20_sim.py` answers balance questions with numbers.
