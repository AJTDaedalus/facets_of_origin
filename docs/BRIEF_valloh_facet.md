# BRIEF — The Val'loh Setting Facet: Lineages, Gift Domains, Spellforms, Crystals

**Date:** 2026-09-08 · **Tier:** Brain · **Parent:** `docs/BRIEF_oraga_starter_module.md` §5
**Depends on:** `docs/BRIEF_lineage.md` (must land first)
**Feeds:** `docs/DESIGN_valloh_facet.md`, `docs/TASKS_valloh_facet.md`
**Owner rulings (2026-09-08):** gifts formalize at the first Facet level of any Facet with no pick spent (`BRIEF_lineage.md` §3.4). **Magic works exactly as the core writes it: no tempo rule, no per-day limit, no slots; gifts and spellforms both cast freely.** Krenn and Tyndi are entered in data with `playable: false` (§3) on Brain's recommendation, pending objection. Every domain's example intents are **drafts for the owner's read** and are marked so in the data until approved.

**Canon this brief obeys** (`/root/wanvil/docs/systems.md` §Magic, §Mage Tribe Magic; `references/oraga_night/TUXXE_NAVAA_CANON.md`; owner, this session): the tribes are human; gifts are innate, inherited, and independent of traditional magic; spellforms are slow and collapse under stress; Orthaen crystals hold spellforms; gift rates as listed. Everything else below is module invention and is flagged.

---

## 1. What is being made

A setting Facet in two parts that always ship together:

1. **Data:** `software/facets/valloh/facet.yaml` — `id: valloh`, `priority: 1` (official expansion band), `requires: [base]`. Contents: ten `lineages`, ten `magic.soul_domains` entries (the gifts), one `items` collection (crystal charges). Nothing in `roll_resolution`, `spark`, `advancement`, `magic` rules, `combat`.
2. **Book:** a short setting Facet, `settings/valloh/` (new top-level directory; Planner may prefer `facets/valloh/` beside the data — one decision, made once), five files: `V0_Ten_Things.md` (the pitch), `V1_Lineages.md`, `V2_Magic_of_Valloh.md` (gifts, spellforms, crystals), `V3_Rekuzan_and_the_Tribes.md` (gazetteer, short, mostly compressed from Oraga Chapter II's public section), `V4_Adaptation.md` (running Val'loh with Shattered Origin characters; what the Facet changes, counted). Oraga Night's Chapter VIII is deleted and replaced by a pointer.

The Facet is built to the setting-book checklist in `style/analysis/setting_books.md` §8: pitch in three pages, tone tied to a mechanic, one recent wound (the mist-tides, 3164), counted novelty, player-usable material before geography, timeline as a table at the end.

## 2. The counted-novelty line (write it first; everything else must agree with it)

> *The core 2d6, Sparks, Conditions, exchanges, advancement, magic, and the three Facets are unchanged. Val'loh adds exactly: ten Lineages (two playable in Oraga Night), ten Gift domains, and crystal charges as one-use items. It removes nothing and it changes no rule.*

## 3. Lineages (data + `V1_Lineages.md`)

Ten entries in the II.5 format. Descriptions compress the module's Chapter VIII and the canon tribe notes; Heritages are new and need the owner's read.

| id | Name | Gift domain | Rate (fiction) | Heritage (draft) | playable |
|---|---|---|---|---|---|
| orthaen | Orthaen *(Orthain)* | crystal | four in five | Reads grown crystalwork: its age, its maker's hand, whether it holds a working | true |
| phern | Phern | warning | nearly all | Knows the caravan roads, who moves what, and the fair price of anything | true |
| thenya | Thenya | the_bond | fewer than one in a hundred | Border survival and the reading of intentions | false (MM-side in Oraga; playable elsewhere) |
| scora | Scora | the_weave | all known | The sanctioned cloth-strip rite; recognizes any Scora's record and its maker | false |
| akathi | Akathi | blade_bond | half | The forms and their counters; reads a fighter's school in three exchanges | false |
| dekhi | Dekhi | stone_flesh | nearly all | Winter-craft and the northern passes | false |
| kshalo | Kshalo | dream | one in twenty | The meaning of dreams; herb-lore of sleep and waking | false |
| fthala | Fthala *(Vethala)* | wildspeech | (not stated in canon; draft "most") | Paths that are not roads; beast-sign | false |
| krenn | Krenn | mindshare | all known | — (a "gone" tribe in 3164; entry exists so Vell can be statted; never shown to players) | false |
| tyndi | Tyndi | resonance_of_stone | most, in specialties | Gadget-lore; reads a device's control gem | false |

`playable` is a per-module flag the Oraga module overrides for its own pregens; the Facet's own text says which lineages a Val'loh campaign opens ("all but Krenn and Tyndi, by default").

**Ungifted members** are the II.5 rule: keep the Background's secondary skill, keep the Heritage. The Facet's text carries the line the module already has about how the ungifted are treated tracking the gift's rarity.

## 4. Magic of Val'loh (`V2_Magic_of_Valloh.md` + data)

### 4.1 Two origins, one system, no new rules

Val'loh has the same magic as the core rules, cast the same way, as often as the fiction allows. What differs is only where a domain comes from.

- **Gifts** are domains carried in the blood (II.5): intuitive tradition, Spirit + Attune, Focused, Minor scope until they formalize at the first Facet level.
- **Spellforms** are the scholarly tradition (Knowledge + Lore) practised by the trained, from the Mind list of domains, exactly as Chapter II.3 writes it. The setting's *fiction* says spellcraft is a patient art learned over years; the *rules* say nothing about it that II.3 does not already say. There is no tempo rule, no slot, no per-day count. **Owner ruling, 2026-09-08: "remove the spell complexity entirely; let magic users use magic freely, as is written."**
- A gifted member of a tribe may learn spellforms as anyone may: cross-Facet Tier 1, at the standard cost (II.3).

`V2` is therefore short: a page on gifts as domains, a paragraph on spellcraft as the scholarly tradition, and the crystal item. It must not restate II.3.

### 4.2 Crystals as consumables (data + `V2` + a one-line pointer in `IV.1`)

Canon: Orthaen crystals hold finished workings. In the game a **crystal charge** is a one-use item: one stored working at one scope, released at a touch by anyone, no roll. Growing one is an ordinary Crystal-domain working done in downtime under the normal II.3 rules; nothing extra is tracked. When the fiction makes a *release* chancy (fumbled in the dark, near an Uninvited), roll Luck at Standard as the module already does.

- Data: new top-level `items` collection (merged by id): `{id, name, kind: consumable, scope: minor|significant|major, effect: str}`. Character `inventory` already exists as `list[str]`; item ids are valid entries alongside free text. Engine: a `use_item` path that removes the entry and emits a narration event; WebSocket event `item_used`. No roll, no arithmetic.
- The module's existing suggested charges (*steady light, seal a door, veil of quiet, chime at a threshold, warmth, held image*) become the first six item entries, all Minor.
- This is the smallest loot system the game can have (audit R8). If even this reads as complexity at the table, the fallback is a sentence in `V2` and no data at all; the items can be free text in `inventory` today.

## 5. The ten Gift domains (data + `V2`, catalog format)

All ten are **Focused**, intuitive tradition, `requires_tier3: false`, `lineage_gift: true` (a new flag so the II.3 Tier 1 Technique's domain list can exclude them — a Soul mage in Shattered Origin cannot pick "Crystal"). INV-7 extends to the Facet: the Facet's catalog text and data must match.

Every example intent below is **new invention for the owner's read**. They are written to calibrate scope, not to be spells. Canon touched only where canon exists (crystal architecture, wards, caravans, the mists, the cloth-strip rite, weapon culture).

**Crystal** *(Orthaen)* — Growing, shaping, charging, and reading soul-crystal; holding a working in a lattice. *Beyond:* light that is not crystal-light; stone that was never grown; any working the crystal merely *holds* (that is the spellform's domain, not this one).
- *Minor:* wake a wall's stored warmth on a cold night; read whether a charge is live without touching it; grow a splinter of crystal to mark a door you must find again in the dark.
- *Significant:* seal a corridor with a lattice grown across it in the time it takes to say so; steer a palace ward to light one stairwell and not another; draw the light out of a room's crystal so the room goes dark.
- *Major:* raise a ward that holds a hall for a scene against anything that is not deep crystal itself; grow, over a night, a charge at Major scope; read a generations-old lattice back to its maker's intent.

**Warning** *(Phern)* — Sensing hidden danger, its direction, and the intent behind it, before it lands. *Beyond:* seeing the unseen (this is a prickle, not sight); reading a specific mind; danger that has not yet been decided on by anyone.
- *Minor:* know which door in a hall you should not open; feel the moment a conversation turns hostile; wake before the thief reaches the tent.
- *Significant:* walk a crowded room and point to the three people who mean harm tonight; feel an ambush's shape well enough to name where it waits; sense that the danger in the palace is *upstairs*, and that it is not human.
- *Major:* hold the whole caravan's watch alone for a night, waking each sleeper the instant they are needed; feel a threat coming from a day away and the road it takes; know, for one held breath, exactly where every knife in a burning hall is.

**The Bond** *(Thenya)* — Protective intervention for someone the caster loves, fired by feeling rather than technique. *Beyond:* anyone the caster does not love; harm to the caster themselves; anything premeditated (the Bond answers a moment, never a plan).
- *Minor:* a loved one's stumble becomes a step; the cup they were about to drink from cracks; you know, across a city, that they are afraid.
- *Significant:* the blade that would have opened them turns on the rib; the fall that would have broken them lands them winded; you are, for one exchange, standing where you were not.
- *Major:* the wall between you and them is not there; the blow already narrated does not land, and the one who swung it does not understand why; the thread that was cut holds.
- *Rules note for the entry:* the Bond may be invoked as a **reaction on a loved one's behalf** (Intercept's fiction without Intercept's Endurance cost, at the Bond's difficulty); this is the one gift the module lets fire without a declared intent, and the entry says so.

**Blade-bond** *(Akathi)* — One bonded weapon: finding it, calling it, striking with it as a part of the self. *Beyond:* any other weapon; armor; anyone else wielding the bonded blade.
- *Minor:* the blade is in your hand before you reached for it; know where it lies from a room away; it does not rust, dull, or lose its edge between fights.
- *Significant:* call the blade back across a hall; the bonded weapon's Strike leaves the enemy Open on a 7–9 as well as a 10+; parry a blow no one saw coming, because the blade did.
- *Major:* the blade goes through what should have stopped it — a ward, a crystal barrier, a door; a Strike with the bonded blade at Major scope resolves as a Final Blow would, once per session; the blade finds its wielder across any distance in the world.

**Stone-flesh** *(Dekhi)* — Enduring: cold, poison, hunger, exhaustion, and blows that would drop another. *Beyond:* healing others; strength as such (this is lasting, not lifting); anything that requires speed.
- *Minor:* walk a winter night in shirtsleeves; shrug off a dose that would sicken a soldier; go a second day without sleep and show nothing.
- *Significant:* hold a collapsing doorway with your back for the exchange it takes everyone to get through; take a Tier 2 Condition as Tier 1 once this scene without armor; keep walking through a blizzard that has stopped the column.
- *Major:* stand in the fire long enough to carry four people out of it; refuse to be Broken once this session (as *Unbreakable*, II.4a, and the entry says the two do not stack); outlast a poison meant to kill a village.

**Dream** *(Kshalo)* — Entering and shaping the dreams of the sleeping. *Beyond:* the waking mind; anyone the caster has not met or does not hold something truly theirs; anything that leaves a physical mark.
- *Minor:* learn what a sleeper is afraid of tonight; leave a face in a stranger's dream that they will recognize tomorrow; sleep, and wake knowing whether someone you have met is alive.
- *Significant:* walk a named person's dream and ask it three questions, answered in dream-logic; plant a warning that survives waking; turn a nightmare aside.
- *Major:* hold a dream open for a whole night and bring another sleeper into it; leave a compulsion that acts on waking, once, in a way the dreamer can explain to themselves; walk the dream of someone the caster has never met, holding only their name and a thing they loved.

**Wildspeech** *(Fthala)* — Speaking with, bonding with, and moving among animals and wild places. *Beyond:* commanding a beast against its nature; plants (that is Verdance); anything inside a city's walls that is not an animal.
- *Minor:* ask a mews of falcons what frightened them; move through undergrowth without a sound; a small companion beast carries a message it understands.
- *Significant:* the dogs of a whole estate decide the intruders are not you; a bear steps aside; every bird in the garden goes up at once when you say so.
- *Major:* the forest closes a road behind you for a day; every animal within a mile turns toward the thing that walked through it; a bonded beast dies for you, and you know it before it does.

**The Weave** *(Scora)* — Perfect recall of anything witnessed or recorded; pattern across memory; one true question of the past. *Beyond:* things never witnessed by anyone; the future; changing what was recorded.
- *Minor:* recite a conversation heard once, verbatim; recognize a mask, a stitch, a coin from a description; know which of two accounts contradicts the other.
- *Significant:* lay out every rumor heard tonight and see which three are the same rumor; read a room's history from the wear on its floor; on a 10+, ask the MM one true question about a past event and be answered.
- *Major:* hold an entire night in memory so exactly that it can be sworn as testimony and *believed*; find the one thread that connects two houses across four centuries; reconstruct a destroyed record from every mind that ever read it.

**Mindshare** *(Krenn; MM-side)* — Telepathy among kin; reading and, at scope, steering other minds. *Beyond:* the dead; anyone shielded by deep crystal; changing what someone *is* rather than what they do next.
- *Minor:* know a stranger's surface intent; go unremembered by one guard; speak to kin across a room without a word.
- *Significant:* be unmemorable to a hall; read the fear in every mind in a room; nudge a weak will toward the door.
- *Major:* edit two hundred minds' attention for a night; hold a mind still; take a decision away from someone and leave them certain it was theirs.
- *Rules note:* only ever an NPC domain in 3164; used to stat Master Vell honestly (a *Very Hard* Spirit roll to notice the nudge, as the module already rules).

**Resonance of Stone** *(Tyndi; MM-side)* — Metals and stones that carry and release magical power; gadgets and their control gems. *Beyond:* crystal grown by the Orthaen gift; living things; anything without a stone or metal in it.
- *Minor:* wake a device from its control gem; feel a vein of ore through a wall; make a knife hum.
- *Significant:* run a machine no one has run in a generation; ground a spellform's power into a nexus stone; make a tool do a thing it was not built for.
- *Major:* light a fort's weave-furnace; awaken every device in a hall at once; smelt a gem that lets the ungifted command what only the gifted could.

Planner: enter all ten in `magic.soul_domains` of the Val'loh file with `lineage_gift: true`; the merge appends them to the base list; the appendix-vs-data invariant (INV-7) is extended to check `V2` against the merged catalog with the Facet loaded.

## 6. The pitch (`V0_Ten_Things.md`; draft shape, not text)

Fragment-triplet opener from the module's own three images (pink crystal walls; masks for the dead; a sea holding its breath). Tone formula: *glamour over a blade*, tied to Sparks (the register that pays the peaceful route). One-page summary compressed from Oraga Chapter II's public section. **Ten Things You Need to Know**, drafted:

1. The tribes are human, and four in five Orthaen are born able to grow crystal.
2. A gift is a domain. It is fast, it is yours, and it is Minor until you have grown into it.
3. Spellcraft is the scholarly tradition, learned over years and cast like any other domain.
4. Crystal is wealth because a charged crystal is magic anyone can carry and spend.
5. There are no books. The Church writes; everyone else remembers, and the Scora remember for everyone.
6. Rekuzan is nine walled districts that grew together; the walls glow at dusk.
7. Everyone carries a knife to a ball. Drawing it is the crime.
8. The mists in the east have fallen to record lows this year, and the people whose job it is to watch them are frightened.
9. The strong are chosen by Fraden, the Church says, so the tribes' wars are holy, and nothing else unites them.
10. This Facet changes nothing about how you roll or how you cast. It adds ten Lineages, ten domains, and crystals you can spend.

**First page states the world:** Val'loh is a continent of the same world as Shattered Origin (owner ruling: one world). `V4` is therefore *adaptation within one world*, not conversion between two. The written-word ban (Ten Things #5) is confirmed canon with its two carve-outs: a chief's formal invitation, and private slate scratch-work.

Reading order: players, `V1` then `V2`; MMs, `V3` then Oraga Night; anyone bringing a core-book character into Val'loh, `V4`.

## 7. Tests and invariants

- Merge with `valloh` loaded: ten lineages, ten more domains, items present, base unchanged; without it, base is byte-identical to today's merge (regression guard).
- `lineage_gift` domains do not appear in Tier 1 Technique choice lists for Soul/Mind characters; do appear for a lineage-gifted character's formalization.
- Crystal item use: removes one charge, emits the event, rejects a second use.
- INV-7 extended; INV-16 (lineage gift resolves) passes for all ten.
- Docs: the counted-novelty line in `V0` is machine-checked against the data (count lineages, count `lineage_gift` domains) so the pitch can never drift from the file.

## 8. Order of work

1. Data file with lineages and domains, flagged `draft: true` on every intent until the owner has read them; tests.
2. `items` schema + engine `use_item` + event; tests.
3. `V0`–`V4` text; delete Oraga Chapter VIII, leave a one-line pointer in the module's README and Overture.
4. Invariant extensions.

## 9. Watch-outs

- **Do not import the 5e-era tribe stats** (`/root/wanvil/intermediate/starting_info.md`). They are a different era and a different system; use them only to check that a gift's *flavor* matches what the owner once wanted at a table (e.g., Thenya as a reactive save on a loved one, Scora's second try on a failed knowledge check — which is now *Dissecting Failure*'s territory and should stay a Technique, not a gift).
- **The Bond's reaction clause** is the one place a gift touches combat rules; Planner should sim it once (a free Intercept at the Bond's difficulty on a loved one) before it prints, and if it reads as a new rule rather than a domain intent, cut the clause and let the Bond be an ordinary reaction-shaped intent.
- **Krenn are "gone"** in 3164 by the module's own framing; the lineage entry is data for Vell and nothing else, and `V1` does not list it among the tribes a player meets.
- **Spelling** follows the player-doc rulings: Orthaen, Fthala (Vethala noted), Oraga, the Blackwatch.
