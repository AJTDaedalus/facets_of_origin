# RESEARCH — Official 5e Module Conventions: Structure and Styling (the yardstick)

*2026-09-30. Status: COMPLETE. Written for the official-style audit of the 5e edition of
Oraga Night (`conversions/dnd5e/oraga_night/`). This file is only the yardstick. It
does not audit the module. The checklist auditors use is §13.*

**Evidence base.** PyMuPDF text extracts with `=== PAGE n ===` markers (catalog:
`docs/RESEARCH_5e_reference_catalog.md`). Page numbers below are those markers, so they
are PDF page indices and can sit a page or two off the printed folio. Abbreviations:
LMoP (Lost Mine of Phandelver), HotDQ, RoT, PotA, OotA, CoS (Curse of Strahd), SKT,
DH (Death House, `5e_CoS_Intro`), AL (the DDEX/DDAL/DDEP session adventures), DMG,
SRD. The extracts lose typography: bold, italic and box shading are not visible. So
typography claims rest on each book's own **format legend** (quoted where it is SRD-
neutral stock phrasing, otherwise paraphrased), and on structural position.

**Frequency scale.** **Always** = every book checked. **Usually** = most books, or every
book of one family (hardcover or AL). **Sometimes** = two or three books.

**Weighting.** Oraga Night is a one-night gothic ball/intrigue for four or five 3rd-level
characters. It has factions, threats and fights. The closest analogs are CoS social set
pieces (the dining hall at K10, the festival and dinner "Special Events" in Vallaki), the
RoT council sessions, HotDQ's one-night siege of a town (hour-by-hour "missions"), the
PotA feast scene, LMoP (starter module), DH (short haunted-house module), and the
four-hour AL adventures (DDAL04-04 and DDEX2-01 have village and party social scenes).

**Copyright posture.** This file records conventions and patterns only. It quotes no
read-aloud text, sentences, NPC names or lore. The quoted items are either stock rules
grammar that is also in SRD 5.1 (CC BY 4.0) or short structural labels such as
"Adventure Background" and "Development". Examples marked *(invented)* are original
and generic.

**Relationship to the house guide.** `style/STYLE_GUIDE.md` and
`style/analysis/adventures.md` were distilled from 3.5-era books. §12 lists where 5e
practice differs. Where the two disagree, the 5e audit uses this file, because the
module is being measured as a 5e product.

---

## 1. Front matter and chapter architecture

### 1.1 The introduction battery (always, order varies slightly by family)

**Hardcovers and the starter set.** The opening chapter is usually titled
"Introduction". It runs these blocks, most often in this order:

| # | Block (typical label) | Content | Evidence | Freq. |
|---|---|---|---|---|
| 0 | Fiction opener | One or two paragraphs of mood prose addressed to the DM, before any rules | CoS p.6 | sometimes (CoS) |
| 1 | **Running the Adventure** (or an untitled lead paragraph) | Party size, starting level, ending level, then the setting in one sentence. Then required books, and where stat blocks and items live | LMoP p.2 (4–5 PCs, 1st→5th); CoS p.6 (4–6, levels 1–10); HotDQ p.6 (4 PCs, 1st→7th/8th, with scale-up/down advice); RoT p.5; SKT p.14–17 | always |
| 2 | **Format legend** (inside Running the Adventure or its own subsection, e.g. LMoP "Glossary" + "Magic Items and Monsters" + "Abbreviations") | Bold creature name = stat block (MM or appendix). Italic = magic item (and spells). Boxed text = read aloud or paraphrase on first arrival or when the text says so. Assumptions about light | LMoP p.3; CoS p.6; HotDQ p.10; RoT p.8; PotA p.18; SKT p.14/17 | always |
| 3 | **Adventure Background** (or "Background") | Villain's history told chronologically, up to the present moment. Sometimes split under bold subheads (goals, organization, secrets) | LMoP p.3; HotDQ p.6 (sub-blocks for the cult, its secrets, its organization); RoT p.5–6 | always |
| 4 | **Overview** / **Story Overview** / **Adventure Synopsis** | One paragraph per part or chapter, each naming what the PCs do and where it leads. Hardcovers add a flowchart figure (SKT p.17–18 "Figure 0.1/0.2"; RoT p.6 "Outline of Episodes" in stages) | LMoP p.3–4; CoS p.6–7; HotDQ p.6; RoT p.6; SKT p.17 | always |
| 5 | **Adventure Structure** / chapter guide | Which chapter covers what, and what the appendices contain | CoS p.7; SKT p.17 | usually |
| 6 | **Character Levels** / **Character Advancement** | Milestone versus XP (see §9). Expected level per chapter or area, sometimes as a table ("Areas by Level", CoS p.7) | CoS p.7; HotDQ p.6; RoT p.5; SKT p.17 | always |
| 7 | **Adventure Hook(s)** | One to four named hooks with bold run-in titles. Each ends by routing to the same opening scene | LMoP p.4 (one hook); CoS p.19–23 (four hooks in ch.1, plus per-faction notes); HotDQ p.7 (points to appendix A backgrounds) | always |
| 8 | Tone or GM-craft toolkit | Named techniques for delivering the genre, each with bullet examples | CoS p.8 (a horror toolkit: unknown, foreshadowing, age, light, personification, details, humor); LMoP p.2–4 (DM role, rules to game by, improvising checks, roleplaying and inspiration) | usually |
| 9 | Troubleshooting / campaign-safety notes | What happens on a TPK, when players wander, when the party is too weak | SKT p.17 (Deadly Encounters section; a first TPK becomes capture); CoS p.7 (flee or hide; how to scale a fight up or down) | usually |

**AL session adventures.** These use a fixed, near-identical battery. It is heavier on
table logistics and lighter on lore:

`Introduction` (party range, optimized party, setting line) → org-play boilerplate →
`Preparing the Adventure` (bulleted DM prep) → `Before Play at the Table` (what to
collect from players) → `Adjusting the Adventure` (APL computation and a **Determining
Party Strength** table) → `Running the Adventure` (golden rule, pacing, read-aloud as a
suggestion) → season rules notes → `Adventure Background` → `Adventure
Overview` (bold run-ins "Part 1. … Part 2. …") → `Adventure Hook(s)`.
Evidence: DDAL04-05 p.2–8; DDAL04-04 p.8; DDEX1-1, DDEX3-06, DDAL04-12, DDEP1 (section
lists read in sequence). **Always** within AL.

**Party-size sentence.** Every book states party size and level before anything
mechanical. AL states a range *and* an optimum: "designed for three to seven characters
of 1st–4th level, optimized for five 4th-level characters" (DDAL04-05 p.2, paraphrased
to its shape). The hardcovers give an ideal size and one line of scaling advice: remove
foes for smaller groups and add them for larger (HotDQ p.6, RoT p.5).

### 1.2 How chapters and parts open (usually)

1. **Title** in the form "Chapter N: Name" (CoS, SKT, OotA), "Part N: Name" (LMoP, AL),
   or "Episode N: Name" (HotDQ, RoT).
2. **Situation paragraph(s)** in GM voice. They say what the place or phase is, who
   controls it, and what is happening *now*. They point forward to the chapter's own
   event section ("see the Special Events section at the end of this chapter", CoS p.96).
3. Optional **epigraph** from the villain, set as a pull quote (CoS every chapter, e.g.
   p.96). This is sometimes used, and specific to CoS.
4. **Arrival / approach** subsection with the first boxed text ("Approaching the [Place]",
   CoS p.96; LMoP p.6 "Read the boxed text when you're ready to start").
5. **General Features** block (see §2.2), then the keyed areas or scenes.
6. **Chapter-end blocks**: Special Events (CoS p.124–125), Conclusion (AL, RoT),
   Rewards (HotDQ), and a Character Advancement sidebar (SKT, every chapter).

**LMoP's opening-scene checklist.** Part 1 does more than begin. After the first boxed
text, it gives the DM a bulleted table-setup list: have players introduce characters and
invent their tie to the patron, then set marching order and travel method. The first
fight then comes as numbered run steps: review the stat block, check surprise, roll
initiative, what the enemies do, when they flee (LMoP p.6–7). This is starter-module
behavior. Session adventures keep a lighter version ("Take a moment to let the
characters introduce themselves", DDAL04-04 p.9).

### 1.3 Subdivision inside a chapter or part (always)

- **Hardcovers.** Chapter → region/site sections → keyed areas (§2.1) → run-in bold
  sub-features. Sites carry a "General Features" block and optional random-encounter
  tables (CoS p.50; OotA p.211).
- **AL.** Part → named scenes (Title Case headers) → run-in labelled blocks inside each
  scene: General Features, Adjusting the Encounter, Tactics, Developments, Treasure,
  XP Award (DDAL04-01 p.19–25; DDAL04-04 p.9–10; DDEX3-01 p.11). AL parts carry an
  **Expected Duration** line under the part title (DDAL04-04 p.9/12/16/19: 30 min,
  45 min, 30 min, 2 hours; DDEP1 p.15). **Usually** in 4-hour AL; absent in hardcovers.
- **Event-based chapters** (CoS Vallaki; HotDQ Greenest; RoT council) mix keyed places
  with a separate **events** section (see §2.4).

### 1.4 Back matter and appendices (always)

| Appendix type | Hardcovers | AL |
|---|---|---|
| Magic items | Appendix of new items; standard items point to the DMG (LMoP p.52 "Appendix A: Magic Items", opening with a short "Using a Magic Item" primer; CoS app. C; RoT app. B) | Item write-up inline in Rewards, with rarity line (DDAL04-05 p.16) or as a player handout (DDAL04-12 p.24, DDAL04-14 p.42) |
| Creatures / NPCs | Only **new** or modified stat blocks; MM creatures by reference (CoS app. D; SKT app. C; RoT app. A; HotDQ app. B). The starter set reprints every block it uses, with a "how to read a stat block" primer (LMoP p.55–56) | **Every** stat block used, reprinted alphabetically ("Appendix: Monster/NPC Statistics") (DDAL04-05 p.18–21; DDEX2-01 p.12; DDEX3-06) |
| NPC summary | Not used | Usually: name, pronunciation, one-line role (DDAL04-05 p.22; DDAL04-14) |
| Handouts | Named in-world documents (CoS app. F p.252–253) | "Player Handout N: Title", plus DM answer keys (DDEX2-01 p.30; DDAL04-01 p.44; DDAL04-04 p.41) |
| Maps | Inline in the chapter, numbered (SKT "Map 1.1", CoS "Map 3") | "Appendix: [Place] Map" (DDAL04-12 p.25; DDAL04-04 p.39) |
| Scorecards / trackers | RoT app. C, the Council Scorecard (p.95) | Faction scoring at an epic (DDEP1) |
| Character options | CoS app. A (background), HotDQ app. A (backgrounds as hooks) | Not used |
| Mini-adventure | CoS app. B (Death House) | Not used |

---

## 2. Keyed areas and scenes

### 2.1 Numbering schemes (always, one scheme per site)

- **Plain numbers per site**, restarting at each map: LMoP "1. Cave Mouth", "2. …"
  (p.8). DH numbers 1–38, with sub-areas "1A/1B", "25A–25E" (DH p.4–11).
- **Letter prefix + number**, with the letter keyed to the chapter or site: CoS "K1…K88"
  for the castle, "E1…" for the village, "N1…N9" for the town, sub-areas "K20a",
  "N2a", "N3t" (CoS p.44–124). PotA and SKT do the same per site.
- **Region letters** for the overland map: CoS "A. Old Road … Y. Hill" (p.34–41).
- **AL scenes are usually named, not numbered.** When an AL site is mapped it uses
  numbers or map letters ("the maw labeled 8 on the map", DDEX3-01; "area labeled X on
  the map", DDEP1 p.16).
- The header form is `Code. Name` in Title Case (small caps in print). Cross-references
  in running text say "area K10" or "(see area N4)".

### 2.2 Site-level block before the areas (usually)

A **General Features** block sits once, above the keyed areas. It uses bold run-in
fields, each a short paragraph that includes any rule or DC: Ceilings, Light, Rubble,
Sound, Stalagmites, Stream (LMoP p.8); Light, Fires, The Stream (HotDQ p.8); Light and
Visibility, Weather, Smells and Sounds (DDAL04-04 p.9); Light, Terrain (OotA p.210).
It is stated once so that area entries don't repeat it. It often includes the boxed-text
assumption ("the boxed text assumes darkvision or a light source", LMoP p.8).

A companion **features / alertness** paragraph describes how the site as a whole reacts
(DH p.4, the house's global behavior). Sometimes present.

### 2.3 Per-area template (always the same order, fields optional)

1. **Header**: `Code. Name`.
2. Optional **one-line GM lead-in** when the area needs context before the box: "When
   the characters cross to the east side, they can see …" (LMoP p.8). Or a **trigger
   clause** (§3.4).
3. **Boxed text** (§3). Present in most inhabited or dramatic areas; absent in many
   minor rooms (DH p.4–11 describes most rooms in plain GM prose).
4. **GM description**: what is really here, who is present and **what they are doing
   now**. Creature names in bold with counts ("Two goblins are stationed here"). Hidden
   features come with their DC ("a successful DC 12 Wisdom (Perception) check reveals
   …", DH p.4).
5. **Bold run-in sub-features**: each named feature gets a paragraph with its rule
   (Thickets., Fissure., Trapdoor., Dumbwaiter., Secret Door.) (LMoP p.8; DH p.4–5).
6. **Development** / **Developments**: consequences, what survivors do, what changes on a
   return visit (LMoP p.8–9; CoS p.56).
7. **Treasure**: itemised, with value in gp and provenance where it matters (DH p.10
   chest-by-chest; CoS p.58).
8. Chapter-specific recurring callouts, e.g. CoS's card-reading callout per area ("If
   your card reading reveals that a treasure is here, it lies …", CoS p.58).
9. **Awarding XP** where the design uses per-area awards (LMoP, AL). See §9.

**Lengths.** A connective area runs one to three sentences, with no box (CoS K12/K13
p.58; DH area 24 p.10). A standard room runs 100–250 words. A set piece runs a page or
more and gets several boxes (CoS K10 p.57–58).

### 2.4 Event-driven and social (non-dungeon) scenes

5e presents time-bound play in five recurring shapes. All five are relevant to a
one-night ball.

**(a) The chapter-end "Special Events" section** (CoS p.124–125, usually in CoS
settlements). Each event has:
- a Title Case header;
- a **timing rule** with DM latitude, e.g. "takes place N days after the characters
  arrive; delay it if they're waylaid, advance it if they're in a hurry" (paraphrased
  shape, CoS p.124);
- or a **prevention condition**: "the characters can prevent this event by doing X or Y;
  if they stay N days without doing so, it happens" (CoS p.125);
- boxed text for the public moment. GM prose then names who acts, what each NPC does,
  and what happens "unless the characters intervene";
- its own **Development** subsection, written as paired conditionals: if the PCs
  challenge the authority figure, X; if the guards fail, Y (CoS p.124–125).
Events chain. One event's outcome sets off an invitation, a dinner or a letter handout
in the next (CoS p.125: a thwarted attack leads to a written invitation shown as an
appendix F handout).

**(b) The clocked night: "missions" on an hour track** (HotDQ p.9–10). The scene opens
with a stated time frame (arrival at sundown; raiders gone before dawn). Then comes a
bookkeeping rule: each mission is assumed to take one hour. Short
rests consume a mission slot. Each mission is a titled subsection with bold run-in
labels (for example Locks., Foes., Rewards.). Enemy reinforcements are timed in rounds
and minutes ("if any are alive at the start of the fourth round, one runs for help; ten
minutes later N more arrive"). An NPC briefer is available "if players need guidance".
This is the closest official structure to a single-night event module.

**(c) The council / session structure** (RoT p.19–24). The council meets four times.
Each **Session** is broken into **Follow-up: [previous episode]** and **Setup: [next
episode]** subsections. Each follow-up states faction-by-faction reactions to what the
PCs did. The result is scored on a **Council Scorecard** (appendix C, p.95): rows of
events, a column per faction, and +, −, +/+ and −/− icons that the DM circles. There is
a subtotal per session and a "score needed for support" threshold, and the total sets
the finale's allies. The book tells the DM they may share the scorecard or convey it
through roleplay, and may award extra respect for good diplomacy "at your discretion"
(p.24). Delegate NPC blocks are in the introduction's "Allies" section (see §5).

**(d) The hosted dinner / feast set piece** (CoS K10 p.57–58; PotA p.50; CoS p.125
"a private dinner" as an event). The pattern:
1. An arrival box that sets the room and ends on the host's entrance or first line.
2. GM prose that scripts the host's *behavior envelope*: what the host will and won't
   reveal, how long the conversation lasts (CoS K10 caps it at 3 rounds, then ends it
   with a scripted trigger), and what the host is secretly doing (PotA: the hosts use the
   feast to learn what the PCs know).
3. A **topics list** of what the host will discuss, as bullets (PotA p.50).
4. **Conditional boxes** on player behavior ("If the characters mention X, read …";
   "If the characters join the feast, read …").
5. An **interruption box** the DM fires at will ("When you decide it's time, read:",
   PotA p.50). It turns the social scene into the next action beat and routes with
   "go to the [X] section".
6. The food and drink get a flat safety verdict in one sentence (CoS p.58).

**(e) The AL social scene** (DDEX2-01 p.7–8; DDAL04-04 p.9–13):
- boxed arrival → **Roleplaying [NPC]** sidebar (appearance, manner, motive, and
  sometimes a one-line signature **Quote:** — DDAL04-04 p.9);
- "use the following bullet points to guide the conversation", or "provides the
  following information, but only if the characters ask", then bullets of facts
  (DDEX2-01 p.7; DDAL04-04 p.11);
- **Interacting with [NPC]**: approach-keyed outcomes (Intimidation / Deception or
  Persuasion / failure at either), each with a DC and a named **success tier**
  (exceptional / marginal / poor). The tier **changes a later fight** (an extra foe on a
  poor result; a foe removed on an exceptional one) (DDEX2-01 p.8, p.10);
- a **Rumors** list: bulleted, overheard or passed along, some flagged untrue
  (LMoP p.15–16 attaches each rumor to a named speaker and a cross-reference;
  DDAL04-04 p.9);
- a pacing caution for open social time: watch real-world time while players chat
  (DDAL04-04 p.12).

**Timelines as tables.** 5e adventures rarely print a day-numbered timeline table. The
clock lives in prose (HotDQ hours; CoS "three days after arrival"; RoT four sessions),
with a flowchart figure for the macro arc (SKT p.18). The DMG recommends building a
timeline and flowchart for event-based adventures (DMG p.75–77, steps "Determine the
villain's actions" and "Anticipate the villain's reactions"). It also classes intrigue as
event-based, with optional **influence** tracked like inspiration or renown (DMG p.78).
Sometimes a table (RoT's scorecard); usually prose.

**Villain presence scenes.** When the main villain appears before the finale, the book
writes a "When [Villain] Attacks" rule: the visits test the party and don't kill; after a
few rounds the villain withdraws (CoS p.11). The villain gets explicit **Goals** as bold
subheads (CoS p.11). Usually present for a recurring villain.

---

## 3. Boxed read-aloud text

### 3.1 Marking and legend (always)

- Printed in a **shaded box** (not italic body text). The legend explains it in one
  sentence: boxed text is read aloud or paraphrased when the characters first reach a
  location or when a stated circumstance arises (CoS p.6, SKT p.14, same sentence in
  both). LMoP defines "Boxed Text" in its glossary as descriptive text, used mostly for
  rooms and for bits of scripted dialogue (p.3).
- AL: the Running the Adventure section tells the DM that read-aloud is a suggestion
  and may be modified, especially dialogue (DDAL04-05 p.4).

### 3.2 Frequency

- Hardcovers: about **one box per inhabited or dramatic keyed area**, plus arrivals and
  event beats. There are none for connective areas, and many minor rooms carry only GM
  prose (DH uses boxes very sparingly; CoS gives most K-areas a box).
- AL: **one box per scene opening**, plus one per NPC entrance or event beat. That is
  typically 8–15 boxes in a 4-hour adventure (DDAL04-04 p.9–13 has a box at nearly every
  scene transition).

### 3.3 Length (measured)

Word counts of 27 boxes sampled across LMoP, CoS, DH, RoT, HotDQ, PotA, SKT, DDEX1-1,
DDEP1 and DDAL04-05 (bounded by trigger and resumption of GM prose):

| Statistic | Words |
|---|---|
| Minimum | 35 |
| Median | ~62 |
| Mean | ~79 |
| Maximum | ~166 |

- **Short (35–60)**: a room glance or a single NPC entrance (CoS p.56, LMoP p.8,
  SKT p.21 creature arrival).
- **Standard (60–100)**: a room or an arrival (LMoP p.8 kennel, CoS p.56–57 halls,
  RoT p.21, HotDQ p.8).
- **Set-piece (130–170)**: opening narration, a banquet reveal, a public festival
  (LMoP p.6 opener ~157, CoS K10 ~166, CoS festival ~158, CoS chapel ~138).
- There are almost none over ~170. Long moments split into a **first box plus an "add
  the following" box** triggered by approach or behavior (CoS p.56; DH p.3; PotA p.50).

### 3.4 Triggers (always)

Every box is introduced by a GM-voice clause. Recurring forms:
- "Read the following boxed text when …" / "When the characters first enter, read:"
  (LMoP p.6; CoS p.57).
- "Read or paraphrase the following" (RoT p.21).
- "If the characters [approach from area X / are here by invitation / mention Y], add
  the following:" (CoS p.56; PotA p.50).
- "When you decide it's time, read:" (PotA p.50). "Once done, read:" (DDAL04-04 p.12).
- **Assumption statements**: "The following boxed text assumes that the characters can
  see underwater / arrive via the north or south tunnel" (PotA p.130); "The following
  read-aloud text assumes [NPCs] arrive after [event]. Adjust as necessary" (DDEX1-1
  p.7); "You can adjust the boxed text for the time of day" (SKT p.21); "Be sure to
  adjust the foes mentioned in the read-aloud text to account for the party's strength"
  (DDEP1 p.15); "Indoor and nighttime descriptions assume a torch or other light source"
  (CoS p.6 legend).

### 3.5 Tense, person, content

- **Second person plural, present tense** for the scene itself: "you see / you hear /
  before you". **Always.**
- **Present perfect or past for the lead-in to an opening scene**: the first box of an
  adventure may summarise the journey so far, and the job the PCs accepted (LMoP p.6;
  SKT p.20; HotDQ p.8; DDEX2-01 p.7). This is usual for the *first* box only.
- **Numbers are spelled out** in boxes ("fifty feet ahead", "twenty feet", "ten miles").
  GM text uses numerals ("30 feet", "DC 15"). **Usually.**
- **Contains**: sight first, then one or two other senses (sound, smell, temperature);
  an NPC's appearance by silhouette and one prop; NPC actions and **quoted dialogue**
  (5e boxes routinely script a host's welcome, a crier's proclamation or a villain's
  taunt: CoS p.56, PotA p.50, DDAL04-04 p.12, DDEX2-01 p.10); creature counts and
  appearance ("four burly humans", "two dead horses").
- **Avoids**:
  - PC **decisions and actions** (the box never has a PC open a door or draw steel);
  - PC **emotions and opinions** as a rule. A few lapses exist: an "expected" town
    (HotDQ p.8), a drowsiness produced by a game effect (OotA p.212), "the entire town
    is staring at you" (DDAL04-04 p.12). Physical sensations caused by an in-world
    effect are tolerated. Feelings about the scene are not;
  - **game terms and mechanics** (no DCs, no condition names);
  - **hidden information and identification**. The box describes what is seen, and the
    GM text afterwards names it: an NPC's name and stat block (CoS p.56), that a figure
    is an illusion (CoS p.57), that the "children" are not what they seem (DH p.3).
- **Mild interiority about the environment is allowed**: statues' eyes "seeming to watch
  you" (CoS p.58). Personification and implication are part of the gothic register, and
  CoS's tone toolkit encourages them (p.8).

### 3.6 Placement relative to mechanics

GM text **after** the box resolves what the box implies: the ambush setup (LMoP p.6–7),
the checks that reveal detail (DH p.4), what an NPC will and won't say (CoS p.57). A box
never contains a DC. The DC always sits in the next GM paragraph.

---

## 4. Sidebars

Sidebars are boxed asides with a Title Case (small-caps) title, set apart from the body
flow. The observed species:

| Species | Typical title shape | Content | Length | Evidence | Freq. |
|---|---|---|---|---|---|
| **What [someone] knows** | "What the [Creatures] Know" | Bulleted facts a captive or informant yields, with cross-refs to areas | 100–170 words | LMoP p.8 | usually (LMoP, OotA, CoS) |
| **Roleplaying [NPC / group]** | "Roleplaying [Name]" / "Roleplaying the [Family]" / "Roleplaying [Town] NPCs" | Appearance, manner, motive, how to voice them; generic acting tips in the starter set | 80–200 words (a family-sized block can reach 500 as a subsection) | LMoP p.15; CoS p.106; DDEX2-01 p.7–8; DDAL04-04 p.9–10 | always (AL), usually (hardcover) |
| **Adjusting the Encounter** (AL) | fixed title | Bullets by party strength (very weak / weak / strong / very strong), "not cumulative" | 30–60 words | DDAL04-05 p.9; DDEX2-01 p.10; DDEX1-1 p.8 | always (AL) |
| **Character Advancement** | fixed title | The milestone condition for levelling at the end of this chapter | 30–80 words | SKT (every chapter); PotA ch. intro | usually (SKT, PotA) |
| **General Features** | "[Site]: General Features" | Light, terrain, sounds, rules | 80–200 words | SKT p.21; OotA p.210 | usually |
| **Troubleshooting** | question-form title, e.g. "Do the players need direction?" | Name the stall, then give an in-fiction nudge (an NPC suggests the next move) | 50–120 words | LMoP p.19 | sometimes |
| **Module-specific recurring callout** | a fixed title repeated per area | Hooks the area into a module subsystem (CoS's card-reading treasure placements) | 20–40 words | CoS p.37, 58, 67 … | sometimes (CoS) |
| **Setting / lore aside** | subject title | Calendar, faction, new lords to create, "Tendays" | 100–200 words | SKT p.13–14; LMoP p.4 | usually |
| **Rules aside / special subsystem** | subject title | A local rule for the scene (visions, spellcasting services, a device) | 50–150 words | DDAL04-04 p.13; DDEX2-01 p.11; DDAL04-05 p.4 | usually (AL) |
| **Continuity / series note** (AL) | subject title | What to do if an NPC died in an earlier module, or the play order | 40–80 words | DDAL04-04 p.8; RoT p.6 ("New Faces") | sometimes |
| **Organizational / award rules** (AL) | "Permanent Magic Item Distribution" | Table-procedure rules | ~100 words | DDAL04-05 p.16 | always (AL) |
| **Map primer** (starter) | "Adventure Maps" | Maps are DM-only; scale and grid; compass rose | ~200 words | LMoP p.9 | sometimes (starter only) |

Notes:
- **There are no signed designer-note boxes** in any 5e module checked. The only
  first-person "we" is in forewords and legends (CoS p.6 recommends, as "we", reading
  the whole adventure first).
- Sidebars don't carry boxed read-aloud. Flavor and rules share sidebars more freely
  than the house guide allows (a setting sidebar may end in a rule), but read-aloud
  never sits in a sidebar.

---

## 5. NPC presentation

### 5.1 First mention in running text

Three conventions, by era:

1. **Parenthetical stat tag** (CoS, SKT; **always** in books from 2016 on): Name
   (alignment abbreviation, sex, race, **stat block name in bold**), e.g. *(invented)*
   "the steward, Orrin Vale (LN male human **noble**)". Counted: 99 in CoS and 189 in
   SKT. None appear in LMoP, HotDQ, RoT, PotA, OotA or AL.
2. **Descriptive apposition** (LMoP, HotDQ, AL): "a lean, balding human male
   shopkeeper of fifty years with a kindly manner" (shape from LMoP p.16; HotDQ p.8),
   with the stat block given separately ("treat as a **commoner**", "Treat the others as
   **scouts**", DDAL04-05 p.9; LMoP p.15 "use the commoner stat block").
3. **Pointer**: "(see appendix D)" / "(see chapter 7)" when the block is new
   (CoS p.56; PotA p.18 legend).

**Non-combatant rule.** Townsfolk who won't fight get no statistics, with one stated
fallback block (LMoP p.15). **Usually.**

### 5.2 NPC personality blocks: four official formats

| Format | Fields, in order | Where | Evidence |
|---|---|---|---|
| **A. Trait triplet** | Header "[Name]'s Traits" → **Ideal.** "first-person quote" → **Bond.** "quote" → **Flaw.** "quote" | Appendix NPC entry, after a lore write-up and a **Statistics.** line naming the MM block and any change | CoS p.226 (app. D) |
| **B. Stat block + Roleplaying Information** | Full stat block → "Roleplaying Information" → 1–2 sentences of situation and temperament → **Ideal:** "quote" → **Bond:** "quote" → **Flaw:** "quote" | Appendix NPC roster | SKT p.248 (a whole roster in this shape) |
| **C. Delegate / faction block** | Name → one line "alignment sex race class" → **Ideals:** (words, or a quote) → **Interaction Traits:** / **Personality:** (2–4 adjectives) → **Pledged / Potential Resources:** → prose on what wins them over and what alienates them | Faction and council NPCs | RoT p.13 (Allies), OotA p.127 |
| **D. Roleplaying sidebar** (AL) | "Roleplaying [Name]" → age, look, one prop → manner and speech → motive/fear → optional **Quote:** one signature line | Inline at first meeting | DDEX2-01 p.7–8; DDAL04-04 p.9–10; DDAL04-14 |

The DMG gives the vocabulary behind these: appearance, abilities, talents,
**mannerisms**, **interaction traits**, ideals, bonds, flaws and secrets (DMG p.90).
Modules print a **subset**: ideal/bond/flaw (A, B), or traits and resources (C), or
prose manner plus a quote (D). No module prints the full DMG list per NPC.

### 5.3 What the NPC knows (always, in one of three shapes)

- **Bulleted fact list** after "Characters who question [NPC] learn the following:"
  Untrue beliefs are flagged in parentheses as untrue (DH p.3; DDEX2-01 p.7; DDAL04-04
  p.11 "only if the characters ask").
- **Topics list** the NPC will discuss (PotA p.50).
- **Tiered reveal by approach** with success tiers (DDEX2-01 p.8).
Prisoner and informant knowledge is a sidebar (§4). Every secret the players might
extract is written down; none is left to improvisation.

### 5.4 Inline vs appendix stat blocks

- **Hardcovers**: never inline in the body. Standard creatures come from the MM by
  bold-name reference; new or changed ones go in the appendix. Small modifications are
  stated inline in prose ("has 8 hit points; her spear attack is +2 to hit for 1d6
  piercing damage", HotDQ p.9; "change its alignment to …", CoS p.226; a CR-changing
  added trait written out in the text, OotA p.212). **Always.**
- **LMoP**: all blocks in appendix B, including MM ones (starter self-sufficiency).
- **AL**: all blocks reprinted in an end appendix. None inline. **Always.**
- **Named villain**: gets a named stat block ("[Name] ([base creature])" header, e.g.
  a named vampire-spawn block, DDAL04-05 p.19), not "use the X block".

### 5.5 Pronunciation

Pronunciation is given in parentheses at first mention (LMoP p.3 for a town; CoS p.96),
and in AL NPC summaries (DDAL04-05 p.22). **Usually** for invented names.

---

## 6. Encounter presentation

### 6.1 Naming creatures at first mention (always)

- **Bold** stat-block name, lowercase, as a common noun, with the count spelled out:
  "four **goblins**", "two **wolves**", "a **bugbear** named …" (LMoP p.6–8 legend
  p.3).
- Where the block lives follows it: nothing for the MM (hardcover default), "(see
  appendix B)" for a new block, "(see chapter 7)" in PotA (PotA p.18 legend explains
  the parenthetical).
- Named individuals of a common block: "N (… **guard**)" (CoS tag) or "treat as
  **scouts**" (AL).
- Map-lettered combatants in epics: "hobgoblin captain (HC) and cult fanatic (F)"
  (DDEP1 p.16).

### 6.2 The encounter body (usual order)

1. Setup: who is here, what they're doing, and why (LMoP p.8, bored inattentive
   guards).
2. Surprise and detection terms: the passive-Perception threshold or contest, stated
   plainly (LMoP p.7; DH p.10 "passive Wisdom (Perception) score under 12 is
   surprised").
3. **Tactics**: a labelled paragraph in AL (DDEX3-01 p.11; DDAL04-01 p.19; DDEP1
   p.16 "Foes and Tactics"). In hardcovers, prose inside the area. Contents: opening
   move, focus target, special behavior, and a **morale / stop condition** ("when three
   are defeated, the last flees", LMoP p.7; "fight to subdue, not kill; after one falls
   the rest surrender", DDAL04-01 p.19; a group flees when half its number dies,
   HotDQ p.9).
4. **Terrain as rules**: bold run-ins with the rule (difficult terrain, cover values,
   fall damage, climb DCs) (LMoP p.8; DDEX2-01 p.10).
5. **Timed escalation**: "after three rounds, [event]" (DDAL04-05 p.9; HotDQ p.9).
6. **Development / Developments**: what happens after, including what happens if the
   PCs **lose**. Defeat routes on to capture or robbery, not a game over (victorious goblins knock
   the party out, loot them and leave, LMoP p.7; SKT p.17 on TPKs as capture).
7. **Treasure** (§9).
8. **XP Award** (AL; LMoP "Awarding Experience Points") (§9).

### 6.3 Scaling and adjusting (AL always; hardcover prose)

- **AL**: the intro defines APL and a **party strength** table: 3–4, 5, or 6–7
  characters × APL below / equal / above → very weak … very strong. Every combat then
  carries an **Adjusting the Encounter** sidebar (a one-line lead-in that ends by
  marking the recommendations "not cumulative"), with bullets that remove or add bodies
  or trim hit points (DDAL04-05 p.3, p.9; DDEX2-01 p.10). Not every
  strength band has to be listed.
- **Hardcovers**: one global rule in the intro (add or remove foes; HotDQ p.6, RoT p.5),
  plus a "raise to max HP or add monsters if a fight is too easy" tip (CoS p.7).
  **No per-encounter difficulty tag** (no "Easy/Medium/Hard/Deadly" label and no XP
  budget in headers) in any hardcover checked. Deadly-by-design fights are flagged in
  the intro (SKT p.17).
- The **success tier from an earlier social scene** can serve as the adjuster (DDEX2-01
  p.8, p.10). This is a sometimes pattern, and useful for intrigue.

### 6.4 Resolution phrasing (always; SRD stock grammar)

"a DC 15 Wisdom (Perception) check"; "must succeed on a DC 10 Dexterity saving throw or
…"; "taking 7 (2d6) bludgeoning damage on a failed save, or half as much damage on a
successful one"; "has advantage on"; "contested by the goblins' passive Wisdom
(Perception) score". Damage is written as the average then the dice in parentheses.

---

## 7. Typography visible in the text

| Element | Convention | Source | Freq. |
|---|---|---|---|
| Creature / NPC stat block name | **bold**, lowercase common noun ("**goblin**", "**mage**") | legends: LMoP p.3, CoS p.6, HotDQ p.10, RoT p.8, PotA p.18, SKT p.14 | always |
| Magic item | *italic*, lowercase unless a proper name (*potion of healing*, *cloak of protection*) | LMoP p.3 legend; DH p.11 | always |
| Spell | *italic*, lowercase (*healing word*, *remove curse*) | DDAL04-04 p.10; DDAL04-05 p.4–5 | always |
| Condition | plain lowercase (restrained, frightened, charmed), sometimes with "see the appendix in the rulebook" | LMoP p.7; SRD | always |
| Ability / skill | Capitalized ability with the skill in parentheses: "Wisdom (Perception)", "Charisma (Deception or Persuasion)" | everywhere | always |
| Dice | "1d6", "2d10 + 2"; average first: "7 (2d6)" | SRD; LMoP p.7 | always |
| Headers | Title Case (rendered in small caps in the hardcovers). Keyed area headers "K10. Dining Hall" style | all | always |
| Run-in labels | **Bold.** followed by prose on the same line ("**Light.** …", "**Treasure.** …", "**Quest: …**") | LMoP p.8, p.16; HotDQ p.9 | always |
| Tables | Titled in Title Case, **not numbered** ("Areas by Level", "Determining Party Strength", "Combat Awards", "Daytime Random Encounters in [Region]"); die-range first column for random tables ("d8", "d20", "d100") | CoS p.7, p.30; DDAL04-05 p.3, p.16; OotA p.211 | always |
| Figures | Flowcharts numbered "Figure 0.1" (SKT p.17) | SKT | sometimes |
| Maps | "Map N" (CoS) or "Map C.N" per chapter (SKT "Map 1.1") | CoS p.4 contents; SKT p.21 | usually |
| Numbers | Numerals for rules quantities (DCs, feet, hit points, gp). Words for small counts of creatures ("Four goblins") and inside boxed text | LMoP p.6–8 | usually |
| Currency | gp/sp/cp/ep/pp, defined once in an abbreviations list | LMoP p.3 | usually |
| Cross-references | "(see area K8)", "(see chapter 5, "[Chapter Name]")", "(see "[Section]" in the rulebook)", "(see appendix C)"; section names in quotation marks | LMoP p.7–8; CoS p.106 | always |
| Letters and in-world documents | Set off as a quoted block, introduced by "It reads as follows:" (PotA p.49), or pushed to a handout (§10) | PotA p.49; CoS p.125 | usually |

---

## 8. Stat block format (SRD / MM / adventure appendices)

**Field order (always, verified in the SRD and in LMoP, AL and SKT appendices):**

1. **Name** (header).
2. Size, type (subtype/tag), alignment, e.g. "Medium humanoid (any race), any
   alignment".
3. **Armor Class** N (armor source).
4. **Hit Points** N (dice + bonus).
5. **Speed** N ft., other modes.
6. Ability row: STR DEX CON INT WIS CHA, each "N (+m)".
7. Optional lines, in this order when present: **Saving Throws**, **Skills**, **Damage
   Vulnerabilities**, **Damage Resistances**, **Damage Immunities**, **Condition
   Immunities**, **Senses** (special senses, then "passive Perception N"),
   **Languages** ("—" if none), **Challenge** N (XP).
8. **Traits**: each a bold-italic name + period + prose (for example "Pack Tactics.").
   Limited use goes in the name ("Legendary Resistance (3/Day).", "(Recharge 5–6)").
   Spellcasting is a trait naming level, ability, save DC and attack bonus, with spells
   listed by level and slots.
9. **Actions** header → **Multiattack.** first → each attack in stock grammar: "*Melee
   Weapon Attack:* +N to hit, reach 5 ft., one target. *Hit:* N (dice + m) type
   damage." Riders follow the Hit clause.
10. **Reactions** header (only if the creature has one) → e.g. a parry-type entry
    (SRD bandit captain).
11. **Legendary Actions** header → stock preamble ("The [creature] can take 3 legendary
    actions, choosing from the options below. Only one legendary action option can be
    used at a time and only at the end of another creature's turn. The [creature]
    regains spent legendary actions at the start of its turn.") → options, with costs
    as "(Costs 2 Actions)" (SRD, adult black dragon).
12. Lair actions and regional effects appear in lore sections, not the block (SRD
    p.263).

**Adventure-appendix habits.**
- A one- or two-sentence flavor paragraph follows each block in starter and AL
  appendices (LMoP p.56; SRD).
- Named variants: "[Name] ([Base Creature])" with the modified trait written out
  (DDAL04-05 p.19).
- The LMoP appendix opens with a field-by-field "how to read a stat block" primer
  (p.55). Only the starter set does this.
- Alphabetical order (LMoP p.56 "presented in alphabetical order"; AL appendices).

---

## 9. Treasure, XP and advancement

### 9.1 Advancement model (always stated up front)

| Book | Model | Where it's stated / paid |
|---|---|---|
| LMoP | XP, with **story-milestone XP bundles** inside the text ("Awarding Experience Points: completing X is a story milestone; award each character N XP") plus per-fight splits ("Divide N XP equally among the characters if the party defeats …") | LMoP p.7, p.19 onward (39 award blocks) |
| HotDQ | Optional milestone: a level after each episode except one; otherwise XP plus mission bonuses | HotDQ p.6, p.9 ("Rewards." run-ins) |
| RoT | Milestone | RoT p.5 |
| CoS | XP, milestone, or mixed. Milestone recommended because so much of the adventure is social interaction and exploration, with named milestone categories (artifacts found, villains defeated, story goals) | CoS p.7 |
| DH | Milestone: two bulleted level-up triggers, at the front | DH p.3 |
| SKT | Milestone: a "Character Advancement" sidebar at the end of every chapter; tracking XP instead is explicitly allowed | SKT p.17 |
| OotA | XP, with a chapter-end "XP Awards" block for story accomplishments | OotA p.17 |
| AL | XP tables at the end (see below), plus per-scene "XP Award" run-ins for non-combat wins | DDAL04-05 p.16; DDAL04-01 p.19–25 |

**Pattern for a short, social-heavy module.** State the model in the intro. The more
social the module, the more likely the book is to choose milestone (CoS's stated
reason). A one-night 3rd-level module that doesn't level the party still states that:
what level the PCs start at and whether they advance.

### 9.2 Where rewards are listed

- **In place**: **Treasure** subsection at the area or scene, itemised with gp values
  and provenance (DH p.10–11; CoS p.58; DDAL04-04 p.10). Payments promised by NPCs are
  stated with amounts and the conditions attached (DDEX2-01 p.8; LMoP p.16).
- **Summary at the end (AL, always)**: **Rewards** → **Experience** (Combat Awards
  table: foe / XP per foe; Non-Combat Awards table: task / XP per character; stated
  **minimum and maximum** total per character) → **Treasure** (Treasure Awards table:
  item / gp value; magic-item write-ups) → **Renown** → **Downtime** → **Story Awards**
  → **DM Rewards** (DDAL04-05 p.16–17; DDEX2-01 p.11).
- **Non-combat XP is printed** for social wins in AL ("attempt the dance", "gain any
  clues", "rescue [NPC]", 25–50 XP each; DDAL04-05 p.16). **Always** in AL.
- **Random treasure guidance** is given once in the intro (SKT p.19: roll or pick
  within range; take the minimum if the party is flush).
- **Story awards and boons** are non-mechanical titles or one-shot benefits recorded on
  the character (DDAL04-05 p.17). Hardcovers do the same with faction titles (LMoP p.16
  joining an order).

---

## 10. Handouts and pregenerated characters

### 10.1 Handouts

- **Naming**: AL numbers them, "Player Handout 1: [Title]" / "Player Handout 2" /
  "DM Handout 1" (answer key) (DDEX2-01 p.30; DDAL04-01 p.44; DDAL04-14 p.39/42).
  Hardcovers title them as in-world documents with possessive names and version
  numbers, e.g. "[Writer]'s Letter (Version 1)" (CoS p.252).
- **Trigger in the body (always)**: "If the characters open and read the letter, show
  the players '[Handout]' in appendix F" (CoS p.125). "Present the players with Handout
  1" (DDEX3-01 p.6). "give Player Handout 1 to the character reading the journal, and
  only that player" (DDAL04-04). The trigger names *who* gets the handout.
- **Types observed**: in-world letters and invitations (CoS app. F; PotA p.49 inline);
  journal extracts (DDAL04-04 p.41); **recap summaries** of rumors and leads gathered
  "off-screen" (DDEX3-01 p.6, offered as a pacing alternative to roleplaying the
  gathering; DDAL04-01 p.44); puzzle sheets with a matching DM key (DDEX2-01 p.30);
  magic-item cards (DDAL04-12 p.24; DDAL04-14 p.42); a reference table of choices and
  consequences (DDAL04-14 p.39).
- **Placement**: always in the appendix or at the end, never interrupting the body.
  Short letters may also be quoted inline where found (PotA p.49).

### 10.2 Pregenerated characters

- The evidence in the extracts is thin (pregen PDFs are image scans; catalog §F). What
  the text establishes:
  - LMoP's introduction describes what each pregen sheet carries: two personality traits
    (one positive, one negative), an ideal, a bond, a flaw, a background, and a
    **secondary goal** tied to the adventure. The hook section tells the DM these
    secondary goals are a motivation source (LMoP p.4).
  - Inspiration is taught alongside the pregens as the reward for roleplaying traits
    and flaws (LMoP p.4).
  - AL allows pregens only as a fallback: an ineligible player "can make a new
    1st-level character or use a pregenerated character" (DDAL04-05 p.2).
  - Hardcovers substitute **backgrounds as hooks** in an appendix (HotDQ app. A,
    referenced p.7; CoS app. A).
- Auditors should expect a pregen set to have: one page per character, the standard
  sheet, personality/ideal/bond/flaw, and one adventure-specific tie or secret goal per
  character. This follows the LMoP convention.

---

## 11. Maps (text-side conventions only)

- **Maps are DM-only unless marked as handouts.** LMoP says so in a sidebar and
  explains scale and grid (5 ft. or 10 ft. squares), the compass rose, and drawing what
  players see (p.9). **Always** implied; stated in the starter.
- **Numbered and named**: "Map N: [Name]" (CoS contents p.4); "Map C.N" per chapter,
  with a sentence saying that the sections which follow describe that map (SKT p.21).
  AL puts them in an appendix, "Appendix: [Place] Map" (DDAL04-12 p.25).
- **Body-to-map pointer sentences**, set before the keyed list: one sentence tying the
  area labels below to a named map and its page (CoS p.46; DH p.4). **Always** when a
  map exists.
- **Map symbols named in text**: an X marking where hidden foes emerge (DH p.10–11), a
  T marking a teleport arrival point (CoS p.119), an X marking the party's start
  (DDEP1 p.16), and numbers on puzzle features (DDEX3-01).
- **Scale lines** are printed on the map ("One square = N feet", DH map page). The
  text gives real distances in feet.
- **When no map exists**, the text carries the geometry in General Features and area
  prose: room dimensions in feet (DDAL04-04 p.13), ceiling heights (DH p.4), and
  exits. Boxed text may omit exits, but GM text states every connection as a one-line
  pointer to the next area code (CoS p.56, p.106).
- **Overland references**: "(as shown on the overland map)" (LMoP p.6); region letters
  keyed to a map of the domain (CoS p.34).
- **For a module without map images** (our case), the text alone must still do what
  the books do in text: name every connection, give room dimensions where a fight can
  happen, give every map-marked symbol a prose equivalent, and say where combatants
  start.

---

## 12. Where 5e differs from the house 3.5-derived guide

| Topic | House guide (3.5 study) | Official 5e practice | Audit consequence |
|---|---|---|---|
| Format legend | A full "how to read these entries" legend documenting every template | A **short legend**: bold = stat block, italic = item/spell, boxed = read-aloud, a light assumption, abbreviations (§1.1) | Require the short 5e legend. A long template legend is extra, not required |
| Designer notes | Signed first-person designer-note boxes | **None** in modules. "We" appears only in forewords and legends | Don't require them. Flag them as non-5e if present |
| Read-aloud length | 2–6 sentences, 40–90 words, ~120 max | Median ~62, mean ~79. Set pieces reach ~160–170 | Accept up to ~170. Flag over ~180 |
| Read-aloud content | Perception only. No NPC identification. Exits omitted | Perception-first, but **scripted NPC dialogue and actions are normal**. Opening boxes may summarise the journey in present perfect. Exits are often included (CoS p.56) | Allow NPC speech and action. Still ban PC actions, decisions, feelings and mechanics |
| Read-aloud marking | Italic | **Shaded box**, legend-declared | In Markdown, whatever device the module declares must be used consistently |
| Area headers | Difficulty tag in the title ("(EL 6)") | **No difficulty tag.** AL scales via party-strength sidebars; hardcovers add or remove foes globally | Flag difficulty tags as non-5e. Require an Adjusting sidebar per fight in a session-length module |
| Tables | Numbered designations ("Table III.3–2") | **Titled, unnumbered** tables. Numbered **maps** and **figures** only | For the 5e edition, numbered tables are a house choice, not a 5e requirement |
| Tactical encounter spreads | One- or two-page encounter units with maps (3.5 late era) | Not used. Encounters are inline. Stat blocks are in the appendix (hardcover) or the end appendix (AL) | Don't require scene cards |
| NPC dialogue | Q&A dialogue format (question in italics, quoted answer) | **Bulleted facts / topics lists** and tiered reveals. A single signature **Quote:** line in AL. Full Q&A is rare | Accept bullets. Q&A is optional |
| Social scenes | Goal / Attitude / Complication / Success fields | Roleplaying sidebar + info bullets + approach-keyed checks with success tiers + interruption boxes; council follow-up and setup blocks; scorecards | Audit against §2.4 shapes |
| Timeline | Day-numbered table with conditional delay lines | **Prose clocks** (hours, days, sessions) with delay/advance latitude; events with prevention conditions; flowchart figures | A prose clock is fine. It needs explicit timing plus a DM latitude line |
| Villain response | A three-stage escalation ladder | "When [Villain] Attacks" rule + Goals + event chain (CoS p.11) | Require the villain's goals and a visit rule |
| Rewards for clever play | Printed awards | Printed **non-combat XP** (AL) and milestone triggers | Same principle; 5e form |
| Morale | Every fight has a morale line | Usually present (flee thresholds, surrender, subdue) | Same |

---

## 13. Checklist for auditors (C-S)

Each item states what an official 5e module does. The frequency is in brackets:
[A] always, [U] usually, [S] sometimes. An [S] item is a style option. Don't count it
as a defect when absent.

**Front matter and architecture**

- **C-S1** [A] The first mechanical statement gives party size (range and ideal or
  optimum), starting level, and ending level or whether PCs advance.
- **C-S2** [A] There is a short format legend: bold creature name = stat block (and
  where: MM or appendix), italic = magic item / spell, boxed text = read or paraphrase
  on arrival or under stated circumstances, and any lighting assumption for boxed text.
- **C-S3** [A] The introduction contains, in this order or close to it: Adventure
  Background → Overview (one paragraph per part/chapter) → Adventure Hook(s) → Running
  the Adventure material (advancement, required books).
- **C-S4** [A] Hooks are named with bold run-in titles, and each routes to the same
  opening scene.
- **C-S5** [U] There is a tone or genre toolkit for the DM (named techniques with bullet
  examples), as CoS does for horror.
- **C-S6** [U] (session-length) There is an **Adjusting the Adventure** section
  defining how to scale: APL and party strength, or an equivalent add-or-remove-foes
  rule.
- **C-S7** [U] Each part or chapter opens with a situation paragraph (what is
  happening now, who is in control), then an arrival subsection with the first boxed
  text.
- **C-S8** [U] (session-length) Each part carries an **Expected Duration** line, and
  their sum matches the stated session length.
- **C-S9** [A] Appendices hold new stat blocks and new items (hardcover), or all stat
  blocks (AL/starter). Handouts come last.

**Keyed areas and scenes**

- **C-S10** [A] Keyed areas use one numbering scheme per site (N. or letter+N, with
  sub-areas as NA/Na), headed `Code. Name`, and are cross-referenced as "area X".
- **C-S11** [U] A General Features block (bold run-ins: light, sound, terrain, other
  site rules with DCs) precedes a site's areas.
- **C-S12** [A] Area entries keep a stable order: header → trigger/lead-in → boxed text
  → GM description (occupants doing something now) → bold run-in features with rules →
  Development → Treasure.
- **C-S13** [A] Every event beat has a timing rule (when it fires) and DM latitude
  (delay or advance), or a prevention condition the PCs can meet.
- **C-S14** [A] Every event has a **Development** written as paired conditionals ("If
  the characters … / If not …") in which failure continues the story.
- **C-S15** [U] A one-night or clocked module states its clock once (start and end
  times, how much time a scene or mission consumes, what a rest costs), as HotDQ's
  night does.
- **C-S16** [U] A dinner/feast/ball set piece has: an arrival box ending on the host;
  a scripted behavior envelope for the host (what they will and won't reveal, how long,
  their hidden aim); a topics or facts list; conditional boxes on player behavior; and a
  DM-fired interruption box that routes to the next section.
- **C-S17** [S] Faction reactions are tracked explicitly (a scorecard with +/− per
  faction per event and a threshold) when factions' support decides the finale.
- **C-S18** [U] A recurring villain has stated Goals and a visit rule (visits test, not
  kill; withdraws after a few rounds).

**Boxed text**

- **C-S19** [A] Every box has a GM-voice trigger clause ("When …, read:", "If …, add
  the following:", "Read or paraphrase …").
- **C-S20** [A] Boxes use second person, present tense (present perfect is allowed only
  to summarise the journey in an opening box). Numbers are spelled out inside boxes.
- **C-S21** [A] Boxes contain no PC actions, decisions or emotions, no mechanics or
  DCs, and no identification the players haven't earned (names, true natures). The GM
  text after the box supplies those.
- **C-S22** [U] Box length is mostly 35–100 words, with set pieces up to ~170. Longer
  moments are split into a base box plus conditional "add" boxes.
- **C-S23** [U] When a box assumes something (time of day, approach direction, who is
  present, party strength), the text says so and permits adjustment.
- **C-S24** [U] Scripted NPC dialogue inside boxes is short (one to three sentences)
  and in voice. Longer conversation moves to bullets in GM text.

**Sidebars**

- **C-S25** [U] Sidebars come from the recognised species (Roleplaying [NPC], What
  [someone] Knows, Adjusting the Encounter, Character Advancement, General Features,
  troubleshooting, setting or rules aside, series/continuity note), each with a Title
  Case title and 30–200 words.
- **C-S26** [A] No read-aloud text inside sidebars.

**NPCs**

- **C-S27** [A] Each NPC's first mention gives either a parenthetical stat tag
  (alignment, sex, race, **stat block**; the CoS/SKT convention) or a descriptive
  apposition plus the stat block to use. The module picks one convention and uses it
  throughout.
- **C-S28** [U] Major NPCs get one personality block in an official shape: trait
  triplet (Ideal/Bond/Flaw as first-person quotes), stat block + Roleplaying Information,
  delegate block (alignment line, Ideals, Interaction Traits, Resources), or a
  Roleplaying sidebar with an optional Quote line.
- **C-S29** [A] What each talkable NPC knows is written down, as bullets, a topics list
  or approach-tiered reveals, with untrue beliefs flagged as untrue.
- **C-S30** [U] Non-combatant NPCs get no stat block, and one fallback block is named
  for them.
- **C-S31** [U] Invented names get a pronunciation at first mention or in an NPC
  summary.

**Encounters**

- **C-S32** [A] Creatures at first mention: count spelled out + **bold** lowercase
  stat-block name + location pointer if not in the MM ("(see appendix B)").
- **C-S33** [A] Each fight states surprise and detection terms (a passive Perception
  threshold or contest).
- **C-S34** [U] Each fight has Tactics (labelled in session-length modules): opening
  move, target priority, and a morale or stop condition.
- **C-S35** [A] Each fight's Development covers the PCs losing, with a route that isn't
  a game over (capture, robbery, a later rescue).
- **C-S36** [U] (session-length) Each combat has an **Adjusting the Encounter**
  sidebar with party-strength bullets, marked "not cumulative".
- **C-S37** [A] No difficulty tag or XP budget appears in encounter headers.
- **C-S38** [S] Earlier social success tiers visibly change later fights (a foe added
  or removed).

**Typography**

- **C-S39** [A] Bold is for stat-block names and run-in labels only. Italic is for
  magic items and spells (lowercase). Conditions are plain lowercase. Checks are written
  "DC N Ability (Skill) check". Damage is written "N (XdY + Z) type damage".
- **C-S40** [A] Headers use Title Case. Tables are titled, not numbered, with die-range
  first columns for random tables. Maps and figures, if any, are numbered.
- **C-S41** [A] Cross-references use "(see area X)", "(see chapter N)" and "(see
  appendix X)", with section names in quotation marks.

**Stat blocks**

- **C-S42** [A] Stat blocks follow SRD field order exactly: name → size/type/alignment
  → AC → HP → Speed → abilities → saves → skills → vulnerabilities/resistances/
  immunities → condition immunities → senses (passive Perception last) → languages →
  challenge (XP) → traits → Actions (Multiattack first) → Reactions → Legendary
  Actions with the stock preamble.
- **C-S43** [U] Named villains get a named block ("Name (Base Creature)") with the
  modifications written out. Small tweaks to MM creatures are stated in prose at the
  encounter.

**Rewards**

- **C-S44** [A] The advancement model (XP, milestone or mixed) is stated in the intro,
  and every milestone trigger or XP award is printed where it is earned.
- **C-S45** [A] Treasure is itemised where it is found, with gp values and provenance.
  NPC payments state the amounts and conditions.
- **C-S46** [U] (session-length) A closing Rewards section summarises XP (combat and
  non-combat tables, with min and max per character), treasure, and story awards.
- **C-S47** [U] Social and clever wins are paid explicitly (non-combat XP, a milestone,
  a story award or boon).

**Handouts and pregens**

- **C-S48** [A] Handouts are named consistently ("Player Handout N: Title", or
  in-world titles with versions), live in the appendix, and are triggered in the body
  with who receives them.
- **C-S49** [S] A recap handout of gathered rumors or leads is offered as a pacing
  alternative for long information-gathering.
- **C-S50** [U] Each pregen carries personality traits, ideal, bond, flaw, background,
  and one adventure-specific tie or goal.

**Maps (text-side)**

- **C-S51** [A] Before a keyed list, a pointer sentence names the map the labels belong
  to. With no map image, text supplies connections, dimensions of fight spaces, and
  starting positions.
- **C-S52** [U] Map symbols used in play (X, T, letters) have prose equivalents in the
  area text.

---

*Resolved. Yardstick complete; auditors apply §13 to `conversions/dnd5e/oraga_night/`.*
