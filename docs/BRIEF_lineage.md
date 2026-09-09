# BRIEF — Lineage: a Core Creation Step

**Date:** 2026-09-08 · **Tier:** Brain · **Parent:** `docs/BRIEF_oraga_starter_module.md` §4
**Feeds:** `docs/DESIGN_lineage.md`, `docs/TASKS_lineage.md` (Planner)
**Owner ruling (2026-09-08):** gift formalization is **option 1** — a lineage gift formalizes at the character's first Facet level in any Facet, consuming no Technique pick. §3.4 is settled; the `formalizes_on` field stays as data so a future setting could choose otherwise.

---

## 1. What is being made

1. A new PHB chapter, **Lineage**, and a seventh step in character creation.
2. One core lineage, **Human**, with no gift.
3. MM guidance for building custom lineages (in the same chapter, MM-labeled).
4. A `lineages` collection in the ruleset data, a `LineageDefinition` schema, `lineage` and `gifted` on the character, one creation validation rule, one advancement hook.
5. Same-commit sync of every quick reference, the character sheet appendix, the glossary, the generated index and table registers, and the app's creation flow.

Val'loh's ten lineages are **not** in this brief; they are `BRIEF_valloh_facet.md`. This brief must land first because that one loads through it.

## 2. Where it goes in the book

**Chapter placement.** Insert as **II.5 Lineage** and renumber Backgrounds to **II.6** and Skills to **II.7**. The book is digital-first (DECISIONS B2), the cross-reference resolver exists (P15), INV-5 catches any `Chapter X.Y` reference that fails to resolve, and INV-4/INV-10 regenerate the index and registers. A `II.4d` insertion was considered and rejected: it would read as part of the Facets chapter forever to avoid a one-time sweep the tooling was built for.

Planner: the renumber is one task, done first, with the resolver run and INV-4/5/9/10 green before any new text is written. Expect touches in II.1, II.3, II.4, Quick Start, Front Matter, Glossary, Table of Contents, the MM Manual wherever "II.5" or "II.6" appears, the character sheet appendix, and `references/phb-examples.md`.

**Creation order (II.1 *The Six Steps* becomes *The Seven Steps*):**

1. Decide who they are.
2. Pick a Primary Facet.
3. **Choose a Lineage** — who you were born as. In the core rules, Human; setting Facets add more. A gifted lineage grants a domain (Chapter II.5).
4. Spend 18 points on the nine Minor Attributes.
5. Derive the three Major Attributes.
6. Pick a Background — Title, Starting Skill, Secondary Skill *or* Domain origin, Specialty. **A character holds one domain at creation, from Lineage or Background, never both.**
7. Fill in the rest.

Lineage sits before attributes because a gift is part of who the character *is* before any number is spent, and because a table building a Val'loh party should settle "gifted or not" before pricing Constitution. It sits after Facet because the formalization rule (§3.4) reads off the Facet.

Quick Start gains one line under step 2: *"Your Lineage is Human unless the setting says otherwise; a setting's lineages may grant a domain — see its Facet."*

## 3. The rules (draft text; Worker polishes voice, not content)

### 3.1 Reading the Entries — Lineages

Every lineage prints four fields in this order, and a field is never printed empty.

- **Name** — with the common in-world variants in italics after it.
- **Description** — two or three sentences: where these people are from, how they live, what the world expects of them.
- **Gift** — *None*, or a **domain**. A gifted lineage names the domain its blood carries (a short list, if the lineage's gift takes more than one shape). The Gift is a domain in every respect (Chapter II.3): intuitive tradition, Spirit + Attune, Minor scope until it formalizes, full scope after. It **replaces the Background's Secondary Skill**, exactly as a magic-granting Background's Domain origin does. Where a lineage is gifted only in part, the entry states the rate as fiction ("four in five carry it") and the player says which their character is.
- **Heritage** — one narrow fact every member of the lineage grows up with, gifted or not. It works as a Specialty does: when it bears directly on a roll, Standard becomes Easy; when it is tangential, the MM hands over the information without a roll. It draws from the same one-step allowance as Specialties and Techniques (Chapter III.1, *Difficulty*).

### 3.2 Human *(the core lineage)*

**Human** *(folk, people)*

**Description:** The default of the core rules and of Shattered Origin. Humans are what the rest of the book assumes: no gift, no heritage, nothing on the sheet that a Background and a Facet do not put there. Every example character in this book is human.

**Gift:** None.

**Heritage:** None. Whatever a human character knows from birth, their Background already says.

*(Through the Mirror box, below the entry:)* **Why the core lineage is empty.** A lineage with nothing in it is not a placeholder; it is the baseline every other lineage is measured against. Shattered Origin defaults to human on purpose: a new table has one fewer choice to make, and every non-human lineage a setting adds is a *counted* difference from a known shape. When a setting Facet says "this world has seven lineages and the gift of each is a domain," the player already knows what a domain is and what it costs, because the rest of this chapter told them.

### 3.3 The Gift is a domain

A gifted character's domain works as Chapter II.3 describes, with three things settled here so the Facet chapters do not need to repeat them.

**It comes from birth, not study.** A Background's Domain origin is a story of learning; a lineage Gift is a fact of blood. The player still answers the four origin questions in II.3 (*where were you when you first understood what you could do…*), because a gift that has never been noticed is not yet a domain the character can reach for.

**One domain at creation.** A gifted character takes a Background that grants no domain; a character whose Background grants a domain takes an ungifted lineage or plays an ungifted member of a gifted one. Second domains arrive the way they always do (Chapter II.4c, *Second Domain*; Chapter II.3, cross-Facet Tier 1).

**Minor scope until it formalizes.** Same as any pre-Technique domain (Chapter II.3, *Before the Technique*): real, reliable, small.

### 3.4 Formalization *(option 1)*

A lineage Gift **formalizes at the character's first Facet level, in whichever Facet that level lands, and spends no Technique pick**. The reflection scene for that level is the Gift arriving in full. A Background domain still formalizes through the Soul or Mind Tier 1 Technique as Chapter II.4 says; the two routes never combine, because a character holds one creation domain.

*(Through the Mirror box:)* **Why blood formalizes for free.** A Background domain is a practice the character is still learning, and the Tier 1 Technique is the curriculum that finishes it — so it costs the pick that any curriculum costs. A Gift is not learned. It grows with the person, and the person grows through whatever Facet they grow through. Charging a Body-Facet Orthaen a cross-Facet Technique to reach full scope would make "born gifted" cost more than "studied magic," which is the wrong way round. The Technique economy is untouched: no pick is spent, and the three-pick career is still three picks.

### 3.5 Creating a custom lineage *(MM-facing, its own subsection with the MM label)*

Five steps, mirroring II.6's custom Background:

1. **Name it, and say who they are.** Two or three sentences. A lineage is a *people*, not a profession; if the description reads like a job, it is a Background.
2. **Decide whether it is gifted.** If not, skip to step 4. If so, the gift is a domain: write it in the catalog format (territory, *beyond this domain's focus*, three example intents at each scope). Focused is the default type for a gift — a people's magic does one thing deeply. Standard if the gift genuinely spans a territory; never Prismatic.
3. **State the rate as fiction.** "Nearly all," "one in five," "vanishingly rare." Rate is texture and a prompt for how the ungifted are treated; it is not a roll.
4. **Write the Heritage.** One narrow fact, phrased as a Specialty is phrased: specific enough that the MM knows when it applies.
5. **Say what the Facet adds.** Every custom lineage lives in a setting Facet, and that Facet's counted-novelty line must name it ("this Facet adds seven lineages; the core 2d6 is unchanged").

Then the standing warning: a lineage is not a stat bonus. A lineage that wants to add to an attribute, to a skill rank, or to the Endurance Pool is asking for a number the core deliberately does not hand out at creation; give it a Heritage or a Gift instead.

### 3.6 Amendments elsewhere (one sentence each, same commit)

- **II.1** step list as above; the Zulnut example gains one line ("Lineage? — Human. Everyone at this table is.").
- **II.3 *Acquiring a Domain*** gains a third origin: *"or your Lineage, if the setting's lineages are gifted (Chapter II.5)"*, and *Before the Technique* gains the formalization exception cross-reference.
- **II.4 *Techniques***: after "If your Background grants a magical domain, your Facet level 1 pick is spoken for": *"A Lineage Gift is different — it formalizes at your first Facet level on its own and leaves the pick free (Chapter II.5)."*
- **II.6 Backgrounds** (renumbered): the one-domain rule in *Magic and Backgrounds*.
- **MM3** *Campaign Design*: a paragraph pointing MMs building a setting to II.5's custom-lineage steps and to the setting-Facet pitch format (`style/analysis/setting_books.md` §8, items 4 and 5).
- **Glossary**: Lineage, Gift, Heritage.
- **Character sheet appendix**: a Lineage line under Background; a Gift/Domain line already exists as Domain.
- **`references/phb-examples.md`**: note that the cast is human and the step is one word for them.

## 4. Data and engine

### 4.1 Ruleset data (`software/facets/base/facet.yaml`)

New top-level collection, merged by `id` like `backgrounds`:

```yaml
lineages:
  - id: human
    name: Human
    variants: [folk, people]
    description: >
      The default of the core rules and of Shattered Origin ...
    gift_domains: []          # empty list = ungifted
    gift_rate: null           # fiction only; a string when present ("four in five")
    heritage: null
    playable: true
    formalizes_on: first_facet_level   # option 1; ignored when gift_domains is empty
```

`spec/FOF-SPEC-v0.1.md` §4.3 gains `lineages[]` under collection sections, keyed by `id`; `spec/types/ruleset.md` gains the section. `MergedRuleset._merge` gains the same loop it runs for backgrounds and a `_lineage_map`.

### 4.2 Schema (`software/app/facets/schema.py`)

`LineageDefinition(BaseModel)` mirroring `BackgroundDefinition`'s docstring discipline: `id, name, variants: list[str], description, gift_domains: list[str], gift_rate: Optional[str], heritage: Optional[str], playable: bool = True, formalizes_on: Literal["first_facet_level", "technique"] = "first_facet_level"`. Validator: every id in `gift_domains` must exist in the merged domain catalog (INV-7's sibling; add INV-16: every lineage gift domain resolves).

### 4.3 Character (`software/app/game/character.py`)

- `lineage: str = "human"` (defaulted so every existing `.fof` loads unchanged).
- `gifted: bool = False`.
- `domain_source: Optional[Literal["lineage","background","technique"]]` recorded when `magic_domain` is set at creation, so the formalization hook knows which rule applies. Keep `magic_domain` as the single primary-domain field; do not add a parallel `lineage_domain`.
- **Creation validation** (where `domain_replaces_secondary` is handled, ~`character.py:1004`): if `gifted` and the Background has `domain_origin`, reject with a message that quotes the one-domain rule. If `gifted`, the lineage must have a non-empty `gift_domains`, the chosen domain must be in it, `magic_domain` is set, `domain_source = "lineage"`, and the secondary skill mark is skipped exactly as `skip_secondary` does today.
- **Formalization hook**: where a Facet level increments (the `advance_skill` path that sets Facet level), if `domain_source == "lineage"` and `formalizes_on == "first_facet_level"` and the magic Technique is not active, set the active flag without recording a Technique pick. The existing `formalizing = tech_def.magic_granting and choice == self.magic_domain` branch must *not* fire for a lineage-source domain that is already active (it would try to consume a pick to re-formalize).

### 4.4 API and app

- The creation request model in `software/app/api/` gains `lineage` and `gifted` (default `"human"`, `false`); the WebSocket `create_character` path validates through the character model, so no rule logic lives in the handler.
- The session-state payload already serializes backgrounds; add lineages so the builder can offer them.
- The builder's creation flow gets a Lineage picker between Facet and attributes, hidden when the merged ruleset has only `human` (so Shattered Origin tables never see an empty choice). This is the only UI work and it is a single task.

### 4.5 Tests (TDD; write first)

- Schema: loads; rejects a gift domain that does not exist; `playable` default.
- Merge: a second module adds a lineage; collision replaces by id; `human` survives.
- Character: default lineage on old files; gifted creation sets domain and skips secondary; gifted + domain Background rejected; ungifted member of a gifted lineage keeps secondary and has no domain; formalization fires on first Facet level with no pick consumed; option-2 flag path (formalizes_on = technique) leaves the old behaviour.
- Docs: INV-4/5/9/10 after the renumber; INV-2 for the new sheet line; INV-12 for the three glossary terms; new INV-16.
- Three tests per public function, per the project rule.

## 5. Order of work (for TASKS)

1. Renumber II.5→II.6, II.6→II.7; run the resolver; regenerate; suite green.
2. Schema + data + merge + INV-16 (tests first).
3. Character fields + creation validation (tests first).
4. Formalization hook (tests first).
5. II.5 chapter text; II.1/II.3/II.4/II.6/Quick Start/MM3/Glossary/sheet amendments; regenerate; INV-2/12 green.
6. API + builder picker.
7. `spec/` updates and `references/phb-examples.md` note.

## 6. Watch-outs

- **Do not let Heritage become a second Specialty in the arithmetic.** It shares the one-step allowance; the text in III.1 *Difficulty* already says "anything future" and needs no change, but the Heritage paragraph must say it.
- **Do not let Gift become a stat.** The custom-lineage guidance's last paragraph is there to stop the first homebrew lineage from adding +1 Constitution.
- **Old characters.** Every `.fof` in `characters/` and `playtest/` loads with `lineage: human`; the loader must not require the field.
- **The Bestiary is setting-agnostic (B9).** Nothing in it references lineage; keep it that way.
