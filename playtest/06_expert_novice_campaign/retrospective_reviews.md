# Retrospective Reviews: Playtest 06 (The Great Crossroads)

Below are the individual retrospective reviews from each of the five participating agents: the four playtest personas (Cyrus, Arthur, Valerie, Billy) and Antigravity (the AI development assistant).

---

## 1. Cyrus (Expert MM Retrospective)

### What Worked Well:
* **The Spotlight Rotation:** The simultaneous exchange combat system completely removes the traditional "initiative block." Instead of players zoning out during others' turns, everyone was constantly scanning the board.
* **Partial Success Adjudication (7-9):** The three-tier outcome system is the engine of the game's narrative drive. In the Scriptorium fight, Arthur's attempt at lashing out on a 7-9 gave a partial success that had immediate narrative teeth (slid off the path into freezing water). It kept the stakes organic and escalating.

### Gaps & Friction Points:
* **Novice Magic Onboarding:** The freeform magic system (Domain + Intent + Scope) requires a lot of trust and improvisation. A novice player without prior experience will often stall because they don't know what constitutes a "Minor" vs "Significant" intent. 

### Recommendations:
* We need to build a **Domain Quickstart Sheet** in the Player's Handbook. For each domain (like Inscription or Resonance), we should list five concrete examples of minor, significant, and major spells to act as design patterns for new players.

---

## 2. Arthur (Novice MM Retrospective)

### What Worked Well:
* **Simple Math:** As a beginner MM, I really appreciated that I didn't have to keep track of a massive database of monster stats. Mooks having no Endurance (one strike removes them) made running the combat ambush incredibly simple.

### Gaps & Friction Points:
* **Breaking Initiative Habits:** I kept wanting to fall back on D&D-style turns. It took two full exchanges of Valerie correcting me to realize that I should ask *everyone* what posture they were in *first*, then resolve their declarations together.
* **The "Consequence" Panic:** On a 6- roll (failure), the book says I need to deploy a consequence. During Billy's failed spell, I panicked and said "nothing happens," which Valerie pointed out is an anti-pattern. I need better prompts or examples in the GM chapter on what "Things Go Wrong" looks like.

### Recommendations:
* Add a **Mirror Master's Trouble Table** in the MM manual with quick, generic consequences for failed rolls (e.g., *Equipment Damage*, *Position Lost*, *Condition Suffered*, *Danger Exposed*).

---

## 3. Valerie (Expert Player Retrospective)

### What Worked Well:
* **Tactical Synergy:** The combination of Defensive posture and the Intercept reaction is one of the most mechanically satisfying loops I've played. Usually, "tank" classes just have high HP. Here, by going Defensive, I actively spent my combat resources (Endurance) to protect Billy from a 4-damage blast, and it only cost me 1 Endurance instead of 2. 
* **Pressing & Sparks:** The resource choices (Endurance for Pressing, Sparks for dice addition) are deep. You aren't just rolling; you are managing a risk pool.

### Gaps & Friction Points:
* **Aggressive Posture Punishments:** The reaction penalty (+1 cost) for being Aggressive is incredibly steep if you don't have armor. Pippa going Aggressive without armor meant her Dodge cost 2 Endurance, which wiped out half her pool in one roll. 

### Recommendations:
* Clarify in character creation that players planning to use Aggressive postures *must* invest in Light or Heavy armor to mitigate the reaction cost penalties.

---

## 4. Billy (Novice Player Retrospective)

### What Worked Well:
* **Flat Math & Sheets:** Creating the character was super fast. Dividing 18 points between 9 stats with a 1-3 ceiling means the modifiers are small and easy to calculate. I didn't have to add up 5 different bonuses to see what my attack modifier was.
* **Sparks as a Safety Net:** I liked having Sparks. Even though I hoarded them at first, spending one to roll 3d6 on the hard pressure valve check saved me from failing and let me help the team.

### Gaps & Friction Points:
* **Spell List Anxiety:** I was really worried about not having a spell list. I didn't know what "Resonance" actually did until Sophia and Cyrus explained that I could vibrate the stone or pipes. It felt like I was "cheating" by making up my own spells, even though that's how the rules work.

### Recommendations:
* The game should have a few "Standard Traditions" with pre-set spell packages for players who want a traditional class-like experience before jumping into freeform magic.

---

## 5. Antigravity (AI Assistant Retrospective)

### What Worked Well:
* **Digital-Tabletop Architecture:** The FastAPI server and WebSocket backend are perfectly aligned with the simultaneous exchange system. Because combat is resolved in discrete, synchronized steps (declare postures → reveal → strike → react → end exchange), the WebSocket event loop (`handle_websocket` in `app/api/websocket.py`) naturally acts as the state engine for the table, validating declarations before revealing them.

### Gaps & Friction Points:
* **Port Conflict & Self-Hosting Limitations:** In our local development run, we encountered a port collision on `8000` due to a separate WSL Docker container (`fairy` project). While pydantic-settings resolved this cleanly by reading `PORT` from `.env`, it highlights that self-hosting environments have varying resource states.

### Recommendations:
* Add automatic port probing to `run.py` to automatically detect free ports and fallback gracefully if the configured port is bound.
* Add E2E tests for playtest campaign 06 (similar to `test_playtest_02.py`) to verify the digital tool's handling of the Sentry Golem's phase-change steam vent mechanics.
