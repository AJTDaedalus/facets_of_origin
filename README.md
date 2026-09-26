# Facets of Origin

A digital-first, open-source tabletop RPG designed so the rules never get in the way of the story or the people at the table.

**Prioritize:** fun, socializing, worldbuilding, and storytelling.
**Minimize:** rules complexity, complicated mechanics, and gameplay friction.

---

## What's In The Box

<!-- Figures below are derived from canon, not hand-maintained — verify against
     source before editing: talent/class/domain counts from software/facets/base/facet.yaml;
     test count from `pytest --collect-only -q` (software/); enemy levels
     from enemies/*.fof; playtest count from committed playtest/ dirs. -->

### Player's Handbook (`player_handbook/`)

The complete rulebook for players:

- **Character Creation** — three stats (Body, Mind, Soul); three Facets that each hold four preset classes, or build your own class from the Facet's talent menu (Morrowind-style); 15 example backgrounds with knacks and Specialties; ten minutes to play
- **Magic** — Domain + Intent + Scope with no spell lists. 21 domains across the two traditions (Thaumaturgy/Mind, Invocation/Soul); Minor workings are free, Significant and Major ones cost Fatigue that fills inventory slots; each caster names signature workings. The Facet of the Body has no magic
- **Core Resolution** — 2d6 + stat (+1 for a knack) with three-tier outcomes (10+ full success, 7–9 success with a cost, 6− things go wrong). Sparks, Help and Borrowed Trouble each add a die, keep the best two
- **Combat** — exchanges with no initiative; players roll to act, enemies roll their attacks in the open; HP, weapon damage dice, flat armor; morale ends most fights; monster cards with one gimmick and a Bloodied phase
- **Levels** — 1 to 10, called by the MM from five end-of-session prompts; each level brings HP and a new talent or an improved one, with a signature at level 3
- **Equipment and Treasure** — inventory slots, weapon dice, flat armor, usage dice, curios and relics
- **Quick Start** — the one rule, a preset character in ten minutes, and combat in five lines

### Mirror Master's Manual (`mm_manual/`)

The companion guide for running the game:

- **MM1** — Encounters and Enemies: monster cards, the level table and roles, morale, the reaction roll, reading a fight's danger
- **MM2** — Session Design: three-act structure, pacing, scene types, improvisation, spotlight management
- **MM3** — Campaign Design: level pacing and prompts, treasure and the reward loop, retainers, the optional name-level endgame
- **MM4** — Running the Table: MM philosophy, table culture, safety and consent, difficult situations
- **MM5** — Quick Reference: mid-session cheat sheet for all core mechanics
- **MM6** — The Toolbox: reaction, morale, the Pressure die, complications, loot, NPCs and the oracle, with 24 generated tables (503 entries)

### Bestiary (`bestiary/`)

The third core book: eighteen creatures across four chapters, every one of them
original to this project and every one of them shipping a resolution that is not
a fight.

- **B1** — Beasts and Vermin: chalk hounds, glassbacks, ledgerlice, the chicken
- **B2** — Folk: the ordinary dangerous, the Bought, the Kindly
- **B3** — The Made: latchlings, latchmen, and the Archive Guardian
- **B4** — What Remains: the Waiting, the Unfinished, hushfall
- **Finding Aids** — every creature by level, role and morale *(generated)*

Entries carry a read-aloud opener, lore, a stat block generated from the
creature's `.fof` file, a tiered "What Characters Can Know" box keyed to the
2d6 outcome tiers, labelled sample encounters, ecology, and an Adaptation note
for porting the creature into a setting. Nothing in the book is Shattered Origin
canon.

### Digital Toolset (`software/`)

A self-hosted web app for running sessions online. The Mirror Master starts the server; players join via single-use invite links. See the [software README](software/README.md) for setup and usage.

Features:
- **Build** — a creation wizard (preset or custom class), level-up picks, and the MM's monster-card builder
- **Play** — character sheet with slots, Wounds and Fatigue; roll, attack, cast, defend and avoid; the MM's combat tracker with enemy attacks rolled in the open, morale and Bloodied phases; the Toolbox (reaction, Pressure die, complications, loot, NPCs, oracle, and Stuck?); threat clocks; end-of-session level prompts; Sparks and chat
- **Tools** — rules reference from the loaded ruleset, inventory, notes, `.fof` export

1103 tests (engine, WebSocket, docs invariants, and Playwright browser flows). TDD throughout.

### .fof File Format (`spec/`)

A YAML-based format for portable game documents. Types: `ruleset`, `character`, `campaign`, `session`, `enemy`, `encounter`. See the [spec README](spec/README.md).

### Example Content

- **Characters** (`characters/`) — Zahna (Mind/Guild Apprentice), Mordai (Body/City Watch), Zulnut (Body/Wandering Disciple)
- **Enemies** (`enemies/`) — 18 stat files, TR 1 through 17, rendered into the Bestiary
- **Playtests** (`playtest/`) — Six simulated playtests with full session logs, dice rolls, and reports

---

## Getting Started

### Run the digital toolset

```bash
git clone https://github.com/AJTDaedalus/facets_of_origin.git
cd facets_of_origin/software
pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open `http://localhost:8000`, set the MM password, and create a session. See [software/README.md](software/README.md) for player invites, remote play, and deployment options.

### Read the rules

Start with `player_handbook/Quick_Start.md` for a ten-minute overview, or `player_handbook/Table_of_Contents.md` for the full structure.

---

## Project Structure

```
facets_of_origin/
├── player_handbook/       # Complete PHB: creation, rules, combat, equipment
├── mm_manual/             # Mirror Master's Manual (5 chapters)
├── bestiary/              # Bestiary: 18 original creatures (4 chapters)
├── software/              # Web app, game engine, tests (1029)
│   ├── app/               # FastAPI backend + vanilla JS frontend
│   ├── facets/base/       # Core ruleset YAML
│   └── tests/             # Unit, integration, and e2e tests
├── spec/                  # .fof format specification and examples
├── characters/            # Example character .fof files
├── enemies/               # Example enemy .fof files
├── playtest/              # Simulated playtest logs and reports
└── research/              # Design analysis documents
```

---

## Roadmap

- [x] Core ruleset (Lean Facets v1.0): stats, Facets and classes, talents, levels 1–10, knacks and Specialties
- [x] 2d6 resolution engine with Sparks
- [x] Combat system: exchanges, HP and damage, enemy rolls, morale, monster cards
- [x] Magic system: Domain + Intent + Scope
- [x] Digital toolset: three-tab web app with real-time WebSocket
- [x] Enemy/encounter design system with Threat Rating
- [x] Mirror Master's Manual (5 chapters)
- [x] Six simulated playtests with issue tracking
- [ ] Persistent storage (sessions survive server restart)
- [ ] First real playtest with human players
- [ ] Adventure module: *The Shattered Crown*
- [ ] Optional Facet modules: Downtime, Crafting, Economy, Feats, Technology

---

## Contributing

Contributions are welcome. This project uses **test-driven development** — all new behaviour requires tests.

1. Fork the project
2. Create a feature branch: `git checkout -b feature/MyFeature`
3. Write tests alongside your changes
4. Commit: `git commit -m 'Add some feature'`
5. Push: `git push origin feature/MyFeature`
6. Open a Pull Request

See `CLAUDE.md` for detailed development guidelines, terminology, and copyright policy.

---

## License

GPLv3 — see `LICENSE.txt`.

---

## Contact

Project Link: [https://github.com/AJTDaedalus/facets_of_origin](https://github.com/AJTDaedalus/facets_of_origin)
