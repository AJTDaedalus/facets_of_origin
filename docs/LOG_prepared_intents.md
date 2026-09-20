# LOG — Prepared Intents (D23) and Player-Chosen Gifts (D24)

**Owner direction, 2026-09-18:** "The tribes/new domains are way too complex… Tribal magic
should be able to just be a variation of the domains we had." Then: "yes, implement this.
No need to map tribes to domains, let players choose." And on magic: "If players can use
magic indiscriminately they can use it to fix anything. Let's find a way to limit its use
without the complexity of preparing spells" — with the owner's own idea of preparing
*intents* rather than spells.

Decisions: **D23** (readied intents; supersedes D17) and **D24** (gifts are the player's
choice of an existing domain; supersedes D19's custom-domain row).

---

## Part A — gifts as the player's choice (D24)

- **Removed:** the ten custom Val'loh domains, their thirty example intents, the V2
  catalog, the `lineage_gift` and `draft` domain flags, the Tier-1 filtering that kept
  gift domains off Technique lists, and the three catalog invariants.
- **Schema:** `LineageDefinition.gift` — one line of how the gift *shows itself*;
  present = gifted. `gift_domains` survives as an optional restriction (empty = any).
  A restriction with no gift is rejected at load.
- **Creation:** a gifted character picks any non-Prismatic Soul or Mind domain; an
  unknown domain or a Prismatic one is refused with the reason.
- **One rule:** a gift is cast **intuitively** (Spirit + Attune) whatever the domain's
  own tradition. Enforced at creation (`magic_tradition`) and at the roll
  (`resolve_magic_roll`), and it survives a `.fof` round-trip — tested in all three
  places, including that the *same* Mind domain learned through a Background still
  rolls Knowledge + Lore.
- **Book:** V0's counted-novelty line is now *ten Lineages and crystal charges; adds no
  domains*; V1's Gift fields are flavour + "a domain of your choice"; V2's gifts section
  rewritten and its catalog removed; II.5's Gift field and custom-lineage step 2 say *do
  not write a new domain*.
- **Pregens:** Serane → Transmutation, Andra → Inscription, Ilesse → Warding, Pello →
  Divination. My choices, fitted to each pregen's existing concept; in the review table.

## Part B — readied intents (D23)

- **Data:** `magic.prepared_intents` — five purposes (Harm, Ward, Mend, Shape, Reveal),
  capacity 3, Minor free, off-purpose costs 1 Spark. Absent = unlimited, so a setting
  may restore the pre-D23 game.
- **Character:** `readied_intents` (None = may ready; a dict locks the choice),
  `ready_intents`, `refresh_intents`, `intent_cost`, `pay_intent_cost`.
  `start_new_session` refreshes. Round-trips through `.fof`. 20 tests.
- **WebSocket:** `ready_intents` (player), `full_rest` (MM only), and `cast` now
  carries `purpose` and reports `intent_cost` and `readied_intents`. The working is
  priced **before** the roll and paid **after** the engine accepts it — a refused
  working never costs an intent or a Spark, the same order Sparks already follow. An
  off-purpose working plus a dice-Spark needs two Sparks. 12 tests.
- **App:** a readied-intents panel (one input per purpose, pips once readied), a
  purpose selector that appears only when the scope needs one and shows the price
  before casting, and the MM's **Full Rest** button. 6 e2e tests.
- **Books, same commit:** II.3 (purposes table, *Readied Intents* section with a
  Through the Mirror box, Spark rules, *Before the Technique*), both formalizing
  Techniques (Arcane Study, Spiritual Domain), II.5, II.6, Quick Start, MM2 (*Calling a
  Full Rest*, as body text) and MM5 (its compression), Glossary (Purpose, Readied
  Intent), the in-app rules card, and Val'loh's V2 — which also says how crystal
  charges interact: growing a big one spends an intent, releasing one spends nothing,
  which is exactly why a charge is worth a season's wages.

## Things I got wrong on the way

- **Zahna's pronoun.** Zahna is *he* in the character file and every existing vignette.
  I wrote *she* in the new II.3 example and — found while checking — in the III.3
  Guardian vignette's closing note from the Second Act work. Both fixed.
- **Zahna's state.** The first draft of the II.3 example had him spending readied
  intents, but he is canonically Facet level 0 and pre-formalization. Recast as what a
  session looks like *once* his Inscription formalizes.
- **A clobbered run.** One full-suite run overlapped my Part B schema edits and reported
  39 failures; a clean rerun showed one (a stale Index). Recorded so the 39 is not
  mistaken for a real regression.

## Not simulated, and why

The combat simulator models no casters, and readied intents change how *many* large
workings happen per session rather than how any one of them rolls. The Series 11
casting curves are untouched. **Capacity 3 is a design number to be tested at a human
table.** A simulation of it would be a simulation of nothing.

## Robustness note, not acted on

`build_ruleset` loads *every* Facet file to discover ids, even ones a session did not
ask for — so one malformed setting Facet takes down base-only sessions too. Seen during
Part A, when the old Val'loh file briefly failed the new schema and the core ruleset
would not build. Worth making discovery tolerant of a broken optional Facet before
anyone else writes one.
