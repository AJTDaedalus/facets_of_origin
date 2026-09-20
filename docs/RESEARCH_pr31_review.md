# Adversarial review — PR #31 (`feat/full-form-magic`)

**Reviewed:** 2026-09-20. Base is `feat/lineage-valloh-second-act` (PR #30), not `main`.
**Claim under test:** a magical Strike costs a readied intent in books *and* engine;
plus a docs-only D26.

**Method.** Read `gh pr diff 31` in full; read `_handle_strike`, `_handle_cast`,
`_handle_support`, `_handle_maneuver`, `_handle_contested_roll`, `_handle_react`,
`_handle_enemy_strike`, `_handle_enemy_update`, `_handle_saving_throw`,
`_handle_use_item`, `_dispatch` in `software/app/api/websocket.py`;
`resolve_magic_roll` and the Spark helpers in `app/game/engine.py`;
`intent_cost`/`pay_intent_cost` in `app/game/character.py`; the changed book
sections and their neighbours; `play.js` + `index.html`; both new test classes.
Every BLOCKER below was **reproduced against the running server** with throwaway
probe scripts (TestClient + the real `/ws` route, `tests.conftest` fixtures) —
transcripts quoted inline. Suite state at review time: `tests/` (non-e2e)
**1742 passed**; `tests/test_docs_consistency.py` **55 passed**. e2e not run.

---

## BLOCKERS

### B1 — `spark_use: "improve_roll"` buys a free extra die on a magical Strike

`software/app/api/websocket.py:970-993` hands the client's `spark_use` straight
to `resolve_magic_roll`, which sets `sparks_spent = 1` internally
(`app/game/engine.py:448-449`) to model the dice bonus. The handler only ever
deducts `sparks_requested` — the `sparks_spent` *field* — at line 923. Nothing
deducts a Spark for `spark_use`. `_handle_cast:1496-1497` does
(`if spark_declared: _spend_sparks(character, 1, session)`); the Strike path
copied the roll call and not the payment.

Reproduced (formalized Zahna, 3 Sparks, `{"harm": 2}` readied):

```
send  {"type":"strike","target":"g","magical":true,"scope":"significant",
       "purpose":"harm","spark_use":"improve_roll"}
recv  strike_result  dice: [4, 4, 4]   roll.sparks_spent: 1
      char.sparks before/after: 3 → 3
```

Three dice, one Spark's worth of benefit, zero Sparks paid — repeatable every
exchange.

**Fix** — in the `if magical:` block at `websocket.py:873`, mirror `cast`:

```python
        spark_declared = msg.get("spark_use") in VALID_SPARK_USES
        if spark_declared and character.sparks <= 0:
            await manager.send_to(websocket, {
                "type": "error", "message": "No Sparks remaining."})
            return
```

and extend the affordability test at line 903 to
`off_purpose_sparks + sparks_requested + (1 if spark_declared else 0)`, then at
line 1011 (after the roll is accepted) add `if spark_declared: _spend_sparks(character, 1, session)`
**before** `pay_intent_cost`.

---

### B2 — A pre-Technique caster gets an unlimited, completely free magical Strike

`Character.intent_cost` returns `"free"` for any scope when
`magic_technique_active` is false (`app/game/character.py:711-712`) — correct
under D23, where a pre-Technique caster is Minor-only and so never reaches the
priced scopes. D25 did not revisit that. Combined with B1's unpaid `spark_use`,
`pre_technique_push` (`engine.py:415-423`) lifts the Minor ceiling for free:

```
Zahna: magic_technique_active = False, sparks = 0, readied_intents = None
send  {"type":"strike","target":"g","magical":true,"scope":"significant",
       "purpose":"harm","spark_use":"pre_technique_push"}
recv  strike_result   intent_cost: "free"   sparks: 0   readied: None
```

A caster who has never formalized, holding zero Sparks, Strikes at Significant
scope for nothing, every exchange, forever. That is precisely the state D25's
*Why* paragraph says it exists to end ("a formalized caster could attack every
exchange, forever, for nothing"), now reachable by the *un*formalized caster.

This also has no book text. `II.3:136` ("Before your magic formalizes, you have
no readied intents and need none: you work at Minor scope") plus III.3:449 ("a
magical Strike is always a full form … **Significant**") together mean a
pre-Technique caster cannot magically Strike at all except by the II.3
reach-Spark — and neither chapter says so. Note the four Oraga Night pregens
(`adventures/oraga_night/03_Masks_and_Agendas.md:218,241,264,311`) are all
pre-Technique Gift casters, so this is the starter module's default state.

**Fix** — two parts.
(a) Gate the handler on formalization, at `websocket.py:874`, next to the
existing domain check:

```python
        if not character.magic_technique_active:
            await manager.send_to(websocket, {
                "type": "error",
                "message": (
                    "Before the Technique formalizes your domain you work at "
                    "Minor scope, and a Minor working is not a Strike (II.3, "
                    "III.3). Reshape the fight with a Maneuver or a Support — "
                    "or spend a Spark to reach Significant (II.3, Reaching "
                    "Significant Early)."
                ),
            })
            return
```

and permit the `pre_technique_push` case explicitly once B1 charges its Spark.
(b) Add one sentence to `player_handbook/III.3_Combat.md:449`, after "There is
no free magical attack.":

> Before your domain formalizes you have no intents to spend, so you have no
> magical Strike: your magic fights as a Maneuver or a Support until the
> Technique, or for one exchange on a Spark (II.3, *Reaching Significant Early*).

---

### B3 — A refused magical Strike spends Endurance, Sparks, and the exchange

The PR's own comment at `websocket.py:867-868` — "Everything here happens
before a single Endurance point or Spark is spent, so a refused declaration
costs nothing" — and at `1009-1010` — "same order as `cast`, so a refused
Strike never costs an intent or a Spark" — are both false. The new block ends
at line 912. Press deducts Endurance at **914-921**, `_spend_sparks` runs at
**923**, `offensive_actions_this_exchange.add` at **926**, the attribute
validation can `return` an error at **933-935**, and `resolve_magic_roll` can
raise at **977-990**. Four refusal paths sit downstream of the payments.

Reproduced (pre-Technique Zahna, 2 Sparks, Press declared, `sparks_spent: 2`):

```
send  {"type":"strike",...,"magical":true,"scope":"significant",
       "purpose":"harm","press":true,"sparks_spent":2}
recv  error  "Before unlocking the Technique, magic is limited to minor scope only…"
      endurance 4 → 3 | sparks 2 → 0 | offensive_actions_this_exchange: {'Zahna'}
```

An Endurance point, two Sparks, and the exchange's contested flag, all consumed
by an action the engine refused. The flag matters on its own: III.3's exchange
flow gives the MM a free advance when *no* PC took an offensive action, and a
rejected declaration now silently cancels that.

**Fix** — move the whole payment group below the roll. Concretely: relocate the
Press deduction (914-921), `_spend_sparks` (923) and
`offensive_actions_this_exchange.add` (926) to immediately after
`result_dict = roll_result_to_dict(result)` at line 994; keep only an
*affordability check* up top (`character.endurance_current >= press_cost`), and
hoist the attribute validation (929-935) above it. The Final Blow block already
follows exactly this discipline and documents why (828-836) — this path should
too, and `cast` is the wrong model to cite since `cast` has no Press and no
exchange bookkeeping.

---

### B4 — Sparks spent on a magical Strike buy nothing

Line 923 deducts `sparks_requested`, then lines 959-969 build a `RollRequest`
carrying `sparks_spent=sparks_to_spend` — and lines 977-987 **throw that
request away** for the magical branch. `resolve_magic_roll` builds its own
request and never sees the number.

```
send  {"type":"strike",...,"magical":true,"scope":"significant",
       "purpose":"harm","sparks_spent":2}
recv  strike_result   dice: [4, 4]      # two dice, not four
      char.sparks: 3 → 1
```

Two Sparks destroyed for no dice. The affordability test at line 903 explicitly
budgets `off_purpose_sparks + sparks_requested`, so the author intended these
Sparks to work.

**Fix** — pass them through. In the `resolve_magic_roll(...)` call at 978-987 add
`sparks_spent=sparks_to_spend`, and give `resolve_magic_roll` the parameter
(`engine.py:333-342`), folding it into the local at 439:
`sparks_spent = max(0, sparks_spent_arg) + (1 if spark_use == "improve_roll" else 0)`.
If that is judged out of scope, the handler must instead refuse
`sparks_spent > 0` on a magical Strike rather than silently eating them.

---

### B5 — The rule is bypassed by omitting the flag on the exact roll the book names

`magical` is a self-declared client field with nothing correlating it to the
roll. III.3:471 (changed by this PR) names the pairing in print:

> **Attune (Spirit):** Channel your domain's force as a direct Strike — a full
> form, spending a readied intent … **Spirit + Attune is the roll for intuitive
> magical attacks; scholarly casters Strike with Knowledge + Lore.**

The handler charges nothing for exactly that roll when the flag is absent:

```
send  {"type":"strike","target":"g","attribute_id":"spirit","skill_id":"attune"}
recv  strike_result   magical: false   intent_cost: null
      char.readied_intents: {'harm': 2}   # untouched
```

Full Resolve depletion, the book's own named magical-attack roll, zero cost.
The client offers it too — the Strike attribute/skill pickers are unrestricted
by INV-8, so Spirit + Attune is two clicks away with the new checkbox left
unticked. This is not "the engine cannot police narration": the engine *can*
see that the tradition skill was rolled, and it is the only signal the book
gives.

**Fix** — after the attribute validation, refuse an undeclared tradition roll:

```python
    tradition_skills = {t.skill for t in
                        (getattr(session.ruleset.magic, "traditions", None) or {}).values()}
    if not magical and skill_id in tradition_skills:
        await manager.send_to(websocket, {
            "type": "error",
            "message": (
                f"A Strike rolled on {skill_id} is a magical Strike (III.3, "
                "Mind and Soul in a Fight). Declare it as a full form — it "
                "spends a readied intent."
            ),
        })
        return
```

This is a rule, so it belongs in `app/game/combat.py` with the handler
delegating, per the "rules live in one place" policy.

---

### B6 — II.3 contradicts itself four lines apart, and contradicts MM5

The PR inserts the new determinant of scope at `player_handbook/II.3_Magic.md:75`:

> The moment a working needs real force … **or real precision — the exact lock,
> the exact word, the one thread in the weave — it has stopped being Minor.**

and `:77`:

> A flame placed inside a lock, at the one point where the mechanism will fail,
> is a precise ask — that is a full form, and you pay for it.

Six lines above it, untouched, Table II.3–2's Minor row (`:69`):

> A candle lit from across the room. **A lock made too hot to touch.** A sound
> masked for a moment.

And fourteen lines below it, also untouched, the example box (`:91`):

> Scope is determined by **scale of change and duration**, not by how impressive
> the result looks.

"Scale of change and duration" is the operative definition and it now excludes
the determinant the PR just added. MM5 repeats it as a ruling aid (`:288`):

> **Scope = scale of change + duration.** Nothing else. Not how impressive it
> looks, not how well it was described, not target count…

"Nothing else" is now false, and MM5 is a quick ref — it may only compress body
text, so it either has to change with the body or it is stating a rule the body
denies. An MM reading :288 mid-fight prices a precise working Minor; an MM
reading :75 prices it Significant. Also note D25's own rationale wants the
"too-hot lock" to stay Minor ("declined for taking … the too-hot lock with it"),
which the :77 lock example reads directly against.

**Fix** — three edits in the same commit.
1. `II.3_Magic.md:91` — replace "Scope is determined by **scale of change and
   duration**, not by how impressive the result looks." with "Scope is
   determined by **scale of change, duration, and precision** — not by how
   impressive the result looks."
2. `MM5_Quick_Reference.md:288` — replace "**Scope = scale of change +
   duration.** Nothing else. Not how impressive it looks, not how well it was
   described, not target count" with "**Scope = scale of change + duration +
   precision.** Not how impressive it looks, not how well it was described, not
   target count".
3. `II.3_Magic.md:77` — change the lock example so it does not collide with the
   Minor row: "A flame set at the one point in a mechanism where it will fail is
   a precise ask — that is a full form, and you pay for it. Making the whole
   lock too hot to touch is not; that stays Minor."

---

### B7 — A magical Strike marks any skill the client names as used this session

`websocket.py:1016-1018` marks the *rolled* skill (right), and then
`1020-1022` marks `skill_id` from the message — which for a magical Strike was
never rolled and defaults to `"combat"`.

```
send  {"type":"strike",...,"magical":true,"scope":"significant",
       "purpose":"harm","skill_id":"stealth"}
recv  strike_result   roll.skill_id: "lore"
      char.skills_used_this_session: ['lore', 'stealth']
```

`skills_used_this_session` gates `spend_skill_point`, so this is free
advancement credit for a skill the character did not use — against T4.1/D7
("the tradition's skill rolled, so the caster used it"), which the PR's own new
comment at :1016 cites.

**Fix** — make `1020-1022` conditional: `if not magical and skill_id and skill_id in character.skills:`.

---

### B8 — The Final Blow, a Combat-only capstone, fires on a Knowledge + Lore working

`websocket.py:849-853` gates the Final Blow on the *declared* `skill_id ==
"combat"`. On the magical branch the declared skill is discarded and Lore/Attune
is rolled, so the gate checks a field that no longer describes the roll:

```
Zahna holds the_final_blow; send {"type":"strike",...,"magical":true,
  "scope":"significant","purpose":"harm","skill_id":"combat",
  "final_blow":true,"sparks_spent":1}
recv  strike_result  final_blow_available: True  roll.skill_id: "lore"
      dice: [4, 4]      # the Spark it demanded bought no die — see B4
      char.sparks: 3 → 2
```

**Fix** — at line 849, check the roll that will actually happen:
`if magical or str(msg.get("skill_id", "combat")) != "combat":` with the message
"The Final Blow requires a Combat roll." (or, if the intent is to allow it,
D25 must say so and the books must state it).

---

### B9 — Dropping `magic.prepared_intents` no longer restores the unlimited game

D23's **Data** paragraph, quoted from `docs/DECISIONS.md:1102` (context line of
this diff):

> …purposes, capacity, free scopes and the off-purpose price are all data, and
> **a setting may drop the section to restore the unlimited game.**

The new schema comment (`app/facets/schema.py:1119-1122`) restates the same
contract: "A setting that wants the free magical attack back widens this list."
But `websocket.py:880-891` hardcodes the fallback:

```python
        _pi = session.ruleset.magic.prepared_intents if session.ruleset.magic else None
        strike_scopes = _pi.strike_scopes if _pi else ["significant", "major"]
```

Drop the section and a Minor magical Strike is still refused, while a
Significant one is now *free* (`intent_cost` returns `"free"` when `pi is None`,
`character.py:707`). That is neither the limited game nor the unlimited one. No
test covers the absent-section case.

**Fix** — `strike_scopes = _pi.strike_scopes if _pi else ["minor", "significant", "major"]`,
with a test asserting a Minor magical Strike lands when the ruleset has no
`prepared_intents`.

---

## SHOULD-FIX

### S1 — "Free Minor magic fights as a Maneuver or Support" is not true of those handlers

III.3:451 and MM5:153 now route the caster's free combat magic through Maneuver
and Support. Neither handler can express magic: `_handle_maneuver`
(`websocket.py:1575-1615`) and `_handle_support` (`1533-1572`) both call
`_build_roll_request`, which takes `attribute_id`, `skill_id` and the MM's
declared `difficulty` — there is no `domain_id`, no `scope`, and no call into
`resolve_magic_roll`, so the domain-type difficulty table never applies. The
client is worse: `play.js:1457` hardcodes `difficulty: 'Standard'` on every
Maneuver, and the Maneuver sub-form (`index.html:494-508`) has no domain, scope
or purpose control at all. A Prismatic caster's Minor Maneuver should be Hard
(II.4b/II.4c, "Hard at Minor scope") and is priced Standard.

**Fix** — either add the same optional `magical`/`domain_id`/`scope` triple to
`_handle_maneuver` and `_handle_support`, routing through `resolve_magic_roll`
(refusing any scope in `strike_scopes` unless it is paid for), with matching
controls in the Maneuver and Support sub-forms; or, if that is deferred, say so
in III.3:451 — "the MM prices a magical Maneuver from the domain table as
usual" — and open a TODO, because right now the book's recommended action is
the one the software cannot price.

### S2 — III.3 says "Significant"; the checklist, MM5, facet.yaml and the code say "Significant or Major"

`III.3_Combat.md:449`:

> so magic used as a Strike is **Significant**, declared with its domain and
> purpose

`III.3_Combat.md:768` (exchange flow, same PR):

> a magical Strike is a full form: **Significant or Major**, and it spends a
> readied intent

`III.3_Combat.md:461` (same PR): "A Strike is Significant or Major".
`facet.yaml:1503`: `strike_scopes: [significant, major]`.
`websocket.py:881` accepts both. The one sentence a table will actually read —
the bolded lead — is the one that is wrong.

**Fix** — `III.3_Combat.md:449`, replace "is **Significant**, declared with its
domain and purpose" with "is **Significant or Major**, declared with its domain,
scope and purpose".

### S3 — The client never applies the `readied_intents` the server now broadcasts

`_handle_strike` broadcasts `readied_intents` (`websocket.py:1060`), and
`onStrikeResult` (`play.js:1564-1632`) ignores it — it updates
`endurance_current` and `sparks` only. `onCastResult` does it correctly
(`play.js:2296`). So after a magical Strike the pip row (`renderReadiedIntents`)
and the new cost preview (`renderStrikeMagicCost`, which reads
`state.character.readied_intents` at `play.js:1340`) both keep showing the
pre-Strike count. The player is told "1 harm readied — this spends one" on a
Strike the server will charge a Spark for. The PR's stated goal is to show the
price before the blow; this is the one place that breaks it.

**Fix** — in `onStrikeResult`, inside the `if (msg.attacker === state.playerName && state.character)`
block at `play.js:1570`, add:

```js
    if ('readied_intents' in msg && msg.magical) {
      state.character.readied_intents = msg.readied_intents;
      renderReadiedIntents();
      renderStrikeMagicCost();
    }
```

### S4 — The cost preview states a rule the server does not enforce

`play.js:1340-1343`:

```js
  const readied = (state.character && state.character.readied_intents) || null;
  if (!readied) {
    out.textContent = 'Nothing readied this session — this will cost a Spark.';
```

For a formalized caster who has not yet readied, `readied_intents` is `null` and
`Character.intent_cost` **raises** — verified: `"Ready your intents for this
session before a Significant or Major working."` The Strike is refused, not
charged a Spark. For a pre-Technique caster the same branch fires and the server
refuses for a different reason again (B2).

**Fix** — replace those three lines with:

```js
  if (!state.character || !state.character.magic_technique_active) {
    out.textContent = 'Your domain has not formalized — no magical Strike yet (II.3).';
    return;
  }
  const readied = state.character.readied_intents;
  if (!readied) {
    out.textContent = 'Ready your intents for this session first.';
    return;
  }
```

and hide the whole `strike-magical` checkbox (`index.html:402`) when
`!state.character.magic_domain || !state.character.magic_technique_active` — at
present every character, caster or not, is offered it.

### S5 — Tests do not test the rule

New server tests (`tests/test_websocket.py:5599-5739`, `TestAMagicalStrikeIsAFullForm`)
are seven happy-path-shaped cases against a formalized caster. Every BLOCKER
above is outside their reach. Specifically untested:

- `spark_use` on a magical Strike, in any form (B1, B2).
- Any pre-Technique caster (B2) — `_mage` takes a `formalized` parameter that
  **no test ever passes**, so the one seam built for it is dead.
- `sparks_spent` on a magical Strike (B4).
- Major scope — the second half of `strike_scopes` is never exercised.
- A ruleset without `magic.prepared_intents` (B9).
- `skill_id` other than the default (B7); interaction with `final_blow` (B8).
- The rider/`enemy_strike` path that actually depletes Resolve.

`test_a_refused_working_spends_no_endurance_and_no_spark` is the one test aimed
at order-of-operations, and it only covers the *one* refusal that happens to sit
above the payments (line 903). Rename it — its current name asserts a general
property that B3 shows is false — and add the pre-Technique twin, which is the
case that fails.

`_strike` pins `random.randint` to 4 for every die. That hides B4: with two dice
or four the total is identical, so a test can assert `outcome` and never notice
that the Sparks bought nothing. `test_press_still_works_on_a_working` is the only
one that counts `dice_rolled`; the Spark path needs the same assertion.

e2e (`tests/e2e/test_ui_flows.py:1283-1346`):
`test_the_scope_picker_never_offers_minor` asserts the contents of a static
`<select>` in `index.html:407-410` — it would pass unchanged if every server-side
check in this PR were deleted. Same for
`test_the_fields_are_hidden_until_the_box_is_ticked`. Neither is worthless as a
regression pin, but neither tests the rule. The gap that matters is S3: no e2e
asserts the pip row or the cost line updates after a magical Strike, which is
exactly the bug.

---

## NOTES

### N1 — D25 changes party offense; no recipe or simulation was re-checked

Under D25 a caster gets at most three magical Strikes per session. The encounter
recipes (`MM5:Encounter Recipe Table (PS 3 — simulation-validated)`, MM1's
Encounter Budget) were calibrated by `tools/combat_sim.py`, whose Zahna
(`tools/combat_sim.py:1209-1220`, "Lore Expert, magic active") is modelled as a
*physical* striker with `strength_mod`/`combat_mod` and strikes every exchange
for free. The corpus therefore never priced a caster and is not invalidated by
D25 — but it also cannot confirm the recipes still hold now that a third of the
party's offense is capped at three uses. Worth a line in D25's *Revisit when*.

### N2 — `_apply_difficulty_step` runs and is discarded on the magical branch

`websocket.py:947-957` computes the Technique step, then line 991 sets
`technique_step = None`. The function is pure, so this is waste rather than a
bug, and it matches `cast` (which applies no Technique step either). But the
broadcast now reports `technique_step: null` for a working a Technique may
legitimately have eased, and the comment at 970-976 asserts "nobody declared a
label" while the client's `performStrike` in fact always sends
`difficulty`/`declared_technique_ids`. Move the `_apply_difficulty_step` call
inside the `else:` branch so the code says what the comment says.

### N3 — `pay_intent_cost` at line 1012 can raise after the roll is recorded

`pay_intent_cost` re-derives the cost by calling `intent_cost` again
(`character.py:735`), which raises on the same conditions the pre-check tested.
Between the check (903) and the payment (1012) there is no `await`, so asyncio
cannot interleave two of this player's messages and the race is closed by
accident rather than by design. If an `await` is ever added in that window, the
second Strike would compute `paid == "spark"` while `off_purpose_sparks` is
still 0 from the first check, and pay nothing. Pass the already-computed cost
into a `pay_intent_cost(cost)` overload, or assert it.

### N4 — Prose

III.3:449-453 and II.3:75-79 read in the house voice and land cleanly at the
table; III.3:451's "Free magic is not weak in a fight. It is indirect." is the
kind of line the books do well. Two snags. (a) II.3:79 "A Minor working … never
decides anything" is an absolute that III.3:451 immediately undercuts — "A
Maneuver's 10+ makes rolls against the target Easy … which is frequently worth
more than a hit." Suggest "never decides a fight on its own". (b) The exchange
flow at III.3:768 is a six-line code block whose step 2 is now a 24-word
parenthetical; compress to "2. Declare actions (Strike / Support / Maneuver /
Magic — a magical Strike is a full form and spends an intent)".

### N5 — Areas read and found clean

- `_handle_react` (`websocket.py:1075-1181`), `_handle_saving_throw`
  (`1386-1426`), `_handle_use_item` (`2136-2173`), `_handle_strike_rider`,
  `_handle_final_blow_confirm`, `_handle_enemy_strike` (`2035-2133`): no magic
  route, nothing this PR could have bypassed.
- `_handle_contested_roll` (`1622-1695`): MM-gated, no magic path, untouched.
- `_dispatch` (`172-281`): `strike` is player-reachable and correctly so;
  `enemy_strike`/`enemy_update` are `is_mm`-gated.
- `tools/combat_sim.py`: does not simulate magic (only reads the D6 variant flag
  at `:46-55`) and re-implements no rule this PR touches — no second copy.
- Generated files: `player_handbook/Index.md` is the only one in the diff and its
  additions are consistent with `build_index.py` output;
  `tests/test_docs_consistency.py` passes 55/55, so the no-diff invariants hold.
  No new tables or boxes, so `List_of_Tables.md`/`List_of_Boxes.md` correctly
  unchanged.
- `docs/DECISIONS.md` D26 (`:1154-1178`): docs-only, self-consistent, correctly
  marked ⏸️, and asserts no mechanic. Nothing to fix.
- `facet.yaml:1500-1503` and `schema.py:1115-1120`: the data encoding is the
  right shape; the defect is in how the handler falls back when it is absent (B9).
