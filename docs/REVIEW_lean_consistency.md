# REVIEW — Lean Facets v1.0 consistency audit

**Date:** 2026-09-26 · **Branch:** `feat/lean-facets` @ `ec370f7` · **Revert pin:** `pre-lean-facets`
**Scope:** PHB, MM Manual, Bestiary, quick refs, `facet.yaml` + `tables.yaml`, engine (`software/app/game/*`), WebSocket layer, static app, Oraga Night, Val'loh, cast files, spec/README/references. The target is what `test_docs_consistency.py` does **not** catch; that suite passes.
**Method:** five parallel passes (books vs rules, software behaviour, talents, module/cast/canon, v0.3 residue). Each finding was re-read at the cited lines, and software findings were reproduced with throwaway scripts (`cd software && PYTHONPATH=. python <script>`; the scripts are in the session scratchpad and not in the repo).
**Precedence:** `facet.yaml` wins unless it is the bug. Quick references may only compress body text.

**Counts:** Critical 1 · Major 11 · Minor 27 (+4 canon items for the owner, K1–K4) · Nit 21

---

## What was checked and agrees (no finding)

These are in agreement across books, YAML and engine:
- stat creation, maximum and the stat levels (4 and 8); bonus cap +4; the knack +1, which never stacks; the difficulty table; player naturals on the kept dice
- Spark earn methods, 3 per session with no carry-over; Borrowed Trouble max 1; the avoid bands
- HP formula, grit dice and averages, minimum gain 1, Tough +4
- slots 10 + Body, Iron Lungs +2; coin per slot 100 (floor); starting coin 2d6×10; the price guide; weapon dice and slots; armor values, cap 3, minimum 1
- attack tiers and the 10+ options; enemy 2d6 + attack with +2 on a hard hit; level gap 3 → Hard, 6 → Very Hard; damage bonus +1/+2/+3 at levels 3/6/9
- Mook drop on 7+; mob +1 per extra Mook, capped at +4 (the rule text); role multipliers; the monster level table (MM1, MM5, Finding Aids, every module statline); morale 2–12, default 7, fearless 12, the four triggers, "over the morale" breaks
- Bloodied; Hold On bands, including Tough improved; tending; the death choice; breather and night rest
- the scope table; heavy armor +1 Fatigue; signature step; Wider Domain step and the level-5 prismatic trade; signature workings at levels 5 and 9; Miracle; Arcane Mastery
- usage die steps and the 1–2 step-down; curio limit 3 (+1 Tinker)
- level-up picks, respec before level 3, the teacher rule, casting talents never taken off-Facet
- hoard formula, oracle odds and reaction bands (MM5 = MM6 = tables.yaml = engine); the danger read (MM1–4 = MM5 = engine)
- every talent's text, improved, normal and choose, which appear verbatim in II.4a/b/c with matching use headers
- all 12 preset class cards; all 15 backgrounds; every pregen's stats, HP, slots and talent menu
- the three Bought reskins (INV-18); Val'loh's facet.yaml adds only; every module and Val'loh `Chapter X.Y` pointer
- the cast files against DESIGN §5 and `references/phb-examples.md`
- Zahna, Mordai and Zulnut are "he" on every live surface; Mordai's Scar is carried verbatim from the pin

---

## Critical

### C1. Weapon Master does nothing for any character built in the app, including the Warrior preset
- **Engine:** `software/app/game/character.py:292-293`: `if wm and w.kind and wm.choice == w.kind:`. The die steps up only when the equipped item carries a matching `kind`.
- **Data:** `software/facets/base/facet.yaml:1094-1096`. `light_weapon`, `standard_weapon` and `heavy_weapon` have no `kind`; only `longbow` (bows) and `staff` (blunt) have one.
- **App:** `builder.js:94-95` asks "Weapon Master: which kind of weapon?", but no step, and no inventory editor (`tools.js:205-208`), ever tags a weapon with a kind.
- **Promise:** `facet.yaml:105-107` "your damage die is one size larger"; `Quick_Start.md:81` "Your longsword rolls a d10 because of Weapon Master"; `III.3_Combat.md:200`.
- **Repro:** `create_character(class_id="warrior", talent_choices={"weapon_master":"blades"})` gives `weapon_die == 8`. The improved form (two options, `combat.py:244-246`) is dead for the same reason.
- **Why it works in the books:** only hand-written files that add `kind: blades` (`characters/Mordai.fof:45`, the Oraga pregens) get the bigger die.
- **Winner:** the rule. Tag the kit weapon with the chosen kind at creation (or let the generic items take any kind), and add a kind field to the inventory editor.

---

## Major

### M1. Exposure is scoped to the foe you attacked, not "a foe that can reach you"
- **Engine:** `combat.py:370-371` `state.expose(character.name, enemy.key …)`; `combat.py:76-83` consumes it only for that key.
- **App:** `app.js:427` "Exposed: the foe's next attack on them rolls an extra die", matching the engine.
- **Books and YAML:** `III.3_Combat.md:45` "If a foe can reach you, its next attack on you this exchange rolls an extra die"; `MM1:250`, MM5, Glossary; `facet.yaml:1006` `applies_when: partial_success_within_reach`.
- **Repro:** a PC attacks foe A and rolls 8. Foe B's attack on that PC gets no exposure die; foe A's does.
- `within_reach` defaults to true (`combat.py:270`) and `play.js` never sends it, so a ranged attacker is always exposed to the foe they shot.
- **Winner:** books + YAML. Expose the PC to every foe in reach and add a reach toggle. If the owner prefers the narrow reading, change III.3, MM1, MM5 and the Glossary instead.

### M2. Studied Foe and Anatomist can never fire in the app, and the engine reads them differently from the text
- **Unreachable:** nothing sets `enemy.studied`. It is declared (`enemy.py:61`), reset (`enemy.py:153`, `combat.py:117`) and read (`combat.py:316, 361`), but `grep studied software/app/api/websocket.py` finds nothing. `studied_foe` is `use: at_will`, so the sheet shows no Use button either. It is a starting talent of two presets, Investigator and Tactician.
- **Scope:** `facet.yaml:416-417` says "your **allies'** attacks on it are Easy"; `combat.py:315-317` eases every attacker, the studier included.
- **Duration:** the text says "Until the end of the **next** exchange"; `combat.py:113-117` clears the flag at the end of the current one.
- **Anatomist:** `facet.yaml:465` says "Your attacks, **and your allies' attacks**, on a foe you have studied ignore its armor". `combat.py:361` `ignore = enemy.studied and character.signature == "anatomist"` applies it only to the Anatomist, and only while the one-exchange flag lasts.
- **Winner:** facet.yaml. Add a `study` event that records who studied, keep the flag through the next exchange, exclude the studier from the Easy, and extend Anatomist to allies.

### M3. Warding Presence can never make an enemy roll Hard
- **Engine:** reads `state.warded` (`combat.py:66, 460-462`). No handler adds to it; `talent_use` (`websocket.py:~997-1010`) only ticks a counter.
- **Promise:** `facet.yaml:582-585` / II.4c "make that roll Hard".
- **Masked when wired:** `combat.py:462` `hard = defending or cover or warded`, so warding an ally who is already Defending or in cover does nothing (see M5).
- **Winner:** facet.yaml. `talent_use` for `warding_presence` should take a target ally and add them to `state.warded`.

### M4. Defend doesn't stop you attacking, and improved Sentinel's "attack at Hard" is never applied
- **Engine:** `combat.resolve_attack` (`combat.py:253-331`) never reads `state.defending`. `declare_defend` returns `can_attack` (`combat.py:136`), but nothing enforces it.
- **Repro:** after `declare_defend`, `resolve_attack` still resolves at Standard.
- **Rules:** `facet.yaml:122-124` (Sentinel normal: "Defend means you do not attack"; improved: "you may still attack, at Hard"); III.3 "Instead of attacking, you guard"; `tools.js:89` "you don't attack".
- **Winner:** facet.yaml. Refuse an attack from a defender unless they have improved Sentinel, and force Hard when they do.

### M5. How Hard and Easy sources combine is never ruled in the books; the engine hard-codes an answer
- **Hard sources on enemy attacks:** Defend (`III.3:85` "Every attack on you this exchange is **Hard**"), Intercept (`III.3:87`), cover (`III.3:43`), Warding Presence, and the Dust-fall curio (`tables.yaml` curios, "enemy attacks this exchange are Hard").
- **On PC attacks:** the level gap gives Hard or Very Hard (`III.3:97-102`); a stunt, a natural-2 opening and Studied Foe each make the attack "Easy".
- **Books:** only `III.1:38` defines "one step Easier/Harder". Defend, cover and Warding are written as *set* difficulties. No book says whether Defend + cover is Hard or Very Hard, whether Warding helps a Defending ally, or whether "Easy" beats a 6-level gap.
- **Engine:** makes all enemy-side sources non-stacking (`combat.py:462-463`) but treats openings and Studied Foe as a one-step shift (`combat.py:315-317`). Repro: a level-1 PC with a stunt opening against a level-5 foe attacks at **Standard**, not the Easy the text promises.
- **Winner:** needs an owner ruling (e.g. "set difficulties don't stack; take the hardest; Easy and Harder sources cancel step for step"). Then write it once in III.1 and compress it into MM5, and make the engine follow it. Right now the engine carries a rule no book states.

### M6. III.1 says 5d6 is the most dice a roll can have, but Sparks are uncapped and more d6 sources exist
- **III.1:** `III.1_Core_Resolution.md:52` "Three things add a die to a roll"; `:60` "A character who spends a Spark, takes Help and accepts Borrowed Trouble rolls 5d6 … That is the most one roll can be made into."
- **Uncapped Sparks:** `III.1:95` "spend as many Sparks as you like"; `facet.yaml:849` has no per-roll cap; `engine.py:146` and `websocket.py` `_extra_dice` accept 0–10 Sparks; `play.js:138` steps up to `me.sparks`.
- **Other d6 sources:** Inspiring (`facet.yaml:528`), Rallying Cry (`:625-626`) and the Lucky-tooth curio each add a d6 too.
- **Winner:** facet.yaml (no cap). Rewrite III.1:52/60. If one Spark per roll was intended, facet.yaml needs `max_per_roll: 1` and the engine and app must enforce it.

### M7. III.1 contradicts itself on Help
- `III.1:56` "One Help per roll." agrees with `facet.yaml:801` `max_per_roll: 1`, `Glossary:65`, and `engine.py:140-141`, which raises an error above 1.
- `III.1:149` says "use Help instead: the lead rolls, and each helper adds a die."
- **Winner:** facet.yaml. III.1:149 should say "one helper adds a die; the others …".

### M8. MM1's worked numbers contradict MM1's own level table and cards (four places)
- **`MM1:93`:** "a level 3 foe that hits deals 4". Table MM1–1 (`MM1:84`) and `facet.yaml:1034` give **6**.
- **`MM1:108`:** "Five Mooks at level 2 … deal 2 + 4 = 6 on a hit. When three of them are down, the survivors deal 2 + 1 = 3." Level 2 damage is 5, and the Mook's −1 makes 4 (`facet.yaml:1033, 1043`; the engine and Finding Aids agree). Correct: **8**, then **5**.
- **`MM1:288` (bridge example):** "a hard hit, 4 + 2 = 6 damage … It deals 4 … Zahna takes 3 and is on 3 of his 6 HP." The Toll Ogre card (`MM1:44-45`, `:130`) says damage 6. Correct: the hard hit deals 8 (Mordai takes 5); the hit deals 6 (Zahna takes 5 and is on 1).
- **`MM1:278`:** "His longsword deals 1d8". Mordai has Weapon Master (blades), so it is **d10** (`Quick_Start.md:81`, `III.3:200`, `Mordai.fof`).
- **Winner:** facet.yaml and the card. Rework the example arithmetic; the bridge example's outcome will shift.

### M9. The Val'loh crystal charges are 0 slots on the pregens, 1 slot in the core rule and in the app
- **Core rule:** `IV.2_Treasure.md:25` "A curio fills a slot like any item."
- **Pregens:** `adventures/oraga_night/characters/serane.fof:45-47`, plus `andra.fof` and `ilesse.fof` (all nine charge entries): `{…, slots: 0, curio: true}`.
- **App:** `software/facets/valloh/facet.yaml:215-258` gives the charge items no `slots`; `schema.py:546` defaults `slots` to 1. A charge added in the app therefore costs 1 slot.
- **Setting book:** `V2_Magic_of_Valloh.md:186` says the charges count against the curio limit, but says nothing about slots.
- **Winner:** IV.2. Set the pregens to `slots: 1`; every pregen still fits. If charges are meant to be slotless, say so in IV.2 and V2, and set `slots: 0` in the Val'loh YAML.

### M10. `spec/` is still the v0.1/v0.3 format, and README links it as the live spec
- `spec/README.md:9` "attributes, skills, techniques"; `spec/examples/character-example.fof:8, 33-49` (`fof_version: "0.1"`, nine attributes); `spec/types/character.md:35-36, 73` (skills with rank and marks, technique IDs); plus `ruleset.md`, `conflict-resolution.md`, `base-ruleset.fof`, `session.md` and `encounter-example.fof`.
- `character.py:989-992` **rejects** a file shaped like the spec example ("uses the retired v0.3 format").
- `README.md:69-71` and `:111` send readers to `spec/`.
- **Winner:** DESIGN §3.3/§3.4 and the engine. Rewrite `spec/` to v1.0, or mark it superseded and point to DESIGN §3.

### M11. README.md advertises retired mechanics, and its counts disagree
- **Retired mechanics:** `README.md:76` "TR 1 through 17"; `:127` "Threat Rating".
- **Chapter count:** `:107` and `:130` say "Mirror Master's Manual (5 chapters)"; MM6 makes six.
- **Test counts:** `:67` says 1103 tests and `:109` says 1029.
- **Winner:** the current tree. INV-27 doesn't scan README (see N21).

---

## Minor

### Rules and books

**m1. MM1 turns enemy naturals into forced results; facet.yaml and III.3 don't say so, but the engine does it**
- `MM1:248` "A natural 12 is a hard hit … A natural 2 is a miss"; `combat.py:480-486` forces the tier both ways.
- `facet.yaml:1013-1014`, `III.3:70-71` (Table III.3–3) and `MM5:62` give only the extra effect. `III.1:75` says the opposite for players ("A natural 2 does not force a failure").
- **Why it matters:** a level 9–10 Boss attacks at +5, so 1+1+5 = 7 would be a hit by the table.
- **Winner:** engine + MM1, if the asymmetry is intended. Add "a hard hit" / "a miss" to `facet.yaml` `natural_high/low`, Table III.3–3 and MM5, and say the asymmetry out loud. Otherwise fix the engine and MM1.

**m2. Stunt openings: duration and who may use them are unstated in books, set in the engine**
- `combat.py:113-117` expires an unused stunt at the end of the exchange, and `combat.py:315` lets the stunter use it.
- `III.3:43` says "an **ally's** next attack on it is Easy". `III.3:19` step 5 lists what expires ("Defend, Intercept, exposure and cover") and omits stunts.
- **Winner:** facet.yaml text ("an ally's"). Rule the duration, then add it to III.3 step 5 and MM5.

**m3. Usage die "starts at d8" in MM6 and MM2; items start at their own die in IV.1 and facet.yaml**
- `MM6_The_Toolbox.md:860` "It starts at d8"; `MM2_Session_Design.md:153` "a die that runs from d8 to d6 to d4".
- `IV.1:56-67, 83` and `facet.yaml:1099-1113`: only arrows start at d8; rations, torches, oil, the healer's kit and bandages start at d6.
- **Winner:** facet.yaml / IV.1.

**m4. MM6 and MM2 add a usage-die trigger that IV.1's body text lacks**
- `MM6:860` "and whenever the Pressure die turns up a cost"; `MM2:153`; `tables.yaml` `pressure_generic` 4.
- `IV.1:81` and `III.2:19` give only "after a scene of use / a leg of a journey".
- **Winner:** keep the trigger, but state it in IV.1:81, the body text.

**m5. Fatigue beyond your free slots is unruled**
- `II.3:96` "If every slot you have is full, you cannot cast at Significant or Major" (also Glossary:55, MM5:137, MM2:321).
- `IV.1:11`: with no free slot, "drop something to make room".
- A caster with one free slot casting Major (2 Fatigue, 3 in heavy armor), or a complication that adds Fatigue, falls in between.
- **Fix:** state the rule once in II.3, then check the engine against it. The engine requires only one free slot.

**m6. Silver Tongue (improved) skips a reaction band**
- `facet.yaml:505-506` / II.4c: "hostile to wary, wary to open."
- `tables.yaml:29-33`, MM5:145 and MM6 have five bands: Hostile → Wary → **Uncertain** → Open → Friendly. Empath improved uses "one step (hostile to wary)" consistently.
- **Winner:** tables.yaml. The fix is "wary to uncertain", in facet.yaml and II.4c. Here the YAML is the bug.

**m7. Improved Brawler adds nothing over the base talent, and the engine over-delivers**
- The base Brawler already makes a brawling hit a stunt, so "On a 10+ … take a stunt and +1d6 damage both" (`facet.yaml:171`, `II.4a:147`) equals base + pick one.
- The engine (`combat.py:247-249, 340-342`) gives improved Brawler two picks *plus* the automatic stunt: three effects.
- **Winner:** neither. The YAML needs a real improved effect, and the engine should follow it.

**m8. Brawling and improved Unarmored Discipline use the equipped weapon's die instead of the unarmed die**
- `combat.py:333-334` `die = character.weapon_die(ruleset)` regardless of `brawling`. `weapon_die` uses the unarmed die only with nothing equipped (`character.py:286-290`), and `_auto_equip` (`character.py:~1146`) equips the Brawler preset's light weapon.
- **Repro:** a Brawler preset's grapple deals d6.
- `facet.yaml:169-170` "you deal your unarmed die"; `:144` improved Unarmored Discipline "unarmed strikes deal d8". `play.js:172` labels the toggle "Brawling (bare hands)".
- **Winner:** facet.yaml. Use the unarmed die, with Unarmored Discipline applied, whenever `brawling` is set.

**m9. Cleave's base effect (leftover damage carries over) isn't implemented or reported**
- `apply_damage_to_enemy` (`combat.py:161-205`) clamps the target at 0 and discards the overkill. The result carries no leftover figure for the MM. Improved Cleave is implemented (`combat.py:365-366`).
- **Fix:** report the overkill on a kill, at minimum.

**m10. Improved Alchemist gets one brew per rest; the text says two**
- `facet.yaml:430` "Brew two draughts each night's rest".
- `schema.py:108-121` `uses_allowed` gives 2 only when the improved text starts with "Twice".
- **Fix:** add an `improved_effects: {uses: 2}` hook (keying on the text is fragile anyway), or reword the text to "Twice per rest".

**m11. Improved forms that add a limited-use ability to a passive talent get no tracker**
- Affected: Scout's Eye, Marksman, Athlete, Fast Hands, Loremaster, Investigator, Tinker, Linguist, Pathfinder, Silver Tongue, Empath (`facet.yaml:159, 195, 232, 245, 333, 359, 372, 395, 407, 505, 541`).
- `websocket.py:266-273` builds uses only for talents whose `use` is limited. `facet.yaml`'s header comment says "the app … tracks its uses".
- **Fix:** add an `improved_use` field to the YAML, and have the app read it.

**m12. Use pips always draw one pip**
- `play.js:96` `usePips(left, 1)`. Improved Lucky, Warding Presence and Hunch allow 2 (`uses_allowed(True) == 2`).

**m13. An improved talent's card replaces the base text**
- `play.js:97` shows `t.improved` in place of `t.text`. `II.4:99` says the improved form "keeps its first effect and adds the improved one".
- Example: an improved Tough's card drops "+4 HP".

**m14. Polymath skips `requires` and `choose`**
- `character.py:677-688, 748-749` don't check the extra talents' requirements.
- **Repro:** a non-caster took Wider Domain (`requires` a casting talent, `facet.yaml:317`), and Weapon Master arrived with `choice: None`. `validate_against_ruleset` also returns no error.
- `builder.js:357` offers Wider Domain to non-casters.

**m15. An off-Facet signature is allowed with a teacher; II.4 says your own list only**
- `character.py:609-624` `_menu_errors` treats a signature like a talent.
- `II.4:37, 101` "from your Facet's signature list"; `builder.js:351` offers only your own Facet's signatures.
- **Winner:** II.4.

**m16. The free rebuild is narrower in the app than II.4 promises**
- `II.4:166` "change your class, swap talents, even change Facet".
- `character.py:778-` `respec` swaps talents and magic within the current Facet only.
- **Winner:** II.4. Offer a full rebuild, or narrow the promise.

**m17. Captain's "up to two retainers" reads as a cap on something MM3 gives everyone without limit**
- `facet.yaml:571-575` / `II.4c:167`; `MM3:220-230` lets any party hire retainers with no count limit (morale 7).
- `combat.retainer_morale` (`combat.py:555`) has no caller.
- **Fix:** say in facet.yaml, II.4c and MM3 what a non-Captain's limit is.

**m18. Harm workings: Mook mobs and the level gap are unruled**
- A Major harm working, "2d8 to a group", drops exactly one Mook from a mob (`magic.py:236` → `drops=1`).
- `magic.plan_cast` never applies `level_gap_difficulty`. III.3 Table III.3–4 says "your attacks", and no book says whether a harmful working is an attack.
- **Fix:** needs an owner ruling, then record it in facet.yaml, II.3/III.3 and the engine.

**m19. Five Bestiary encounter labels disagree with MM1's danger bands**
- Bands at `MM1:195-200`: under 2 threats is a skirmish, up to 3 a real fight, up to 4.5 hard, more than that deadly.
- `B1:185` "one cow — a fair fight" = 1 (skirmish); `B4:64` "one level 3 standard — a fair fight" = 1; `B4:65` "two Waiting Ones — hard for a new party" = 2 (real fight); `B4:66` "one Waiting One — a fair fight" = 1; `B3:98` "one latchman and three latchlings — hard" = 3 (real fight).
- The vocabulary differs too ("fair fight" / "easy" vs skirmish, real fight, hard, deadly).
- **Winner:** MM1–4, which the app's read uses.

**m20. MM3's quick reference moves the faction turn**
- `MM3:249` "Between sessions, roll 2d6 for each faction"; the MM3 quick-ref block (`MM3:354-356`) files it under "BETWEEN ARCS".
- **Winner:** the body text.

**m21. The Glossary says foe armor is 0–2; MM1's override example uses armor 3**
- `Glossary.md:7`, `facet.yaml:1054` `armor_range: [0, 2]` vs `MM1:120` "the construct with armor 3".
- **Fix:** say "0–2, overrides aside", or drop the example.

### Module, setting and cast

**m22. Pregens marked as presets don't carry their preset's kit**
- `dassa.fof` (Guardian, `custom: false`) has a sword and light armor only (2 slots). `facet.yaml:689` gives the Guardian standard weapon, shield, heavy armor and rations.
- Printed at `03_Masks_and_Agendas.md:295`. `serane.fof` (Speaker) has no rations.
- **Fix:** give them the preset kit, or explain the deviation in the prose ("no one wears plate to a ball").

**m23. Dassa's Specialty is the generic template text**
- `dassa.fof` / `03_Masks_and_Agendas.md:299` "…from **your** service years" (verbatim `facet.yaml:1159-1160`). Every other pregen has a personalised Specialty.

**m24. The stat a gift is cast with is inconsistent across surfaces**
- `II.5_Lineage.md:47` "A gift is always cast with **Soul**"; `magic.py:22-23` hard-codes `GIFT_STAT = "soul"`. `facet.yaml` `magic` has no such field, so the rule is missing from the source of truth.
- The Val'loh books (`V1:5`, `V2:156-168`) and the module (`03:10-31`) never state the stat. `references/valloh/INVENTIONS_FOR_REVIEW.md` §3 says "the intuitive-tradition rule is gone".
- **Fix:** add `magic.lineage_gift_stat: soul` to facet.yaml and a clause to V2, and correct the ledger.

**m25. V1 claims the II.5 entry format but prints extra fields**
- `V1_Lineages.md:7` "Entries follow the format in Chapter II.5", but V1 adds **Gift** and **Heritage** fields.
- II.5 (`:11-19`) has no Heritage field; the word appears nowhere in `player_handbook/`.
- **Fix:** owner's call. Either II.5 gains optional setting fields, or V1 drops the claim.

**m26. The Overture says stat lines print "six TWISTS"; the generated ones don't**
- `01_Overture.md:94`. Every block in `09_Scene_Cards.md` (e.g. `:35-47`) prints Wants, Special, When bloodied, Tells, Breaks and Nastier, but no Twists.
- **Fix:** the sentence, or the generator.

**m27. `references/phb-examples.md`, the vignette guide CLAUDE.md sends writers to, describes v0.3 scenes**
- `:31` "Zahna identifies the working (**Knowledge**, full success); Mordai forces the hinges (**Athletics vs. Hard**…)". The PHB (`II.3_Magic.md:168-170`) now has Mind and Body at Hard.
- `:32` Mordai "**is Broken**". `III.2_Adventuring.md:142-158` now has 0 HP, Hold On 6− and the death choice.
- **Winner:** the PHB. The shoulder canon line stays.

---

## Canon (Minor unless the owner rules otherwise)

**K1. The Artificers' Guild is still asserted as fact in two live files; its canon status is an open owner ruling**
- `characters/Zahna.fof:28, 34, 53` "Formally apprenticed at the Thornwall Artificers' Guild … the Guild dissolved".
- `enemies/archive_guardian.fof:40` "commissioned by the Thornwall city government through the Artificers' Guild". This is a **Bestiary card**, which is setting-agnostic by rule (CLAUDE.md); its prose (`B3_The_Made.md:141`) was already genericised to "a guild that has since dissolved".
- `references/phb-examples.md:33` records the ruling as open. Both lines predate the overhaul.
- **Fix:** genericise `archive_guardian.fof` now. Leave Zahna.fof pending the ruling.

**K2. Zahna's signature workings are flagged for owner review, but the PHB states them as fact**
- `characters/Zahna.fof` "# Owner review: the two signature workings are new".
- `II.3_Magic.md:114` "The other casters in the city know Zahna as the one who seals things"; III.3 "That's your signature working, the sealing glyph".
- **Fix:** ask the owner. No text change until it is ruled.

**K3. V0's "four people in five … born without a gift" inverts the Orthaen rate**
- `V0_Ten_Things.md:35` vs `V0:29` and V1 (four in five Orthaen *carry* a gift). This predates the overhaul; ask the owner.

**K4. v0.1 spec examples carry cast lore that was never ruled**
- `spec/examples/session-example.fof:41` "Zahna's old classmate from the University", with an NPC named "Silt". This goes with M10.

---

## Nit

- **N1.** `Glossary.md:97` sends enemy naturals to Chapter III.1; they are in III.3 (Table III.3–3).
- **N2.** `Appendix_Magic_Domains.md:25, 216`: the prismatic column header reads "yes".
- **N3.** `Appendix_Character_Sheet.md:83-99` has 13 slot rows. The maximum is 15 (Body +3 plus Iron Lungs).
- **N4.** `Table_of_Contents.md:29` "trinkets, curios and relics" vs `IV.2:3` "It comes in four kinds" (coin first).
- **N5.** `Quick_Start.md:63` "heavy armor fills two" leaves out heavy weapons. This is harmless, since no preset carries one.
- **N6.** `II.4a:269` says Unarmored Discipline spares a fighter from choosing between "being hard to hit" and being quiet. Armor reduces damage, not the chance to be hit; "hard to hurt" would fix it.
- **N7.** Mordai's knack is "City Watch" in `MM2:454` and DESIGN §3.3/§5, but "City Watch Veteran" in `Mordai.fof:26` and `facet.yaml:1158`. DESIGN is the stale side; MM2 may keep the short form (II.6 allows it).
- **N8.** `06_Aftermath.md:120`: level 2 gives "one new talent", which leaves out the improve-a-talent option.
- **N9.** `08_Handouts.md:66, 90, 108, 126, 148, 159`: Chapter VIII's tables are numbered IX–n.
- **N10.** `bought_captain.fof:35-36` says the "**third** clause"; every other surface says the Second Clause.
- **N11.** The Captain is "it" on the card (`09_Scene_Cards.md:166-178`) and "he" in the prose (`:181, 185`; `07_Cast_of_the_Ball.md:444-458`). `09:189` says "in front of the Sergeants", but only one Sergeant is at the gate.
- **N12.** `V1_Lineages.md:133` "*Most, in specialties carry it.*" is ungrammatical; it is generated from `gift_rate`.
- **N13.** The Val'loh books (`V0:33`, `V2:152-178`) name only gifts and study (Thaumaturgy). Invocation is never mentioned, though the module offers it (`03:12`, `06:139`).
- **N14.** III.3's guardian vignette rewrites the card's WHEN BLOODIED line ("Reduced Mode", `archive_guardian.fof`). The vignette announces only a numbers override. "Reduced Mode" is also v0.3 wording.
- **N15.** After any `level_up`, `warnings()` reports a false stored-vs-computed max-HP mismatch, because `hp_max_stored` isn't updated (`character.py:762-766` vs `909-913`).
- **N16.** Rule numbers are hard-coded outside facet.yaml:
  - danger-read points and bands: `encounter.py:15-17, 355-362`
  - oracle odds and the hoard formula: `toolbox.py:15, 151`
  - the gift stat: `magic.py:23`
  - the "+2/+1" creation stats: `builder.js:70, 86-87`
  - Spark pips fixed at 3: `play.js:291, 491`, and "Sparks are back to three": `app.js:391`
  - the Hold On banner: `play.js:36`, which also leaves out Tough improved
- **N17.** Talent hooks the UI can't reach:
  - The Morale button sends no `bonus`, so improved Dread Presence's +2 can't apply (`play.js:471, 573`).
  - An MM-clicked Tend passes `tender=None`, so Field Surgeon never applies (`websocket.py:~881-886`).
  - `death_choice` is accepted at any time while dying, not only when the scene ends untended.
- **N18.** `docs/TODO.md` is live (CLAUDE.md cites T6), but open items T2, T3, T7 and T14 concern retired mechanics. Close them as obsoleted by L2/L3/L7/L9.
- **N19.** Review ledgers in `references/` present v0.3 mechanics as pending proposals:
  - `oraga_night/INVENTIONS_FOR_REVIEW.md:68, 69, 86, 99, 160` (Resolve, Tier 2, Spirit, Facet level 1, secondary skill)
  - `valloh/INVENTIONS_FOR_REVIEW.md:8, 110, 115, 118`
  - `[private canon notes]` (TR)
  - `WORKING_NOTES.md:182-185`

  Add a v1 translation for each open item.
- **N20.** Smaller v0.3 residue:
  - eight `enemies/*.fof:10` keep a "# v0.3: Named … rating N" comment
  - `Mordai.fof:36` "Combat technique developed…"
  - `software/README.md:325-335` project tree (TR budget, Threat Rating, budget tab, "613 tests"; no combat/magic/toolbox)
  - docstrings in `tools/build_index.py:11, 63, 74, 85` and `build_table_register.py:14` (Posture, Tier, Resolve)
- **N21.** Hardening INV-27:
  - compile its patterns with `re.I`
  - add `\bAthletics\b`, bare `\bTR\b`, `Broken (with|is)`, `Named (NPC|enem)` and `skill rank`
  - scan `README.md`, `software/README.md`, `spec/` and `references/phb-examples.md`

  Also consider an invariant that every talent with `effects` has at least one engine test driving it from a *preset-built* character. C1 would have been caught that way.

---

## Suggested order of work
1. C1, M1–M4 (engine/app: the talents and combat rules the books promise but the app never delivers).
2. M5 and m1/m2/m5/m18 need **owner rulings** (difficulty stacking, enemy naturals, stunt duration, Fatigue overflow, harm vs mobs and the level gap). Rule them together, since they are all one "how difficulty and effects combine" question.
3. M6–M8 (III.1 and MM1 text), M9 (pregen slots).
4. M10–M11 and the N18–N21 residue (spec, README, references), then INV-27 hardening.
5. K1–K4 go to the owner.
