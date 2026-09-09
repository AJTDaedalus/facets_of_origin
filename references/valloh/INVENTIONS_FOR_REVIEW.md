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

## 2. The domain names

Canon describes what each tribe's gift *does*; the names are mine. **Crystal**,
**Warning**, **The Bond**, **Blade-bond**, **Stone-flesh**, **Dream**,
**Wildspeech**, **The Weave**, **Mindshare**, **Resonance of Stone**. Rename freely
— each appears in `facet.yaml`, `V1`, and the appendix format, and nowhere else.

## 2b. The thirty example intents — now in the book

They were drafted in `BRIEF_valloh_facet.md` §5 and, until now, never carried into
`settings/valloh/V2`, which claimed a catalog it did not contain. Written in, in the
core appendix's format: territory, beyond-the-focus, three intents at each scope.

**Three gifts arrived carrying rules, and all of them are cut.** Blade-bond let its
Strike leave an enemy Open on a 7–9 as well as a 10+, and resolve as a Final Blow
once per session at Major scope. Stone-flesh let its holder take a Tier 2 Condition
as Tier 1 once per scene, and refuse to be Broken once per session.

Cut for the reason the Thenya Bond's reaction clause was cut: we have measured what
happens when a gift carries a mechanic, and it put the Hard encounter row at 75%
against a 40–60% band. A gift granting an extra Condition tier or a second Final Blow
is a Technique that skipped the Technique economy, handed out at creation to a
character who paid nothing for it.

Those intents are replaced with fiction of the same weight — *the blade goes through
what should have stopped it*; *be the last thing between a thing and a door, for as
long as that has to be true* — and a Through the Mirror box says why. **If you want
any of the three as real mechanics, say so and they become Techniques in a Facet
tree, simulated before they print.** A new invariant now refuses a gift entry that
carries one.

## 3. The *beyond this domain's focus* lines

Every domain in the core catalog prints what it cannot do; these ten needed the
same, and every one is invention. They are the load-bearing half of a Focused
domain — they are what stops "Crystal" from meaning "anything made of matter" at a
table three sessions in — so they are worth your read even if the names stand.

The ones that make a real ruling rather than an obvious one:

| Domain | The line that decides something | Why |
|---|---|---|
| Crystal | *"any working the crystal merely holds — that is the spellform's domain, not this one"* | Draws the line between the Orthaen gift and traditional spellcraft, which canon says the crystal *stores*. Without it, Crystal absorbs the whole magic system. |
| The Bond | *"anything premeditated — the Bond answers a moment, never a plan"* | Canon says the Thenya gift fires when a bonded loved one faces death. This makes that a limit rather than flavour. |
| Warning | *"this is a prickle, not sight"* | Keeps Warning from becoming clairvoyance. |
| Wildspeech | *"plants — that is Verdance's"* | Deconflicts with the core catalog. |
| Mindshare | *"changing what someone is, rather than what they do next"* | The line that keeps Vell's nudge a nudge. |

## 4. Fthala gift rate — **"most"** *(⚠ not in canon)*

`systems.md` gives a rate for every tribe except the Fthala. "Most" is a guess
chosen to sit between the Phern's "nearly all" and the Akathi's "half". Flagged in
the data with an inline comment. One word to change.

## 5. The Bond's reaction clause — **drafted, simulated, CUT**

The brief proposed that a Thenya could invoke the Bond as a *reaction* on a loved
one's behalf — Intercept without the Endurance cost. It was simulated before it
printed (`docs/LOG_valloh_facet.md` V9) and cut: it took the Hard encounter row from
41% to **75%** party wins, making one lineage's gift worth more than a category of
encounter difficulty.

**Nothing is lost in the fiction.** A Thenya can still throw themselves between a
loved one and a blade — that is an ordinary Bond working at Significant scope, and
it is rolled. What was cut is the free, unrolled, always-on version. Raise it again
if you want it; the numbers are recorded.

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
