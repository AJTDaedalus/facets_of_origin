# Map rubric (DESIGN_mapgen §7.3)

Score each 1–5 by looking at the rendered PNG (at VTT zoom: one square ≈ a
fingertip). For a contact sheet, score the comparator too so the gap is visible.

| # | Criterion | 5 looks like | 2 looks like |
|---|---|---|---|
| 1 | **Legibility** | Walls, doors, elevation changes and hazards read at a glance | You have to hunt for where a door is or where a ledge drops |
| 2 | **Surface** | Every material reads as what it is (stone, wood, water, grass); nothing is a flat fill | Big areas of one flat colour |
| 3 | **Depth** | Shadows and occlusion separate floor, wall, raised and sunken | Everything sits on one plane |
| 4 | **Line** | Ink weights rank (walls heaviest, detail finest); natural edges wobble, built edges are true | One line weight everywhere, or ruler-straight caves |
| 5 | **Palette** | Cohesive and period-plausible, close to its category's references (or the canon art brief) | Garish, muddy or monochrome |
| 6 | **Grid** | Present, aligned, readable, subordinate to the walls | Missing, or louder than the walls |
| 7 | **Props** | Recognisable at one square and drawn in the map's line style | Blobs, or clip-art in a different style |
| 8 | **Shelf test** | Could sit in a published module beside the comparator | Clearly a programmer's diagram |

**Pass:** average ≥ 4.0, no criterion below 3. The owner has the final say.

Automated proxies (`python -m mapgen quality`) must also land in the category
band: Q1 tonal range, Q2 fine detail, Q3 mid-scale variation, Q4 ink density,
Q5s saturation. They're necessary, not sufficient. A canon palette that the
art brief fixes may sit outside the Q5s band, so say so instead of drifting from canon.
