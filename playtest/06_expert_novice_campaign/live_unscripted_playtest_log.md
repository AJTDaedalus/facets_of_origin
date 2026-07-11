# Live Unscripted Playtest Log: Hearth-Core Vault

This document records the live, unscripted playtest session run on **July 10, 2026**. 
Instead of a pre-written script, all rolls, postures, combat states, and rule validations were executed and resolved in real-time against the active game server on port `8010` (Session ID: `89fdc5c8-5da8-4c13-9ccf-1a055a1559d9`).

---

## The Cast (5 Agents)
1.  **Cyrus (Expert MM):** Hosting the session, narrating the environment, and setting stakes.
2.  **Arthur (Novice MM):** Observing, assisting with rules-math, and validating conditions.
3.  **Valerie (Expert Player):** Playing **Alaric of the Iron Gate** (Body Guardian).
4.  **Billy (Novice Player):** Playing **Pippa Swift** (Dex/Luck Urchin).
5.  **Toby (Novice Player):** Playing **Thorne Woodcroft** (Soul Resonator).
6.  **Antigravity (AI Assistant):** Interfacing with the server API and WebSocket routes.

---

## Act I: The Rusted Gate (Investigation Phase)

**Cyrus (Expert MM):**
> "Your small rowboat bumps against the damp stone steps of the Sunken Spire. A massive rusted bronze gate blocks the entry channel, secured by an intricate Weaver lock mechanism. Watery moss clings to the ancient gears. How do you inspect it?"

**Valerie (Expert Player - Alaric):**
> "I want to get up close and inspect the mechanical cylinder. Since I served in the City Watch, I want to see if I can figure out the tumbler order. I'll make a standard **Intelligence** roll."

### [Server Resolution: Alaric's Intelligence Check]
*   **Action:** Intelligence roll (Standard difficulty, +0 modifier).
*   **Server Roll:** 2d6 [3, 4] + 0 = **7**
*   **Server Outcome:** `partial_success` (Success with Cost).

**Cyrus (Expert MM):**
> "Alaric, you figure out the mechanical tumbler alignment, but you feel the cylinder vibrating under high pressure. If you release the valve, it's going to backfire. You have a choice: either brace it with your bare hands (taking a **Scorched** dexterity condition but opening it silently) or step back and let it vent (making a loud bang that will echo into the spire)."

**Valerie (Expert Player - Alaric):**
> "I'll brace it. I'm a Guardian; I can take the heat to keep the group quiet. I press my gauntlets against the cylinder and twist."

**Cyrus (Expert MM):**
> "With a low hiss of steam, Alaric's hands are singed (Alaric gains the **Scorched** condition, -1 to actions requiring manual dexterity), but the gate clicks open and swings backward. Beyond it lies the Flooded Scriptorium."

---

## Act II: Flooded Scriptorium (Combat Exchange 1)

**Cyrus (Expert MM):**
> "As you drift into the shallow water of the scriptorium, two **Water-Logged Sentinels (TR 1 Mooks)** rise from the weeds. Their mechanical eyes flare blue. Combat is initiated! Declare your postures."

**Valerie (Expert Player - Alaric):**
> "I declare **Defensive** posture. I'll brace my shield to intercept any attacks targeting Pippa."

**Billy (Novice Player - Pippa):**
> "I choose **Aggressive** posture! I draw my dual daggers and sprint forward!"

### [Server Resolution: Posture Reveal]
*   **Server Broadcast:** `REVEALED: {'Alaric of the Iron Gate': 'defensive', 'Pippa Swift': 'aggressive'}`
*   *Mechanics:* Alaric's Defensive posture reduces his reaction costs by 1 Endurance. Pippa's Aggressive posture gives her a +1 bonus to strikes but increases her reaction costs by 1.

**Billy (Novice Player - Pippa):**
> "I slide under the arms of the first sentinel and slash at its leg joints! I roll **Dexterity** + **Combat**!"

### [Server Resolution: Pippa's Strike]
*   **Action:** Strike roll (Standard difficulty, Dexterity + Combat + Aggressive = +3 modifier).
*   **Server Roll:** 2d6 [6, 5] + 3 = **14**
*   **Server Outcome:** `full_success` (Full Success).

**Cyrus (Expert MM):**
> "Pippa, you deliver a devastating strike. You sever the leg joints completely. Because the sentinel is a TR 1 Mook, your strike destroys it instantly. It collapses into a heap of wet metal."

**Cyrus (Expert MM):**
> "Simultaneously, the second sentinel swings its heavy iron arm at Pippa. Since Pippa is in Aggressive posture, her Dodge reaction cost is increased to 2 Endurance. Billy, do you want to dodge?"

**Valerie (Expert Player - Alaric):**
> "No need! I am in Defensive posture. I spend 1 Endurance (base cost 2 - 1 Defensive modifier) to **Intercept** the attack and shield Pippa!"

### [Server Resolution: Alaric's Intercept]
*   **Action:** React: Intercept.
*   *Mechanics:* Deducts 1 Endurance from Alaric. No dice roll required by the server engine; the action succeeds deterministically.

**Cyrus (Expert MM):**
> "Alaric steps in, his tower shield taking the blow. The sentinel's arm clangs harmlessly against the steel. The exchange ends, the first sentinel is destroyed, and the second is left open. The combat dissolves as Pippa finishes off the remaining sentinel."

---

## Act III: Hearth-Core Vault (Combat Exchange 2 & Final Victory)

**Cyrus (Expert MM):**
> "You descend into the glowing Hearth-Core Vault. The room is hot, warmed by a pulsing geothermal well. Guarding it is the **Sentry Golem (TR 9 Boss)**. Steam vents hiss from its back pipes, and its central core burns orange. Combat begins! Valerie, Alaric is still Aggressive. Billy, Pippa chooses Measured."

**Valerie (Expert Player - Alaric):**
> "I'm going to charge right at it. I declare **Aggressive** posture to smash it with my warhammer! I roll **Strength** + **Combat**."

### [Server Resolution: Alaric's Aggressive Strike]
*   **Action:** Strike roll (Standard difficulty, Strength + Combat + Aggressive = +3 modifier).
*   **Server Roll:** 2d6 [6, 6] + 3 = **15**
*   **Server Outcome:** `full_success` (Double 6s - Critical Strike!).

**Cyrus (Expert MM):**
> "Incredible! A double-six critical! Your warhammer shatters the golem's volcanic chest plate, sending glowing stone shards flying. Its armor is permanently shattered! The golem takes 2 damage, dropping from 10 Endurance to **8**."

**Billy (Novice Player - Pippa):**
> "Now it's my turn! I'll plunge my dagger directly into the exposed core! I roll **Dexterity** + **Combat**."

### [Server Resolution: Pippa's Strike]
*   **Action:** Strike roll (Standard difficulty, Dex + Combat = +2 modifier).
*   **Server Roll:** 2d6 [2, 4] + 2 = **8**
*   **Server Outcome:** `partial_success` (Success with Cost).

**Cyrus (Expert MM):**
> "Your blade sinks into the magma core, dealing another 2 damage (Golem drops to **6** Endurance). But the core flares, venting superheated gas back at you. Billy, do you want to Dodge?"

**Billy (Novice Player - Pippa):**
> "Yes! I spend 1 Endurance and dive backward!"

### [Server Resolution: Pippa's Dodge]
*   **Action:** React: Dodge (Standard difficulty, Dexterity = +1 modifier).
*   **Server Roll:** 2d6 [3, 1] + 1 = **5**
*   **Server Outcome:** `failure` (Things Go Wrong).

**Valerie (Expert Player - Alaric):**
> "I'll spend 1 Endurance to **Intercept** the flame backlash again! I dive over Pippa, shielding her with my body!"

**Cyrus (Expert MM):**
> "Alaric shields her in time. Alaric's shield absorbs the flare (Alaric takes 2 damage to his Endurance pool). Pippa is safe, but Alaric is panting. The exchange ends. Golem is at 6 Endurance."

---

## Act IV: The Resonant Core (The Final Strike)

**Toby (Novice Player - Thorne):**
> "I see the golem's core vibrating as Alaric and Pippa suppress its movements. I want to project a high-frequency acoustic wave with my chimes to resonate inside its body and shatter the internal gears! I cast **Resonance** magic at **Significant** scope!"

### [Server Resolution: Rules Validation]
*   **Server Response:** `{"type": "error", "message": "Before unlocking the Technique, magic is limited to minor scope only. Unlock the corresponding Facet Technique to access broader scopes."}`

**Arthur (Novice MM):**
> "Toby, the rules say starting characters can only cast at **Minor** scope. A Significant scope requires unlocking the Resonance Facet Technique first."

**Toby (Novice Player - Thorne):**
> "Ah, right! I'll reduce the intensity. I just want to vibrate a hairline fracture in the gears. I'll roll **Resonance** at **Minor** scope."

### [Server Resolution: Thorne's Magic Cast]
*   **Action:** Cast Resonance (Minor scope, Knowledge = -1 modifier).
*   **Server Roll:** 2d6 [3, 6] - 1 = **8**
*   **Server Outcome:** `partial_success` (Success with Cost).

**Cyrus (Expert MM):**
> "A partial success! Your chimes ring out in a high, sharp hum. The sound wave travels through the golem's cracked body. The crystal gears lock, shatter, and the colossus collapses into a heap of dead stone. Combat is over!"

**Cyrus (Expert MM):**
> "But for the complication: the backlash of sonic energy crackles back into your chimes, fracturing the copper. Your chimes are broken until repaired, and you gain the **Deafened** condition."

---

## Post-Session MM Awards
*   **Thorne Woodcroft** is awarded **1 Spark** for the final resonant blow that shattered the core.
*   **Alaric of the Iron Gate** is awarded **1 Spark** for the heroic shield intercept to save Pippa.
