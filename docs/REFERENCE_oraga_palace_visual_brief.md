# Palace Boranis: Visual Reference Brief for Maps and Images

*Oraga Night, D&D 5e edition (`conversions/dnd5e/oraga_night/`). A working brief for an
image-generation agent: site plan, floors, every keyed room, the key scenes, the cast and
the objects that matter. Drafted 2026-10-25 against the module text and the owner's
rulings TP1–TP55 (`docs/DECISIONS.md`). Not a module file. The owner approved the quiet
rooms in TP56 and the §7 extrapolations in TP64 (after the architecture review,
`docs/REVIEW_oraga_palace_architecture.md`); those approvals are for art, not module canon.
Four questions are still open (end of §7).*

---

## 0. How to Use This Brief

### 0.1 The three tags

Every statement in this brief is one of three kinds, plus two tags for approved
extrapolations. The artist may treat the first two as fixed; the third is a proposal.

- **[PRINTED]**: stated in the module or in an owner ruling (TP1–TP55). Sizes, rooms,
  objects and descriptions with this tag must not change. Where the module gives a number,
  the number is used exactly.
- **[MAP]**: a drawing choice already made for the module's schematic maps
  (`maps/build_maps.py`, recorded in DECISIONS O53–O56 and in `facts.yaml`). These are
  approximate positions the text leaves open: gallery depth, door positions, room order in
  the east wing, the gatehouse's size. Keep them, so new art agrees with the book's maps.
- **[VX]**: short for **[VISUAL EXTRAPOLATION: not in the module; for art only, owner to
  approve]**. Everything the module is silent on and the art still needs: extra wings,
  towers, the facade, the street, room sizes the book doesn't give, decor, materials, the
  overall footprint. Extrapolations are architecture, decor and scale only. None of them
  adds a person, an event, a secret or a plot object. If a [VX] detail ever seems to
  matter to the story, drop it.
- **[APPROVED TP56]**: a [VX] room the owner approved as placed in ruling TP56 (the quiet
  rooms), now printed in chapter IV, "The Rest of the Palace". Treat it as fixed, like
  [PRINTED]; its one **Detail:** line is the only story detail it may show.
- **[APPROVED TP64]**: a [VX] decision the owner approved in ruling TP64 (the fifteen items
  of §7, as amended by the architecture review). Treat it as fixed for art, like [MAP]. It
  is still architecture, decor and scale only, and it is not module canon. A [VX] tag that
  remains in the brief is either outside §7's fifteen items or one of the four questions
  still open (end of §7).

A heading marked [VX] means the whole section under it is extrapolated unless a line inside
is tagged otherwise.

### 0.2 Palette and mood

**The owner's visual anchor** (a reference image the owner keeps): a towering gothic
palace of dark violet-charcoal and grown crystal, two big towers flanking a central front,
spires, pinnacles and buttress arcs, tall pointed-arch windows, a great tall pointed window
headed by a rosette, every pane and crystal glowing hot pink to magenta from within; a
steep grand staircase about 20 feet wide climbing straight from the street to a tall arched
entrance, crystal lanterns on posts at its foot and along it; carriages waiting at street
level beside the stair foot (no ramps); night, rain, wet cobbles; half-timbered jettied
townhouses with warm amber shopfronts on both sides; guests in dark formal dress. Match it.
**Rain** is the image's, not the module's: keep it to the street plates (Scene 1, and
Scenes 2 and 14 on the same ground) if the owner wants it, and never carry it into the
gardens, the Crossing or the boat.

**What the module says about the light [PRINTED]:**

- Rekuzan's walls are grown pink crystal and glow at dusk. All the city's old crystal does.
- The palace's crystal "glows faintly after dusk", and tonight it is lit deliberately for
  the first time in two years: "lanterns in the gardens, fire in the great hearths, and the
  walls themselves shining like the inside of a shell."
- From the street: "the walls themselves are doing it, pink crystal grown course over
  course by hands two hundred years dead, holding the last of the day and giving it back."
- The Court is "a vault of rose-lit crystal"; its walls give off "a faint warmth where you
  brush them, like stone that has been in sun all day."
- In the Dead Dance the lamps come down "until the only real light is the walls, and the
  walls are the color of the inside of a shell."
- At midnight "the light goes out of the walls. Not blown out — drawn out, the rose
  draining away from the crystal like water out of a cracked basin."
- From the river at the end, the palace is "burning rose-colored behind them."

**Reconciling the two [APPROVED TP64]:** one material, pink grown crystal. Where it is
thick, unlit or seen against the night sky it reads deep violet to charcoal (the owner's
image); wherever it is thinner or lit from within it glows rose to magenta up close and from
the street. Before midnight rose leads and the dark mass supports it; up close the light is
warm and shell-like. After the drain the crystal is colorless, milky, gray-violet dead glass
everywhere; any rose after midnight is fire seen through or reflected in it, never the
walls' own glow. Ward-light is a hard white-rose. Nothing glows white or blue except as
noted for wards. Draw the palace warm, not as a horror castle: it is "the color of the
inside of a shell" until midnight.

**Mood by hour:**

| Hour | Palette | Mood |
|---|---|---|
| Dusk to Movement IV | rose and magenta crystal, amber candle and hearth light, black and jewel-toned formal dress, gold on the high table | splendor stretched thin: lavish food and music in a house that is plainly too empty |
| Movement V, the Dead Dance | lamps down; walls alone light the hall in shell-pink; faces are masks in silhouette | the most beautiful hour of the year, and the easiest to move unseen in |
| Midnight onward | crystal drained to colorless, milky gray-violet glass; candle and fire orange; smoke; sudden ward-flares | the burning building with three killers out of another age in it |
| The gardens after midnight | dark; lanterns going out one by one; the palace dark above, burning behind (any rose is firelight through dead crystal) | the open, the chase, the one collision |
| Dawn | fires out; gray light; soot on crystal | the counting |

**Ward-light [APPROVED TP64]:** the module calls it ward-fire, ward-light, light flooding stairwells,
crystal barriers sealing corridors, wards flaring over huddled guests, but gives no color.
Proposal: a hard white-rose blaze, brighter and colder than the walls ever were, with the
crystal of a sealed doorway visibly growing shut across it like frost in fast motion.

### 0.3 Scale and orientation conventions

- **Grid:** 5-foot squares, as the book's maps use. One guest per 5-foot square wherever
  the crowd is [PRINTED].
- **North:** the text names only east ("the east doors", "the east wing"). The book's
  maps put the dais end of the Crystal Court at the top and the river beyond it [MAP].
  This brief calls that direction **north**: the street and gatehouse are south, the
  gardens and river north, the east wing east. Keep that orientation on every map.
- **Coordinates:** this brief uses the book maps' own frame, in feet: x runs east, y runs
  north, and the origin (0, 0) is the south-west corner of the Crystal Court's dance floor,
  at the main-doors wall [MAP]. A table of every block's coordinates is in §1.4.
- **Elevations** are in feet above the Crystal Court floor (0).
- **Battlemaps for the VTT:** the existing art convention (`art/ART_AND_MAP_MANIFEST.md`)
  is gridless, unlabeled battlemaps, so a virtual tabletop can lay its own grid. Keep that
  for any battlemap: no grid lines, no baked-in text, numbers, keys or compass. Draw to an
  exact scale (state it in the file name or the hand-off note, e.g. 1 inch or 70 px = 5
  feet) so a grid laid on top fits. Overview plates (the isometric cutaway, the site plan)
  may carry labels if the owner wants a book plate rather than a VTT map; ask.

### 0.4 Setting rules every image must obey [PRINTED unless tagged]

- **No books, ever.** "There are no books. The Church writes; everyone else remembers."
  No bookshelves, scrolls, ledgers, open pages, quills, inkwells, letters, maps on paper,
  signage or notices anywhere in the palace. The only writing at the ball is the
  invitation cards (one of the two exceptions to the law), the Church wardens' record
  after midnight, and the Bought's contract in its chained case.
- **No lettering on the building [VX]:** no carved inscriptions, plaques, labels or name
  plates. Heraldry and memory are carried by images and crystal pattern, never by letters.
- **Records are crystal and memory.** Grown crystal holds knowledge in the Root
  (recall-lattices); households keep accounts on knotted tally-cords (the cellar
  tally-cords in B10). Scratch-work goes on a slate that is wiped (the work-slate in B8).
- **Light is crystal and fire.** The walls glow; lanterns in the gardens are crystal
  lanterns (they "burst in a line" at the Crossing); great hearths burn; candles on the
  tables and sconces. The dais's four ward-points are sconces:
  turning one is "turn a sconce" (Table V–2). Only the dais's ward-points are printed as
  sconces; draw them as crystal wall sconces brighter than the wall around them. [VX] Other
  ward-points (B7, the dark wing, the doors Raunu sealed) are never called sconces; their
  look is a proposal.
- **Humans only.** Every person in Rekuzan is human. No pointed ears, horns, tails, scales
  or non-human anatomy, on guests, staff, the Uninvited or the Attendant.
- **Masks.** On the last night of Oraga everyone wears a spirit-face: "the dead of the
  year, the spirits of the harvest, the luck and grief of the season made wearable."
  Masks are on before the gate and come off at the Unmasking (midnight), except three.
  Player characters' masks are the players' to describe and are never fixed in art.
- **Everyone is armed, discreetly.** "A knife in the sash, a slim blade along the thigh";
  stronger personalities wear larger steel openly. Nobody is disarmed. No bare steel in
  the public rooms before midnight unless it is a scene of brandishing.
- **The house is too empty.** A household of sixty is now twenty-two skeleton staff plus
  festival hires who don't know where anything is. "Whole wings are dark." Nine honor
  guards where forty would be expected. Shut rooms read dusty and shrouded [VX: dust
  sheets over furniture, unlit crystal, cold hearths].
- **The violence is never aimed at Veier on the page.** Never draw an attack on her. Never
  draw her before the Crossing (see §3 and §4).

---

## 1. The Palace as a Whole

### 1.1 Site and setting

**[PRINTED]** Rekuzan is "nine walled districts grown together." The palace stands at the
top of a hill; the street (Gate Street) climbs to it, and on the night the carriage line
"reaches down to the second gate" (a gate lower on the hill). Behind the palace, gardens
step down in terraces to a river and a modest, always-locked iron gate onto the river
walk. Vell's boat goes from there "north up the tributary to the foothills."

**[APPROVED TP64] The neighborhood.** Gate Street is steep and cobbled, lined both sides with tall
half-timbered, gabled townhouses: jettied upper storeys, steep slate roofs, warm amber
shop windows at street level (the owner's anchor). Rekuzan's own grown-crystal district
walls glow pink on the skyline behind. [VX, still open] Whether Gate Street lies inside or
outside the Boranis district's crystal walls is the owner's to confirm; the image's timber
houses stand either way. The second gate is a squat crystal gate-arch in a district wall a
few hundred feet down the hill. A narrow lane runs along each side of the palace's street
front: the **West Lane** to the stable yard and the servants' postern (carriages set down
at the stair foot and go round by it to the stable yard), the **East Lane** to the kitchen
yard gate. At the garden's foot the river runs past the river walk; Vell's boat goes
upstream, north, up the tributary toward the foothills (the tributary flows south). No river
mist, except perhaps a thin line on the water in the boat scene (owner to decide).

### 1.2 The plan in one paragraph

The core is printed: the **Gatehouse Court** behind the street gate, the **Crystal Court**
(the great hall) straight ahead of it with its two **banquet galleries**, the **gardens**
beyond the Court's far end stepping down to the river, and the **east wing** running north
along the gardens' east side at gallery level. **[APPROVED TP64]** Around that core this brief builds
a palace: a long **West Range** (the Audience Hall, its antechamber, the chapel, shut state
rooms, and on its second floor, the storey above the ground, the **dark wing** with
Raunu's study in a corner tower), a
**garden wing** mirroring the east wing on the gardens' west side (the trophy gallery
and two drawing rooms above, the lower gallery beneath, the falcon mews behind), an **East Range** behind the
gatehouse (kitchens, servants' hall, household offices, the dormitories of a staff that is
mostly gone), a **street front** of towers and a grand stair, and a ring of service
passages threading all of it. The shape is a broad **U opening north**: the Crystal Court
is the bar, the two wings are the arms, and the upper terraces lie cupped between them.

### 1.3 Overall footprint [APPROVED TP64]

- **Built footprint:** about **370 ft east–west × 290 ft north–south** (x −170 to +200,
  y −60 to +230), not counting the grand stair and gardens.
- **With the grand stair and the gardens:** about **400 × 580 ft**, some five acres, from
  the foot of the grand stair (y −150) to the river walk (y +430).
- **Height:** Crystal Court vault 50 ft inside [PRINTED]; its roof ridge about 85 ft; the
  twin towers flanking its south front about 120 ft to the parapet and 165 ft to the spire
  tips; the bell tower about 130 ft; the study tower about 110 ft; gate towers about 70 ft (95 ft with spires); wing
  turrets about 60 ft. Dozens of pinnacles on every buttress. No flèche.
- **The blocks of §1.4 do not overlap** on any one level (corrected after the architecture
  review); the footprint itself is unchanged.

### 1.4 Coordinates of every block

Feet, in the book maps' frame (x east, y north, origin at the south-west corner of the
Court floor). [PRINTED] and [MAP] rows match `maps/build_maps.py` exactly; the rest were
approved in TP56 or TP64, with the overlaps the architecture review found corrected.

| Block | x (west → east) | y (south → north) | Level | Tag |
|---|---|---|---|---|
| Crystal Court floor (B2) | 0 → 80 | 0 → 140 | 0 | PRINTED size; MAP position |
| West aisle under the west banquet gallery | −20 → 0 | 0 → 140 | 0 (gallery above at +12) | MAP |
| East aisle under the east banquet gallery | 80 → 100 | 0 → 140 | 0 (gallery above at +12) | MAP |
| Banquet galleries (B3) | −20 → 0 and 80 → 100 | 0 → 140 | +12 | rail height PRINTED; depth MAP |
| Dais | 25 → 55 | 120 → 135 | +3 | PRINTED (30 ft across, 3 ft high, ~120 ft from doors); depth MAP |
| Main doors (10 ft, double) | 35 → 45 | wall at y 0 | 0 | PRINTED width; MAP position |
| Gallery stairs (two, rising 12 ft northward, in the aisles) | −19.5 → −11.5 and 91.5 → 99.5 | 3 → 27 | 0 → +12 | PRINTED existence (WP8, T8.2); MAP position |
| Musicians' gallery, over the main doors | 0 → 80 | 0 → 15 | +12 | MAP (WP8, T8.2) |
| Ward-points by the main doors (Table V–3) | 32 and 48 | ~2 | 0 | MAP (WP8, T8.3) |
| Garden doors (two pairs, 10 ft) | 8 → 18 and 62 → 72 | wall at y 140 | 0 | MAP |
| East doors and the passage under the east gallery | 80 → 100 | 30 → 40 | 0 | MAP |
| East stair (rises 12 ft, northward) | 100 → 110 | 30 → 54 | 0 → +12 | PRINTED rise; MAP run |
| Cleared corridor | 100 → 110 | 54 → 114 | +12 | PRINTED (10 × 60) |
| East wing double doors | 100 → 110 | at y 114 | +12 | PRINTED |
| East wing corridor | 100 → 110 | 114 → 214 | +12 | PRINTED (10 × 100) |
| East wing rooms (Veier's, Raunu's, the nursery, south to north) | 110 → 135 | 118 → 148, 148 → 178, 178 → 208 | +12 | PRINTED 20–30 ft across; MAP 25 × 30 and order |
| Service stair hall, with the wing's service door at its head | 110 → 120 | 86 → 118 | 0 → +12 | MAP |
| Service run (5 ft) toward the service stair | 114 → 119 (from the kitchens, y −10 → 11); 100 → 119 (cross-leg, y 6 → 11); 100 → 105 (the plank stretch behind the east aisle, y 6 → 26); 100 → 115 (cross-leg south of the east stair's foot, y 21 → 26); 110 → 115 (beside the east stair and on, y 21 → 86) | as given | 0 | PRINTED width; MAP schematic; route APPROVED TP64 (§B10); clears the east stair and the SE Court tower |
| Garden stair (the private stair), down the wing's west wall | 93 → 99 | ~212 → ~164 | +12 → upper terrace | PRINTED; MAP position |
| B9's west wall line = the terraces' east end | x 100 | — | — | MAP |
| West wall door to B4 (double, 10 ft) | at x −20 | 56 → 66 | 0 | MAP |
| West service door (5 ft, card S11's door) | at x −20 | 96 → 101 | 0 | PRINTED width; MAP position |
| Garden walk (railed) | −20 → 100 | 140 → 150 | 0 | MAP depth (10 ft) |
| Upper terrace | −20 → 100 | 150 → 190 | −8 [APPROVED TP64 height] | PRINTED 40 × 120 |
| Second terrace | −20 → 100 | 190 → 230 | −18 | PRINTED 10-ft drop |
| Third terrace | −20 → 100 | 230 → 270 | −28 | PRINTED |
| Lower garden | −20 → 100 | 270 → 420 | −38, falling gently to −42 at the gate [APPROVED TP64] | PRINTED ~150 ft |
| River gate (iron) | 35 → 45 | at y 420 | river-walk level | PRINTED; MAP position |
| River walk and river | all | 420 → 440 and beyond | water ~4 ft below the walk [VX] | PRINTED; the tributary flows south, so upstream is north |
| Gatehouse Court (B1 / B12) | 10 → 70 | −45 → 0 | 0 | MAP (~60 × 45) |
| Gatehouse: the cell / the arch / the stair tower | 20 → 32.5 / 32.5 → 47.5 / 47.5 → 60 | −60 → −45 | gate-walk +15 | PRINTED heights; MAP plan |
| The gate (two leaves, wicket in the court-side left leaf) | 32.5 → 47.5 | at y −60 | 0 | PRINTED; MAP |
| Gate landing (head of Gate Street) | 0 → 80 | −90 → −60 | 0 | APPROVED TP64 (the Blades stand 10 ft out on it: PRINTED) |
| Grand stair (steep, about 20 ft wide; no carriage ramps; carriages set down at its foot) | 30 → 50 | −150 → −90 | 0 → −25 | APPROVED TP64 |
| Gate towers | 6 → 20 and 60 → 74 | −64 → −46 | to +70 | APPROVED TP64 |
| Court towers (SW and SE), flanking the south front | −34 → −14 and 94 → 114 | −14 → 6 | to +120 | APPROVED TP64 (the chapel and state rooms now start west of the SW tower; the East Range starts east of the SE tower) |
| Bell tower, on the east gallery's north end, clear of the east wing | 82 → 100 | 122 → 140 | to +130 | APPROVED TP56 (existence); position APPROVED TP64. Its base is the last 18 ft of the east aisle and gallery bay; the gallery's MAP extent is unchanged |
| West Range: B4 antechamber | −50 → −20 | 46 → 76 | 0 | APPROVED TP64 |
| West Range: B4 Audience Hall | −160 → −50 | 36 → 86 | 0 (ceiling ~35) | APPROVED TP64 |
| West Range: B6 Chapel (octagon), off the antechamber by a 10-ft passage | −76 → −34 | −6 → 36 | 0 | APPROVED TP64 |
| West Range: shut state rooms (ground), with the dark-wing stair rising from among them, and the dark wing (second floor) | −170 → −34 (south of y −6, west of the SW tower); −170 → −76 (y −6 → 36) | −60 → 36 | 0 and +15 | APPROVED TP56; heights APPROVED TP64 |
| Study tower (B8 on its second floor) | −176 → −146 | −66 → −36 | to +110 | APPROVED TP64 |
| West service passage (S11's door to the gallery corridor's back stair), its branch west to the servants' postern, and its link south behind the Audience Hall's dais wall | −30 → −20 (y 86 → 140); −170 → −20 (y 86 → 96); −170 → −160 (y 36 → 86) | as given | 0 | APPROVED TP64 |
| Garden wing (lower gallery below; trophy gallery B7, 30 × 40, then the two drawing rooms at the north end, above) | −55 → −20 | 150 → 214 (B7 150 → 190; drawing rooms 190 → 214) | −8 and +12 | APPROVED TP56; sizes APPROVED TP64 |
| Falcon mews and weathering yard | −120 → −55 | 150 → 230 | terrace level | APPROVED TP56 (mews PRINTED "behind the garden wing") |
| Stable and carriage yard | −170 → −60 | 96 → 150 | 0 | APPROVED TP56 |
| East Range: kitchens, sculleries, kitchen yard | 114 → 200 | −60 → −10 | 0 | APPROVED TP64 |
| East Range: servants' hall and household offices | 119 → 170 | −10 → 30 | 0; dormitories above at +30 | APPROVED TP56; heights APPROVED TP64 |
| Wine cellars / lower cellar / the Root (B11) | the wine cellars run from under the kitchens west beneath the Gatehouse Court to the Court's south end; the lower cellar under their west end; the Root beneath that, under the Court's south half | see B11 | −15 / −30 / −45 | APPROVED TP64; route PRINTED |
| Garden below the east wing (card S10) | 135 → 220 | 92 → 270 | about −5, falling north [APPROVED TP64] | PRINTED existence; MAP position |

### 1.5 Levels and how they connect

| Level | Elevation | What is on it |
|---|---|---|
| The Root (B11) | about −45 [APPROVED TP64] | the hidden laboratory, beneath the wine cellars' west end, under the Court's south half [PRINTED: "beneath the wine cellars"] |
| Lower cellar | about −30 [APPROVED TP64] | reached by "the lower cellar stair" that Anha is barred from sweeping; its far wall of living crystal holds the seam [PRINTED] |
| Wine cellars | about −15 [APPROVED TP64] | from under the kitchens west beneath the Gatehouse Court to the Court's south end [PRINTED route: kitchens → wine cellar → lower cellar stair → seam] |
| Terrace level | −8 [APPROVED TP64] | the upper terrace; the lower gallery and B13 in the garden wing; the mews (the garden below the east wing is a little higher, about −5) |
| Ground | 0 | the Gatehouse Court, the Crystal Court and its aisles, the garden walk, the Audience Hall, the chapel, the kitchens [PRINTED: the Court and its garden doors are at ground level] |
| Second floor: gallery level | +12 | the storey above the ground floor, the module's "second floor" in its American usage: the banquet galleries, the musicians' gallery [APPROVED TP64 position], the gallery corridor, the east wing (S10's lit window "on the second floor"), the trophy gallery [PRINTED for B3 and B9] |
| Second floor: the dark wing | about +15 [APPROVED TP64] | the dark wing with Raunu's study [PRINTED: "second floor, in the dark wing"], roughly level with the banquet galleries but with no door to them; reached only by the dark-wing stair from the ground-floor state rooms |
| Gate-walk | +15 | the walk over the gate arch [PRINTED] |
| High gallery | about +30 [APPROVED TP64 height] | the high gallery above the Crystal Court [PRINTED existence]; the empty servants' dormitories above the East Range's tall kitchens and hall |
| Towers | +45 and up | tower rooms, bell chamber, spires [APPROVED TP64] |

**Why the terraces sit below the Court [APPROVED TP64, reconciling two printed facts]:**
the Court's garden doors open on a railed walk at ground level and "the upper terrace lies
below that rail," by a height the book never gives. Card S10 says the wall from the garden
below the east wing up to a lit window is 20 feet of grown crystal, while the wing's floor
is 12 feet above the Court. Both are true if the hill falls away north and east: the upper
terrace lies about **8 feet below** the Court (so the garden stair falls 20 feet from the
wing's corridor), and the garden below the east wing about **5 feet below** the Court, so
the wing's lit window (sill about 3 feet above the +12 floor) is 20 feet above that garden,
as card S10 prints. The wing's gallery level is the "second floor" S10 names, in the
module's American usage. Draw the walk's rail as a waist-high balustrade over an 8-foot
retaining wall, with flights down at either end.

**Stairs and passages:**

- **Public stairs [PRINTED since WP8, T8.2]:** two grand stairs from the Court's south corners
  (beside the main doors, in the aisles) up to the banquet galleries and the musicians'
  gallery. Chapter V's General Features now prints them ("a stair in each aisle at the
  main-doors end"), with the galleries as a mezzanine over floor-level aisles; map VIII–3
  draws them.
- **The east stair [PRINTED]:** from the Court's east doors, a stair rises 12 feet to the
  cleared corridor and the east wing.
- **The service stair [PRINTED]:** "beside" the east wing's double doors; it carries the
  wing's service door at its head and runs down and out to the garden below the wing.
- **The garden stair [PRINTED]:** the east wing's private stair, from the far end of the
  wing's corridor down the wing's outer (west) wall to the upper terrace.
- **The dark-wing stair [PRINTED existence; APPROVED TP64 position]:** the stair the Church
  wardens come down after midnight. It rises from among the ground-floor shut state rooms
  (TP56's clean path through their dust leads to it) to the dark wing on the second floor
  (+15). It has no door to the banquet galleries.
- **The gallery corridor [PRINTED existence; APPROVED TP64 position]:** the private corridor B7 is
  off. Place it at gallery level, running west then north from the west banquet gallery's
  north end into the garden wing.
- **The lower gallery [PRINTED existence; APPROVED TP64 position]:** B13 is off it. Place it at
  terrace level beneath the gallery corridor, with a narrow stair up into B7.
- **The terrace stairs [PRINTED]:** each terrace has a stair at either end down to the
  next. Two flights also go down from the garden walk to the upper terrace [MAP].
- **The service passages [PRINTED]:** "thread the whole palace, including the east wing and
  the garden stair." 5 feet wide, "one lamp in three", one stretch with a wall to the Court
  "one plank thick." See B10 for the approved route.
- **The cellar stairs [PRINTED order; APPROVED TP64 positions]:** kitchens → wine cellars
  (west, under the Gatehouse Court) → the lower cellar stair at their west end → the sealed
  seam → the Root.

### 1.6 Site plan (north up; schematic, not to scale)

```
               ~ ~ ~ THE RIVER (the tributary, flowing south; upstream is north) ~ ~ ~     N
   ..............................river walk...........[RG]...........................     ^
                 |                                                  |   :
                 |                LOWER GARDEN                       |   :  GARDEN
                 |       about 150 ft from the third terrace          |   :  BELOW THE
                 |              to the river gate                    |   :  EAST WING
                 |                                                  |   :  (dark beds;
                 |===st=========== balustrade, 10-ft drop ======st===|   :   card S10;
                 |   THIRD TERRACE           40 x 120 ft             |   :   about -5)
                 |===st=========== balustrade, 10-ft drop ======st===|   :
     FALCON      |   SECOND TERRACE          40 x 120 ft             |   :
     MEWS   +----+                                                  +---+---+
            |GARD|===st=========== balustrade, 10-ft drop ======st===| E | t |
            | EN |   UPPER TERRACE  (lawn)   40 x 120 ft         gs <| A | u |
            |WING|                                               gs <| S | r |
            |    |===st=st========= rail, ~8-ft drop =====st=st======| T | s |
            | B7 |   GARDEN WALK  (10 ft deep, ground level)         |   |   |
   STABLE   +----+---[gd]---------------------------[gd]-------------| W |   |
   YARD     |    |  W  |                                     |BELL | I | R |
            |WEST|  E  |              CRYSTAL COURT  (B2)    |  E  | N | O |
            |SVC |  S  |   dais (30 ft, 3 ft high) at north  |  A  | G | O |
   +--------+PASS|  T  |                                     |  S  |   | M |
   | AUDIENCE    |     |       dance floor 80 x 140 ft       |  T  |B9 | S |
   | HALL (B4) [ante]--|          vault 50 ft                |  B3 |   |   |
   |             |  B3 |                                     | +12 +---+---+
   +-------------+ +12 |                                     |     |svc stair
   |  CHAPEL B6  |     |                                     |[east doors]->east stair
   |  (octagon)  |     |                                     |     | -> cleared corridor
   +-------------+-----+-----------[main doors]--------------+-----+
   | STATE ROOMS |[SW tower]   +------------------+   [SE tower]|  EAST RANGE
   | (shut), the |             | GATEHOUSE COURT  |             |  servants' hall,
   | dark-wing   |             | (B1; B12 after   |             |  offices; KITCHENS
   | stair; dark |             |  midnight) 60x45 |             |  and kitchen yard
   | wing above; |             +--[cell][arch][stair]-----------+
   | STUDY TOWER |          [gate tower]  GATE  [gate tower]
   +-------------+                                                     East Lane
     West Lane                      GATE LANDING
                          GRAND STAIR (steep, about 20 ft wide)
                carriages set down at the stair foot, then round by the West Lane
                              G A T E   S T R E E T   (down the hill)
                       half-timbered townhouses, amber shopfronts (owner's anchor)
                                 ... the second gate, far below
```

Legend: `gs <` the garden stair down the east wing's west wall; `[gd]` garden doors; `st`
terrace stairs; `[RG]` river gate; `+12` gallery level (the second floor); `BELL` the bell
tower on the east gallery's north end; `WEST SVC PASS` the west service passage behind the
Court's west wall (S11's door opens into it). The kitchens are in the East Range, behind the
gatehouse (B10). Not shown: the wine cellars run from under the kitchens west beneath the
Gatehouse Court to the Court's south end, and the Root lies beneath their west end, under the
Court's south half (B11). Everything outside the printed core is [APPROVED TP56] or
[APPROVED TP64].

### 1.7 Floor adjacency diagrams

**Ground (0) and terrace level (−8):**

```
 [Gate Street] -> (grand stair) -> [gate landing] -> GATE/wicket -> [arch]
                                                                      |
     [the cell]--(door)--[GATEHOUSE COURT B1]--(door)--[gatehouse stair]--> gate-walk (+15)
                                  |
                           [MAIN DOORS, 10 ft]
                                  |
 [chapel B6] -- [B4 antechamber] --(west door)-- [CRYSTAL COURT B2] --(east doors)-- passage under
       \            |                 |                |      |                  east gallery
        \      [AUDIENCE HALL B4]     |           (garden doors)  \               -> EAST STAIR (+12)
         \                     (west service door, S11)     |      \
     [state rooms, shut]              |              [GARDEN WALK]  (plank-thin wall)
                               [west service passage]       |        \
                                  |         \        (flights down)   [SERVICE RUN, 5 ft]
                       [servants' postern]   \              |              |
                         -> West Lane     [south cross-passage]   [UPPER TERRACE] -> terraces -> lower garden -> RIVER GATE
                                               \                     ^
                                         [KITCHENS B10] ----------  (garden stair foot)
                                          |        \
                                   [wine cellars]  [kitchen yard -> East Lane]
                     (west, under the Gatehouse Court, to the Court's south end)
                                          |
                     (lower cellar stair, at their west end) -> [lower cellar] -> (seam) -> [THE ROOT B11]

 West Range: [state rooms, shut] --(TP56's clean path)--> (dark-wing stair up) --> [THE DARK WING, second floor, +15]

 Terrace level, west: [upper terrace]--[lower gallery]--[B13 door]--[service run branch]
                                              |
                                   (narrow stair up into B7)
 Terrace level, east: [garden below the east wing, about -5] <- (door at the foot of the service stair)
```

**Second floor: gallery level (+12):**

```
   [WEST BANQUET GALLERY B3]--[musicians' gallery over the main doors]--[EAST BANQUET GALLERY B3]
   (wine court, alcoves)                                      (alcoves at its north end only; bell tower base)
              |
   [gallery corridor] --> [TROPHY GALLERY B7] --> [two drawing rooms]       EAST STAIR (from the east doors)
                          (garden wing)          (wing's north end)                  |
                                               [CLEARED CORRIDOR 10 x 60] --(door)-- [service stair]
                                                         |                                |
                                              [DOUBLE DOORS: guarded; seal at midnight]   |
                                                         |                                |
                                    [EAST WING CORRIDOR 10 x 100] --(wing's service door)-+
                                     |-- Veier's rooms (shut door; never entered)
                                     |-- Raunu's rooms
                                     |-- the nursery
                                     `-- (far end) door -> GARDEN STAIR down the west wall -> upper terrace

   No door joins the banquet galleries to the dark wing.
```

**Second floor: the dark wing (+15); the high level (+30) and above [APPROVED TP64 except where tagged]:**

```
   [shut state rooms, ground] --(dark-wing stair up)--> [THE DARK WING: shut apartments, shrouded, +15]
                                                                   |
                                     [STUDY TOWER: B8 Raunu's study, PRINTED "second floor, in the dark wing"]

   [HIGH GALLERY above the Crystal Court, +30, PRINTED existence] -- along both long walls and across
              |                                                        the north end, above the dais
   [Court tower stairs]        [BELL TOWER stair]        [East Range dormitories above the kitchens, mostly empty]
```

---

## 2. Area by Area

*Each entry: purpose · size and shape · exits · surfaces and light · furniture and features ·
mood · before and after midnight · who is there · fight-card terrain · items of interest.
Positions of people come from Tables VIII–2, VIII–6 and VIII–7.*

### B0. Gate Street, the Approach and the Line

**Purpose [PRINTED]:** where play begins. The party walks up the hill among everyone else
invited, hired or smuggled in; the line to the gate is "the best gossip hour of the year."

**Printed facts:**
- "The street climbs the hill, and so does everyone in it: carriages, sedan chairs, people
  on foot in their best, all going the same way, all masked already." Music reaches them
  before the gate does. The carriage line reaches down to the second gate.
- At the top "the whole palace is lit," the walls themselves glowing.
- In the line: the Thenya delegation, "the only non-Orthaen faces in fifty," waiting with
  thinning patience, two of them with slings at their belts; a footman selling a genuine
  invitation card with a scorched corner and someone else's name on it, in an undertone;
  every great house's hired swords idling at the edge of the court "in unmatched colors";
  nine honor guards on the gate, **every one facing inward**, toward the palace doors.
- A little apart from the carriages stands the Attendant, a cloak folded over one arm,
  staring at the road behind the party, unblinking, as if someone is expected. It moves
  with the line, and nobody comes (TP30).
- Card S3's ground: Gate Street directly outside the gate, where three Bought Blades will
  stand "in a loose line across Gate Street, 10 feet out from the gate" after midnight.

**Size and shape [APPROVED TP64]:** Gate Street is about 30 feet wide between house fronts,
cobbled, climbing at a stiff grade. At the top it reaches the **gate landing** (80 × 30 feet,
the head of Gate Street), a level paved apron before the gatehouse. The landing is reached
from below by a steep **grand stair** about 20 feet wide, rising 25 feet in about 60 feet,
with heavy balustrades and **crystal lanterns on posts** at its foot and up both sides,
matching the owner's image. It is one stair in one hand and one style. There are **no
carriage ramps**: carriages set down at the stair foot and go round by the West Lane to the
stable yard. At night the stair is the focal approach, its wet steps throwing back the
magenta of the facade.

**Surfaces and light [APPROVED TP64; rain is the owner's image, street plates only]:** wet black cobbles; rain; the townhouse shopfronts warm amber
(lamplit windows of chandlers, vintners, mask-sellers); the palace above glowing hot pink
through the rain; lantern crystals on the stair posts pink-white. Carriages with black
lacquer and brass lamps; sedan chairs; horses steaming.

**The facade seen from the street [APPROVED TP64]:** at the stair head the **gatehouse
arch** is the tall arched entrance of the owner's image: a pointed arch 15 feet wide [MAP]
under the gate-walk (15 feet up [PRINTED]), flanked by two slender **gate towers** with
crystal spires. The stair does not run into the Court's main doors: the Gatehouse Court lies
hidden behind the arch, and the Court's **south front** rises above it, about 85 feet to its
peak, with a **great tall pointed window of grown tracery headed by a rosette**, glowing
magenta. The front is flanked by the twin **Court towers**, 120 feet to their pierced
parapets and 165 to their spire tips. Beyond them, the spires and pinnacles of the wings and
the bell tower at the Court's north-east corner. Buttress arcs down the Court's flanks, each
with a crystal pinnacle. All of it is grown, not cut: facets and growth lines, no mortar
joints, no carved figures or gargoyles. Each wing may show a slightly different crystal
habit, since each was one ancestor's working life. No flèche. To the left the long West
Range with the study tower at its corner; to the right the lower East Range with its kitchen
chimneys.

**Before midnight:** dusk going to night; the line; masked guests in dark formal dress,
jewel-toned linings, crystal pins; liveried footmen; hired swords loitering in unmatched
colors. **After midnight:** the gate is shut from the street side; matched gray coats on the
landing; the city beyond is burning in two districts (fires on the skyline, orange under
the clouds) [PRINTED: fires in two sect districts and the Blackwatch courier post, out in
the city]; at the end, sect guard banners come up Gate Street.

**Who:** everyone arriving; Corval at the head of the line (B1); the Attendant apart; Vell
already inside (nobody saw him arrive).

### B1. The Gatehouse Court (and B12, the same court after midnight)

**Purpose [PRINTED]:** where invitations are presented by name against Corval's memory.
"There is no written list." Nobody is disarmed. After midnight (B12) the Bought hold the
gate from outside, and two hundred guests pile up against it.

**Size and shape:** about **60 × 45 feet**, open to the sky, its north side the Crystal
Court's south wall with the 10-foot main doors in the middle [MAP]. The **gatehouse** closes
its south side: **40 × 15 feet**, the cell on one side of the arch and the gatehouse stair
on the other [MAP]. The gate opening is **15 feet**, two tall leaves "with a grille at head
height," a **wicket** 5 feet wide in the left leaf (left as seen from the court) "with its
own small grille" [PRINTED; MAP for the side]. **The bar** is on the street side; "nobody
lifts that bar from the court" [PRINTED].

**Heights [PRINTED, card S3 and O53]:** the **gate-walk** runs 15 feet above the ground over
the arch. A door in the court side of the gatehouse opens on the **gatehouse stair**,
ladder-steep and one body wide, which turns at a **landing 5 feet up**; a creature shoved
from the top falls 10 feet to the landing. A second stair runs down from the walk to the
street along the street face. From the walk it is a **15-foot drop** to the street.

**Surfaces and light:** "The court's crystal wall, lit" is Bright Light [PRINTED, S3]: the
court is the brightest place outdoors, and anyone in it is silhouetted to the street.
[VX] The court walls are tall grown crystal, deep violet where it is thickest at the base,
glowing rose above; a ring of crystal lanterns on posts; a paving of dark stone with a rose-crystal
inlay in a radiating pattern leading to the main doors. The **cell** [PRINTED: where a
detained guest wakes, "without mask or invitation"]: a bare 12-by-15-foot room with a crystal
grille, a bench, no window to the street.

**Before midnight:** the line comes in under the arch; Corval at a small lectern-less post
inside the arch [VX: no lectern, no list, nothing written] greeting each guest by name;
nine honor guards facing inward. Steady, stately, crowded. **Movement V:** a sergeant's
runner of the Bought, in the festival crowd, looking over the ground [PRINTED].

**After midnight (B12) [PRINTED, card S3]:** the outer gate "shut from the far side."
"Through the grille: matched gray coats, more of them than there are of you, arranged with
the unhurried spacing of people who have done this before. One of them is holding a chained
case up where you can see it, the way you would hold a lantern, and he is reading aloud."
The sergeant at the wicket, reading through its grille; three Blades in a loose line across
Gate Street, 10 feet out; the fourth on the gate-walk. The court packed with frightened
guests (one per 5-foot square: the court holds about a hundred, and the rest of the two
hundred are packed back into the Crystal Court behind them), smoke drifting out of the main
doors behind them; the bells
of Oraga tolling; the city's fires red on the clouds. When the gallery fire reaches the
Court's doors, the crowd's back is to the heat [PRINTED: the fire clock].

**Terrain (S3) [PRINTED]:** the grille gives Three-Quarters Cover; the lit crystal wall
silhouettes both sides; the gatehouse stair with its landing; the crowd is Difficult
Terrain.

**Items:** the contract case (chained at the sergeant's hip; §5); the half-burned
invitation card being sold in the line (B0).

### B2. The Crystal Court

**Purpose [PRINTED]:** the grand hall, "the room where nearly every scheduled event
happens: dance floor, musicians' gallery, the high table on its dais." Its walls are the
palace's oldest work.

**Size and shape [PRINTED]:** about **140 feet long and 80 feet wide under a vault some
50 feet high.** The **main doors (10 feet wide)** are at one end, the **dais (3 feet high,
30 feet across)** at the other, about **120 feet** from them. The **banquet galleries**
run the length of both long sides, their **rails 12 feet above the floor**. The **east
doors** open on a stair rising **12 feet** to the east wing. The **garden doors** open on
the Court's railed garden walk, at ground level. [MAP] The dance floor is the full
80 × 140 feet, clear; the galleries stand outside it, 20 feet deep each, so the Court with
both galleries is 120 feet across, the width of the terraces. The dais is 15 feet deep. The
garden doors are two 10-foot pairs in the dais-end wall, one each side of the dais. The east
doors are about 30 feet from the main-doors end of the east wall, through a passage under
the east gallery. The west wall carries the double door to the Audience Hall (around 56–66
feet from the main doors) and the 5-foot service door (around 96 feet).

**Architecture [APPROVED TP64]:** a gothic hall in three tiers, all grown crystal (grown,
not cut: facets and growth lines, no mortar joints, no carved figures).
- *Ground:* the dance floor, a single sweep of polished crystal paving, rose-veined, with a
  great radiating pattern converging on the dais. Along each long side, a row of seven
  clustered piers on the floor's edge line carries the galleries; behind them the shadowy
  **side aisles** at ground level (20 feet deep, 11 feet high under the gallery floor),
  where guests step out of the dance. No piers stand on the dance floor itself.
- *Gallery level (+12):* the banquet galleries open to the hall through the arcade above the
  piers, a waist-high crystal rail between each pair of piers.
- *High gallery (about +30):* a narrow walkway (5 feet wide) in the wall thickness above
  the banquet galleries along both long walls and across the north end above the dais,
  behind a screen of tracery. This is "the high gallery above the Crystal Court" where Raunu
  is glimpsed in Movement III [PRINTED existence; APPROVED TP64 form].
- *Upper windows and vault:* tall windows of clearer, brighter crystal above the high
  gallery (the walls are the light; windows are where the crystal is thinnest, never holes
  in a dark wall); a ribbed crystal vault, 50 feet at the crown [PRINTED height], the ribs
  carrying the glow up into a starburst boss over the floor's center. The great tall pointed
  window headed by a rosette fills the south front above the main doors, seen from inside
  behind the musicians' gallery. The north wall above the dais: three tall lancets.
- *The musicians' gallery [PRINTED existence; APPROVED TP64 position]:* a grown crystal
  balcony at gallery level over the main doors, spanning between the two banquet galleries,
  15 feet deep; "dancers under a gallery of musicians."
- *Hearths [PRINTED "fire in the great hearths"; APPROVED TP64 position]:* two great hearths
  in the side aisles, mid-hall, hooded in dark crystal.

**The dais and high table [PRINTED]:** "a high table on a dais at the far end, laid and
canopied and empty." [MAP, T8.3] Map VIII–3 draws the two ward-points of Table V–3 inside
the main doors, one each side. Four ward-points on the dais, shown as sconces [PRINTED: "turn a
sconce"]. The high table carries table linen, candles, plates; the canopy can be pulled down
(Table V–2). [VX] The canopy: a tall baldachin of rose-violet silk on four slender crystal
posts, fringed; the high table a long board of dark wood with crystal inlay, laid in white
linen and gold; one great chair at its center for the host; the four ward-sconces stand two
each side, crystal brackets holding fist-sized shaped crystals that glow brighter than the
walls.

**Light and sensory [PRINTED]:** rose-lit crystal; the walls warm to the touch "like stone
that has been in sun all day"; music from the gallery; two hundred masked guests. [VX]
Candles in standing candelabra along the aisles; the smell of beeswax, wine, roast meat
drifting from the galleries; the floor faintly reflecting the vault's glow.

**Before midnight, by Movement:**
- *I–II:* the ball proper; dancing; Vorlain holding court by the wine; the high table empty
  under its canopy [PRINTED].
- *III:* the summonses; a still figure on the high gallery, gone when looked for [PRINTED].
- *IV:* the banquet called; Raunu standing at the high table, unmasked, plainly dressed,
  holding a cup; the toast; the two plates; out by the east doors [PRINTED].
- *V, the Dead Dance:* lamps lowered "until the only real light is the walls," shell-pink;
  slow, strange music; two hundred spirit-faces turning in the gloom; a bell striking the
  quarter somewhere above [PRINTED]. Corro and his bodyguards against a wall, facing out.
- *Midnight:* the east doors open; Raunu mounts the dais; masks come off in a wave of
  laughter and candle-relight, except three [PRINTED].

**After the lights die [PRINTED]:** "The light goes out of the walls... the rose draining
away from the crystal like water out of a cracked basin, from the far end of the hall toward
you. The music stops in pieces." The hall is Dim Light, candles and fire only. The double
doors at the head of the east stair boom shut somewhere above. The Wept crosses toward the
dais "not running, arriving." The Hollow at the main doors, the crowd breaking around him
"like water" and not passing. Lanterns going dark along the gallery one by one "like a fuse
burning" (the Radiant going east). Raunu on the dais snapping wards alight, "spending his
house's stored centuries like coin"; seven honor guards dying or falling around the dais.
The canopy may come down; the high table may be tipped; fire in the linen [Table V–2]. A
rectangle of lamplight opens on the west side: the 5-foot service door, two big men in it
with blades out (S11). [APPROVED TP64] The drained crystal looks like dead glass: colorless, milky,
violet-gray, every reflection gone; the vault is suddenly a black cave above the candles.
Ward-flares throw hard white-rose light in bursts around the dais.

**Who:** see Table VIII–6: Vorlain (I, IV), Corro (all night, worse each Movement), Kovaun
(II, IV), Draunel (I, IV), Corval (IV), Sella (IV), the Uninvited at the edge (III), the
Radiant dancing "where the light falls" (V), the Attendant at a crystal wall (II), following
the music (IV), at the edge of the Dance watching the party (V).

**Fight-card terrain:** S11 (the Phern door: the crowd prones people; the 5-foot door is
one at a time and silhouetted in lamplight); S13 spills from B3; the dais tricks
(Table V–2).

**Items:** the four dais ward-sconces; the canopy; the high table; Raunu's two wrist
crystals; the folded cloak the Attendant sets down "on the nearest table" at midnight.

### B3. The Banquet Galleries

**Purpose [PRINTED]:** "Long feast halls flanking the Court, tables groaning with harvest
excess, where the real conversations happen in alcoves built for the purpose." The B3
"wine court" is where Draunel's duelists and Essin's blades jostle. The seating feud (S1)
and, after midnight, the fire and Vorlain's rescue (S13) happen here.

**Size and shape:** two halls, each running the Court's full **140 feet**, **20 feet deep**
[MAP], their floors at **+12** with a **waist-high rail over a 12-foot drop** into the Court
[PRINTED, S1]. [APPROVED TP64] Ceiling about 14 feet, ribbed. In the west gallery's outer
wall, six deep **alcoves** (about 8 × 10 feet), each a half-octagon bay with a crystal window
and a cushioned bench, half-curtained. The east banquet gallery has no alcoves and no doors
in its outer wall south of y 114, where the east stair and cleared corridor run behind it;
its alcoves sit in its north end or within its 20-foot depth (screened bays on the gallery
floor). The bell tower rises from its last 18 feet at the north end. The **wine court** [PRINTED name; VX form]: a wider bay at the north end of
the west gallery, 20 × 25 feet, with the wine tables and great crystal decanters.

**Furniture [PRINTED]:** fixed, crowded **benches** (S1: Difficult Terrain); long tables;
harvest food; table linen. [VX] Trestle tables end to end under white linen, mounded with
harvest: whole roast fowl, breads shaped as wheat sheaves, pyramids of fruit, wheels of
cheese, crystal bowls of preserves, pitchers; candles in crystal holders every few feet;
autumn garlands of wheat, apples and dried flowers along the rail.

**Before midnight:** noise of two hundred guests ("covers almost anything" [PRINTED, S1]);
the Circle and Corro comparing margins in an alcove; Maiven pressing Corval; Vorlain
watching the audiences; the Radiant's antique blessing over the food (IV); the Wept watching
the young pages a beat too long [PRINTED].

**After midnight [PRINTED]:** "The banquet gallery is burning, and smoke fills the galleries
under walls gone dark." Heavily Obscured beyond 10 feet; fire at the far end; overturned
tables (Half Cover); guests on the floor. Vorlain, "his sleeves pushed up and soot to the
elbows," carrying a guest out over his shoulder (S13). [VX] Which gallery burns: the west
one, from its north end (the wine court), the fire running south along the linen and
garlands; the east gallery fills with its smoke.

**Fight-card terrain:** S1 (benches; the rail and its 12-foot fall into the crowd); S13
(fire DC 13; smoke; overturned tables; guests on the floor; "the fire never finishes
anyone").

### B4. The Audience Hall (and its antechamber)

**Purpose [PRINTED]:** "The room where Orthaen chiefs have always received the ruled, on a
dais that generations of petitioners wore down." Raunu's summonses in Movement III, through
a screen of ministers "so thin it is almost an invitation." A waiting line outside, rivals
comparing masks and nerve. Kovaun waits in "the B4 antechamber."

**Printed description:** "A vast crystal chamber off the Court, lit for the first time in
two years — you can tell, because the light finds dust in the air that nobody has had
reason to disturb. A dais, worn down its center. One chair." And when walked in: "The hall
is bigger than it needs to be and almost entirely empty. Crystal walls, unlit at the edges,
throwing back a little of the light from the door behind you. A dais at the far end, worn
smooth down the middle where several centuries of people have knelt. One chair on it.
Somebody is sitting in the chair, and the length of the room is between you and them."

**Size and shape [APPROVED TP64]:** the **antechamber** is a 30 × 30-foot vestibule entered from the
Court's west double door, with a bench along each wall for the waiting line and a door south
to the chapel. The **hall** runs west from it: **110 feet long × 50 feet wide**, ceiling
about 35 feet, a ribbed crystal barrel vault. The dais at the far (west) end: 20 feet
across, 4 feet high, five broad steps worn into a shallow trough down their middle; one
high-backed chair of grown crystal and dark wood. No other furniture at all. Crystal walls
lit only near the door and over the dais, dark in between, so the walk is from light, through
dimness, into light. Dust motes in the beams.

**The screen [PRINTED existence; VX form]:** a pair of ministers at a low folding screen of
pierced crystal just inside the door, vetting each supplicant: a formality nobody pretends
is a barrier.

**Mood:** "quiet in the particular way of a room that a great many people are deliberately
not entering." The long walk is the scene.

**The rest of the West Range [APPROVED TP56; heights APPROVED TP64]:** shut state rooms on the
ground floor, with the dark-wing stair rising from among them (TP56's clean path leads to
it); the dark wing on the second floor, the storey above the ground floor (about +15,
roughly level with the banquet galleries but with no door to them).

**After midnight [VX]:** dark and empty; nothing happens here in the printed attack.

### B5. The Garden Terraces and the River Gate

**Purpose [PRINTED]:** "Lantern-strung gardens stepping down to the water, ending at a modest
iron gate to the river walk, which is always locked. Couples, conspirators, and anyone
needing air." Agenda 6 and the escape route: **Court → terraces → lower garden → river
gate.** The duel (S9), the quiet word (S6), the Crossing.

**Sizes [PRINTED]:** **three terraces, each about 40 feet deep and 120 feet wide**, stepping
down from the Court's garden doors. Each ends at a **waist-high balustrade over a 10-foot
drop** to the next, **with a stair at either end**. Below them **the lower garden runs about
150 feet to the river gate.** The Court's garden doors open on the Court's **railed garden
walk** at ground level; the upper terrace lies below that rail. The **garden stair** comes
down the east wing's outer wall to the upper terrace.

**Layout [MAP]:** the garden walk is 10 feet deep across the full 120-foot width; two flights
go down from it to the upper terrace near each end. The terraces' stairs are 6-foot flights
at the east and west ends. The river gate is centered in the far wall, on the river walk.
The garden stair descends along the terraces' east edge (the wing's west wall) from north
to south, landing on the upper terrace.

**Printed ground detail:** lanterns leave **pools of Dim Light** between them and "tick" in
the cold (S6, S9); **gravel paths** (S9); **flower beds** off the gravel (Table V–5); the
terrace **balustrade** (smashed by the duel at the Crossing); **crystal lanterns** along the
terrace that go out one after another and burst in a line at the Crossing; the falconry
**mews** "behind the garden wing" erupt in Movement IV (TP34). The gardens are "cold after
the Court."

**Garden design [APPROVED TP64]:**
- *Garden walk:* a broad paved promenade at the Court's foot, its balustrade of dark crystal
  with rose-crystal finials, crystal lanterns on the newels; the "rail crowd" watches the
  duel from here (S9).
- *Upper terrace (−8):* an open lawn, the duelling ground of S9 ("anyone on the grass";
  Draunel "will not set foot on the grass"), framed by gravel paths and low flower borders
  of late roses and autumn asters against the balustrades; crystal lanterns on poles, with
  smaller lanterns on cords strung between. No hedges on the lawn. The foot of the garden
  stair is at its north-east corner.
- *Second terrace (−18):* a parterre of low clipped beds around a gravel cross, with stone
  benches against the retaining wall.
- *Third terrace (−28):* an orchard walk of pleached apples (ripe for Oraga), gravel
  between.
- *Lower garden (−38):* a looser garden: a central gravel path straight to the river gate
  between deep flower beds, clumps of ornamental trees, a few lanterns that stop short of the
  gate, so the last stretch is dark. High garden walls of crystal on both sides.
- *River gate:* a modest wrought-iron gate, about 8 feet wide and 9 feet high, in a 12-foot
  wall [VX sizes; MAP draws a 10-foot opening], an old lock [PRINTED: DC 15 with Thieves'
  Tools], steps down to the **river walk**: a paved quay along the water, mooring rings.
  No river mist.
- *Retaining walls:* each 10-foot drop is a battered wall of dark crystal, rose-glowing
  faintly at its coping, with climbing roses.

**Before midnight:** lanterns lit, couples and conspirators; in Movement II, Vell walks the
gardens once; in Movement V he stands a while at the river gate, alone [PRINTED]. In
Movement V the duel on the upper terrace (S9: two young men with coats off, seconds behind
them, a knot of masks at the walk's rail looking down).

**After midnight:** dark terraces, lanterns going out one after another as the Radiant comes
out of the smoke; the duel tearing the garden apart; the boat at the river walk; the palace
"burning rose-colored" above and behind: firelight through dark, drained crystal, not the
walls' own glow (see scenes 10 and 11).

**Fight-card terrain:** S6 and S9 (balustrade drop 1d6, out of the scene; lantern pools;
gravel Disadvantage on Stealth; the rail crowd sees everything); the Crossing sidebar (flying
crystal, collapsing stonework, gaps, stairs gone); Table V–5 (relight the garden stair; push
the broken balustrade onto the stair; through the beds; shut the river gate; push the boat
off; grapple him in the shallows).

### B6. The Chapel

**Purpose [PRINTED]:** where Raunu and Veier were married; Mother Sella's all night; the only
Short Rest at the ball. Kovaun summons characters here.

**Printed description:** "Eight niches, one for each god, and the grandest of them is
Fraden's as it is everywhere. The room smells of cold wax and old smoke. Seven of the niches
hold what a house this rich would be expected to leave in them." The eighth, **Elanna's**
(the death-goddess the northern tribes honor), holds **fresh offerings, tended recently and
with care**; in Movement IV the Wept leaves a mourner's offering there in a rite centuries out
of date.

**Size and shape [APPROVED TP64]:** an **octagon about 40 feet across**, one niche in each of the eight
walls (the entrance is cut through the base of one wall beneath its niche), ceiling a ribbed
crystal dome 35 feet high with a small oculus. Floor of dark crystal with a rose inlay star.
Niches 6 feet wide, 9 feet high, each a pointed arch. **Fraden's niche** faces the door,
twice the size of the others, with the richest offerings [VX: gilt harvest sheaves, crystal
vessels, banked candles]. **Elanna's niche** [VX look of the offerings, nothing more]: small,
plain, on the north side; a few fresh flowers, a bowl of grain, a single lit candle, a folded
piece of dark cloth. Benches around the walls. No inscriptions, no icons with lettering.

**Mood:** cool, quiet, cold-wax smell, low candlelight; "a good place for the characters to
catch their breath." Sella sits here "calm as deep water."

**After midnight [VX]:** candles still burning; a few frightened guests sheltering.

### B7. The Trophy Gallery

**Purpose [PRINTED]:** "The house's pride and plunder: banners, weapons, and grown crystals
taken in old settlements, including a heart-sized soul-crystal of uncommon beauty (Agenda 5).
Warded by old crystalwork," with **three of the nine honor guards** here from the end of
Movement I until Movement V (Table VIII–7). "The gallery's case" holds old soul-crystals
(Tavva's target). It is in the private palace, "off the gallery corridor." Its wards gutter at
midnight; two of Tavva's knives hit it.

**Size and shape [APPROVED TP64]:** a long hall in the garden wing at gallery level, **30
feet wide × 40 feet long**, ceiling 22 feet, a ribbed crystal vault. Entered from the
gallery corridor at its south end; the two shut drawing rooms lie beyond it at the wing's
north end (TP56: "beside the trophy gallery"); a narrow stair in its north-west corner goes
down to the lower gallery. Tall lancet windows on the east side look over the terraces.

**Contents:**
- [PRINTED] **Banners** of old settlements and old wars, hung from the vault ribs [VX: faded,
  some scorched, none with lettering, devices only].
- [PRINTED] **Weapons** on the walls [VX: racks of spears, curved swords, axes, a few great
  two-handed blades, all old].
- [PRINTED] **Grown crystals taken in old settlements**, and **the gallery's case** of old
  soul-crystals [VX: a long, low case of crystal panes on a dark plinth down the hall's
  center, a dozen or so palm-sized soul-crystals on dark velvet, each glowing faintly].
- [PRINTED] **The grandmother's soul-crystal** (§5): heart-sized, "a lifetime of light in a
  lattice the size of a heart," on its own ward. [APPROVED TP64] It stands alone at the far
  (north) end on a slender crystal pedestal, on its own old ward: generations-old crystalwork
  on its pedestal, not a ring of Raunu's. Draw no ring in the floor. Where "a gallery ring of
  Raunu's own work" is, if anywhere, is the owner's to decide.
- [PRINTED] **Wards** "teachable": light, seals, alarms. [VX] Ward-points as crystal sconces
  between the windows; the three guards stand by the door and the pedestal.

**Mood:** a museum of other people's grief; trophies of conquest "like a hunting prize."
After midnight [PRINTED]: "The gallery's wards are guttering, its guards are dying on the
dais"; Tavva's knives stripping the case. [VX] Glass broken, banners torn down, a ward-sconce
sputtering.

**Who:** three honor guards (I–V); Tavva's scout walks the B7 corridor in Movement III; the
Agenda 5 character studying wards.

### B8. Raunu's Study

**Purpose [PRINTED]:** "Locked, dark wing, second floor." The lock is **crystal, not iron**
(an Orthaen with the gift can work it, TP54). "Two years of a genius's solitude. The characters
will look for papers and find none, because there are none anywhere: the room thinks in
crystal." The Church wardens work its lock in Movement V (S8).

**Printed contents (TP38: no drawer of invitations, no papers, no hearth of scorched cards):**
- **The instruments.** "Nobody can name them."
- **The great table.** "A grown relief of the eastern coast, its mist-lines remembered in
  colored lattice. The recent lines have been reworked many times." It gives Half Cover; it
  is grown and cannot be carried out.
- **The work-slate.** "A half-erased lattice diagram: temporary scratch-work." It is the
  Root's key.

**Approach (S8) [PRINTED]:** "The dark wing's corridor is cold after the Court, and the only
light in it is at the far end, a thin line of it under a door that ought to be dark." In
Movement V two figures in gray robes kneel at the door; one holds a small crystal against the
lock "the way you wait for a kettle."

**Size and shape [APPROVED TP64]:** a corner tower room on the second floor (about +15) of
the study tower (the West Range's south-west corner), **30 × 25 feet** plus a 10-foot window
bay looking west over the city, ceiling 18 feet. The great table fills the room's center:
about **14 × 7 feet**, waist-high, a single grown slab whose top is the coast in relief (§5).
The work-slate on a low stand by the window. The study has no shelves and no fireplace: the
instruments stand on a long grown bench along the north wall and on ledges grown out of the
wall. A plain chair, a stool. No bed: Raunu's cot is in the east wing, and the study is a
workroom.

**Light and mood:** dark wing, cold corridor; inside, the faint glow of the great table's
lattice lines (colored threads of light across the relief) and of the instruments; otherwise
dark. A room that feels thought in, not lived in.

**After midnight [PRINTED, Table V–7]:** the wardens coming down the dark-wing stair with a
written record of the mist map, the slate wiped behind them.

**Fight-card terrain (S8):** the dark corridor (Darkness except the lamplight at the door);
the crystal lock; the great table's Half Cover; instruments that break with a sound
"nobody can name."

### B9. The East Wing: the Living Quarters

**Purpose [PRINTED]:** "Sealed, guarded, forbidden." Raunu and Veier's private quarters,
where the midwife attends Veier near her time. The ring errand (Agenda 4) is done at its
doors; the way inside is Undercurrent C or force. After midnight the Radiant hunts through
it; the household moves Veier ahead of him.

**Sizes [PRINTED]:** "The wing is upstairs, at gallery level: a stair rises 12 feet from the
Court's east doors, and the cleared corridor at its head is about 60 feet long" and **10 feet
wide**. "Behind the doors, one 100-foot corridor" (**10 feet wide**) "has the rooms off it"
(**each 20 to 30 feet across**), "with the private stair (the garden stair) at its far end,
running down the wing's outer wall to the upper terrace." The **service stair** beside the
double doors carries **the wing's service door** at its head and runs down and out to the
garden below the wing [MAP/PRINTED]. [MAP] Rooms on the corridor's east side, each 25 × 30
feet, in order from the doors: **Veier's rooms, Raunu's rooms, the nursery.** The wing's west
outer wall lines up with the terraces' east end.

**The approach [PRINTED]:** "Double doors, closed, with guards on them who are plainly not
there for show. The corridor in front of them has been cleared of furniture. Nobody is walking
down it." Two guards on the doors (four from Movement V). [VX] The cleared corridor: crystal
walls glowing low, pale rectangles on the floor where furniture stood, a long runner rolled
against the wall. The doors: tall, paired, grown crystal leaves with bronze-dark crystal
fittings, 10 feet wide.

**Inside [PRINTED]:** "Warm light, a midwife's quiet traffic, and one door kept shut:
Veier's own." The household keeps that door closed, "courteously and absolutely." **Her room
is never entered and must not be illustrated inside** (TP53). Only two finds:

- **Raunu's rooms.** "Nearly bare: a soldier's cot in a palace." Two personal objects only: a
  small, flawed, badly grown crystal, decades old, on the sill where the light finds it (his
  first, grown at six); and, side by side, **Veier's worn border sling** and **a second sling,
  new, its knots clumsy, re-tied many times.** [VX] The room 25 × 30, crystal walls glowing
  warm, a narrow camp cot with a plain wool blanket, one chair, a washstand, nothing on the
  walls; the two slings hung together on a single peg (or laid together on the chair) near
  the window with the little crystal.
- **The nursery.** "Newly and beautifully made, fresh paint and cedar, a mobile of grown
  crystal turning slowly over the crib." [VX] Cedar-paneled lower walls, freshly painted upper
  walls in a soft warm color, a cedar crib in the middle under the mobile, a low chair, a
  chest of small linens (the "small, soft, new-hemmed" linens of Undercurrent C). No
  lettering, no painted names. Do not add toys that tell a story (no rocking horse unless the
  owner approves; it isn't printed).

**Corridor [VX]:** warm-lit, crystal sconces, a long rug; the shut door of Veier's rooms
nearest the double doors; at the far (north) end a door onto the head of the garden stair.

**After midnight [PRINTED]:** only the double doors seal at the lights (TP28); the service
stair and the garden stair stay open. The Radiant hunts "through corridors that lock
themselves behind her (Raunu's last gift, working)"; the inner doors lock behind Veier one by
one on Raunu's last charge. Unlit corridors are Darkness; "nobody sees him without a light."
Characters come in by the service stair or the garden stair; Corval guides some of them.
Maiven goes toward the wing and dies in its corridor unless someone competent goes with her.
The household moves Veier "a door ahead of him"; nobody reaches her here (TP13, TP40).

**Fight-card terrain:** S4 (the cleared corridor; two guards, four more coming); Table V–4
(hold a sealed door; drag furniture back into the cleared corridor; the service door; kick
through the plank wall in the run; the wrong stair).

### The garden below the east wing (card S10)

**Printed [S10]:** "Below the east wing the lanterns stop short, and the garden is dark except
for one lit window on the second floor." Flower beds (Difficult Terrain); "the wall is 20 feet
of grown crystal to the window"; the lit window "is somebody's room. Anyone who reaches it
sees warm light, a quiet household holding its breath, and nothing that looks like a prison."
The slingers stand under it with a rope and a weighted end. [MAP] On the wing's east side,
around the corner of the building from the terraces. [APPROVED TP64] The garden lies about 5
feet below the Court floor (§1.5), so the wing's lit window (sill about 3 feet above the +12
floor) is 20 feet above it, as card S10 prints. The wing's gallery level is the "second
floor" S10 names, in the module's American usage. Do not identify whose window it is.

### B10. Kitchens and Service Passages

**Purpose [PRINTED]:** "Understaffed chaos, festival hires, and the skeleton staff of two
silent years, Anha among them." The passages "thread the whole palace, including the east
wing and the garden stair" and at midnight are "the only unwarded way through the palace."
Staff hires and a turned-away guest "slip in through the kitchens."

**Printed detail:** "Through the service door the kitchen is roaring — every pot on, every hand
busy, the second course going up" (S7). The **service run**: **5 feet wide**, "one lamp in
three," doorways and stacked trays (Three-Quarters Cover), the wall to the Dance "one plank
thick" (S2, S7), crates of table linen (S2), lowered service lamps. The wing's service door at
the far end of the run, "a narrow door... that has a guard's lantern burning on the other side
of it." The cellar **tally-cords**: knotted cords counting what goes down the lower stair.
Supplies have gone down for two years: candles by the crate, lamp-oil, and once a salt-packed
crate from the eastern coast that hissed (Undercurrent A).

**Kitchens [APPROVED TP64]:** in the East Range, behind the gatehouse: a vaulted kitchen about **50 ×
40 feet**, two roaring hearths with spits and cauldrons, a long scrubbed center table, copper
pans, bread ovens in the side wall, a scullery and a pastry room off it, a kitchen yard with a
gate onto the East Lane (the way the festival hires came in). The cellar stair goes down from
the kitchen's west end. The kitchens are hot, loud and amber-lit: the one room in the palace
lit by fire more than crystal.

**Servants' hall and offices [APPROVED TP64]:** beside the kitchens: a long servants' hall with tables
laid for sixty and used by twenty-two (most places bare), Corval's office (a desk with no
papers, tally-cords on pegs, a slate), the linen room, the laundry.

**The service passages [APPROVED TP64 route, consistent with S2, S7, S11 and map VIII–5]:**
a ring:
1. From the kitchens north between the SE Court tower and the servants' hall, then west
   along the tower's north face to the outside of the Court's east wall; on the stretch
   behind the east aisle, south of the east stair's foot, the wall to the Court is an old
   doorway boarded with a single plank screen (the plank-thin wall). This is "the service
   corridor behind the Dance."
2. East round the foot of the east stair and on north beside it to the foot of the
   **service stair**, which climbs to the wing's service door and also opens down onto the
   garden below the wing.
3. A branch continues along the outside of the east wing, under its rooms, to the garden
   stair's foot (the passages "reach it too").
4. From the kitchens west along a **south cross-passage** behind the Gatehouse Court and
   beneath the gate towers' range into the West Range's shut state rooms, then north behind
   the Audience Hall's dais wall to a cross-passage between the Audience Hall and the stable
   yard. That cross-passage has the **servants' postern** into the stable yard and so to the
   West Lane (how Corro's bodyguards get people out), and runs east to the **west service
   passage** behind the Court's west wall, where the 5-foot service door (S11) opens. The west
   passage runs on north to the gallery corridor's back stair and to the lower gallery (B13's
   way in).
All 5 feet wide, low vaulted (8 feet), plain crystal gone dull with handling, not plaster;
one small crystal lamp in every three niches, worn flagstones, doors with iron latches,
stacked trays and linen crates in the bays.

**After midnight, outside [PRINTED numbers; VX, still open]:** the Bought hold more than the
gate: sixteen Blades, four at the gatehouse and twelve on the perimeter. That perimeter lies
outside the lanes and gates; what it does at the servants' postern and the kitchen-yard gate
is the owner's to decide, and no art should show it.

**Mood:** "understaffed chaos"; the music through the wall "a pulse without a tune." After
midnight [PRINTED]: Anha leads people out through them; smoke and dark that slow everyone
else; Darkness except where a ward flares; Corval leading his household out through
the kitchens (TP58).

**Fight-card terrain:** S2 (dim, linen crates, plank wall, noise clock); S7 (5 feet wide, one
abreast; one lamp in three; the guarded service door).

### B11. The Root of the House (with the wine cellar and lower cellar)

*TP8, TP17, TP18, TP47: the Root is Raunu's hidden gift-research laboratory, the
strongest-warded place in the palace, and a trap, not a refuge. Guests can shelter there
because the Uninvited go only where their errands are; one that enters is caught. The
Attendant walks in and out unaffected. Raunu never knew it caught them.*

**The way down [PRINTED]:** kitchens → **wine cellar** → **the lower cellar stair** (Anha is
barred from sweeping it; "nothing is down there but wine") → the far wall of the cellar,
"older than the rest: living crystal, faintly warm, with a seam in it that is not a crack."
The seam is a **door**, "grown, not locked"; Thieves' Tools find nothing to work on; it does
not scratch; *Knock* fails. The lattice diagram from the study's slate, traced on the seam,
opens it.

**Cellars [APPROVED TP64]:** the wine cellars, about **60 × 40 feet** at −15, run from
under the kitchens west beneath the Gatehouse Court to the Court's south end: low barrel
vaults of dark crystal sweating faintly, racks of bottles and great casks, tally-cords hung
at the door. The lower cellar stair, narrow and steep, goes down at their west end to the
**lower cellar** at −30: a long, narrow vault (15 × 70 feet) beneath the wine cellars' west
end, more casks, colder, the floor stone, ending in the **living-crystal wall**: glassy, warm
to the touch, rose-glowing very faintly from deep inside, unlike every other wall down here,
with a fine vertical seam like a closed eyelid. Beyond the seam a short stair of grown
crystal descends to the Root.

**The Root [PRINTED]:** "Beneath the wine cellars, behind a seal of living crystal, lies the
oldest place in Rekuzan: the chamber where the first Boranis ancestor grew the first crystal
of the palace, centuries of house rising from this one root." The find: "Raunu's true
workshop, and it is beautiful: no torture-vault, no horror. A grown-crystal chamber lit from
within." Its contents (§5 has each in detail): racks of **recall-lattices**; **one lattice that
speaks** (Raunu's dry voice); **instruments** of glass and lattice that read the gift, and
beside them **a chair with a wide armrest, a stool, and a lap-blanket of Thenya wool folded
over its back**; **the skeleton** on a stone bier in an alcove "the lamplight has to be
carried into," fine crystals grown through every bone; **dated observation lattices**, months
of them, the latest the finest; **the coast in crystal**, a relief of the eastern shore with
four centuries of mist-lines; and at the center **the crystal orrery of two family trees**,
with the repeated figure of two streams falling into one pool woven into its base. "Candles
by the crate, lamp-oil" went down for two years.

**Size and shape [APPROVED TP64]:** the Root lies at about −45, beneath the wine cellars'
west end, under the Crystal Court's south half (the Court's walls are "the palace's oldest
work," grown up from it). A **rotunda about 50 feet across**, domed 30 feet high, its walls a
single continuous growth of crystal that rises from a central **root-node** in the floor
(owner to confirm the root-node's look; the proposal is the first crystal as a column of
dense, ancient crystal as thick as a cart, flowing up and out into the walls and dome like
the roots of a tree turned upside down). The orrery stands on a low plinth before the root-node. Around the
walls, radiating bays: the recall-lattice racks (six bays of floor-to-vault racks of glowing
lattice plates); the instrument bay with the chair, stool and Thenya blanket; the coast relief
on a long grown table; the observation lattices in a single dated row on a ledge; and, opposite
the stair, the deep **skeleton alcove**, dark until a lamp is carried in. Candles and oil lamps
on the floor and ledges: Raunu's working light, because the crystal's own glow is soft.

**Light and mood:** "lit from within," soft rose-white glow from every surface; quiet; warm;
beautiful and devotional; the stillest room in the palace. At midnight it is "the
strongest-warded place in the palace" [PRINTED]. [VX, still open] Whether the Root keeps its
glow after the drain is the owner's to decide; until then, draw it after midnight lit by
Raunu's candles and lamps.

**Who:** nobody but Raunu, ever, before tonight; a dozen sheltering guests if a party brings
them after midnight; the Attendant, unaffected; an Uninvited, if lured across the threshold,
held in a sudden cage of light until the last bell.

### B12. The Gatehouse Court, Held

See **B1** for the place and **scene 13** (§3) for the image. Printed sizes and posts are card
S3's: the gate-walk 15 feet up, the 5-foot wicket in the left leaf, three Blades 10 feet out
across Gate Street, the fourth on the walk, the sergeant at the wicket.

### B13. The Room You Put Here

**Printed:** "Somewhere off the lower gallery there is a door this module does not open. It is
on the palace diagram, it is reachable from B7 and from the service run, and it is yours."
Deliberately empty: the DM fills it.

**For the artist:** draw only **the door**, closed, in the lower gallery, and an **empty room
shell** behind it (about 20 × 25 feet [VX], one window, bare walls). Never furnish it, light a
fire in it or put anything in it: whatever it holds is the DM's to decide, and it must not
contradict chapter II.

### The rooms the brief adds [APPROVED TP56 unless tagged otherwise]

These exist for the palace to feel like a palace. All are shut, dark and shrouded unless noted
(a household of sixty cut to twenty-two). None holds anything that matters to the story. The
owner approved them as placed (TP56), and the module now prints them in chapter IV, "The Rest
of the Palace". Each approved room has at most one ordinary detail, given below as
**Detail:**; draw that detail and nothing more. Rooms TP56 lists as "no detail" have none.

- **The lower gallery** [APPROVED TP56; no detail] (garden wing, terrace level −8): a vaulted walk 10 feet wide and 60
  feet long under the trophy gallery and the drawing rooms, plain crystal piers, cold, one lamp; B13's door on its
  west side; a narrow stair up into B7; a door to the service passage at its south end.
- **The gallery corridor** [APPROVED TP64; not in TP56] (+12): 10 feet wide, from the west banquet gallery's north end west
  then north into the garden wing; crystal sconces, long unlit lengths, a few covered busts on
  plinths (no lettering).
- **The garden wing** [APPROVED TP56] (−8 and +12): 35 feet wide, mirroring the east wing on
  the gardens' west side, ending in a turret over the second terrace. Upper floor: the trophy
  gallery (30 × 40) and, beyond it at the wing's north end, two shut drawing rooms with dust
  sheets and cold hearths. Lower floor: the lower
  gallery, store rooms. **Detail (drawing rooms):** tall windows looking straight down the
  terraces to the river gate.
- **The falcon mews** [APPROVED TP56] (behind the garden wing, terrace level): a long, low
  range of crystal-and-timber with barred openings, perches, a sanded weathering yard with
  blocks. The falcons scream and fall silent in Movement IV (TP34). **Detail:** hooded falcons,
  uneasy all night; after the Movement IV omen every bird sits silent facing the garden route.
  The falconer's lodge beside it [APPROVED TP56; no detail].
- **The stable and carriage yard** [APPROVED TP56] (north-west of the West Range, off the
  West Lane): coach-houses, stalls, a pump, grooms of the guests' carriages waiting. Rarely
  visited in play. **Detail:** the guests' grooms with the carriages, trading the ballroom's own
  rumors (nothing new).
- **The West Range ground floor** [APPROVED TP56]: besides B4 and the chapel, a suite of
  **state reception rooms** (a long salon 80 × 30 feet with shrouded chandeliers of crystal, a
  smaller music room, a dining hall laid with dust sheets), dark tonight. **Detail (the shut
  state rooms):** two years of dust, except one clean path walked straight through toward the
  dark-wing stair. The music room and dining hall have no detail.
- **The dark wing** [APPROVED TP56] (West Range, second floor, about +15, with no door to the
  banquet galleries; reached by the dark-wing stair from the shut state rooms): a long corridor of shut
  apartments (former guest suites and the old household officers' rooms), furniture under
  sheets, crystal walls dimmed, dust on the floor showing two years of nobody; the study tower
  at its south-west end. **Detail:** at the far end, the one door kept free of dust, the
  study's (in Movement V, lamplight under it [PRINTED]).
- **The East Range** [APPROVED TP56]: kitchens, servants' hall, offices and laundry at ground
  level (east of the SE Court tower); above, the servants' dormitories, rows of stripped beds for the thirty-eight who were
  sent away, and the few slept-in cots huddled by the stair.
  - **Detail (servants' hall):** a table laid for 22; aprons on pegs; the duty rota on knotted
    cords by the door, where Corval's cord alone has an extra knot at the east-wing tray hour.
    Knots only: no writing, no marks that read as letters.
  - **Detail (dormitories):** a bowl of carters' tokens by the door, full and unused for two
    years. Plain tokens, no writing.
  - **Detail (laundry):** among the table linen, small soft new-hemmed cloths no ball needs
    (the printed Undercurrent C linen spark).
- **The towers** [APPROVED TP56]: gate towers (guard rooms, the gatehouse's upper chamber [no
  detail]); the twin Court towers (spiral stairs to the high gallery and the roof leads, empty
  upper rooms [no detail]); the bell tower (the house bell: "somewhere above, a bell strikes a
  quarter" is printed, and TP56 places its rope here); the study tower; the wing turrets.
  **Detail (bell tower):** the quarter-bell rope and a view over the city; in Movement V the
  first fires show in two districts at the quarter-bell (the Bought's contract task 1, B12).
- **The roofscape** [APPROVED TP56 as a place, no detail; its materials APPROVED TP64]: steep roofs of thick crystal tiles reading dark,
  crystal ridges, crestings of rose crystal, buttress arcs, a forest of grown pinnacles each
  tipped with a glowing crystal finial. No flèche.


---

## 3. Key Scenes for Illustration

*Each brief is ready to hand to the image model. "Must" items are printed or ruled; "must
not" items protect canon. Costume and architecture beyond the printed facts follow §1–§2 and
§4 and are [APPROVED TP64] unless tagged [VX].*

### Scene 1. The Street Approach (Movement I, dusk into night)

- **Composition:** low, wide, from the foot of the grand stair looking up Gate Street's last
  stretch; the steep stair (about 20 feet wide) and its lantern posts lead the eye to the
  tall gatehouse arch; the Crystal Court's south front and its great rosette-headed pointed
  window tower above, flanked by the twin Court towers; spires, pinnacles and buttress arcs
  against a dark, rain-heavy sky (rain is the owner's image). Townhouses frame both edges.
- **Focal point:** the glowing gatehouse arch and the great pointed window stacked above it.
- **Lighting:** the palace glowing hot pink to magenta from within, every window and spire
  tip lit; amber shopfronts left and right; crystal lanterns on the stair posts; wet cobbles
  and steps reflecting both colors; the last blue of dusk at the horizon.
- **People:** a slow crowd climbing: carriages setting down at the stair foot, sedan chairs, guests on foot in
  dark formal dress with jewel-toned linings, all **masked already** in spirit-faces
  (stylized faces of the dead, harvest spirits, luck and grief: wheat, leaves, bone-white
  faces, gilt tears, moons). A cluster of plainly dressed hired swords in unmatched colors
  idling at the landing's edge. Music implied by a lit gate.
- **Mood:** a whole city going up a hill to see a recluse; splendor and nerves.
- **Must:** everyone masked; the glow coming from the walls themselves; nine honor guards
  visible at the gate, all **facing inward** toward the palace (tiny, but there).
- **Must not:** any lettering or banners with writing; any non-human figure; Veier; Raunu;
  the three gray masks (they arrive later, in Movement III).

### Scene 2. The Receiving Line: Corval, and the Attendant Apart (Movement I)

- **Composition:** three-quarter view from the gate landing toward the arch. The line runs
  diagonally from foreground into the arch; at its head, just inside the arch in the lit
  Gatehouse Court, Corval greets a masked couple. In the left foreground, a little apart from
  the carriages and not in the line, the Attendant stands still, a cloak folded over one arm,
  staring past the viewer down the road "the way a servant watches a door when someone is
  expected."
- **Focal points:** Corval (center-distance, lit) and the Attendant (foreground, in shadow,
  its stillness against the moving line).
- **Lighting:** the Gatehouse Court's lit crystal wall makes the arch a bright pink
  rectangle; the landing outside is darker, rain-glossed; the Attendant lit only by a
  carriage lamp.
- **People:** Corval: a thin, upright old man in Boranis livery, steady hands, nothing in
  them, no list, no paper; greeting each guest by name. The nine honor guards in chain and
  shields lining the court, all facing inward. Masked guests, some hands on concealed knives
  by habit. The Thenya delegation in the line, plain border wool, two with slings at their
  belts, the only non-Orthaen faces, counting guards on the east side of the court. A footman
  passing a card in an undertone (optional).
- **Mood:** stately, crowded, deniably wrong.
- **Must:** the Attendant **apart** and **not in the line**, cloak over one arm, empty other
  hand, unblinking stare at the road; Corval greets from memory.
- **Must not:** a cup or goblet on the Attendant (TP30 cut it); anyone giving up a blade;
  a written guest list, lectern or ledger.

### Scene 3. The Crystal Court Ball (Movement II)

- **Composition:** high, wide view from the musicians' gallery over the main doors, looking
  north down the 140-foot hall toward the dais. Dancers fill the floor; the banquet galleries
  run along both sides at the 12-foot rail, crowded and lit; the empty canopied high table on
  its dais at the far end.
- **Focal point:** the empty high table under its canopy, small and bright at the vanishing
  point, with the whole ball turning in front of it.
- **Lighting:** rose-lit crystal everywhere: walls, piers, the ribbed 50-foot vault glowing
  shell-pink, brightest in the tall upper windows; candle stands and the two great hearths
  adding warm amber in the side aisles.
- **People:** about two hundred masked guests in dark formal dress; dancers in sets; servants
  in livery threading through with trays (too few of them); musicians in the gallery in the
  foreground; small knots of politics: an iron-gray woman and a small merry man in an alcove;
  young men laughing a little too near a ring of cousins.
- **Mood:** real splendor, the finest food, wine and music of the festival, in a house that is
  visibly too empty: stretched-thin staff, dark doorways.
- **Must:** dais at the far end; galleries along both sides at the rail; the high table **laid,
  canopied and empty**.
- **Must not:** Raunu or Veier; the three gray masks (they arrive in Movement III); bare steel;
  books or writing; pillars standing on the dance floor (the floor is clear; piers stand on its
  edges).

### Scene 4. Raunu's Summons in the Audience Hall (Movement III)

- **Composition:** from just inside the antechamber door, looking down the length of the
  110-foot hall [APPROVED TP64 length]; two masked characters (player characters, so keep their faces and
  masks generic or in silhouette) have just stepped in and stand small in the doorway light.
  The hall is long, tall and almost empty. At the far end, a dais with steps worn down their
  middle, one chair, and a figure seated in it.
- **Focal point:** the seated figure at the far end, framed by the only other light in the
  room.
- **Lighting:** light from the door behind the characters spills a short way; the crystal walls
  "unlit at the edges, throwing back a little of the light"; dust motes in the air; a pool of
  glow over the dais. Darkness between.
- **People:** the two characters; Raunu in the chair, distant; at the door, a minister at a thin
  pierced screen (optional).
- **Mood:** "the length of the room is between you and them." Silence as a test.
- **Must:** the worn dais, one chair, the vast emptiness, the long walk.
- **Must not:** a close-up of Raunu's face here [VX recommendation: the module never says
  whether he is masked during the summonses; keep him too distant to tell]; guards in the hall;
  furniture.

### Scene 5. The Toast and the Two Plates (Movement IV)

- **Composition:** from the west banquet gallery's rail, looking down and along at the dais.
  The galleries and floor are full of seated, masked diners frozen mid-movement, every head
  turned toward the high table. On the dais, Raunu stands alone at the high table, filling two
  plates himself, carefully.
- **Focal point:** Raunu's hands and the two plates.
- **Lighting:** full banquet light: candles along every table, crystal walls rose, the high
  table's candles brightest; a hush you can see.
- **People:** Raunu Boranis: **unmasked**, "plainly dressed for a chief," a cup set down beside
  him, filling two plates, "taking his time about it, the whole hall dead silent." The guests:
  two hundred masks turned to him; a Prelate in vestments very still; an iron-gray woman
  recalculating; a young-faced noble drinking (Vorlain, masked). The east doors (on the east
  wall, nearer the main doors) waiting.
- **Mood:** two years of silence ended by a man feeding someone. Tender, strange, and to the
  room, ominous.
- **Must:** Raunu unmasked and plain; two plates; total silence in posture.
- **Must not:** Veier; a third plate on the high table (the third tray is Corval's, carried
  separately, TP31); anyone eating.

### Scene 6. The Dead Dance (Movement V)

- **Composition:** on the floor among the dancers, eye level, a slow turning figure of couples
  in near-dark; in the foreground a character's hand taking a warm, sure hand out of the dark;
  the partner is the tall gray mask with carved tears (the Wept).
- **Focal point:** the two joined hands and the Wept's carved-tear mask, half lit.
- **Lighting:** "The lamps come down until the only real light is the walls, and the walls are
  the color of the inside of a shell": soft pearly pink from the walls only, faces reduced to
  masks in silhouette; a bell striking the quarter somewhere above.
- **People:** dancers in spirit-masks, all anonymous; the Wept dancing "flawlessly, in a style
  generations out of fashion"; elsewhere, a mirror-bright mask dancing beautifully where a
  patch of wall-light falls (the Radiant, optional, background).
- **Mood:** the most beautiful hour of the Val'loh year; tender, sad, intimate; "you dance like
  my daughter would have."
- **Must:** lamps lowered; walls the only light; gray masks among the colorful spirit-faces;
  the Wept gentle.
- **Must not:** menace; weapons; any figure showing their face.

### Scene 7. The Unmasking: the Moment the Light Drains (Movement VI, midnight)

- **Composition:** from the middle of the Court floor facing the dais, wide. Raunu on the dais
  mid-sentence, looking once toward the east wing. Around the viewer, a sea of just-unmasked
  faces, masks in hands. The rose light is draining out of the crystal **from the far end of
  the hall toward the viewer**: the vault and north wall already dead glass, the near walls
  still glowing. "In the last of the light, three faces are still masked": the tallest (the
  Wept) in the crowd toward the dais; the mirror-bright mask (the Radiant) near the east side
  of the hall; the blank mask (the Hollow) toward the main doors behind the viewer (out of
  frame in this composition; reverse it to show him). Nobody has moved yet: the Wept's
  crossing, the Hollow's post at the doors and the Radiant's vanishing (the gallery lanterns
  going dark one by one toward the east) come a breath later and belong to a follow-on image.
- **Focal point:** the line where the glow ends, crossing the room like a tide, and the three
  masks in it.
- **Lighting:** half the hall pink, half dead gray-violet glass lit by candles; faces lit from
  below by candles; a fuse of dying lanterns along the east gallery.
- **People:** Raunu, unmasked, plainly dressed, the cup set down, his hand going to his wrist,
  not startled; two hundred guests turning; musicians stopping "in pieces"; on the nearest
  table, a **folded cloak set down neatly**, and beside the three gray masks the Attendant,
  facing the room, empty-handed, looking "at the spaces between the room and the three."
- **Mood:** the breath before the scream.
- **Must:** the drain moving far end → near end; exactly three masks still on; the folded
  cloak; Raunu's hand at his wrist.
- **Must not:** blood; anyone already attacked; Veier.

### Scene 8. Raunu's Last Stand on the Dais (Movement VI)

- **Composition:** low angle at the foot of the dais. Raunu stands on it, working: one arm out
  as a wall of white-rose ward-crystal grows between the Wept and the fleeing crowd; the high
  table overturned; the canopy down and burning at one edge. The Wept comes through the last
  barrier, arriving, not running. Raunu holds up the second small crystal from his wrist and
  looks once more toward the east wing.
- **Focal point:** the crystal in Raunu's fist, the instant before he crushes it.
- **Lighting:** dark hall, candle and fire; violent ward-flares around the dais; the four
  ward-sconces blazing in turn.
- **People:** Raunu, "magnificent," commanding the burning room; honor guards in chain and
  shield falling at the frame's edges (seven die or fall here; keep them peripheral and
  undramatized); a character at his side turning a sconce at his word ("the third sconce —
  turn it — NOW"); the Wept: tall, gray carved-tear mask, formal dress of an antique cut,
  bare hands, the tears perhaps beginning to run (if Bloodied); guests fleeing past.
- **Mood:** the recluse nobody saw all night, spending his house's stored centuries like coin.
- **Must:** Raunu choosing the doors over himself; the Wept unarmed (her weapons are her
  hands).
- **Must not:** Raunu's death shown; gore; the Wept looking monstrous (she is a person).

### Scene 9. The East-Wing Chase (Movement VI)

- **Composition:** down the 10-foot-wide, 100-foot east-wing corridor from behind the pursuers.
  A character holds up a light (lantern or crystal); in its circle stands the Radiant,
  slowed, turning to pose for his witnesses, mirror-bright mask throwing the light back. Beyond
  him, far down the corridor, a door is sealing itself shut with growing crystal. Side doors
  along the right (east) wall; one, nearest the double doors, firmly shut.
- **Focal point:** the Radiant caught in the light, savoring.
- **Lighting:** Darkness except the pursuer's light and the sealing door's ward-glow; warm
  household sconces dead.
- **People:** the Radiant, courtly, beautiful even now, posing; two or three characters with
  the light (or Maiven's slingers watching, optional); no household visible except perhaps a
  shadow beyond the sealing door.
- **Mood:** a hunt slowed by being watched; every second bought is a hallway.
- **Must:** the light making him Witnessed; doors sealing ahead; the narrowness.
- **Must not:** Veier visible; anyone touching or escorting her; the inside of her room; the
  Radiant attacking a woman.

### Scene 10. The Crossing: Vell and the Radiant on the Terrace (Movement VI)

- **Composition:** wide, from the second terrace looking back up toward the upper terrace and
  the palace. On the upper terrace, Vell and the Radiant meet: crystal lanterns bursting in a
  line, the balustrade going to gravel, force tearing the flower beds. In the foreground, on
  the stair down from the upper terrace, the party carries or supports Veier toward the lower
  garden and the river gate. The east wing's wall and the garden stair rise at the right;
  above everything, the palace, its crystal drained dark everywhere, burning in places, the
  rose only firelight through dead glass.
- **Focal points:** two: the collision above (Vell's stillness against the Radiant's motion);
  the party with Veier below.
- **Lighting:** dark terraces, lanterns going out one after another behind them; bursts of
  crystal light from the duel; fire glow from the palace windows. No mist.
- **People:** **Vell**: tall, pale, in a trade factor's plain good clothes, moving "the way the
  gray masks move, arriving instead of running," bare-handed, **the enormous broadsword still
  wrapped in white cloth on his back**, untouched. **The Radiant**: mirror-bright gray mask,
  formal antique dress, bare hands, in wary, hating recognition ("...You."). **Veier**: upright
  though wounded across the ribs, heavily pregnant, in plain Thenya border wool, moving with
  blunt determination, one arm over a character's shoulders or carried. The characters: their
  own looks (keep generic).
- **Mood:** two powers the mortal world has no answer for, and the people carrying history in
  their arms down a garden being demolished behind them.
- **Must:** sword wrapped and on his back; Vell holding the Radiant; the party with Veier;
  the smashed balustrade.
- **Must not:** Vell drawing or gripping the sword; any attack aimed at Veier; a visible gory
  wound (a dark stain at her side, hand pressed to it, is enough); names or explanations.

### Scene 11. The Boat at the River Gate (Movement VI)

- **Composition:** from the river walk just outside the open river gate, looking out over the
  water. A small fisher's rowing boat pulling away into the dark: a pale man rowing hard, a woman
  bent over her own heartbeat in the stern. In the shallows, the Radiant stands knee-deep,
  stopped "as if hooked through the spine," watching the boat. At the gate behind, the
  characters (one holding the gate, or lying where they stood in his way). Above and behind, up
  the terraces, the palace "burning rose-colored" (fire through drained crystal).
- **Focal point:** the boat leaving the light.
- **Lighting:** dark water (at most a thin line of mist on it, if the owner wants); the
  palace's fire glow, rose and orange through dead crystal, reflected in the river; the boat
  passing into gray.
- **People:** Vell at the oars (sword on his back); Veier; the Radiant in the shallows; option:
  the Wept at the water's edge "carved tears catching the fire-light," watching, not pursuing.
- **Mood:** escape, loss, the leash about to take him "gone east with the mist."
- **Must:** a small boat with one rower; the boat going upstream, north, up the tributary
  (away from the viewer; the tributary flows south, toward the viewer); the palace burning
  behind.
- **Must not:** a large or four-oared boat; anyone else in the boat; any attack.

### Scene 12. The Burning Banquet Gallery (Movement VII)

- **Composition:** inside the west banquet gallery at gallery level, looking toward its burning
  north end. Smoke thick beyond ten feet; overturned tables; guests crawling along the floor
  toward the stairs. In the foreground, Vorlain Boranis, sleeves pushed up and soot to the
  elbows, comes out of the smoke with a guest over his shoulder and sets her down against the
  wall "with a care that looks strange on him."
- **Focal point:** Vorlain and the rescued guest.
- **Lighting:** fire-orange from the far end, smoke-diffused; dead crystal walls reflecting the
  fire dully; the rail open on a dark, smoky Court below.
- **People:** Vorlain (unmasked after midnight; silk, a blade at his hip, his brother's face);
  guests, unmasked, sooty, shielding strangers; optional, two men in good coats closing round
  him (S13, if Draunel's heat is high).
- **Mood:** "people are brave"; the night's strangest hero.
- **Must:** smoke, fire at the far end, overturned tables, guests on the floor.
- **Must not:** burning bodies; the fire killing anyone (it "never finishes anyone").

### Scene 13. The Gate Held by the Bought (Movement VII)

- **Composition:** from inside the packed Gatehouse Court, over the heads of the crowd, toward
  the shut gate. Through the grille: matched gray coats spaced across the landing; at the
  wicket's small grille, the sergeant holding up a chained case "the way you would hold a
  lantern," reading aloud. A fourth Blade on the gate-walk 15 feet above. Behind the gate, the
  city burning on the skyline.
- **Focal point:** the sergeant's face and the chained case at the wicket grille.
- **Lighting:** the court's lit crystal wall throws hard pink light on the crowd's backs and
  silhouettes the Bought beyond the grille; fire glow on the clouds; smoke rolling out of the
  main doors behind the crowd.
- **People:** the Bought (sixteen Blades in the company, four sergeants and a captain in all;
  here, the sergeant and three or four Blades): gray wool cut plainly, the company's mark at
  the shoulder, cudgels and company blades, unhurried; the sergeant with the case chained at
  his hip; the crowd of unmasked guests, servants, retinues; a character at the wicket.
- **Mood:** the one antagonist who can be talked to; the contract settles more arguments than
  the sword.
- **Must:** gate shut, bar on the street side; wicket in the left leaf (left as seen from the
  court); gray coats; the chained case.
- **Must not:** any writing legible on the contract; a bronze tablet or indenture plate (it is a
  case of writing); two hundred people inside the gatehouse court (it holds about a hundred
  at one per 5-foot square; the rest are in the Court behind).

### Scene 14. Dawn

- **Composition:** from Gate Street at the foot of the grand stair, the palace in gray first
  light: fires out, smoke thinning from the west gallery's windows, soot streaking the crystal
  above them. Sect guard posted at the gate; their banners. Guests in blankets on the steps,
  unmasked, dirty, holding each other. Masks dropped on the steps and cobbles.
- **Focal point:** the palace itself, damaged and still standing, its crystal faintly
  recovering a dawn blush.
- **Lighting:** cold gray dawn; the crystal's faint natural glow almost gone in daylight; wet
  stone.
- **People:** the characters standing outside "with whatever and whoever they carried out";
  Corval, bleeding, counting; sect guards with cudgels.
- **Mood:** the counting; the story already wrong by noon.
- **Must:** "the fires are out by dawn"; the sect guard sealing the palace.
- **Must not:** bodies laid out in rows (keep the dead off-page); Raunu or Veier; the Uninvited.


---

## 4. Characters

*Printed traits first, then [APPROVED TP64] costume. The module describes very few faces and
almost no clothes; most costume below is extrapolated and marked. Everyone is human.
Before midnight every guest is masked; after the Unmasking every face is bare except the three
gray masks. Player characters' masks are never fixed in art. The costume below was a [VX]
proposal, approved in TP64 as amended by the architecture review.*

**No mask but the three may be plain gray.** Every other mask is a spirit-face: the year's
dead, a harvest spirit, the season's luck or grief.

**House style for costume [APPROVED TP64]:** Orthaen formal dress for Oraga runs dark: black,
charcoal, deep violet, oxblood and night-blue, with jewel-toned linings and small crystal
ornaments that catch the walls' glow (crystal pins, buttons, hair ornaments). Long tailored
coats for men, high-collared gowns and long coats for women, or either for anyone. Knives worn
as dress at sash or thigh. **Boranis livery [APPROVED TP64]:** deep violet-charcoal coat,
rose-pink crystal buttons, a narrow rose piping, no badge with lettering. [VX, still open]
Whether household staff and honor guards wear Oraga masks is the owner's to decide; until
then, don't make a point of it either way. The Thenya wear plain undyed or
earth-colored border wool, and slings are their mark.

### Raunu Boranis, the host

- **Printed:** chief of the Orthaen; "called a genius, a maniac, or both since childhood."
  Seen four times: a still figure on the high gallery (III), the summonses (III), the toast
  (IV), the Unmasking. At the toast he is **unmasked, "plainly dressed for a chief,"** holding
  a cup "as if someone had handed it to him and left." Awkward, unhurried, long pauses; listens
  completely; "watches the room the way a man watches weather." Vorlain has "his brother's
  face." He wears **two small crystals at his wrist** (one seals the double doors at the
  lights, the twin he crushes for Veier). A man young enough that Sella wondered why "a man
  that age" asked about dying well; his first crystal, grown at six, is "decades old."
- **Pose:** stillness; hands at rest; a direct, unsettling gaze; at the end, commanding a
  burning room.
- **[APPROVED TP64]:** early forties; lean; dark hair worn short, a little untidy; clean-shaven, pale from
  two years indoors; a long plain coat of very dark violet-gray with no ornament but the house's
  rose-crystal buttons; the two wrist crystals on a plain cord or band of dark metal at the left
  wrist, each the size of a fingertip, rose-clear. No crown, no chain of office.
- **Must not:** a tuning fork, a glowing wine glass as a signature prop, a book, a letter.

### Veier Nolonaire, the bride (only at the Crossing and the boat)

- **Printed:** of the Thenya, cousin of the Thenyan chief; one of five gifted Thenya alive.
  Never seen before the Crossing (TP13, TP41); her room never entered (TP53). Near her time
  (heavily pregnant). At the Crossing: **"wounded across the ribs by the Radiant's one clean
  pass,"** "upright anyway, moving with Thenya bluntness toward the water"; Speed 15; carried
  or supported by a character. The Second Clause calls her "a woman in Thenya wool." In the
  boat: "a woman bent over her own heartbeat." Blunt, dry, funny, homesick; happy. Her worn
  border sling hangs in Raunu's room, not on her.
- **[APPROVED TP64]:** about thirty; strong, weathered; dark hair in a long practical braid; a plain
  long dress and over-tunic of undyed Thenya wool, belted high over the pregnancy, a wool
  shawl; a hand pressed to her side where the cut is, a dark stain under it.
- **Must not:** any image of her inside the palace before midnight; any image of her in the
  Crystal Court; a sealed letter or any writing; an attack on her shown.

### Vorlain Boranis, the brother

- **Printed:** "silk over springs"; charming, funny at others' expense; armor worn under silk;
  a blade; Raunu's face "and none of his brother's stillness." Drinks harder through the night.
  After midnight: sleeves pushed up, soot to the elbows, hauling guests out of the burning
  gallery (S13).
- **[APPROVED TP64]:** late thirties; Raunu's face, a few years younger and never still;
  handsome, restless; rich oxblood silk over a fitted breastplate;
  a slim blade at the hip; mask (before midnight) a laughing gilt spirit-face.

### Minister Corval, the majordomo

- **Printed:** "a thin, upright old man in Boranis livery," doing the work of six chamberlains
  with "visible, dignified exhaustion"; greets every guest by name from memory; his hands
  steady. At the end: "bleeding, and he is counting his staff like a man counting his own
  fingers." Carries a key to the wing's service door (TP39).
- **[APPROVED TP64]:** past seventy; white hair cropped close; long face; the house livery worn
  immaculately, a little loose on him; a single rose-crystal chain of office; no list, no
  slate in his hands at the gate.

### Anha, the under-cook

- **Printed:** "quick, practical, frightened in a low-grade chronic way she has stopped
  noticing." Four years in the kitchens. Her hands "going still on the tray" (S7).
- **[APPROVED TP64]:** early twenties; sleeves rolled, a kitchen apron over a plain dark dress, hair tied
  in a cloth; flour and burn-marks on her forearms; carrying a laden tray.

### The Uninvited

- **Printed:** three guests in spirit masks: **"gray, unornamented, beautiful in a way nobody
  can place."** The masks match no maker's style in Rekuzan, "and the material is wrong."
  Charming, gracious, antique manners and turns of speech; they eat, drink, dance "in a style
  centuries out of fashion." Near them Orthaen crystals go faint. They fight with their bare
  hands. They move by "arriving, not running."
- **[APPROVED TP64] for all three:** formal dress of an antique cut, rich but subdued (high collars, long
  sleeves, fabrics a century or two out of fashion), in grays and faded black; the masks
  full-face, smooth, of a pale gray material like matte porcelain or ash-glazed stone with no
  visible ties.
- **The Wept** — *"the gray mask with carved tears."* The tallest; a woman; leads. Warm, sure
  hands; dances flawlessly. When Bloodied, "the mask's carved tears begin to run — actually
  run," and she hums a cradle-song. During the attack, "under the carved tears, the mask is a
  woman's face." [APPROVED TP64] Tall and stately; a long gown of dove-gray with a mourning veil of gray
  gauze over the back of the head; the tears carved as shallow channels from the eyeholes.
  *Must not:* claws, rags, a ghostly or skeletal look, robes like a monk.
- **The Radiant** — *"the mirror-bright mask."* A man; "warm, courtly, delightful on the
  subject of duty"; asks "Whom do you serve?"; blesses the food with an antique sign; "dances
  beautifully, where the light falls"; poses and savors when watched; stages kills "offered
  upward, like rites." [APPROVED TP64] Tall, elegant; a long coat of pale gray silk; the mask the same
  unornamented shape as the others but polished to a mirror sheen that throws back the light
  (gray-silver, not gold), reflecting whoever watches him. *Must not:* sculpted aristocratic
  features on the mask (it is unornamented), a weapon.
- **The Hollow** — *"the blank gray mask."* A man; stands beside a different exit all night;
  "devastating flatness"; holds the doors, never advances; flinches from ward-fire "the way a
  tired man flinches from being asked to try." [APPROVED TP64] Broad, heavy-shouldered; a plain dark-gray
  coat of antique cut; the mask a perfectly blank gray oval, no features at all. *Must not:*
  plate armor or any armor (he passes as a guest at a ball).

### The Attendant

- **Printed:** "a great house's attendant, by its clothes: a cloak folded over one arm,
  standing apart and staring oddly, as if it expects a master nobody at the ball can find to
  arrive." "It" (a made thing). Never fights before midnight; walks into a shadow and is gone.
  Habits: stares at worked crystal and light; waits for a master who is not there; follows
  music that changes. At the Unmasking it sets the cloak down "neatly" on the nearest table and
  stands beside the three, "its hands empty now," looking "at the space between you and the
  three." It attacks with **Joined Hands** (fists joined).
- **[APPROVED TP64]:** looks human, of middle height, unremarkable, neither young nor old; a
  great house's upper-servant's dark coat, correct and current, nothing to remark on; the cloak a heavy dark
  traveling cloak, carefully folded; posture too still, eyes too steady; mask: a plain dark
  half-mask of a servant's kind, or none (owner to choose).
- **Must not:** a cup or goblet (TP30); any monstrous feature.

### Master Vell, the pale factor

- **Printed:** "Tall, pale, soft-spoken; a trade factor no one remembers inviting — carrying,
  of all things, an enormous broadsword wrapped in white cloth across his back." He "never
  touches it and never unwraps it"; at the Crossing **the sword stays on his back** while he
  holds the Radiant (TP19). Unmemorable "and that is not luck." Courteous, brief. At the
  Crossing he "moves the way the gray masks move, arriving instead of running." Rows the boat.
- **[APPROVED TP64]:** forties; very tall and spare; white-blond or ash hair, close-cut; a plain,
  well-cut factor's coat of gray-brown, travel boots, nothing that draws the eye; the wrapped
  sword nearly as long as he is tall, its white wrappings bound with cord, the hilt also
  wrapped; mask before midnight a plain, forgettable spirit-face, not gray.
- **Must not:** his hand on the sword; the blade bare; a bone mask; a named people for him (the
  module never says where he is from).

### Prelate Damaris Kovaun, the Church

- **Printed:** "urbane, watchful, a career diplomat in vestments"; "works the room like a
  census-taker of souls"; a **staff of office**; her Wardens in gray robes.
- **[APPROVED TP64]:** sixties; silver hair under a close cap; layered vestments of deep
  slate-gray and white with a heavy plain metal pectoral (no inscriptions); the staff a tall
  plain rod; mask a dignified white spirit-face.

### Mother Sella, the death-sister

- **Printed:** a lay sister of Elanna; "calm as deep water, kind without softness"; the chapel
  is hers all night.
- **[APPROVED TP64]:** old, small, upright; a plain undyed habit and a dark shawl; unmasked,
  or a dark grief-spirit face (owner to choose); never gray.

### Mistress Rhaza Callun, the Merchant's Circle

- **Printed:** "iron-gray, cordial, terrifyingly numerate"; a knife; pays on delivery.
- **[APPROVED TP64]:** fifties; iron-gray hair severely dressed; a high-necked gown of
  steel-gray with a short fitted coat; no jewelry but one plain ring; mask a narrow silver
  spirit-face of the year's dead.

### Master Pellin Corro, the Phern magnate

- **Printed:** "small, merry, expansive," in "a merchant's coat"; increasingly wrong as the night
  goes on: losing sentences, glancing at doors, back to the wall; at midnight already moving,
  bodyguards closing round him.
- **[APPROVED TP64]:** round-faced, quick, sixty; a bright, well-made merchant's coat in warm,
  bright colors, rings; mask a cheerful painted harvest-spirit pushed up by evening's
  end.

### Lord Essar Draunel, the rival

- **Printed:** "polished, obvious, ambitious in the standard noble key"; breastplate worn under
  silk; rapier. Will not set foot on the grass at the duel.
- **[APPROVED TP64]:** forties; handsome in a groomed way; peacock-blue silk over the
  breastplate; rapier with a jeweled guard; a gilt harvest-spirit face.

### Essin Boranis, the cousin

- **Printed:** "affable, forgettable on purpose, always somehow between Vorlain and whoever is
  working him"; a knife; "for the first time tonight, without a smile" after the toast.
- **[APPROVED TP64]:** thirties; average height, average everything; dark, well-made but
  unmemorable clothes; a plain spirit-face, not gray.

### Maiven Nolonaire, the cousin from the border, and her slingers

- **Printed:** "Veier ten years younger and thirty degrees hotter-tempered"; armor worn under
  border wool; a **long knife** and a **border sling**; at midnight goes straight for the east
  wing. Her slingers: "plain border wool," slings at their belts; in Movement V two of them in
  the garden below the east wing, one paying out a rope "weighted at the end with something that
  is not quite a stone."
- **[APPROVED TP64]:** Maiven about twenty; lean, sunburned; hair in Thenya braids; earth-brown wool tunic
  over a leather jerkin; the sling wrapped at her wrist. Slingers in the same plain wool with
  hoods, slings at belts, coils of rope.

### Tavva, the other thief, and her Gallery Knives

- **Printed:** "somewhere in her forties, somewhere from the coast"; tonight "a steward in
  Boranis livery," armor under it; unhurried, courteous, forgettable; carries crystal charges (a
  *Dark-Burst* and a *Door-Seal*). Her knives: "livery that fits like a borrowed coat."
- **[APPROVED TP64]:** weathered, sharp-eyed; the livery worn perfectly; a sack after
  midnight.

### The Bought: the sergeant, the captain, the Blades

- **Printed — the Sergeant:** "Gray wool, cut plainly, with the company's mark at the shoulder
  and a case chained at the hip, produced more readily than steel." Reads the terms aloud.
- **Printed — the Captain:** "Older than the sergeants and quieter than the Blades. The coat is
  very good, and the scar is older than the coat. The chain on the case has been replaced more
  recently than the case." A "very good sword."
- **Printed — the Blades:** matched gray coats, company blades and cudgels; "the unhurried
  spacing of people who have done this before."
- **[APPROVED TP64]:** the company's mark a simple shape (a closed hand or a ring), no letters; gray
  coats to the knee over mail; the case a flat iron-bound leather document case the size of a
  large book, chained to a belt; the captain grizzled, scar across the jaw.

### The Boranis honor guard

- **Printed:** nine, chain mail and shield, a house blade; "two charged house crystals" at the
  belt (a *House Seal* and a *House Flare*); facing inward on the gate at dusk; three in the
  trophy gallery, two then four at the east wing doors, the rest with the household; at
  midnight seven to the dais (where they die or fall), two holding the east wing doors.
- **[APPROVED TP64]:** violet-charcoal surcoats over mail, rose crystal at the shield boss, open-faced
  helms; the two crystals in a belt holder like a pair of rose-glass eggs.

### The faction retainers, in brief

- **Circle Hired Knives [PRINTED]:** plain good coats over armor; knives; lips moving at every
  name Corval calls; they do not look at the crystal.
- **Church Wardens [PRINTED]:** gray robes; maces; never look at the dancing.
- **Draunel Duelists [PRINTED]:** young men; rapiers; good coats taken off for the duel;
  laughing too near the wrong people.
- **Boranis Cousin's Blades [PRINTED]:** chain shirts worn under festival coats; longswords;
  a loose ring around Vorlain.
- **Phern Bodyguards [PRINTED]:** big, relaxed, laughing at their master's jokes, then backs to
  the walls; caravan blades.
- **The festival hires [PRINTED]:** borrowed livery, not knowing where anything is.
- **The guests [PRINTED]:** about two hundred; merchants, ministers' cousins; after midnight
  shielding strangers.
- **Sect guard [PRINTED]:** cudgels; sect banners coming up Gate Street at the end.
- **The midwife and the two Tithe ministers [PRINTED existence]:** the midwife "moving like a
  woman who counts hours," glimpsed once crossing the gallery; the ministers unnamed ("the
  elder" and "the younger"). [APPROVED TP64] Keep all three plain and background.


---

## 5. Items of Interest

### The grandmother's soul-crystal (B7, Agenda 5)
- **Printed:** "a lifetime of light in a lattice the size of a heart"; "a heart-sized
  soul-crystal of uncommon beauty"; grown by one woman over her working life, taken from a
  border settlement two generations ago; "hangs in their trophy gallery like a hunting prize";
  on its own ward; "glows faintly at dusk, as all old crystal does"; not a magic item.
- **[VX]:** a clear rose-gold crystal about 5 inches across, roughly heart-shaped but grown, not
  cut, its interior a dense lattice of fine planes like frost inside glass, each plane holding a
  faint warm light. [APPROVED TP64] On a slim crystal pedestal on its own old ward
  (generations-old crystalwork on the pedestal); no ring in the floor.

### The great table and the work-slate (B8)
- **Printed:** "A grown relief of the eastern coast, its mist-lines remembered in colored
  lattice. The recent lines have been reworked many times." Grown, cannot be carried. The
  work-slate: "a half-erased lattice diagram," the door-key of the Root; the wardens wipe it.
  No papers (TP38).
- **[VX]:** the table a single waist-high slab of grown crystal about 14 × 7 feet; its top a
  raised coastline in pale crystal (headlands, coves, river mouths) with the sea a lower,
  darker plane; the mist-lines are threads of colored light (rose, amber, violet, pale green)
  laid in nested contour lines offshore, the newest lines nearer the coast and visibly
  re-grown over older ones, a palimpsest of light. The slate: a dark slab the size of a
  serving tray in a plain frame; a fine diagram of interlocking lattice lines (a geometric
  web, not letters), half rubbed out at one side.

### The instruments (B8 and the Root)
- **Printed:** "Nobody can name them." In the Root, "instruments of glass and lattice" that read
  the gift "the way a jeweler's glass reads a stone."
- **[VX]:** armatures of fine dark metal holding lenses of crystal, nested rings, small lattice
  cages around empty centers, rods tipped with faceted points; nothing with a dial marked in
  numbers or letters.

### The Root's contents (B11)
- **Recall-lattices [PRINTED]:** "racks of grown lattices, decades of research held in light";
  touched, they show images and remembered gesture; many oldest ones are relics. [VX] Thin
  plates of crystal, palm to forearm size, standing in grown crystal racks floor to vault, each
  with a faint inner image-glow; the oldest cloudier and amber-tinted.
- **The lattice that speaks [PRINTED]:** one crystal "holds a voice," Raunu's. [VX] A small
  clear lattice on its own, slightly brighter, the light in it pulsing like breath.
- **The chair, stool and blanket [PRINTED]:** "a chair with a wide armrest, a stool beside it,
  a lap-blanket of Thenya wool folded over its back," beside the instruments. [VX] A plain,
  comfortable chair of dark wood; the blanket undyed border wool with a simple woven stripe.
- **The skeleton [PRINTED]:** a full human skeleton on a stone bier in an alcove; "through every
  bone of it grow fine-grained crystals... They thread the ribs, vein the long bones, and
  cluster like frost in the eye sockets." Old, unbroken bones, "arranged with something like
  respect"; "a few threads in the ribcage glow, very faintly, if no one is speaking." [VX] The
  crystal rose-white, hair-fine, like hoarfrost; the bier plain dark stone; never gruesome.
- **Dated observation lattices [PRINTED]:** "months of them, in meticulous sequence," beginning
  about eight months ago; "the latest plate is the finest work in the room, grown with a care
  that has stopped being science." [VX] A row of some thirty plates on a ledge, left to right,
  each holding a small bright knot of light that grows from plate to plate; the last plate
  larger and exquisitely grown. No dates written: the order is the date.
- **The coast in crystal [PRINTED]:** "a grown relief of the eastern shore and its mist-lines
  going back four centuries, the recent lines reworked many times." [VX] Kin to the study's
  table, longer and older, with many more strata of lines.
- **The two-family orrery [PRINTED]:** "a crystal orrery of two family trees. The Boranis line
  and the Nolonaire line are rendered in light, descending generations deep and intertwining as
  they descend. Both converge toward a single darkened junction older than either house, where
  one name has been deliberately, physically burned out of the lattice." In its base, "one
  figure repeats over and over: two streams of light falling into a single pool." [VX] Two
  great branching lattices of light, one rose and one amber-gold, about 8 feet tall on a low
  round plinth, branching downward like roots rather than up like trees, weaving through each
  other as they descend until both meet at a dark scorched node near the base; the base a ring
  of crystal with the two-streams-into-one-pool figure repeated around it as a pattern (two
  falling lines meeting in a circle). **No names are written anywhere on it** (a name in a
  lattice is a light-pattern, not letters).
- **Must not:** planets, armillary rings, "world-anchors" or any cosmic orrery; any legible name.

### The nursery mobile (B9)
- **Printed:** "a mobile of grown crystal turning slowly over the crib."
- **[VX]:** a ring of fine crystal arms from which hang small grown crystal shapes (drops,
  stars, a crescent), turning, throwing small rose lights across the cedar.

### Raunu's first crystal (B9)
- **Printed:** "A small, flawed, badly-grown crystal, decades old, kept on the sill where the
  light finds it: his first, grown at six."
- **[VX]:** thumb-sized, lopsided, cloudy at one end, with a single clear facet; glowing very
  faintly on the bare sill.

### The two slings (B9)
- **Printed:** "the worn border sling that is obviously hers," and beside it "a second sling,
  new, its knots clumsy, re-tied many times."
- **[VX]:** hers: dark braided cord, the pouch leather worn shiny and pale at the edges, the
  finger-loop frayed; his: bright new cord, stiff, the knots bulky and lopsided, several
  re-done (old kinks showing where knots were). Shown side by side, touching.

### Raunu's two wrist crystals (B2)
- **Printed:** worn at his wrist, twins; the first spent sealing the east wing's double doors
  at the lights; the second "a second small thing, worn at his wrist," crushed in his fist to
  seal every door between Veier's rooms and the river.
- **[VX]:** two fingertip-sized rose-clear crystals on a plain dark band; when crushed, rose
  light leaks between his fingers.

### Crystal charges and wards
- **Printed:** a charge is "one stored working, released at a touch by anyone." The honor
  guard's pair: *House Seal* and *House Flare*. Tavva's: *Dark-Burst* and *Door-Seal*. Common
  charges: *Steady Light*, *A Sealed Door*, *A Veil of Quiet*, *A Chime at a Threshold*,
  *Warmth*, *A Held Image*. Near the Uninvited "the light goes out of the crystal" on a failed
  release. Ward-points: the dais's four "sconces"; two by the main doors; every door Raunu
  sealed. A sealed door "grows closed."
- **[VX]:** charges are egg- to palm-sized grown crystals, each with a faint internal pattern
  that hints at its working (a steady flame-glow, a closed-door lattice, a dark core); releasing
  one: the crystal flares and its light pours out and goes dark. A seal: crystal grows across a
  doorway from the edges inward like fast frost. A *House Flare*: a 30-foot sphere of hard
  white-rose light with no shadows in it. A *Dark-Burst*: a ball of perfect black.

### The masks
- **Printed:** spirit-faces of the year's dead, harvest spirits, luck and grief. The three gray
  masks (above). Otta Vesh, the aftermath's mask-maker, "keeps a casting-blank of every face
  she has ever fitted."
- **[VX]:** guest masks in lacquer, leather, papier-mâché and fine porcelain: bone-white
  ancestor faces, wheat-and-leaf harvest masks, gilt harvest-spirit and silver year's-dead
  faces, masks with painted tears, animal spirits, half-masks and full faces; ribbons and
  crystal beads. [APPROVED TP64] Every guest mask is a spirit-face, and none but the three is
  plain gray.

### The invitation card (B0, B1; Player Handout 1)
- **Printed:** a great house's formal invitation is one of the two exceptions to the written-word
  law; a footman sells "a genuine invitation with a scorched corner and somebody else's name on
  it." The text is canonical (chapter VIII, Handout 1): HOUSE BORANIS / To My Esteemed Guest /
  ... / Given Under My Hand, Raunu Boranis.
- **[VX]:** heavy cream card, the house's device embossed (an image, no motto), the text in a
  fine hand; the sold card scorched at one corner.

### The grandmother's ring (Agenda 4; B9 doors)
- **Printed:** the Thenya grandmother's ring proves whose mouth the message comes from; "the door
  opens a hand's width and her hand comes through it and takes the ring. Her face stays unseen."
- **[VX]:** a plain old silver ring with a small dark stone. Image: a hand (a woman's, strong,
  a little weathered) reaching through a hand's-width gap of a tall door to take it from a
  character's palm, nothing else of her visible.

### The Attendant's folded cloak (B2)
- **Printed:** "On the nearest table, a folded cloak, set down neatly."
- **[VX]:** a heavy dark traveling cloak, folded into a precise square, on a banquet table
  among the plates.

### Vell's wrapped sword
- **Printed:** "an enormous broadsword wrapped in white cloth across his back." Never touched,
  never unwrapped.
- **[VX]:** nearly six feet long, broad-bladed, every inch bound in white cloth wrapped in
  overlapping turns and cord-tied, hilt included; slung diagonally.

### The Bought's contract case (B12)
- **Printed:** "a case of writing chained to the sergeant's hip"; it holds the three tasks; held
  up to the grille "the way you would hold a lantern"; the captain's chain replaced more
  recently than his case. Not magic.
- **[VX]:** a flat iron-cornered leather document case, worn, with a short chain to a belt
  ring; when opened, folded sheets (writing, because it is a contract, but never legible in
  art).

### The cellar tally-cords (B10)
- **Printed:** "the cellar tally-cords don't add up"; knots read by anyone who has kept a
  household's cords.
- **[VX]:** bundles of colored cords on pegs by the cellar door, knotted in clusters, some with
  tied-on crystal beads.

### The wardens' record of the map (S8)
- **Printed:** "a written copy of the great table's mist relief, made by the Church in Raunu's
  study." The Church alone may write.
- **[VX]:** a few sheets of heavy paper in a warden's satchel with a careful ink drawing of
  contour lines; drawn from behind or folded, never legible.

### The boat (B5)
- **Printed:** Vell's; "a purchased boat"; a fisher's boat "paid for in old coin at three times
  its worth"; one pale man rowing.
- **[VX]:** a small, tarred wooden fishing skiff, about 14 feet, one pair of oars, a coil of net
  shoved under the thwart.

### Tavva's sack
- **Printed:** rings, a few trophies from B7, maybe one or two old soul-crystals from the case.
- **[VX]:** a dark canvas sack, a glint of crystal at its mouth.


---

## 6. Correction List for the Existing Art (`art/ART_AND_MAP_MANIFEST.md`)

*Each line was checked against the module text and the rulings. "Fix" says what the image or
the manifest should become. File names are under `conversions/dnd5e/oraga_night/art/`.*

### 6.1 Manifest-wide errors

1. **Chapter files and headings that don't exist.** The manifest targets `08_Palace_Boranis.md`
   ("### Diagram VIII.1" etc.), `09_Bestiary.md`, `10_Cast_of_Characters.md` and
   `02_A_Quick_Primer_for_the_Table.md`. The real files are `08_Handouts.md` (maps under "The
   Palace, Keyed", titled "Map VIII–1" to "Map VIII–5"), `10_Bestiary.md`,
   `07_Cast_of_the_Ball.md` and `02_The_World_and_the_Night.md`; chapter IX is
   `09_The_Snakes.md`. Fix every drop-in snippet's target before anything is pasted.
2. **Area numbering.** The manifest calls the Crystal Court **B3**, the galleries **B4 Upper
   Galleries**, and uses **B2 Entry Hall** and **B12 Outer Gatehouse & Guardroom**. Canon: B2 is
   the Crystal Court, B3 the Banquet Galleries, B4 the Audience Hall, B12 the Gatehouse Court
   after midnight (held by the Bought). There is no Entry Hall: the main doors open from the
   Gatehouse Court straight into the Crystal Court.
3. **Lineages.** The manifest's four lineage labels are not the module's peoples. Two of them
   appear nowhere in the module; Rekuzan is the city. The peoples at the ball are Orthaen, Thenya
   and Phern (with the Kshalo and Mazaa mentioned in rumor). Remove the two non-module labels.
4. **"Stamped metal/clay tablets" as Orthaen records.** That is writing, which the law forbids to
   everyone but the Church. Records are crystal (recall-lattices), memory, tally-cords and wiped
   slates. Remove tablets from every interior.

### 6.2 Maps (`art/maps/`)

5. **`map_viii_2_gatehouse.png`: footprint and labels.** Stated as 80 × 140 feet with "B2 Entry
   Hall" and "B12 Outer Gatehouse & Guardroom". Canon/MAP: the Gatehouse Court is about 60 × 45
   feet, the gatehouse 40 × 15 (the cell one side of the arch, the stair the other), the gate-walk
   15 feet up, the 5-foot wicket in the gate's left leaf as seen from the court, the bar on the
   street side, the main doors on the court's north side into B2.
6. **`map_viii_3_crystal_court.png`: dimensions, orientation and doors.** States a "60 × 140 ft
   main floor + 12 ft galleries + 15 ft South Dais + 12 ft railed South Garden Walk." Canon: the
   floor is **80 × 140** (galleries 20 feet deep outside it per MAP, total width 120); the dais
   (30 feet across, 3 feet high, 15 deep) is at the **north** end with the garden doors either side
   and the railed garden walk (10 feet deep) beyond them, also north; the main doors (10 feet) at
   the south. The "doors to B6, B7" are unsupported: B7 is private, off the gallery corridor, not
   off the Court; the chapel's door is not printed (this brief proposes it off the B4
   antechamber). The west wall carries the B4 double door and the 5-foot service door (S11); the
   east doors are on the east wall about 30 feet from the main-doors end, with the stair up 12
   feet behind the east gallery. "Two rows of 6 crystal pillars": if they stand on the dance floor
   they break the printed floor (the crowd count assumes a clear 80 × 120); move them to the floor's
   edge lines under the gallery rails. Check the "4 spiral gallery stairs" are in the aisles, not
   on the floor.
7. **`map_viii_4_terraces.png`: names, fountain and boat.** The terrace names ("Upper/Lantern",
   "Middle/Fountain" with a 20-foot dry basin, "Lower/Herb") are not in the module; a basin on the
   second terrace is an unapproved addition (harmless, but flag for the owner). "Veier's moored
   four-oared boat" is wrong twice: the boat is **Vell's** (TP11, TP12), a fisher's boat he bought,
   rowed by one man. Check the garden stair is drawn down the **east wing's west wall** to the
   upper terrace, a stair at either end of every terrace, and the river gate centered on the river
   walk.
8. **`map_viii_5_east_wing.png`: size, room contents.** "40 × 90 ft + grounds" is too small:
   the cleared corridor is 10 × 60 feet, the wing corridor 10 × 100, the rooms 20–30 feet across
   (MAP: 25 × 30, east side, order Veier's, Raunu's, the nursery from the doors). Veier's room must
   not be shown furnished inside (TP53: never entered; draw it as a closed room). "Rocking horse
   and carved cradle": the nursery's printed contents are fresh paint, cedar, a crib and a crystal
   mobile; remove the rocking horse unless the owner approves it. Show the service stair beside
   the double doors with the wing's service door at its head, and the door down to the garden
   below the wing.
9. **`map_b7_trophy_gallery.png`: invented exhibits.** "Three bell-jar Soul-Crystal pedestals
   (three figures labeled by people)" are invented and use non-canon peoples. Canon:
   banners, weapons, grown crystals taken in old settlements, "the gallery's case" of old
   soul-crystals, and one heart-sized soul-crystal on its own ward (the grandmother's). Make the
   grandmother's crystal the single focal exhibit, on a pedestal on its own old ward, with no
   ring in the floor (TP64).
10. **`map_b8_raunus_study.png`: the hearth of scorched invitations.** Cut by **TP38**: no
    drawer or hearth of invitations, no papers of any kind. Remove the scorched cards. Also remove
    the "wall-mounted recall-lattices": recall-lattices are the Root's (B11), and putting them in
    the study gives away Undercurrent A. Keep the great table (the eastern coast with colored
    mist-lines), the work-slate with its half-erased lattice diagram, and the unnameable
    instruments. Draw no shelves and no fireplace: the instruments stand on a long grown bench
    and on ledges grown out of the wall (TP64).
11. **`map_b11_root_of_the_house.png`: the orrery and the slate.** The "Orrery of the Seven
    World-Anchors" with "6 massive crystal roots converging" contradicts the text. Canon: a
    **crystal orrery of two family trees**, Boranis and Nolonaire, in light, intertwining down to
    one darkened junction with one name burned out, and in its base the repeated figure of **two
    streams of light falling into a single pool**. Also: the "wiping-slate" belongs in the study
    (B8), not the Root (the slate is the Root's key and the wardens wipe it upstairs). Add what is
    missing: the recall-lattice racks, the chair with a wide armrest, the stool and the Thenya wool
    lap-blanket by the instruments, the coast-in-crystal relief, the dated observation lattices.
    The skeleton on its bier is right.
12. **`map_viii_1_palace_overview.png`.** Check it against §1: dais end and gardens north, the east
    wing projecting north at gallery level along the terraces' east side, the gatehouse south,
    the wine cellars running west from under the kitchens beneath the Gatehouse Court, and the
    Root beneath their west end, under the Court's south half (TP64). It may also need the dark
    wing (B8) on the second floor (about +15, the storey above the ground, with no door to the
    banquet galleries), the bell tower on the east gallery's north end, and no carriage ramps
    at the grand stair.

### 6.3 Cast, bestiary and pregens

13. **`cast_master_vell.png`: gripping the sword; a non-module people label; bone mask.** Vell "never touches" the
    sword and it stays wrapped on his back all night (TP19; 07, 10). Redraw with the wrapped sword
    on his back, hands empty. The people label is not canon and the module never says where he is from;
    remove it. The "carved bone half-mask" is unsupported; keep his look forgettable.
14. **`cast_raunu_and_veier.png`: setting and props.** Veier never enters the ball and is never
    seen before the Crossing (TP13, TP41), so a joint portrait "inside the Crystal Court" breaks
    canon; set any portrait of her outside the ball's story (a neutral ground), or show her only
    at the Crossing. Her "sealed letter" is writing she would not carry; remove it. Raunu's "bronze
    tuning fork" and glowing wine glass are invented signature props; his printed signature items
    are the **two crystals at his wrist**, his plain dress and, at the toast, a cup and two plates.
15. **`cast_veier_nolonaire.png`.** Same as 14: no letter; Thenya wool, near her time; not in the
    Crystal Court.
16. **`bestiary_the_radiant.png`: "sculpted aristocratic features."** The three masks are "gray,
    unornamented"; his is "mirror-bright" but still featureless. Polish the mask to a gray mirror;
    remove sculpted features.
17. **`bestiary_the_hollow.png`: "battered plate armor."** The Uninvited pass all evening as
    charming guests in antique dress who eat, drink and dance; plate armor contradicts that. Redraw
    in formal antique dress. His blank gray oval mask is right.
18. **`bestiary_the_wept.png`: "damp ash-gray robes."** Not printed; she dances at a ball, "gracious,
    a little sad." Prefer a formal gown of antique cut. Her carved-tear mask is right; the "silver"
    tear tint is an extrapolation (acceptable if subtle; the mask is gray and unornamented).
19. **`pregen_serane_vaskarin.png`: class.** Labeled "Wizard 3". Serane is **Bard (College of
    Lore) 4**, gifted Orthaen. Her mask is the player's to describe (11: "No guest's mask is written
    down"); do not fix one in the portrait.
20. **`pregen_pello.png`: people, class, mask.** Labeled "Masks-Only Guest, Bard 3" under a non-module people label with a
    lute and "porcelain fox half-mask". Pello is **Phern**, **Rogue (Thief) 4**; no such people; the
    mask is the player's.
21. **Handout 4 target "11_Pregenerated_Characters.md (## 4. Tovan)".** There is no pregen named
    Tovan; the pregens are Serane, Pello, Andra, Dassa and Ilesse.

### 6.4 Handouts

22. **`handout_1_boranis_invitation.png`: plate and scorched plates.** The invitation is a
    **card** (one of the two exceptions to the written-word law), not a silver-foil plate. The
    "three scorched, unaccepted plates found in Raunu's Study hearth" with names (Master Ollo,
    Lady Keshan, the Guild of the Third Lamp) are cut by **TP38** and the names are invented. The
    only scorched invitation is the footman's card in the line (B0), "a genuine invitation with a
    scorched corner and somebody else's name on it." Use the canonical text in chapter VIII,
    Handout 1.
23. **`handout_2_court_primer_slate.png`: invented content.** "Three Bell-Strikes (First Bell,
    Mid-Bell, Unmasking Bell)", "Four Tiers of Admission (High-Table, Floor, Gallery,
    Masks-Only)" and "Four Lineages at the Table" are not in the module. Chapter VIII's Player
    Handout 2 is the **Agenda Cards**. Retire this image or replace it with the agenda cards.
24. **`handout_3_orthaen_crystals.png`: two errors.** "Crystal Charges (Captured Soul-Crystals)":
    a charge is "one stored working" grown by a gifted Orthaen; a soul-crystal is a lifetime's
    growth, and the grandmother's "is not a magic item." Keep them separate. "Orrery of the Seven
    World-Anchors": see item 11. Chapter VIII's Player Handout 3 is the crystal charges table.
25. **`handout_4_the_bought_contract_tablet.png`: wrong object, wrong terms.** "Stamped Bronze
    Debt-Ledger Tablet", "seven-year indenture", "Breath and Memory" clause: none of this is in
    the module. The Bought are a contract company hired two nights ago; their contract is "a case
    of writing chained to the sergeant's hip" holding three tasks (the fires, the gate, the sealed
    Second Clause). Redraw as the chained case, writing illegible, or retire it.

### 6.5 The cover

26. **`cover_oraga_night.png`.** Acceptable as a cover. Check two things: the Hollow and the
    Radiant are not in armor or sculpted masks (items 16, 17), and nothing in it shows Veier or an
    attack on her. Rain is the owner's anchor, not the module's; fine.

---

## 7. Extrapolations Approved by the Owner (TP64)

A one-place list of every extrapolation that shapes the maps. **All fifteen items are
owner-approved (TP64)**, in the wording below: items 7 and 12 as first drafted, the other
thirteen with the changes in the independent architecture review
(`docs/REVIEW_oraga_palace_architecture.md`), which have been applied throughout this brief.
Statements they cover are tagged [APPROVED TP64]. TP56 had already approved the quiet rooms as
placed (the shut state rooms and dark wing in item 5, the garden wing's rooms and the mews in
item 6, the East Range in item 7, and the bell tower in item 3); TP64 approves their sizes,
heights and positions as given here. Four questions inside these items stay open; they are
listed at the end and remain tagged [VX].

1. **Footprint and shape:** about 370 × 290 ft built, a U opening north; about 400 × 580 ft with
   the grand stair and gardens (§1.3). The §1.4 block table must be corrected so that no two
   blocks on the same level overlap (see the review's geometry list); the footprint itself is
   unchanged.
2. **The street front:** a gate landing (80 × 30 ft, the head of Gate Street) and a steep grand
   stair about 20 ft wide rising 25 ft, heavy balustrades, crystal lanterns on posts at its foot
   and up both sides, matching the owner's image; carriages set down at the stair foot and go
   round by the West Lane to the stable yard (no carriage ramps). At the stair head, the
   gatehouse arch is the tall arched entrance of the owner's image, flanked by two gate towers;
   the Gatehouse Court lies hidden behind it and the Court's south front rises above it.
3. **The south front** over the main doors, as in the owner's image: a great tall pointed window
   of grown tracery headed by a rosette, flanked by twin 120-ft Court towers; the bell tower at
   the Court's north-east corner (TP56), placed on the east gallery's north end so it clears the
   east wing; pinnacles and buttress arcs throughout. All of it is grown, not cut: facets and
   growth lines, no mortar joints, no carved figures or gargoyles. Each wing may show a slightly
   different crystal habit, since each was one ancestor's working life (04:29–31). No flèche.
4. **The Court's interior:** clear dance floor; piers on its edge lines; ground-level side aisles
   beneath the banquet galleries; a high gallery at about +30 in the wall thickness; tall windows
   of clearer, brighter crystal above it (the walls are the light; windows are where the crystal
   is thinnest); a grown crystal musicians' gallery over the main doors; grand stairs to the
   galleries in the south corners; two hearths in the aisles. The east banquet gallery has no
   alcoves and no doors in its outer wall south of y 114, where the east stair and cleared
   corridor run behind it; its alcoves sit in its north end or within its 20-ft depth.
5. **The West Range:** the B4 antechamber (30 × 30) and Audience Hall (110 × 50, ceiling 35)
   west of the Court; the octagonal chapel (40 ft) off the antechamber; shut state rooms on the
   ground floor, with the dark-wing stair rising from among them (TP56's clean path leads to
   it); the dark wing on the second floor, the storey above the ground floor (about +15,
   roughly level with the banquet galleries but with no door to them), with Raunu's study in a
   south-west corner tower (30 × 25). The study has no shelves and no fireplace: the
   instruments stand on a long grown bench and on ledges grown out of the wall.
6. **The garden wing** mirroring the east wing on the terraces' west side: the trophy gallery
   (30 × 40) at gallery level off the gallery corridor, with the two drawing rooms beyond it at
   the wing's north end; the lower gallery and B13's door beneath; the falcon mews behind it.
   The soul-crystal stands on its own old ward (generations-old crystalwork on its pedestal),
   not inside a ring of Raunu's. Where "a gallery ring of Raunu's own work" is, if anywhere, is
   the owner's to decide.
7. **The East Range:** kitchens, servants' hall, offices and laundry behind the gatehouse, with
   a kitchen gate on the East Lane; dormitories above.
8. **The service-passage ring** and its route, including where the plank-thin wall to the Court
   is (behind the east aisle) and a servants' postern on the West Lane. All passages are plain
   crystal gone dull with handling, not plaster. After midnight the Bought's twelve-Blade
   perimeter (facts.yaml) lies outside the lanes and gates; what it does at the postern and the
   kitchen gate is the owner's to decide, and no art should show it.
9. **The ground falls north and east:** the upper terrace about 8 ft below the Court (so the
   garden stair falls 20 ft from the wing's corridor), and the garden below the east wing about
   5 ft below the Court, so the wing's lit window (sill about 3 ft above the +12 floor) is 20 ft
   above that garden, as card S10 prints. The wing's gallery level is the "second floor" S10
   names, in the module's American usage.
10. **The cellars and the Root:** the wine cellars (about 60 × 40, −15) run from under the
    kitchens west beneath the Gatehouse Court to the Court's south end; the lower cellar stair
    goes down at their west end to the lower cellar (−30) and its living-crystal wall; the Root
    (a 50-ft domed rotunda, −45) lies beneath the wine cellars' west end, under the Court's
    south half, grown from a central root-node (owner to confirm the root-node's look). Whether
    the Root keeps its glow after the drain is the owner's to decide; until then, draw it lit by
    Raunu's candles and lamps.
11. **Materials and color:** one material, pink grown crystal. Where it is thick, unlit or seen
    against the night sky it reads deep violet to charcoal (the owner's image); wherever it is
    thinner or lit from within it glows rose to magenta up close and from the street. Before
    midnight rose leads and the dark mass supports it; up close the light is warm and
    shell-like. After the drain the crystal is colorless, milky, gray-violet dead glass
    everywhere; any rose after midnight is fire seen through or reflected in it, never the
    walls' own glow. Ward-light is a hard white-rose.
12. **Boranis livery** (violet-charcoal, rose-crystal buttons) and the honor guard's surcoats.
13. **All costume, age and hair proposals in §4, as amended** (long tailored coats, not
    doublets; spirit-face masks only, and no mask but the three plain gray; the Attendant's
    coat correct and current; Kovaun's pectoral plain metal; no Phern colors, wooden token or
    ring of keys; Veier about thirty; Vorlain with Raunu's face).
14. **Garden planting:** upper terrace an open lawn (the duelling ground, S9) framed by gravel
    paths and low flower borders against the balustrades, lanterns on poles; second terrace a
    parterre of low clipped beds around a gravel cross; third terrace an orchard walk of
    pleached apples; lower garden looser, a central gravel path to the river gate between deep
    flower beds; garden walls of crystal.
15. **Neighborhood:** half-timbered townhouses and amber shopfronts on Gate Street (the owner's
    image; owner to confirm the street lies outside or inside the Boranis district walls), the
    West and East Lanes, the stable yard. At the garden's foot the river runs past the river
    walk; Vell's boat goes upstream, north, up the tributary toward the foothills (the
    tributary flows south). No river mist, except perhaps a thin line on the water in the boat
    scene (owner to decide).

**Also applied with TP64 (the review's findings outside §7):** the §1.4 overlaps are corrected
(bell tower, SE Court tower, S10 garden, service run, SW tower); no glow on the walls after the
drain in §0.2 or Scenes 10 and 11; rain kept to the street plates; the owner's image described
as a rosette-headed pointed window, not a rose window; the Gatehouse Court shown holding about a
hundred, not two hundred; and the sconce rule limited to the dais's ward-points.

**Still open for the owner** (tagged [VX] where they appear):

- Whether household staff and honor guards wear Oraga masks (§4, livery; item 12).
- What the Bought's perimeter does at the servants' postern and the kitchen-yard gate after
  midnight (B10; item 8). No art shows it until then.
- Whether the Root keeps its glow after midnight (B11; item 10). Until then, draw it lit by
  Raunu's candles and lamps.
- Whether Gate Street lies inside or outside the Boranis district walls (§1.1; item 15).
