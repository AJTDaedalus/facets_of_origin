# Hands-on UX Review: Lean Facets v1.0 table app

Branch `feat/lean-facets` (head `ec370f7`), reviewed 2026-09-26. I drove the app in headless Chromium through Playwright against a live `run.py`, with an MM and three players (Zahna at 1440px, Mordai at 1280px, Zulnut at 390px mobile). The session was realistic and covered:

- first-run setup, a session and invites
- three characters: a preset Thaumaturge caster, a preset Warrior, and a custom Body class (Wandering Disciple) built on a phone; after a server restart, a second table with a custom Soul caster class ("Hedge Priest", Invocation) and a preset Guardian
- a monster card, the Bestiary load, a Mook mob, an Elite and a Boss
- two fights covering telegraphs, all three attack bands with 10+ picks, enemy attacks in the open, Intercept, casting until the slots ran out, 0 HP → Wound → Hold On → dying → tended, morale and Bloodied, and the Toolbox with reveals
- end of session, Grant level, and level-ups 1→4 (the level-3 signature and the level-4 stat)
- a breather and a night's rest, a `.fof` export, reloads mid-fight, a server restart, keyboard and contrast probes, and mobile layouts for both roles

Screenshots are in `/tmp/claude-0/-root-facets-of-origin/55fd913e-d3f6-4135-aef9-fb4a4af0ef9d/scratchpad/shots/`, written below as `shots/NN_name.png`. The throwaway scripts sit next to that folder.

**Overall.** The core loop works, and in places it is genuinely nicer than paper:

- The wizard is clear.
- Foes roll in the open with readable dice.
- Exposure, level gap, armor and Intercept redirection are all computed.
- Players never receive foe HP or the MM's notes over the socket.
- There were no JavaScript exceptions during the whole run. Console noise was only expected 401/422 responses and a missing favicon.

Where it falls short of "easier than paper":

- **Persistence and auth.** Nothing survives a server restart, and a player's seat lives in one browser tab.
- **Exchange bookkeeping.** The app doesn't track who has acted, who is defending, or how many attacks a foe has made. Those are exactly the things paper forces the MM to track by hand.
- **Mechanical text the app shows but never applies.** Examples are "take 1 damage" and "take 1 more Fatigue", and there is no control anywhere to apply them by hand.
- **Mobile players can miss the moments that matter.** The action panel and the feed sit far below the sheet.

Counts: **2 Critical · 12 Major · 19 Minor · 7 Nit**. No retired v0.3 vocabulary was found in the UI or the client ruleset. I searched for Resolve, Endurance, Technique, posture, Strike, Staggered/Winded, readied intents, Press, GM and DM.

---

## Critical

### C1. A player's own `.fof` export contains the MM's private notes
- **Steps:**
  1. As the MM, open Tools → Notes, pick Zahna, write "SECRET: Zahna's mentor is the villain" in *Mirror Master notes (only you see these)*, and save.
  2. As Zahna, open Build → **Download .fof**.
- **Happened:** the file contains `notes_mm: 'SECRET: Zahna''s mentor is the villain'`. The socket view strips `notes_mm` correctly, so the leak is only the REST export.
- **Expected:** a player's export never carries `notes_mm`. The label promises "only you see these".
- **Evidence:** `scratchpad/zahna_export.fof`, line 83.
- **Fix:** in `export_character` (`app/api/routes/character.py:188`), drop `notes_mm` when the caller isn't the MM. Add a test.

### C2. A server restart wipes the table, and every client then loops on an error forever
- **Steps:** run a session with characters, library cards, foes on the tracker and a clock. Restart `run.py`.
- **Happened:**
  - Everything held in memory is gone: sessions, the enemy library, tracker, clocks and combat state. So is **the MM password**, because `_mm_password_hash` lives in memory in `routes/session.py`.
  - The MM's sign-in now answers "Invalid password." with no hint that setup has reset (`shots/64_login_after_restart.png`).
  - Anyone who reaches the server can now run *First run setup* and become the MM.
  - Each connected client reconnects every 3 s and gets a new "Session not found." toast, forever (`shots/63_after_server_restart_player.png`).
  - The characters' `.fof` files are still on disk under `data/sessions/<id>/characters/`, but they belong to a session that no longer exists. The UI has no way to import them, although `POST /api/characters/upload` exists.
  - Players' invite links were single-use, so nobody can rejoin until the MM makes a new session and new links.
- **Expected:** a restart (a crash, a laptop lid, an update) is invisible to the table, or at worst the MM signs back in and everything is still there.
- **Fix:**
  - Persist the MM password hash, sessions, the library, the tracker and clocks under `DATA_DIR`, and reload them at startup.
  - Stop reconnecting after a fatal "Session not found": show a full-screen "This table has closed. Ask your MM for a new link." message.
  - Add an Import `.fof` button (Build → Characters for the MM, and the empty Build screen for a player).

---

## Major

### M1. A 10+ Stunt's "opening" is spent by the attacker who made it
- **Steps:** Mordai attacks Glassback Bull, rolls 10+ and picks **Stunt**, then attacks the Bull again.
- **Happened:** the second attack reads "Easy +1 · Used an opening: one step Easier". Mordai chained stunt → Easy → stunt → Easy all exchange (log attacks 1, 3, 5 and 7).
- **Expected:** III.3 says the stunt makes "an **ally's** next attack on it" Easy.
- **Evidence:** `shots/38_after_attacks.png`.
- **Fix:** record who created the opening and skip it for that attacker. Show the opening on the player-facing foe row as well ("Opening: next ally attack is Easy").

### M2. Intercept keeps pulling attacks onto an ally who is already down
- **Steps:**
  1. Zulnut Intercepts for Zahna.
  2. The Glassback Bull drops Zulnut to 0 HP (Wound, must Hold On).
  3. The Chalk Wraith attacks Zahna, three times.
- **Happened:** every attack reads "Chalk Wraith attacks Zulnut (aimed at Zahna)… Zulnut intercepts". The unconscious Zulnut keeps taking the hits and Zahna is untouchable.
- **Expected:** Defend and Intercept end when the defender drops (0 HP, out, or dying).
- **Evidence:** `shots/43_mm_after_enemy_attacks.png`.
- **Fix:** clear the defender's Defend/Intercept in `_drop_to_zero`, or skip redirection when the interceptor's status isn't `ok`.

### M3. The Harm toggle and cast target are sticky, so later non-harmful workings silently hurt a foe
- **Steps:**
  1. Zahna casts a Significant working with **Harm** on the Chalk Wraith.
  2. Later she casts three Significant "seal door" workings with her signature working and doesn't look at the toggle.
- **Happened:** each one was sent as `harm: seal door N` and dealt 3 damage to the Wraith (22 → 13 HP). The toggle and the target select stayed on from the first cast.
- **Expected:** Harm is a per-cast choice and resets after each cast. The app shouldn't rewrite the player's intent text.
- **Evidence:** `shots/40_cast_form.png`; feed "Zahna casts: harm: seal door 0 … harm 3 = 3".
- **Fix:** in `playerAction('cast')`, reset `ui.harm`, `ui.castTarget` and `ui.group`. Show the target inline on the Cast button ("Cast (harm → Chalk Wraith)"). Send `harm: true` as a field instead of prefixing the intent.

### M4. Costs printed in the feed are never applied, and there is no control to apply them
- **Steps:**
  1. A cast rolls 6−; the mishap reads "Drained: it fizzles, and you take 1 more Fatigue."
  2. Another cast rolls 7–9; Zahna chooses "It bites back: take 1 damage."
- **Happened:** Fatigue stayed at 1 and HP stayed at 6. Nothing applies the text, and nobody can apply it by hand: the MM's party card has Hurt, Heal and Wound but **no Fatigue control**, and neither role can change coin, Sparks spent or items consumed.
- **Also affected:** Backlash (1d6), Silenced, Consumed and Changed in `magic_mishaps` are all text only.
- **Expected:** the wizard promises "The app keeps the numbers straight". Structured costs should apply themselves, and anything else should get a one-tap apply control.
- **Evidence:** `shots/49_cast_blocked.png`, and the feed lines for the Drained mishap and the "bites back" cost.
- **Fix:**
  - Tag table entries with an optional machine effect (`{damage: 1}`, `{fatigue: 1}`, `{damage_die: 6}`) and apply it when the entry is chosen or rolled.
  - Add ± Fatigue to the MM's party card and ± coin to the inventory editor.

### M5. No action economy: nothing tracks who has acted or how many attacks a foe has left
- **Steps:**
  1. In exchange 1, Mordai clicks Attack eight times.
  2. The MM clicks Attack three times for the Chalk Wraith, which has *Attacks 2*.
- **Happened:** all of it resolved. Mordai removed three Mooks and chained openings in one exchange, and the Elite made a third attack.
- **Expected:** III.3 says "everyone acts once" and elites and bosses "attack twice". The app doesn't need to forbid extra actions (the MM rules), but it should show them.
- **Fix:**
  - Add per-exchange "acted" chips on the MM's party cards (✓ once a PC has attacked, cast, defended or rolled).
  - Add an "attacks used 1/2" counter on each foe card that resets at End exchange.
  - When a PC acts twice, show a soft warning to that player ("You've already acted this exchange. Ask the MM.").

### M6. The MM can't see Defend, Intercept, exposure or cover status
- **Steps:** Zulnut Intercepts for Zahna, and Mordai is Exposed after a 7–9. Look at the MM's tracker and party.
- **Happened:** neither appears anywhere on the MM's cards; each exists only as a feed line that scrolls away. When the MM decides who to attack, they can't tell who is defending or covered.
- **Expected:** step 3 of the exchange ("foes roll") needs exactly this information.
- **Fix:** add status chips on the MM's party cards (Defending, Intercepting → Zahna, Exposed, Covered by X) and on the players' party panel. Clear them at End exchange.

### M7. A pending 10+ pick is lost on reload, and the player is soft-locked
- **Steps:**
  1. Mordai rolls 10+ and the pick modal opens.
  2. He reloads the tab, as a phone does when it swaps apps.
  3. He tries to attack again.
- **Happened:** there is no banner and no modal, and the only feedback is "Pick your 10+ option first." He can't reach the picker until the MM ends the exchange.
- **Evidence:** `shots/61_mordai_reload_pending.png`.
- **Expected:** the pending choice survives a reconnect.
- **Fix:** include the pending attack option and the pending casting cost in the join-time `state`, and restore `state.pendingAttack` and `state.pendingCost` from it.

### M8. A reload wipes the MM's Spark calls, Toolbox results and the readable feed
- **Steps:**
  1. With a peer "Spark?" call waiting and seven private Toolbox results, the MM reloads.
  2. For comparison, look at a player's feed after a reload.
- **Happened:**
  - The Spark calls go from 1 to 0 and the Toolbox results from 7 to 0.
  - The feed is rebuilt from the last 20 rolls only, as terse lines ("Zahna cast: harm: seal door 0 3 5 11 Full success"). Telegraphs, damage, Bloodied, morale and "is choosing…" are all gone.
  - A player's reload also drops the "Things went wrong / Claim a Graceful Fail" banner.
- **Evidence:** `shots/60_mm_after_reload.png`.
- **Fix:** keep Spark nominations, unrevealed Toolbox results and a rendered feed log (the last 150 entries) on the server, and send them in `state`.

### M9. "Show the table at once" does nothing for most Toolbox buttons
- **Steps:** turn on **Show the table at once**, then click **Trinket** (or Fight cost, Explore cost, Social cost, MM move, Curio or Relic).
- **Happened:** the result stays private (it still has a Reveal button) and players see nothing. `wireMMPlay` captures `const reveal = !!ui.revealNow` once, when the panel is wired, and toggling the chip doesn't re-wire. The `data-tb` buttons read it live and work.
- **Fix:** read `ui.revealNow` inside the click handler for `[data-table]`.

### M10. A player's seat lives in one browser tab
- **Steps:** a player joins through their single-use invite, then closes the tab, or opens the app in a second tab, or their phone browser discards the tab.
- **Happened:** the token is kept in `sessionStorage` only, so a new tab lands on the MM sign-in screen, and the invite is spent ("Invite link has already been used.", `shots/08_reused_invite.png`). Found by reading `app.js` boot and `storeAuth` and confirmed with the reused-invite test.
- **Expected:** a player can rejoin all evening, and next week, without the MM.
- **Fix:** store the player token in `localStorage`. Make invites re-usable by the same player, or add a "rejoin as <name>" link on the MM's party card.

### M11. Going down isn't announced, and on a phone it happens off-screen
- **Steps:** on the phone (390px), Zulnut scrolls down to his slots or actions. The Bull drops him to 0.
- **Happened:** there is no toast, vibration or scroll. The only signal is the "You're at 0 HP / Roll Hold On" banner at the very top of the page. The same is true for "You are dying", a level-up, and a 7–9 cost choice (which does open a modal, but only for the caster).
- **Also:** on a phone the action panel sits below the whole sheet (talents, slots, usage dice), about 1,300px down, and the feed is below that. A player can't see the result of their own roll without scrolling.
- **Evidence:** `shots/21_mobile_sheet.png`, `shots/44_mobile_hold_on.png`, `shots/45_mobile_hold_on_banner.png`, `shots/46_mobile_dying.png`.
- **Fix:**
  - On narrow screens, put the banners and actions first and the sheet second, or use a sticky bottom action bar.
  - Make the feed a pull-up drawer showing the latest entry.
  - `notify()` and scroll to the banner on `must_hold_on`, `dying` and `level_up_ready`.

### M12. Features the rules promise that the UI doesn't expose
- **Coin and loot.** A Hoard rolls "180 coin; curio: Climber's chalk". There is no way to give coin or the curio to anyone: no coin field exists in Inventory, and the sheet shows coin read-only.
- **Respec.** The rules make rebuilding free before level 3 (`respec_until_level: 3`) and the server has a `respec` handler, but there is no button. A new player who regrets a pick at level 1 is stuck.
- **Character import.** `POST /api/characters/upload` exists but has no UI (see C2).
- **Encounters.** The REST routes for encounters exist, but nothing lets an MM save "3 thugs + the sergeant" as a set and spawn it in one click.
- **Spending a Spark outside a roll.** The server has `spend_spark`, but the UI can only spend Sparks as extra dice.
- **Fix:** add a coin ± and a "give item" action (MM → character), a Rebuild button on Build while `can_respec` is true, and Import `.fof`. Decide whether encounters stay.

---

## Minor

1. **Raw validation error on an empty sign-in.** Clicking Sign in with no password shows "String should have at least 1 character" (the pydantic message). Say "Enter your password." instead.
2. **No hint that setup is needed.** Signing in before the first-run setup (or after C2) says only "Invalid password." (`shots/02_login_before_setup.png`). When no password is set, say "No MM password yet. Use First run setup."
3. **The setup screen has no Back button** to return to sign-in.
4. **Invites overwrite each other.** Each new invite replaces the previous link, and the name field isn't cleared (`shots/04_dashboard_invites.png`). An MM inviting three players must copy each link before making the next. Keep a list of outstanding invites with Copy buttons.
5. **An enemy attack's target defaults to the first PC, not the telegraphed one.** The telegraph is free text ("swing clubs at Mordai") while the attack target select still shows "Zahna" (`shots/33_mm_tracker.png`). Put a target select in the telegraph and pre-select it for the attack.
6. **A level-up error clears the talent pick.** On level 4 without a stat, the error "Level 4 raises a stat: name body, mind or soul." appears, and the chosen talent is deselected, because `wireLevelUp` deletes `ui.lvTalent` before the server answers. Clear it only on `level_up_done`, and use the stat names (Body/Mind/Soul) in the message.
7. **Ending the fight leaves every foe on the tracker,** including defeated and broken ones. Add "Clear the tracker" or ask on End the fight.
8. **Fearless foes still offer Morale and Mark broken.** The Archive Guardian has morale 12 but shows both buttons (`shots/70_mm_mobile_tracker.png`).
9. **No morale nudges.** The rules list the triggers (first falls, half down, leader down, alone and hurt), and the app knows when these happen, but it never suggests a check.
10. **Morale results and card lines reach the players.** The feed shows "Harbor Thug 6 6 12 vs 5 — it breaks. Runs, loudly… takes the nearest portable cargo along". That is the foe's morale number and the card's BREAKS line. An attack on a foe crossing half HP likewise prints its WHEN BLOODIED line. The card is otherwise MM-private. Consider showing players only "it breaks" or "it holds" and a telegraph-style description.
11. **Borrowed Trouble doesn't prompt the MM.** The feed says only "extra dice: Borrowed Trouble"; there is no nudge to name the complication.
12. **Help doesn't involve the helper.** The ally named isn't asked and doesn't lose their action, and "shares the cost" isn't tracked.
13. **Being offline is a 10px dot with a tooltip.** Anything attempted while offline warns, but also clears what the player typed (`resetExtra()`, `ui.desc = ''` run anyway). Show an offline bar and keep the input.
14. **An attack outside a fight** is allowed and shows "Exposed: the foe's next attack…" with no fight running.
15. **The death choice is offered immediately.** The dying player gets "Heroic final action" and "Live, with a Scar" as soon as they're dying, before anyone could tend them. The rule says "if no one tends you before the scene ends". A confirm dialog exists. Consider offering the choice only when the MM ends the scene, and warning the MM on New scene if anyone is still dying.
16. **Keyboard and screen-reader gaps.**
    - The extra-dice toggles (knack, Help, Borrowed Trouble) and the MM's "Show the table at once" are `<span>`s. They can't be reached with Tab, so a keyboard user can't add a knack or Help. The stat cards are clickable `<div>`s.
    - The stepper's − and + have no label.
    - Tabs lack `aria-selected` and segmented buttons lack `aria-pressed`.
    - The connection dot has no text alternative.
    - 13 MM inputs have no associated label (spawn select, HP boxes, oracle, clocks and others).
    - Focus rings are present and visible (`shots/66_focus_ring.png`).
    - Fix: make the toggles `<button aria-pressed>` and use `<label for>` or `aria-label`.
17. **Low-contrast text.** `.label .dim` measures 2.93:1 and the "free" slot label 3.15:1, both below WCAG AA's 4.5:1. The muted text elsewhere is fine at about 5.8:1.
18. **The mobile header takes about 130px** on two rows, with Leave on its own row (`shots/07_mobile_wizard_start.png`).
19. **Cast-preview chatter.** The Cast tab sends a `cast_preview` on every re-render, so each enemy or character update triggers a round-trip for every open Cast tab. It's harmless but noisy. Send it only when a cast input changes.

## Nit

1. Doubled periods in generated text: "proud of how it happened.. Wants To break a bad habit, with help..", and "Wound: Rung head. … casting.. Roll Hold On."
2. The telegraph renders as "is about to: lowers its horns at Zulnut", which is ungrammatical with the "Telegraph: about to…" placeholder. Render it as "Glassback Bull: lowers its horns at Zulnut".
3. The feed shows "Zahna casts: harm: a glyph of cutting light", with the auto-prefixed "harm:".
4. The card error reads "chalk_wraith: a card has exactly six twists, not 5.", using the slug instead of the card name.
5. The Library's Mook count box (default 4) has no label; the Play tracker's count box is labelled only by a tooltip.
6. `/favicon.ico` returns 404.
7. The Major scope button (min level 3) looks almost identical when disabled at level 1 (`shots/40_cast_form.png`). Add "(level 3)" to the label.

---

## Rules vs UI coverage (Quick Start and III.3)

| Rule | In the app? |
|---|---|
| Telegraph → act → foes roll → narrate → end exchange | Yes, as a hint line and buttons. Not tracked (M5, M6). |
| Attack 10+ pick / 7–9 exposed / 6− miss | Yes. The stunt opening is wrong (M1). |
| Enemy 10+ +2 damage, natural 12, natural 2 opening, exposure die | Yes, clearly shown. |
| Armor, level gap Hard/Very Hard | Yes, automatic. |
| Mook drops on a 7+; mobs +1 per extra (max +4) | Yes. |
| Elite and Boss attack twice; Boss phase at Bloodied | Stats and "Phase 2" chip shown; attack count not tracked (M5). |
| Defend / Intercept | Yes. Not visible to the MM (M6), and persists past 0 HP (M2). |
| Cover (10+ pick) | Pickable; status not visible anywhere (M6). |
| Morale, fearless | Yes. No trigger nudges (Minor 9), and buttons still shown on fearless foes (Minor 8). |
| Magic scopes, Fatigue in slots, signature one step Easier | Yes, with a good live cost preview. Costs and mishaps aren't applied (M4). |
| 0 HP → Wound → Hold On → dying → tend → Scar or heroic end | Works end to end. Weak on mobile (M11). |
| Help, Sparks, Borrowed Trouble, Graceful Fail, peer "Spark?", act break | Yes. Nominations are lost on reload (M8). |
| Breather and night's rest | Yes (night: full HP, Fatigue cleared, one Wound healed). |
| Levels, signature at 3, stat at 4/8, damage bonus, pacing prompt | Yes. |
| Coin, loot, respec before level 3 | Missing (M12). |

---

## Five highest-leverage UX improvements

1. **Make the table durable.** Persist sessions, the library, the tracker, clocks and the MM password. Keep player tokens in `localStorage` with re-usable rejoin links. Import `.fof`. Stop the reconnect-toast loop. Right now one restart or one closed tab can end the evening (C2, M10).
2. **An exchange board on the MM screen.** Per-PC chips for acted, defending, intercepting, exposed and covered. Per-foe "attacks 1/2" and "telegraphed at X", with the attack target pre-filled from the telegraph. Morale nudges. This is the bookkeeping paper makes the MM do by hand (M5, M6, Minor 5, Minor 9).
3. **Apply what the app announces.** Machine-readable effects on costs and mishaps. ± Fatigue, coin and item-transfer controls for the MM. "Give hoard to…" on Toolbox results (M4, M12).
4. **A phone-first player layout.** Banners and the action panel on top (or a sticky action bar), the feed as a drawer, and toasts plus auto-scroll for 0 HP, dying, level-up and your turn to pick (M11).
5. **Reset per-action state, and restore pending state on reconnect.** Reset Harm, target and extra dice after every action. Restore the 10+ pick, casting costs, Spark calls and the Toolbox results from the server. Fix the stale "Show at once" toggle. This removes the silent wrong-damage and soft-lock bugs (M3, M7, M8, M9).
