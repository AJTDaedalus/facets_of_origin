# Facets of Origin

A digital-first, open-source tabletop RPG designed so the rules never get in the way of the story or the people at the table.

**Prioritize:** fun, socializing, worldbuilding, and storytelling.
**Minimize:** rules complexity, complicated mechanics, and gameplay friction.

---

## What's In The Box

### Player's Handbook (`player_handbook/`)

The complete rulebook for players:

- **Character Creation** — Attributes (9 stats, 18-point buy), three Facets (Body, Mind, Soul), 15 Backgrounds with starting skills and specialties, 24 skills across three facets
- **Magic** — Domain + Intent + Scope system with no spell lists. 27 domains across three traditions (Resonance, Channeling, and one TBD). Focused, Standard, Broad, and Prismatic domain types
- **Core Resolution** — 2d6 + modifier with three-tier outcomes (10+ full success, 7-9 partial, 6- consequence). Sparks add dice and drop lowest for pre-roll agency
- **Combat** — Exchange-based (simultaneous action, no turn order), posture system, Endurance pool, conditions instead of HP, armor as condition downgrade
- **Equipment** — Weapons, armor, adventuring gear, and services
- **Quick Start** — Pre-generated characters and a ten-minute intro scene

### Mirror Master's Manual (`mm_manual/`)

The companion guide for running the game:

- **MM1** — Encounters and Enemies: stat blocks, Threat Rating formula, encounter budget, action economy
- **MM2** — Session Design: three-act structure, pacing, scene types, improvisation, spotlight management
- **MM3** — Campaign Design: campaign structures, NPC design, world-building, encounter sequencing
- **MM4** — Running the Table: MM philosophy, table culture, safety and consent, difficult situations
- **MM5** — Quick Reference: mid-session cheat sheet for all core mechanics

### Digital Toolset (`software/`)

A self-hosted web app for running sessions online. The Mirror Master starts the server; players join via single-use invite links. See the [software README](software/README.md) for setup and usage.

Features:
- **Play Field** — Dice rolling, combat tracker (postures, strikes, reactions, conditions), magic casting, Spark economy, enemy tracker, table chat
- **Tools** — Read-only character sheets, inventory management, rule reference cards, encounter budget calculator
- **Builder** — Skill advancement (with PHB II.4 usage enforcement), technique selection, enemy/encounter builder, campaign notes

613 tests. TDD throughout.

### .fof File Format (`spec/`)

A YAML-based format for portable game documents. Types: `ruleset`, `character`, `campaign`, `session`, `enemy`, `encounter`. See the [spec README](spec/README.md).

### Example Content

- **Characters** (`characters/`) — Zahna (Mind/Guild Apprentice), Mordai (Body/City Watch), Zulnut (Body/Wandering Disciple)
- **Enemies** (`enemies/`) — Harbor Thug (Mook TR 1), City Watch Sergeant (Named TR 8), Archive Guardian (Boss TR 16), and others
- **Playtests** (`playtest/`) — Two simulated playtests with full session logs, dice rolls, and reports

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
├── software/              # Web app, game engine, tests (613)
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

- [x] Core ruleset: attributes, skills, Facets, Backgrounds, advancement
- [x] 2d6 resolution engine with Sparks
- [x] Combat system: exchanges, postures, conditions, armor
- [x] Magic system: Domain + Intent + Scope
- [x] Digital toolset: three-tab web app with real-time WebSocket
- [x] Enemy/encounter design system with Threat Rating
- [x] Mirror Master's Manual (5 chapters)
- [x] Two simulated playtests with issue tracking
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
