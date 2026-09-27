# BRIEF — Oraga Night, 5e Edition

*Brain output, 2026-09-27. Owner request: "making a high quality copy of Oraga Night
for 5e so I can play it in the mean time. This should include 5e bestiary for combat,
focusing on the fact that he has invited the snakes into the chicken pen by inviting
all of his enemies. Make a high quality workflow of the module as well so we have a
good visual."*

## 1. What we are making

A complete, table-ready D&D 5e edition of `adventures/oraga_night/` (the Lean Facets
version on `feat/lean-facets` is the source text). Same night, same canon, same seven
Movements, same spine (the Uninvited cannot be beaten; history bends toward the
recorded outcome through play). What changes:

1. **Rules layer** → D&D 5e, written against **SRD 5.2.1 (CC BY 4.0)** terms and
   compatible with 2014 5e tables. Checks are `DC 15 Wisdom (Insight)`; fights are
   5e stat blocks with CR and XP; loot is 5e items.
2. **Combat emphasis — "the snakes in the chicken pen."** Raunu invited every enemy he
   has into his own house. The 5e edition makes that the combat spine the Facets
   version kept offstage: every hostile faction at the ball brought knives, and each
   has a **visible, optional, escalating** threat line the party can walk into — before
   midnight as schemes, after midnight as knives out in the dark. The Uninvited remain
   the unbeatable storm; the snakes are what a sword can answer.
3. **A visual workflow** of the whole module (Movements → scenes → fights → branches
   → endings) as a published HTML page, plus the data behind it in the repo.

## 2. Decisions

- **Party**: four or five characters of **3rd level**, balanced for four. Every fight
  card carries a one-line scaling note for 2nd and for 4th–5th level / five PCs.
  3rd level because 1st-level 5e characters die to one crit, and this module now has
  real fights.
- **Location**: `conversions/dnd5e/oraga_night/` (outside `adventures/` so the Facets
  docs invariants in `software/tests/test_docs_consistency.py` do not bind it).
- **Licence**: SRD 5.2.1 only for rules/monster/spell/item references. No non-SRD WotC
  content (no non-SRD monsters, subclasses, feats, or setting names). Every file's
  README carries the SRD 5.2.1 attribution statement:
  > This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1")
  > by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD
  > 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License,
  > available at https://creativecommons.org/licenses/by/4.0/legalcode.
  Module text and canon remain the project's (GPLv3; Svara canon by the setting's
  author).
- **Iron law (CLAUDE.md)**: no new lore. Stat blocks for canon NPCs are mechanics, not
  lore. **Every** new fictional fact the snakes layer needs (a retainer type, a scheme
  step, a fight location, an item) is (a) derived from the NPC's canonical Wants/
  Fears/Secret/Agenda in Ch. III/VII, and (b) logged in
  `conversions/dnd5e/oraga_night/INVENTIONS_5e.md` for owner review, in the same table
  format as `references/oraga_night/INVENTIONS_FOR_REVIEW.md`.
- **Owner rulings that carry over** (from project memory — do not violate):
  no mandatory fights; optional fights must be *visible* (the players see trouble and
  choose to walk in); the Radiant cannot be turned, only made to feel guilty; Tavva's
  crew is the night's winnable fight aimed at noble-minded PCs; the Bought hold the
  gate at midnight; Raunu dies by his own choice by default; the tribes are human;
  written-word ban (no books; a great house's invitation is an exception); the module
  never answers the "What the Module Never Says" list.
- **The Uninvited in 5e**: full stat blocks (they must feel lethal, ~CR 9–11) with a
  **Leashed** trait that makes them unkillable tonight in a way a 5e table accepts
  (e.g. at 0 HP they fold into shadow and return at the next Movement beat; the east
  pulls harder each hour) and the module's **Fractures** rendered as 5e-legible
  triggers. Never make them beatable by a clever 5e exploit (banishment, power word,
  etc. — address the obvious SRD answers explicitly).
- **Val'loh player options in 5e**: the tribes are human; each tribe's gift → a 5e
  **origin feat-equivalent trait** (written fresh, SRD-shaped). Crystal charges →
  common/uncommon consumable magic items. Source: `settings/valloh/` + module Ch. III.
- **Pregens**: the module's five (`characters/*.fof`: Andra, Dassa, Ilesse, Pello,
  Serane) as 3rd-level 5e characters, SRD classes and SRD subclasses only, keeping
  name, concept, agenda hook and personality; mechanical choices are ours.

## 3. The snake roster (fixed names — all drafters use these)

Canon enemies (convert): **Feuding Kinsman** (S1 mob, from harbor thug), **Tavva**,
**Gallery Knife**, **Boranis Honor Guard**, **Sect Guard**, **Bought Blade**,
**Bought Sergeant**, **Bought Captain**, **The Hollow**, **The Radiant**, **The Wept**.

The snakes (canon NPCs who came as Raunu's enemies — stat blocks + retinues):

| Faction (canon NPC) | Leader block | Retinue block(s) |
|---|---|---|
| Merchant's Circle (Mistress **Rhaza Callun**) | Rhaza Callun | **Circle Hired Knife** |
| The Church (Prelate **Damaris Kovaun**) | Damaris Kovaun | **Church Warden** |
| Rival sect (Lord **Essar Draunel**) | Essar Draunel | **Draunel Duelist** |
| His own house (**Vorlain Boranis**, **Essin Boranis**) | Vorlain Boranis; Essin Boranis | **Boranis Cousin's Blade** |
| Phern (Master **Pellin Corro**) | Pellin Corro | **Phern Bodyguard** |
| Thenya (**Maiven Nolonaire**) — not a snake; a wary ally who can become a fight if provoked | Maiven Nolonaire | **Thenya Border Slinger** |

Noncombatants (Raunu, Veier, Corval, Anha, Mother Sella, Master Vell, Otta Vesh) get
a short "if it comes to it" stat line, never a fight card. Master Vell **will not
fight** if he can avoid it; give him a block that makes that obvious (escape, not
damage).

Drafters may add at most three further generic blocks if a fight needs one; log them.

## 4. Deliverables and ownership

`conversions/dnd5e/oraga_night/`

| File | Owner | Contents |
|---|---|---|
| `README.md` | Module | Overview, contents, how to run, attribution |
| `01_Overture.md` | Module | Running the module in 5e: level, pacing, rewards (XP + Inspiration-for-play mapping of "What the Night Pays"), safety, the snakes framing |
| `02_The_World_and_the_Night.md` | Module | World + MM truth, converted lightly (mostly prose; keep it) |
| `03_Masks_and_Agendas.md` | Module | Hooks, agendas with 5e rewards, masks, Val'loh 5e player options (tribe gifts, crystals), pregens summary |
| `04_The_Ball.md` | Ball | Rooms B1–B12, Movements I–V, undercurrents, all checks as 5e DCs; each snake scheme placed as visible trouble |
| `05_The_Longest_Night.md` | Ball | Movements VI–VII, the Uninvited in 5e, Fractures, the snakes in the dark, endings, If-History-Breaks |
| `06_Aftermath.md` | Module | Converted |
| `07_Cast_of_the_Ball.md` | Module | NPC roleplay pages, each pointing to its bestiary block |
| `08_Handouts.md` | Module | Handouts; night-tracker with a **Snake Tracker** column |
| `09_The_Snakes.md` | Bestiary | **The snakes chapter**: each faction's threat line (scheme → tell → escalation → what they do at midnight), the Snake Tracker, and all fight cards (S1–S5 converted + new snake fights), each with CR budget, terrain, objective, clock, outs, morale, scaling |
| `10_Bestiary.md` | Bestiary | Every 5e stat block, alphabetical, SRD format |
| `11_Pregenerated_Characters.md` | Module | Five 3rd-level pregens |
| `INVENTIONS_5e.md` | all | Every new fictional fact, for owner review |
| `flow/flow.json` | Flow | Node/edge data of the whole module for the visual |

## 5. Quality bar

- A 5e MM can run any scene from the page without the Facets books.
- Every fight: visible before it starts, optional, has ≥2 non-kill outs, a clock or
  objective that is not a body count, and a CR/XP budget line ("Medium for four
  3rd-level PCs: 450 XP adjusted…" — use SRD 5.2.1 encounter-building: XP budget per
  character by level and difficulty).
- Prose reads human (house rule: no AI rhythm; keep the original's voice — mostly
  *reuse* the source prose and change only the mechanics).
- Terminology: in this 5e edition, the table role may be called "DM" in rules
  sentences **only where quoting 5e terms is unavoidable** — house style prefers
  **Mirror Master (MM)**; use MM throughout.
