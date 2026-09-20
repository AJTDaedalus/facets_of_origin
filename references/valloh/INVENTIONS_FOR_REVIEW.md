# The Val'loh Facet — New Inventions Requiring Your Review

Everything below is **new invention** written for `settings/valloh/` and
`software/facets/valloh/facet.yaml` — not found in the wanvil corpus, the player
doc, or `references/oraga_night/TUXXE_NAVAA_CANON.md`. Per the project's iron law
nothing here is settled until you approve, amend, or strike it.

**Every domain entry in the data carries `draft: true`** for exactly this reason.
The flag does not gate loading — the Facet can be tested and simulated before it is
approved — it just says out loud, in the file, which parts are waiting on you.

**Canon this Facet stands on and did not invent:** the ten tribes and their gift
territories (`/root/wanvil/docs/systems.md` §Mage Tribe Magic); the gift *rates* as
listed there; the tribes being human (your ruling, 2026-09-08); Orthaen crystal
holding spellforms; the written-word ban and its two carve-outs (S4); Rekuzan's nine
districts, eight sects, and pink crystal walls; the mist-tides of 3164; weapons
culture; Val'loh as one continent of Shattered Origin's world (S2).

---

## 1. The Heritages — all ten are new

A Heritage is the II.5 field for what every member of a lineage grows up knowing,
gifted or not. Canon gives gift territories but says nothing about this, so all ten
are written from the tribe's described life. They are the cheapest thing here to
change: each is one sentence in `V1_Lineages.md` and one field in the data.

| Lineage | Heritage (draft) |
|---|---|
| Orthaen | Reads grown crystalwork — its age, whose hand shaped it, whether it is holding a working now |
| Phern | The caravan roads, who moves what along them, and the fair price of anything |
| Thenya | Border survival, and reading intentions in people trying to hide them |
| Scora | The sanctioned cloth-strip rite; recognizes any Scora's record and can name who tied it |
| Akathi | The forms and their counters; reads a fighter's school in three exchanges |
| Dekhi | Winter-craft and the northern passes |
| Kshalo | The meaning of dreams; herb-lore of sleep and waking |
| Fthala | Paths that are not roads; beast-sign |
| Krenn | *(none — the entry exists only to stat Vell)* |
| Tyndi | Gadget-lore; reads a device's control gem |

## 2. Retired: the ten custom domains *(owner ruling, 2026-09-18 — D24)*

The domain names, beyond-the-focus lines, thirty example intents, and the three
gift mechanics (Blade-bond, Stone-flesh, the Bond's reaction clause) that used to be
reviewed here are **gone**. Your ruling: tribal magic is a variation of the domains the
game already has, and the player chooses which. A gifted lineage now carries one line
saying how its gift *shows itself*; the domain is the player's pick from the core
catalog (any non-Prismatic Soul or Mind domain), always cast intuitively.

What is left to review from that layer is just the ten **gift lines** in
`software/facets/valloh/facet.yaml` and `V1`. They paraphrase canon — *"shows itself
through grown soul-crystal"* for the Orthaen, *"as warning: a prickle before danger"*
for the Phern — and add nothing canon does not say, except that each is worded as
appearance rather than capability, so it never restricts a player's domain choice.

## 3. The Oraga pregens' gift domains *(my choice — please check)*

The four gifted pregens needed a domain once the custom ones were gone. Chosen to fit
each pregen's existing concept; change any of them and the printed block regenerates.

| Pregen | Lineage | Domain chosen | Why |
|---|---|---|---|
| Serane | Orthaen | **Transmutation** | the Orthaen gift as crystal grown and shaped |
| Andra | Orthaen | **Inscription** | "her charges are her notebook" — recording into lattice |
| Ilesse | Orthaen | **Warding** | the palaces' stored defensive crystalwork |
| Pello | Phern | **Divination** | the Phern gift in canon is danger sense |

All four are cast intuitively (Spirit + Attune), including the three that are Mind
domains.

## 6. The six crystal charges

*Steady light, seal a door, veil of quiet, chime at a threshold, warmth, held
image.* These were the module's own suggested charges; what is new is the one-line
effect text for each and the decision that all six are Minor scope. Adding a
Significant charge is a data change.

## 7. Prose inventions in the book text

- **`V0`'s tone formula** — *"glamour over a blade"*, tied to Sparks. This is a
  claim about what the setting is *for* at a table, and it drives how the module
  pays out. Worth a look even though it is not a rule.
- **`V1`'s ungifted-treatment note** — that how the ungifted are treated tracks how
  rare the gift is, with the Orthaen fifth as "a private disappointment nobody
  mentions twice" and the Kshalo nineteen as running the herb-lore. Extrapolation
  from the rates, not canon.
- **`V1`'s MM note on gifted Thenya** — needing MM agreement because the gift points
  at another character. A table-practice suggestion, not a rule.
- **`V3`'s "Where the Tribes Are" table** — canon places the Orthaen in the central
  farmlands and the Blackwatch in the east. Every other row is a plausible guess
  and is the single most disposable thing in this Facet.
- **`V3`'s timeline** — assembled from canon events; the *ordering* between the
  written-word law, Rekuzan's founding and the Krenn's disappearance is inferred.
- **`V2`'s MM Note on crystal suppression** — generalises the module's
  "crystals gutter near the Uninvited" (already invention #4 in the module's own
  review file) into an MM tool. Says nothing new about *why* it happens.

## 8. What this Facet deliberately does NOT do

Recorded so you can check the boundary rather than take it on trust:

- **No tempo rule for spellcraft.** Your ruling (D17). The fiction says spellforms
  are patient work; the rules say nothing about it that II.3 does not.
- **No stat bonuses.** No lineage grants an attribute, a skill rank, or Endurance.
- **No 5e-era tribe material** from `/root/wanvil/intermediate/starting_info.md`.
  It is a different era and a different system. Consulted only to check that a
  gift's flavour matched what you once wanted at a table; the Scora's old
  "second try on a failed knowledge check" stayed out, because that is
  *Dissecting Failure*'s territory and belongs to a Technique.
- **No rule changes at all.** Checked by test (INV-17 and siblings): the Facet may
  not write into `roll_resolution`, `spark`, `advancement`, `combat`, or the magic
  rules, and loading it leaves every core skill, Background, domain and rule
  exactly as it was.
