# REVIEW — Lean Facets v1.0 software (code review)

**Date:** 2026-09-26 · **Branch:** `feat/lean-facets` (HEAD `ec370f7`) · **Scope:** `software/` as it stands (diff base `pre-lean-facets`)
**Reviewer brief:** correctness, rule re-implementation, security, test quality, code health.
**Nothing in `software/`, the tests or the books was modified.** Repro scripts live in the session scratchpad
(`/tmp/claude-0/-root-facets-of-origin/55fd913e-d3f6-4135-aef9-fb4a4af0ef9d/scratchpad/`):

| Script | What it drives |
|---|---|
| `test_repro_ws.py` | pytest, reuses `tests/test_websocket.py`'s `Table` harness; **every test passes while its bug exists** (12/12 passed) |
| `repro_engine.py` | engine-only checks (Intercept, dying, Polymath, Hold On, round-trip) |
| `repro_rest.py` | REST: path traversal, HTML name, zero-slot inventory |
| `repro_xss.py` | Playwright + a live `run.py` server: stored XSS in the MM's page |

Run from `software/`: `python -m pytest <scratchpad>/test_repro_ws.py -q -s -p no:cacheprovider`.

**Counts:** Critical 1 · Major 14 · Minor 17 · Nit 5.

---

## Critical

### C1. Stored XSS: a character name runs script in every connected browser, the MM's included
- **Where:** `app/static/js/app.js:307` — `character_created(m) { … feedSys(\`${m.character.name} joins the party.\`) … }`. `feedSys` → `feedPush` → `el.innerHTML = html` (`app.js:401`). The name is the one value on that path that is not wrapped in `esc()`. Server side, `CreateCharacterRequest.character_name` (`routes/character.py:74`) takes any 1–64 characters.
- **Failure:** a player creates a character named `<img src=x onerror="window.__xss=1">`. It is broadcast as `character_created` to every socket, and the script runs in the MM's page. The CSP (`app/main.py:54`) allows `'unsafe-inline'` scripts and `connect-src ws: wss:` to **any host**, and the MM's JWT sits in `sessionStorage` (`app.js:36`). So a player can take the MM token and, with it, every MM REST route and WS event.
- **Repro:** `repro_xss.py` (live server + Chromium; the MM logs in through the UI, then a player creates the character over REST) → `script ran in the MM's page: True`. `repro_rest.py` shows the API accepts and echoes the name verbatim.
- **Fix:** `feedSys(\`${esc(m.character.name)} joins the party.\`)`. Then make `feedSys` escape its argument by default, add an HTML variant for the few callers that pass markup, and use a lint/grep test so no `${…}` of server data reaches `innerHTML` unescaped. Tighten the CSP: drop `'unsafe-inline'` for scripts (the app's JS is already in files) and limit `connect-src` to `'self'`. Refusing `<>` in names server-side (the player-name regex already does this) would add defence in depth.

---

## Major

### M1. A Major harm working hits the same foe once per repeat in `targets` (damage ×N)
- **Where:** `app/api/websocket.py:821` builds `group` from `targets` without de-duplicating. `app/game/magic.py:237` applies damage to every entry and skips only `foe is enemy`.
- **Failure:** at level 3, `cast {scope: major, intent: harm, targets: [k,k,k,k,k]}` rolls 9 damage once and applies it five times. An Elite with 40 HP goes 40 → 0 from one roll.
- **Repro:** `test_R1…` → `single roll raw damage 9 hp 40 -> 0 entries 5`.
- **Fix:** in the engine, de-duplicate by identity: `seen = {id(enemy)}`, then skip any foe whose `id(foe)` is already in `seen` before damaging it. Also refuse duplicates in `_cast` (WSError). Add a test.

### M2. Players can take unlimited breathers during a fight (free half-HP heals)
- **Where:** `websocket.py:905-924` (`_rest`). A player may call `breather` at any time, any number of times, with combat running. `Character.breather` (`character.py:~503`) has no scene limit and no combat check, and it also brings an `out` character back to `ok`.
- **Failure:** a player at 1 HP sends `rest {kind: breather}` three times during exchange 1 and is back at full HP.
- **Repro:** `test_R2…` → `combat running: True hp 16 / 16`.
- **Fix:** refuse player breathers while `session.combat is not None` (or make breathers MM-called, like nights). Optionally track one breather per scene in the engine. Test it.

### M3. MM notes leak to players through REST (and across sessions)
- **Where:** `routes/character.py:250` `list_characters` returns `to_client_dict()`, which includes `notes_mm`, to **any** valid token, with no session check. `routes/character.py:189` `export_character` returns the full `.fof` (with `notes_mm`) and checks only `player_name`, never `session_id`.
- **Failure:** (a) any player, including one from a different session, lists every character's MM notes. (b) A player named "Player1" in session B exports "Player1" from session A.
- **Repro:** `test_R3…` → `200 SECRET: Mordai's sister is the villain` using a token for a *different* session. `test_R4…` → `200 ['  notes_mm: SECRET plan']` using a same-named token from another session.
- **Fix:** check `token.session_id == session_id` for players on every route. Strip `notes_mm` from player responses (reuse `_player_safe`), and from the player's export. Also rewrite `test_list_characters_with_player_token_allowed`, which currently asserts only `200` (see T1).

### M4. A player's `.fof` upload skips every rule: level 10, 99 Sparks, 500 HP, 3/3/3 stats, self-written MM notes
- **Where:** `routes/character.py:141-185` (`upload_character`) → `Character.validate_against_ruleset` (`character.py:~830`). Validation checks ids and ranges only. It does not check stats against the Facet's +2/+1/+0 (+level increases), talent count against level, `hp_current ≤ hp_max`, Sparks, `signature` vs `class`, `status`, or who wrote `notes_mm`.
- **Failure:** a player downloads their sheet, edits it, and re-uploads it mid-session. The result is level 10 with two talents, `sparks: 99`, `hp.current: 500` (max 71), stats 3/3/3, and `notes_mm` set by the player. The same trick also resets HP, Wounds or a `dying` status at any time.
- **Repro:** `test_R5…` → `200 level 10 sparks 99 hp 500 / 71 stats {'body': 3, 'mind': 3, 'soul': 3} talents ['weapon_master', 'tough'] notes_mm the MM never wrote this`.
- **Fix:** give players' uploads a strict validator (`validate_build()`): stats match the Facet plus stat-increase levels; talent picks = starting + (level − 1) − signature; `0 ≤ hp_current ≤ hp_max`; `sparks ≤ base`; and so on. Or allow uploads only while the session has no character for that player (join, not overwrite), and keep the server's `notes_mm`/state for an existing character. Let only the MM upload arbitrary state.

### M5. A stale `pending_hold_on` lets a healed character roll Hold On at positive HP and go down again
- **Where:** `websocket.py:862-869` guards Hold On with `player in pending_hold_on or (hp == 0 and status == ok)`. Nothing removes a player from `pending_hold_on` when they are healed (`hp_adjust`, breather, night rest, Mend). `Character.hold_on` (`character.py:436`) never checks `hp_current == 0`, so every tier overwrites HP (to 1 or 0).
- **Failure:** a foe drops Mordai (Wound, pending Hold On). The MM heals him to 8 before he rolls. He then rolls Hold On, gets 6−, and ends at **0 HP, dying**. Engine-only: a character at full HP who calls `hold_on` ends at 0/dying.
- **Repro:** `test_R6…` → `hp after heal 8 -> after Hold On 0 dying`. `repro_engine.py` → `hp 16 -> 0 dying`.
- **Fix:** in `Character.hold_on`, raise unless `hp_current == 0 and status == "ok"`. Drop the WS set in favour of that state, or clear it in every heal/rest path.

### M6. Healing (or levelling) a dying character leaves them `dying` with HP > 0
- **Where:** `Character.heal` (`character.py:405`) flips only `out → ok`. `level_up` raises `hp_current` without touching `status`.
- **Failure:** the MM heals a dying character by 5 (Mend, a draught). They have 5 HP and are still `dying`. They cannot attack ("in no state to attack"), yet `death_choice` is still open. A level-up does the same (`[] hp 6 status dying`).
- **Repro:** `test_R7…` → `hp 5 status dying attack: Mordai is in no state to attack.`; `repro_engine.py` "level-up while dying".
- **Fix:** decide the rule (healing a dying character stabilises them → `ok` at that HP, or `out` until a breather), put it in `heal()`, and cover `level_up` too. Test all three statuses.

### M7. Taking Thaumaturgy/Invocation at a level-up produces an invalid character (no magic block), and the UI offers it
- **Where:** `Character.level_up` (`character.py:~655-760`). `_apply_talent_choice` (`:640`) handles only `wider_domain`, and nothing accepts or installs the domain and two signature workings for a new casting talent. `builder.js:384-397` sends no magic fields.
- **Failure:** a Mind Investigator picks Thaumaturgy at level 2. `level_up` returns `[]`, `magic` stays `None`, `validate_against_ruleset` now fails ("needs a magic block"), and every `cast` fails ("holds no … domain"). Uploading the exported file is refused.
- **Repro:** `test_R10…` → `level_up errors: [] magic: None validate: ['A character with a casting talent needs a magic block …']`.
- **Fix:** `level_up(..., magic={domain, signature_workings})`, validated with `_magic_setup_errors` whenever the pick grants a tradition. Add the fields to `level_pick` and to the level-up screen.

### M8. Respec silently drops the Wider Domain's second domain
- **Where:** `Character.respec` (`character.py:778-826`) sets `trial.magic = None` and rebuilds from `domains[0]` only. The Wider Domain `choice` is never reapplied.
- **Failure:** a level-2 Thaumaturge with Wider Domain (Inscription + Warding) respecs to the same picks. Afterwards `domains == ['inscription']` while `wider_domain` is still held.
- **Repro:** `test_R11…` → `before respec ['inscription', 'warding'] … after respec ['inscription'] wider_domain held: True`.
- **Fix:** after `_magic_setup_errors`, apply `wider_domain` states' `choice` (validated as in `create_character`). Add a test.

### M9. Defend does not stop you attacking
- **Where:** `combat.resolve_attack` (`combat.py:253`) never checks `state.defending`. `declare_defend` returns `can_attack` (Sentinel improved), but nothing enforces it.
- **Failure:** Mordai (no Sentinel) Defends, so attacks on him are Hard. He then attacks at Standard and hits.
- **Repro:** `repro_engine.py` inline → `defending attacker attacks anyway: difficulty Standard hit True`.
- **Fix:** in `resolve_attack`, when `state.defending` holds the attacker, raise unless `has_talent("sentinel", improved=True)`, and in that case force at least Hard. Add a test for each branch.

### M10. Studied Foe, Warding Presence and Anatomist cannot happen in the app
- **Where:** the engine reads `enemy.studied` (`combat.py:316, 361`) and `state.warded` (`combat.py:461`), but nothing in `app/` or `tools/` ever sets either: `grep -rn "studied = True\|warded.add"` finds nothing. `talent_use` only ticks a counter. `enemy_update` cannot set `studied`, and `enemy_attack` takes no override flags.
- **Failure:** a Soul character uses Warding Presence; the MM's next `enemy_attack` on that ally still rolls at Standard. Studied Foe never makes allies' attacks Easy, and Anatomist never ignores armor.
- **Repro:** code search (above). The engine paths are tested in `test_combat.py`, but the WS layer that should set them is not, so the gap is invisible to the suite.
- **Fix:** add WS events such as `study {enemy}` (sets `enemy.studied`, ticks nothing: it is at-will) and `ward {ally}` (ticks the use and adds to `state.warded`), plus UI buttons. Or have `talent_use` accept a target and apply the engine hook.

### M11. The simulator carries a rule the engine does not have: exposure on a 7–9 working (CLAUDE.md violation)
- **Where:** `tools/combat_sim.py:176` — `if res.outcome == "partial_success": state.expose(ch.name, target.key)` after `resolve_cast`. Exposure is an attack rule (`combat.resolve_attack`). `magic.resolve_cast` has no exposure, and the design gives a 7–9 working "pick one of two costs".
- **Failure:** sim casters take extra enemy dice that app casters never take. Every danger-read calibration drawn from `combat_sim` with casters in the party is biased. This is the same kind of divergence CLAUDE.md records as having invalidated an earlier research corpus.
- **Repro:** code; compare `magic.py:246-259` (no exposure) with `combat_sim.py:176`.
- **Fix:** delete the line. If casting in melee should expose the caster, put that rule in `magic.resolve_cast` (with a `state` argument) and in facet.yaml. Rerun the calibration afterwards.

### M12. The HTTP roll's natural 2 pays its Spark, then can be claimed and confirmed for a second Spark
- **Where:** `routes/rolls.py:67-68` calls `record_roll` (which copies the dict into the log) **before** `confirm_natural_two_graceful_fail` (which marks the dict). The logged entry never gets `graceful_fail_claimed`. The WS path uses `_record_roll` in the right order.
- **Failure:** a player rolls a natural 2 over HTTP (+1 Spark automatically), then sends `graceful_fail` over WS. The log entry is unclaimed, so the claim succeeds and the MM's confirm pays a second Spark.
- **Repro:** `test_R8…` → `logged entry claimed flag: None`, `sparks 3 -> 5`.
- **Fix:** call confirm first, then record, as `websocket._record_roll` does, or reuse that helper. Test it.

### M13. Path traversal: an MM-created character name writes a file outside the session directory
- **Where:** `routes/character.py:111` uses `player_name = body.character_name` (free text, ≤ 64 chars) for MM creations. `session.py:131` writes `self._character_dir / f"{player_name}.fof"`. Uploads take `player_name` from the file, unvalidated for the MM.
- **Failure:** a character named `../../../escaped` writes `DATA_DIR/escaped.fof`, and deeper `../` sequences reach any directory the server can write. This needs an MM token, but C1 hands that token to a player.
- **Repro:** `repro_rest.py` → `files written outside the session dir: ['escaped.fof']`.
- **Fix:** key files by `_slug()` of the name, or validate `player_name` with `PLAYER_NAME_RE` everywhere. Also assert `path.resolve().is_relative_to(self._character_dir.resolve())`.

### M14. One broken optional Facet on disk stops every session from being created, even base-only
- **Where:** `registry.build_ruleset` (`registry.py:322-323`) runs `load_facet_file` on **every** discovered file before filtering by `wanted`, so any `FacetLoadError` aborts. `create_session` turns that into a 500.
- **Failure:** a homebrewer drops a half-written `facets/mine/facet.yaml`, and no MM can start any session.
- **Repro:** a temporary facets dir with base plus one invalid setting Facet: `build_ruleset([])` → `FacetLoadError facet.yaml: Schema validation failed …`.
- **Fix:** read only the `id` cheaply (or catch per file). Fail only for the core and for requested ids, and log the rest as warnings (`/api/facets/available` already reports per-file errors). Add a test. The abandoned `fix/engine-housekeeping` branch had this fix ("broken-optional-Facet containment").

---

## Minor

1. **Player identity `"mm"` receives the MM's private view.** `PLAYER_NAME_RE` (`auth/tokens.py:19`) allows `mm`, while `broadcast_split` / `send_to_identity` / `_push_state` pick the MM view by `ident == "mm"` (`websocket.py:85, 332`). A player invited as "mm" gets unrevealed toolbox results (oracle questions, NPC secrets), foe HP and MM notes. *Repro:* `test_R9…` → `player 'mm' got: Is the duke the traitor?`. *Fix:* key MM connections by `is_mm` (store a tuple `(ws, identity, is_mm)`) and reserve "mm" in the regex.
2. **Inventory PUT lets players rewrite item weights and dice.** `InventoryItemRequest.slots` (`routes/character.py:301`, `ge=0`) overrides the ruleset's slots, and `usage_die` accepts any int. 30 × heavy armor at 0 slots each plus a rope with a d1000 usage die gives `200 … slots_free: 11` (`repro_rest.py`). *Fix:* for ruleset ids ignore client `slots`/`armor`/`weapon`; allow `usage_die` only from `ud.steps`.
3. **Talent-use limits can be bypassed with `period`.** `talent_use` (`websocket.py` `_talent_use`) passes a client `period`, and each `talent@period` key gets its own limit of 1 (`character.py:357`). A once-per-scene talent is used 4× in one scene (`test_R12…`). *Fix:* reject `period` unless the talent's improved form defines a second period (e.g. the casting talent's `@scene`).
4. **Player-declared modifiers.** `roll`/`attack`/`cast` take `difficulty`, `knack`, `bonus` (0–2), `within_reach` and `in_cover` from the player. A player can declare Easy, +knack and +2 on every roll, or `within_reach:false` to never be exposed. This is a trust-model decision, but it should be one: consider MM-set difficulty per scene and an MM-visible flag when a player self-declares.
5. **`/api/rolls/` is private** (not broadcast; `rolls.py` docstring), so a player can roll unseen and re-roll until they get a result they like. Restrict it to the MM or broadcast it.
6. **`reduce_fatigue` spends the once-per-scene use on a 0-Fatigue working** (`magic.py:142-152, 265`): Minor scope → `fatigue paid 0 uses left 0` (`repro_engine.py`). Spend it only when it removed a point.
7. **Polymath's extra talents skip `requires` and `choice`** (`character.py:681`). A non-caster gets `wider_domain` and a `weapon_master` with no kind, and `validate` still returns `[]` (`repro_engine.py`). *Fix:* run `_menu_errors` minus the teacher check, plus `_choice_errors`, per extra, and accept choices.
8. **An interceptor who has dropped still intercepts** (`combat.py:89 interceptor_for`). The dying Mordai takes the hit meant for Bex (`repro_engine.py`). Skip defenders whose `status != "ok"` (needs `party`).
9. **Morale results leak card secrets.** `morale_result` (`websocket.py:1304`) broadcasts the foe's `morale` and BREAKS text to players, while `_player_enemy_view` deliberately hides card text. Use `broadcast_split`.
10. **Stale per-player state after delete/recreate.** `delete_character` leaves `level_up_ready`, `pending_hold_on`, `pending_attacks` and the file on disk, so a rebuilt level-1 character inherits a called level-up.
11. **A 10+ attack's option pick can silently vanish.** `_choose_option` replays the stored dice but recomputes difficulty (openings, level gap). If an opening was consumed in between, the replay can fall below 10 and `chosen` is dropped without an error. *Unverified* (code reading); store the preview's difficulty in `pending` and replay with it.
12. **Uncaught exception types drop the socket.** `_dispatch` catches only `WSError/ValueError/KeyError`. For example, `respec` with `{"id": ["x"]}` raises `TypeError` from `get_talent(list)`, and the outer handler closes the connection. There is no per-socket rate limit on WS events (each broadcasts to the table).
13. **Enemy heal is handled in the WS layer** (`_enemy_update`: `min(mx, hp + heal)`, `defeated = False`) and never clears `bloodied`, so a foe healed to full stays Bloodied. Move it to `combat.heal_enemy`.
14. **The WS layer re-implements `Character.fall`.** `_drop_to_zero` (rolls the wounds table, `add_wound`) duplicates `fall()` minus Hold On, and `_level_pick` rolls the grit die itself. Split `fall()` into `take_fall_wound()` + `hold_on()` and call those.
15. **JS repeats rule arithmetic** that the engine should supply: mob damage `Math.min((count-1)*per, cap)` (`play.js:458`), the Bloodied threshold `Math.floor(hp/2)` (`play.js:455`), coin slots (`components.js:114`), creation slot total (`builder.js:156`), and Wider Domain eligibility (`builder.js:372`). Put `mob_bonus`, `bloodied_at` and `coin_slots` in the engine's `card`/`derived` dicts.
16. **The level-up UI cannot trade Wider Domain up to a prismatic domain.** The choice `<select>` appears only for `kind === 'talent'` (`builder.js:372`), so an `improve` pick never sends `choice`.
17. **Rule data lives in code, not facet.yaml:** `encounter.ROLE_POINTS`/`LEVEL_SWING`/thresholds (`encounter.py:15`), `GIFT_STAT = "soul"` (`magic.py:23`), prismatic `new_level < 5` (`character.py:713`), heavy armor matched by the literal `"heavy"` (`magic.py:135`), and use counts parsed from prose `"Twice…"` (`schema.py:119`). CLAUDE.md makes facet.yaml the single source of truth.

## Nit

1. `improve_requires_levels_held` (`character.py:705`): `level - level_taken + 1 < 1` can never be true, because a talent cannot be improved in the level it was taken, so the check is dead code. Either delete it or make the rule mean something.
2. Bloodied at `hp <= mx // 2` puts a 7-HP foe Bloodied at 3, not 3.5 → 4 (`combat.py:192`). This is consistent with the JS, but "half HP" should be defined in facet.yaml.
3. The repo's canon `.fof` files omit `weapon`/`armor` on inventory items, and the round trip adds them (`repro_engine.py`: only `inventory` differs, by enrichment; no loss). Regenerate the canon files so they round-trip byte-stable.
4. `Enemy.from_fof` does not `int()`-cast the `hp`/`damage`/`attack` overrides; a quoted YAML number becomes a string and breaks the arithmetic later.
5. `tables_file` is joined to the Facet's directory without containment (`loader.py:104`). This only matters for server-side content, but add a containment check to match M13.

---

## Test quality

- **T1 (Major impact).** `test_api.py:458 test_list_characters_with_player_token_allowed` asserts only `status_code == 200`, so it enshrines M3. It should assert that `notes_mm` is absent and that a foreign session's token is refused.
- **T2.** No test covers any of M1, M2, M5–M10, M12: duplicate targets, combat breathers, Hold On after a heal, healing the dying, levelling into a casting talent, respec with Wider Domain, attacking while Defending, or the WS side of Studied/Warding. Each is a public path with fewer than the 3 tests per function CLAUDE.md requires.
- **T3.** `ScriptedRNG.randint` (`test_websocket.py:38`) **clamps** queued values into range. A test that pushes a 7 for what should be a d8 but is actually a d6 passes silently. Raise on out-of-range values instead.
- **T4.** `test_magic.py:225 test_to_dict_is_json_safe` has no assert (it relies on `json.dumps` raising). Fine, but assert a field round-trips.
- **T5.** The e2e suite exercises the UI with benign names only. Add one hostile-string pass (names, notes, chat, custom class/knack, working names containing `<img onerror>`) so C1-type regressions fail.

## Checked and found sound

- Keep-best-two with extra dice; naturals read on the kept dice (with extra dice, a natural 1+1 needs every die ≤ 1); the +4 cap on stat + knack + bonus; the difficulty clamp. Enemy exposure die consumed once per foe per exchange. Mook drop and Cleave counts. Morale "over" and fearless ≥ 12. d66 / 2d6 table expansion and coverage validation. The oracle's natural checks.
- Level-up blocks: signature early/late, stat cap, off-Facet casting talents, teacher for off-menu talents, max level.
- Sparks are debited exactly once on attack (preview uses `apply=False`). WS size cap, auth timeout, invite single-use, MM-only gating on all `mm_only` handlers, players act only as themselves (`_actor`). Clients cannot supply dice.
- `.fof` v1.0 round trip of the three canon characters loses nothing (see Nit 3).
- Module-level `RNG` is shared across sessions, but the server is single-threaded asyncio. It is a test seam, not a race.
