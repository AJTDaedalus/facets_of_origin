"""The Lean Facets v1.0 character (PHB II, DESIGN §1 and §3.3).

A character is a Facet (which owns the numbers), a class (words, kit, picks),
a background (a knack and a Specialty) and a lineage. Every rule is read from
the merged ruleset; methods that need a rule take `ruleset` explicitly, so a
`Character` is plain data that round-trips through `.fof` files.

Level-ups, respec, damage, Hold On, rests, Fatigue, Wounds, slots, the usage
die, Sparks and talent-use tracking all live here. Combat and casting
(`combat.py`, `magic.py`) call into these methods rather than editing fields.
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Optional

from app.game.dice import DiceSpec
from app.game.engine import RollResult, resolve_roll

FOF_VERSION = "1.0"
DIE_SIZES = [4, 6, 8, 10, 12]
STATUSES = ("ok", "out", "dying", "dead")
_USE_PERIOD = {"once_per_scene": "scene", "once_per_session": "session", "once_per_rest": "rest"}
_RESET_PERIODS = {"scene": {"scene"}, "rest": {"rest", "scene"}, "session": {"session", "scene"}}


class CharacterFormatError(ValueError):
    """A character file that cannot be read as a v1.0 character."""


# ---------------------------------------------------------------------------
# Parts
# ---------------------------------------------------------------------------

@dataclass
class TalentState:
    id: str
    improved: bool = False
    choice: Optional[str] = None
    level_taken: int = 1
    via_teacher: bool = False

    def to_dict(self) -> dict:
        d: dict[str, Any] = {"id": self.id, "improved": self.improved}
        if self.choice is not None:
            d["choice"] = self.choice
        if self.level_taken != 1:
            d["level_taken"] = self.level_taken
        if self.via_teacher:
            d["via_teacher"] = True
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "TalentState":
        return cls(id=d["id"], improved=bool(d.get("improved", False)),
                   choice=d.get("choice"), level_taken=int(d.get("level_taken", 1)),
                   via_teacher=bool(d.get("via_teacher", False)))


@dataclass
class InventoryItem:
    id: str
    name: str
    slots: int = 1
    kind: Optional[str] = None          # weapon kind: blades, bows ...
    weapon: Optional[str] = None        # weapon category: light, standard ...
    armor: Optional[str] = None         # armor category: light, heavy, shield
    usage_die: Optional[int] = None
    curio: bool = False
    effect: Optional[str] = None

    def to_dict(self) -> dict:
        d: dict[str, Any] = {"id": self.id, "name": self.name, "slots": self.slots}
        for key in ("kind", "weapon", "armor", "usage_die", "effect"):
            if getattr(self, key) is not None:
                d[key] = getattr(self, key)
        if self.curio:
            d["curio"] = True
        return d

    @classmethod
    def from_dict(cls, d: dict, ruleset=None) -> "InventoryItem":
        """Build from a .fof entry; fields missing there are filled from the ruleset item."""
        base = ruleset.get_item(d.get("id", "")) if ruleset is not None else None
        def pick(key, default=None):
            if key in d:
                return d[key]
            return getattr(base, key, default) if base is not None else default
        return cls(
            id=d.get("id", ""), name=d.get("name") or (base.name if base else d.get("id", "")),
            slots=int(pick("slots", 1)), kind=pick("kind"), weapon=pick("weapon"),
            armor=pick("armor"), usage_die=pick("usage_die"), curio=bool(pick("curio", False)),
            effect=pick("effect"))

    @classmethod
    def from_ruleset(cls, ruleset, item_id: str) -> "InventoryItem":
        item = ruleset.get_item(item_id)
        if item is None:
            raise ValueError(f"Unknown item {item_id!r}.")
        return cls(id=item.id, name=item.name, slots=item.slots, kind=item.kind,
                   weapon=item.weapon, armor=item.armor, usage_die=item.usage_die,
                   curio=item.curio, effect=item.effect)


@dataclass
class MagicState:
    tradition: str
    domains: list[str] = field(default_factory=list)       # [primary, wider ...]
    signature_workings: list[str] = field(default_factory=list)
    origin: str = ""

    def to_dict(self) -> dict:
        d = {"tradition": self.tradition, "domains": list(self.domains),
             "signature_workings": list(self.signature_workings)}
        if self.origin:
            d["origin"] = self.origin
        return d

    @classmethod
    def from_dict(cls, d: Optional[dict]) -> Optional["MagicState"]:
        if not d:
            return None
        return cls(tradition=d["tradition"], domains=list(d.get("domains") or []),
                   signature_workings=list(d.get("signature_workings") or []),
                   origin=d.get("origin") or "")


# ---------------------------------------------------------------------------
# Character
# ---------------------------------------------------------------------------

@dataclass
class Character:
    name: str
    player_name: str
    facet: str
    stats: dict[str, int]
    class_id: Optional[str] = None
    class_name: str = ""
    concept: str = ""
    custom_class: bool = False
    class_talents: list[str] = field(default_factory=list)   # a custom class's starting pair
    class_signature: Optional[str] = None                   # its planned level-3 signature
    level: int = 1
    knacks: list[str] = field(default_factory=list)
    specialty: str = ""
    background: dict = field(default_factory=dict)       # {id, name, description}
    lineage: str = "human"
    gifted: bool = False                                # carries the lineage's gift
    gift_domain: Optional[str] = None
    talents: list[TalentState] = field(default_factory=list)
    signature: Optional[str] = None
    magic: Optional[MagicState] = None
    inventory: list[InventoryItem] = field(default_factory=list)
    equipped: dict = field(default_factory=lambda: {"weapon": None, "armor": "none", "shield": False})
    coin: int = 0
    fatigue: int = 0
    wounds: list[dict] = field(default_factory=list)
    scars: list[dict] = field(default_factory=list)
    sparks: int = 3
    talent_uses: dict[str, int] = field(default_factory=dict)
    hp_current: int = 0
    hp_gains: list[int] = field(default_factory=list)   # HP gained at levels 2..level
    hp_max_stored: Optional[int] = None                 # as read from a .fof
    status: str = "ok"                                  # ok | out | dying | dead
    notes_player: str = ""
    notes_mm: str = ""
    id: Optional[str] = None
    arcane_mastery_working: Optional[str] = None      # the working Arcane Mastery cheapens

    # ------------------------------------------------------------ talents
    def talent(self, talent_id: str) -> Optional[TalentState]:
        for t in self.talents:
            if t.id == talent_id:
                return t
        return None

    def has_talent(self, talent_id: str, improved: Optional[bool] = None) -> bool:
        """True if held (as a talent or as the signature); `improved` narrows it."""
        if self.signature == talent_id:
            return improved is not True
        t = self.talent(talent_id)
        if t is None:
            return False
        return improved is None or t.improved == improved

    def held_talent_ids(self) -> set[str]:
        ids = {t.id for t in self.talents}
        if self.signature:
            ids.add(self.signature)
        return ids

    def _effect_total(self, ruleset, key: str) -> int:
        total = 0
        for t in self.talents:
            tdef = ruleset.get_talent(t.id)
            if tdef is not None:
                total += int(tdef.effect(key, t.improved, 0) or 0)
        return total

    def _effect_max(self, ruleset, key: str) -> Optional[int]:
        best = None
        for t in self.talents:
            tdef = ruleset.get_talent(t.id)
            if tdef is not None:
                v = tdef.effect(key, t.improved)
                if v is not None:
                    best = v if best is None else max(best, v)
        return best

    # ------------------------------------------------------------ derived
    def facet_def(self, ruleset):
        f = ruleset.get_facet(self.facet)
        if f is None:
            raise ValueError(f"Unknown Facet {self.facet!r}.")
        return f

    def expected_gains(self, ruleset) -> list[int]:
        """Per-level HP gains, padded with the Facet average for unrecorded levels."""
        avg = self.facet_def(ruleset).grit_average
        gains = list(self.hp_gains[: max(0, self.level - 1)])
        gains += [avg] * (max(0, self.level - 1) - len(gains))
        return gains

    def hp_max(self, ruleset) -> int:
        """Grit die max + Body at level 1, plus each later level's gain, plus talent HP."""
        f = self.facet_def(ruleset)
        total = (f.grit_die + self.stats.get("body", 0) + sum(self.expected_gains(ruleset))
                 + self._effect_total(ruleset, "hp_bonus"))
        return max(1, total)

    def slots_total(self, ruleset) -> int:
        s = ruleset.slots
        return s.base + self.stats.get(s.plus_stat, 0) + self._effect_total(ruleset, "slots_bonus")

    def coin_slots(self, ruleset) -> int:
        return self.coin // ruleset.slots.coin_per_slot

    def slots_used(self, ruleset) -> int:
        used = sum(i.slots for i in self.inventory) + self.coin_slots(ruleset)
        if ruleset.wounds.takes_slot:
            used += len(self.wounds)
        if ruleset.magic.fatigue_takes_slot:
            used += self.fatigue
        return used

    def slots_free(self, ruleset) -> int:
        return self.slots_total(ruleset) - self.slots_used(ruleset)

    def curio_limit(self, ruleset) -> int:
        return ruleset.slots.curio_limit + self._effect_total(ruleset, "curio_bonus")

    def curios_carried(self) -> int:
        return sum(1 for i in self.inventory if i.curio)

    def equipped_weapon(self) -> Optional[InventoryItem]:
        wid = self.equipped.get("weapon")
        if not wid:
            return None
        for i in self.inventory:
            if i.id == wid and i.weapon:
                return i
        return None

    def is_ranged(self, ruleset=None) -> bool:
        w = self.equipped_weapon()
        return bool(w and w.weapon == "ranged")

    def armor_value(self, ruleset) -> int:
        """Worn armor + shield, capped; Unarmored Discipline when wearing neither."""
        eq = ruleset.equipment
        worn = self.equipped.get("armor") or "none"
        shield = bool(self.equipped.get("shield"))
        value = eq.armor[worn].armor if worn in eq.armor else 0
        if shield and "shield" in eq.armor:
            value += eq.armor["shield"].armor
        if worn == "none" and not shield:
            unarmored = self._effect_max(ruleset, "unarmored_armor")
            if unarmored is not None:
                value = max(value, int(unarmored))
        return min(value, ruleset.combat.armor.cap)

    def weapon_die(self, ruleset) -> int:
        """The equipped weapon's die (unarmed if none), after Weapon Master's step."""
        w = self.equipped_weapon()
        if w is None:
            die = ruleset.combat.unarmed_die
            better = self._effect_max(ruleset, "unarmed_die")
            return max(die, int(better)) if better else die
        die = ruleset.equipment.weapon_categories[w.weapon].die
        wm = self.talent("weapon_master")
        if wm and w.kind and wm.choice == w.kind:
            tdef = ruleset.get_talent("weapon_master")
            step = int(tdef.effect("weapon_die_step", wm.improved, 1)) if tdef else 1
            idx = DIE_SIZES.index(die) if die in DIE_SIZES else None
            if idx is not None:
                die = DIE_SIZES[min(len(DIE_SIZES) - 1, idx + step)]
        return die

    def damage_bonus(self, ruleset) -> int:
        return ruleset.advancement.damage_bonus_at(self.level)

    def traditions(self, ruleset) -> list[str]:
        out = []
        for t in self.talents:
            tdef = ruleset.get_talent(t.id)
            g = tdef.effects.get("grants_tradition") if tdef else None
            if g:
                out.append(g)
        return out

    @property
    def is_caster(self) -> bool:
        return self.magic is not None

    # ------------------------------------------------------------ sparks
    def spend_spark(self, n: int = 1) -> int:
        if n < 1:
            raise ValueError("Spend at least one Spark.")
        if n > self.sparks:
            raise ValueError(f"{self.name} has only {self.sparks} Spark(s).")
        self.sparks -= n
        return self.sparks

    def earn_spark(self, n: int = 1) -> int:
        if n < 1:
            raise ValueError("Earn at least one Spark.")
        self.sparks += n
        return self.sparks

    def start_session(self, ruleset) -> None:
        """Sparks reset to the base (no carry-over); session and scene uses refresh."""
        self.sparks = ruleset.spark.base_sparks_per_session
        self.reset_uses(ruleset, "session")

    # ------------------------------------------------------------ talent uses
    def _period_of(self, ruleset, key: str) -> Optional[str]:
        if "@" in key:
            return key.split("@", 1)[1]
        tdef = ruleset.get_talent(key)
        return _USE_PERIOD.get(tdef.use) if tdef else None

    def uses_remaining(self, ruleset, talent_id: str, period: Optional[str] = None,
                       limit: Optional[int] = None) -> Optional[int]:
        tdef = ruleset.get_talent(talent_id)
        if tdef is None:
            raise ValueError(f"Unknown talent {talent_id!r}.")
        state = self.talent(talent_id)
        key = talent_id if period is None else f"{talent_id}@{period}"
        allowed = limit if limit is not None else (
            1 if period is not None else tdef.uses_allowed(bool(state and state.improved)))
        if allowed is None:
            return None
        return max(0, allowed - self.talent_uses.get(key, 0))

    def use_talent(self, ruleset, talent_id: str, period: Optional[str] = None,
                   limit: Optional[int] = None) -> Optional[int]:
        """Spend one use of a talent. Returns uses left (None = untracked).

        `period` ("scene" | "session" | "rest") tracks an improved-form ability
        whose period differs from the talent's own `use`.

        Raises:
            ValueError: not held, unknown, or no uses left.
        """
        if not self.has_talent(talent_id):
            raise ValueError(f"{self.name} does not have {talent_id!r}.")
        if period is not None and period not in _RESET_PERIODS:
            raise ValueError(f"Unknown period {period!r}.")
        remaining = self.uses_remaining(ruleset, talent_id, period, limit)
        if remaining is None:
            return None
        if remaining < 1:
            raise ValueError(f"{talent_id} has no uses left.")
        key = talent_id if period is None else f"{talent_id}@{period}"
        self.talent_uses[key] = self.talent_uses.get(key, 0) + 1
        return remaining - 1

    def reset_uses(self, ruleset, period: str) -> None:
        """Refresh uses: 'scene' → scene; 'rest' → rest + scene; 'session' → session + scene."""
        if period not in _RESET_PERIODS:
            raise ValueError(f"Unknown period {period!r}.")
        clear = _RESET_PERIODS[period]
        for key in list(self.talent_uses):
            if self._period_of(ruleset, key) in clear:
                del self.talent_uses[key]

    # ------------------------------------------------------------ damage & rest
    def take_damage(self, ruleset, amount: int, allow_unstoppable: bool = True) -> dict:
        """Lose HP (not below 0). Unstoppable turns a drop to 0 into 1, once per scene."""
        if amount < 0:
            raise ValueError("Damage cannot be negative.")
        before = self.hp_current
        after = max(0, before - amount)
        unstoppable = False
        if (after == 0 and before > 0 and allow_unstoppable and self.signature == "unstoppable"
                and self.uses_remaining(ruleset, "unstoppable")):
            self.use_talent(ruleset, "unstoppable")
            after, unstoppable = 1, True
        self.hp_current = after
        return {"hp_before": before, "hp_after": after, "damage": amount,
                "dropped": after == 0 and before > 0, "unstoppable_used": unstoppable}

    def heal(self, ruleset, amount: int) -> int:
        if amount < 0:
            raise ValueError("Healing cannot be negative.")
        if self.status == "dead":
            raise ValueError(f"{self.name} is dead.")
        self.hp_current = min(self.hp_max(ruleset), self.hp_current + amount)
        if self.hp_current > 0 and self.status == "out":
            self.status = "ok"
        return self.hp_current

    def add_wound(self, name: str) -> dict:
        """Take a Wound. It fills a slot; if none is free the Wound is still
        taken and `items_to_drop()` says how many items must be dropped (PHB
        ruling: the character drops an item)."""
        if not name or not name.strip():
            raise ValueError("A Wound needs a name.")
        wound = {"name": name.strip()}
        self.wounds.append(wound)
        return wound

    def items_to_drop(self, ruleset) -> int:
        """Slots over capacity (e.g. after a Wound): items the character must drop."""
        return max(0, -self.slots_free(ruleset))

    def remove_wound(self, index: int = 0) -> dict:
        if not self.wounds:
            raise ValueError(f"{self.name} has no Wounds.")
        if not 0 <= index < len(self.wounds):
            raise ValueError(f"No Wound at {index}.")
        return self.wounds.pop(index)

    def hold_on(self, ruleset, dice=None, rng=None, sparks: int = 0) -> RollResult:
        """Roll Hold On (2d6 + Body) at 0 HP. Sets status and HP from the tier.

        10+ stand at 1 HP · 7-9 out of the fight (Tough improved: stand at 1)
        · 6- dying. Improved Tough makes the roll Easy.
        """
        if self.status == "dead":
            raise ValueError(f"{self.name} is dead.")
        if sparks > self.sparks:
            raise ValueError(f"{self.name} has only {self.sparks} Spark(s).")
        tough_plus = self.has_talent("tough", improved=True)
        stat = ruleset.hold_on.stat
        result = resolve_roll(ruleset, stat_value=self.stats.get(stat, 0), stat=stat,
                              difficulty="Easy" if tough_plus else "Standard",
                              sparks=sparks, dice=dice, rng=rng, kind="hold_on")
        self.sparks -= sparks
        if result.outcome == "full_success" or (result.outcome == "partial_success" and tough_plus):
            self.hp_current, self.status = 1, "ok"
        elif result.outcome == "partial_success":
            self.hp_current, self.status = 0, "out"
        else:
            self.hp_current, self.status = 0, "dying"
        result.extra["status"] = self.status
        result.extra["text"] = ruleset.hold_on.outcomes.get(result.outcome, "")
        return result

    def fall(self, ruleset, wound: Optional[str] = None, dice=None, rng=None) -> dict:
        """At 0 HP: take a Wound (rolled on the wounds table unless named) and roll Hold On."""
        if wound is None:
            from app.game.toolbox import roll_table   # local: toolbox imports nothing of ours
            table_id = ruleset.wounds.table
            wound = (roll_table(ruleset, table_id, rng=rng)["text"]
                     if ruleset.get_table(table_id) else "Wound")
        w = self.add_wound(wound)
        result = self.hold_on(ruleset, dice=dice, rng=rng)
        return {"wound": w, "hold_on": result, "items_to_drop": self.items_to_drop(ruleset)}

    def tend(self, field_surgeon: bool = False) -> str:
        """An ally tends a dying character: saved (out of the fight), or with
        Field Surgeon counted as a 10+ Hold On (standing at 1 HP)."""
        if self.status != "dying":
            raise ValueError(f"{self.name} is not dying.")
        if field_surgeon:
            self.hp_current, self.status = 1, "ok"
        else:
            self.status = "out"
        return self.status

    def death_choice(self, ruleset, choice: str, scar: Optional[str] = None, rng=None) -> dict:
        """Untended at scene's end: a permanent Scar (and live), or a heroic final action."""
        if self.status != "dying":
            raise ValueError(f"{self.name} is not dying.")
        if choice == "scar":
            if scar is None:
                from app.game.toolbox import roll_table
                tid = ruleset.death.scar_table
                scar = roll_table(ruleset, tid, rng=rng)["text"] if ruleset.get_table(tid) else "Scar"
            entry = {"name": scar}
            self.scars.append(entry)
            self.status = "out"
            return {"choice": "scar", "scar": entry, "status": self.status}
        if choice == "heroic":
            self.status = "dead"
            return {"choice": "heroic", "status": self.status,
                    "text": "A heroic final action that succeeds."}
        raise ValueError("The death choice is 'scar' or 'heroic'.")

    def breather(self, ruleset) -> int:
        """A few quiet minutes: recover half max HP (Iron Lungs improved: all)."""
        if self.status in ("dying", "dead"):
            raise ValueError(f"{self.name} is {self.status}; tend them first.")
        mx = self.hp_max(ruleset)
        gain = mx if self.has_talent("iron_lungs", improved=True) else mx // 2
        self.hp_current = min(mx, self.hp_current + gain)
        if self.hp_current > 0:
            self.status = "ok"
        return self.hp_current

    def night_rest(self, ruleset, wound_index: int = 0) -> dict:
        """A night's rest in safety: full HP, all Fatigue, one Wound, rest+scene uses."""
        if self.status == "dead":
            raise ValueError(f"{self.name} is dead.")
        if self.status == "dying":
            raise ValueError(f"{self.name} is dying; tend them first.")
        nr = ruleset.recovery.night_rest
        self.hp_current = self.hp_max(ruleset)
        self.status = "ok"
        cleared_fatigue = self.fatigue
        self.fatigue = 0
        cleared = []
        for _ in range(nr.clears_wounds):
            if self.wounds:
                idx = wound_index if 0 <= wound_index < len(self.wounds) else 0
                cleared.append(self.wounds.pop(idx))
        self.reset_uses(ruleset, "rest")
        return {"hp": self.hp_current, "fatigue_cleared": cleared_fatigue, "wounds_cleared": cleared}

    def add_fatigue(self, ruleset, n: int) -> int:
        """Fatigue fills slots. No free slot, no Fatigue (and so no full working)."""
        if n < 0:
            raise ValueError("Fatigue cannot be negative.")
        if ruleset.magic.fatigue_takes_slot and n > self.slots_free(ruleset):
            raise ValueError(f"{self.name} has {self.slots_free(ruleset)} free slot(s); "
                             f"{n} Fatigue will not fit.")
        self.fatigue += n
        return self.fatigue

    # ------------------------------------------------------------ gear
    def add_item(self, ruleset, item) -> InventoryItem:
        """Add an item (an id from the ruleset, or an InventoryItem).

        Raises:
            ValueError: unknown id, not enough free slots, or the curio limit reached.
        """
        it = InventoryItem.from_ruleset(ruleset, item) if isinstance(item, str) else item
        if it.slots > self.slots_free(ruleset):
            raise ValueError(f"{it.name} needs {it.slots} slot(s); "
                             f"{self.slots_free(ruleset)} free.")
        if it.curio and self.curios_carried() >= self.curio_limit(ruleset):
            raise ValueError(f"{self.name} already carries {self.curio_limit(ruleset)} curios.")
        self.inventory.append(it)
        return it

    def remove_item(self, item_id: str) -> InventoryItem:
        for idx, it in enumerate(self.inventory):
            if it.id == item_id:
                removed = self.inventory.pop(idx)
                if self.equipped.get("weapon") == item_id and not any(
                        i.id == item_id for i in self.inventory):
                    self.equipped["weapon"] = None
                return removed
        raise ValueError(f"{self.name} carries no {item_id!r}.")

    def usage_roll(self, ruleset, item_id: str, roll: Optional[int] = None, rng=None) -> dict:
        """Roll an item's usage die after a scene of use; 1-2 steps it down (d8→d6→d4→gone)."""
        item = next((i for i in self.inventory if i.id == item_id), None)
        if item is None:
            raise ValueError(f"{self.name} carries no {item_id!r}.")
        if not item.usage_die:
            raise ValueError(f"{item.name} has no usage die.")
        ud = ruleset.exploration.usage_die
        die = item.usage_die
        if roll is None:
            roll = (rng or random).randint(1, die)
        elif not 1 <= roll <= die:
            raise ValueError(f"A d{die} cannot roll {roll}.")
        stepped, gone = False, False
        if roll in ud.steps_down_on:
            stepped = True
            idx = ud.steps.index(die) if die in ud.steps else len(ud.steps) - 1
            if idx + 1 < len(ud.steps):
                item.usage_die = ud.steps[idx + 1]
            else:
                gone = True
                self.inventory.remove(item)
        return {"item": item.id, "roll": roll, "die": die, "stepped_down": stepped,
                "usage_die": None if gone else item.usage_die, "gone": gone}

    def spend_coin(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        if amount > self.coin:
            raise ValueError(f"{self.name} has only {self.coin} coin.")
        self.coin -= amount
        return self.coin

    def add_coin(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        self.coin += amount
        return self.coin

    # ------------------------------------------------------------ advancement
    def _menu_errors(self, ruleset, tdef, teacher: bool, kind: str) -> list[str]:
        errors = []
        if tdef.kind != kind:
            errors.append(f"{tdef.name} is a {tdef.kind}, not a {kind}.")
        casting = bool(tdef.effects.get("grants_tradition"))
        if not tdef.on_menu_of(self.facet):
            if casting:
                errors.append(f"{tdef.name} is a casting talent of another Facet; "
                              "only its own Facet can take it.")
            elif ruleset.advancement.off_facet_requires == "teacher" and not teacher:
                errors.append(f"{tdef.name} is off your Facet's menu; it needs a teacher "
                              "found in play.")
        if tdef.requires and tdef.requires.any_talent:
            if not (self.held_talent_ids() & set(tdef.requires.any_talent)):
                errors.append(f"{tdef.name} requires one of: {', '.join(tdef.requires.any_talent)}.")
        return errors

    def _choice_errors(self, ruleset, tdef, choice: Optional[str]) -> list[str]:
        if tdef.id == "weapon_master":
            if choice not in ruleset.equipment.weapon_kinds:
                return [f"Weapon Master needs a weapon kind: {ruleset.equipment.weapon_kinds}."]
        elif tdef.id == "wider_domain":
            if self.magic is None:
                return ["Wider Domain needs a tradition."]
            dom = ruleset.get_domain(choice or "")
            if dom is None or dom.tradition != self.magic.tradition or dom.prismatic:
                return ["Wider Domain needs a non-prismatic domain of your tradition."]
            if dom.id in self.magic.domains:
                return [f"You already hold {dom.name}."]
        return []

    def _apply_talent_choice(self, tdef, choice: Optional[str]) -> None:
        if tdef.id == "wider_domain" and self.magic is not None and choice:
            self.magic.domains.append(choice)

    def level_up(self, ruleset, *, kind: str, talent_id: Optional[str] = None,
                 choice: Optional[str] = None, teacher: bool = False,
                 stat: Optional[str] = None, signature_working: Optional[str] = None,
                 hp_roll: Optional[int] = None, extra_talents: Optional[list[str]] = None) -> list[str]:
        """Advance one level (MM-called). Returns errors; nothing changes if any.

        kind: "talent" (a new talent), "improve" (the improved form of a held
        talent) or "signature" (required at the signature level, and only then).
        stat: required at levels 4 and 8 (+1, max 3).
        signature_working: required for casters at levels 5 and 9.
        hp_roll: the grit die result; None takes the Facet average.
        extra_talents: Polymath's two talents from any menu (no casting talents).
        """
        adv = ruleset.advancement
        errors: list[str] = []
        if self.status == "dead":
            return [f"{self.name} is dead."]
        if self.level >= adv.max_level:
            return [f"{self.name} is already level {adv.max_level}."]
        new_level = self.level + 1
        tdef = ruleset.get_talent(talent_id or "")
        if tdef is None:
            return [f"Unknown talent {talent_id!r}."]

        # --- the pick
        if new_level == adv.signature_level:
            if kind != "signature":
                errors.append(f"At level {adv.signature_level} the pick is your signature.")
            else:
                errors += self._menu_errors(ruleset, tdef, teacher, "signature")
                if tdef.id == "arcane_mastery" and self.magic and choice and \
                        choice not in self.magic.signature_workings:
                    errors.append("Arcane Mastery must name one of your signature workings.")
                if tdef.id == "polymath":
                    extras = extra_talents or []
                    if len(extras) != 2 or len(set(extras)) != 2:
                        errors.append("Polymath takes two different talents.")
                    for eid in extras:
                        e = ruleset.get_talent(eid)
                        if e is None or e.kind != "talent":
                            errors.append(f"{eid!r} is not a talent.")
                        elif e.effects.get("grants_tradition"):
                            errors.append("Polymath never takes a casting talent.")
                        elif self.has_talent(eid):
                            errors.append(f"You already hold {e.name}.")
        elif kind == "signature":
            errors.append(f"A signature is taken at level {adv.signature_level}.")
        elif kind == "talent":
            if self.has_talent(tdef.id):
                errors.append(f"You already hold {tdef.name}.")
            errors += self._menu_errors(ruleset, tdef, teacher, "talent")
            if not errors:
                errors += self._choice_errors(ruleset, tdef, choice)
        elif kind == "improve":
            held = self.talent(tdef.id)
            if held is None:
                errors.append(f"You do not hold {tdef.name}.")
            elif held.improved:
                errors.append(f"{tdef.name} is already improved.")
            elif not tdef.improved:
                errors.append(f"{tdef.name} has no improved form.")
            elif self.level - held.level_taken + 1 < adv.improve_requires_levels_held:
                errors.append(f"Hold {tdef.name} for {adv.improve_requires_levels_held} "
                              "level(s) before improving it.")
            if tdef.id == "wider_domain" and choice:
                dom = ruleset.get_domain(choice)
                if dom is None or not dom.prismatic or self.magic is None \
                        or dom.tradition != self.magic.tradition:
                    errors.append("Wider Domain can only trade up to a prismatic domain of your tradition.")
                elif new_level < 5:
                    errors.append("A prismatic domain needs level 5.")
        else:
            errors.append(f"Unknown pick kind {kind!r}.")

        # --- stat increase
        if new_level in adv.stat_increase_levels:
            if stat not in self.stats:
                errors.append(f"Level {new_level} raises a stat: name body, mind or soul.")
            elif self.stats[stat] + ruleset.stat_rules.increase_amount > ruleset.stat_rules.maximum:
                errors.append(f"{stat} is already at the maximum.")
        elif stat is not None:
            errors.append(f"Level {new_level} does not raise a stat.")

        # --- casters' signature working
        if self.magic is not None and new_level in adv.signature_working_levels:
            if not signature_working or not signature_working.strip():
                errors.append(f"At level {new_level} a caster names another signature working.")

        # --- HP
        die = self.facet_def(ruleset).grit_die
        if hp_roll is not None and not 1 <= hp_roll <= die:
            errors.append(f"A d{die} cannot roll {hp_roll}.")

        if errors:
            return errors

        # --- apply (measure max HP first, so a new Tough or Body point also
        # raises current HP by what it adds to the maximum)
        old_max = self.hp_max(ruleset)
        if kind == "signature":
            self.signature = tdef.id
            if tdef.id == "arcane_mastery" and self.magic:
                self.arcane_mastery_working = choice or (self.magic.signature_workings[0]
                                                         if self.magic.signature_workings else None)
            for eid in extra_talents or []:
                self.talents.append(TalentState(id=eid, level_taken=new_level))
        elif kind == "talent":
            self.talents.append(TalentState(id=tdef.id, choice=choice, level_taken=new_level,
                                            via_teacher=not tdef.on_menu_of(self.facet)))
            self._apply_talent_choice(tdef, choice)
        else:
            held = self.talent(tdef.id)
            held.improved = True
            if tdef.id == "wider_domain" and choice and self.magic:
                old = held.choice
                if old in self.magic.domains:
                    self.magic.domains[self.magic.domains.index(old)] = choice
                else:
                    self.magic.domains.append(choice)
                held.choice = choice
        if stat is not None:
            self.stats[stat] += ruleset.stat_rules.increase_amount
        if signature_working and self.magic is not None:
            self.magic.signature_workings.append(signature_working.strip())
        f = self.facet_def(ruleset)
        gain = max(ruleset.hp.minimum_gain, hp_roll if hp_roll is not None else f.grit_average)
        self.hp_gains = self.expected_gains(ruleset) + [gain]
        self.level = new_level
        self.hp_current += self.hp_max(ruleset) - old_max
        return []

    def can_respec(self, ruleset) -> bool:
        return self.level < ruleset.advancement.respec_until_level

    def respec(self, ruleset, talents: list[dict], magic: Optional[dict] = None) -> list[str]:
        """Rebuild talent picks for free before the signature level.

        `talents` lists {id, improved?, choice?}; each improved counts as a pick.
        Picks must equal starting talents + (level - 1), all from your own menu.
        """
        if not self.can_respec(ruleset):
            return [f"Rebuilding stops being free at level {ruleset.advancement.respec_until_level}."]
        errors: list[str] = []
        picks = sum(1 + (1 if t.get("improved") else 0) for t in talents)
        expected = ruleset.advancement.starting_talents + self.level - 1
        if picks != expected:
            errors.append(f"A level-{self.level} character has {expected} picks; got {picks}.")
        ids = [t.get("id") for t in talents]
        if len(set(ids)) != len(ids):
            errors.append("A talent is listed twice.")
        new_states = []
        for spec in talents:
            tdef = ruleset.get_talent(spec.get("id", ""))
            if tdef is None:
                errors.append(f"Unknown talent {spec.get('id')!r}.")
                continue
            if tdef.kind != "talent" or not tdef.on_menu_of(self.facet):
                errors.append(f"{tdef.name} is not on your Facet's talent menu.")
            new_states.append(TalentState(id=tdef.id, improved=bool(spec.get("improved")),
                                          choice=spec.get("choice")))
        if errors:
            return errors
        trial = Character.from_fof(self.to_fof([]))
        trial.talents = new_states
        trial.magic = None
        if magic is None and self.magic is not None and trial.traditions(ruleset):
            magic = {"domain": self.magic.domains[0],
                     "signature_workings": list(self.magic.signature_workings)}
        errors += _magic_setup_errors(ruleset, trial, magic)
        for st in new_states:
            tdef = ruleset.get_talent(st.id)
            if tdef.requires and tdef.requires.any_talent and not (
                    {s.id for s in new_states} & set(tdef.requires.any_talent)):
                errors.append(f"{tdef.name} requires one of: {', '.join(tdef.requires.any_talent)}.")
            if st.id == "weapon_master" and st.choice not in ruleset.equipment.weapon_kinds:
                errors.append("Weapon Master needs a weapon kind.")
        if errors:
            return errors
        self.talents = new_states
        self.magic = trial.magic
        self.hp_current = min(self.hp_current, self.hp_max(ruleset))
        return []

    # ------------------------------------------------------------ validation
    def validate_against_ruleset(self, ruleset) -> list[str]:
        """Hard errors: anything the engine cannot run."""
        errors: list[str] = []
        f = ruleset.get_facet(self.facet)
        if f is None:
            return [f"Unknown Facet {self.facet!r}."]
        if set(self.stats) != {s.id for s in ruleset.stats}:
            errors.append(f"Stats must be exactly {[s.id for s in ruleset.stats]}.")
        for sid, v in self.stats.items():
            if v > ruleset.stat_rules.maximum or v < -1:
                errors.append(f"Stat {sid} = {v} is out of range.")
        if not 1 <= self.level <= ruleset.advancement.max_level:
            errors.append(f"Level {self.level} is out of range.")
        if self.status not in STATUSES:
            errors.append(f"Unknown status {self.status!r}.")
        if self.class_id and not self.custom_class and ruleset.get_class(self.class_id) is None:
            errors.append(f"Unknown class {self.class_id!r}.")
        if not self.knacks:
            errors.append("A character needs a class knack.")
        if ruleset.get_lineage(self.lineage) is None:
            errors.append(f"Unknown lineage {self.lineage!r}.")
        for t in self.talents:
            tdef = ruleset.get_talent(t.id)
            if tdef is None:
                errors.append(f"Unknown talent {t.id!r}.")
            elif tdef.kind != "talent":
                errors.append(f"{t.id} is a signature, not a talent.")
        if self.signature:
            sdef = ruleset.get_talent(self.signature)
            if sdef is None or sdef.kind != "signature":
                errors.append(f"Unknown signature {self.signature!r}.")
            if self.level < ruleset.advancement.signature_level:
                errors.append("A signature is taken at level "
                              f"{ruleset.advancement.signature_level}.")
        traditions = self.traditions(ruleset)
        if traditions and self.magic is None:
            errors.append("A character with a casting talent needs a magic block "
                          "(tradition, domain, signature workings).")
        if self.magic is not None and not traditions:
            errors.append("Only a character with a casting talent has a magic block.")
        if self.magic is not None:
            if traditions and self.magic.tradition not in traditions:
                errors.append(f"Tradition {self.magic.tradition!r} does not match the casting talent.")
            if self.magic.tradition not in ruleset.magic.traditions:
                errors.append(f"Unknown tradition {self.magic.tradition!r}.")
            for d in self.magic.domains:
                if ruleset.get_domain(d) is None:
                    errors.append(f"Unknown domain {d!r}.")
        lin = ruleset.get_lineage(self.lineage)
        if self.gifted and lin is not None and not lin.gifted:
            errors.append(f"The {lin.name} lineage carries no gift.")
        if self.gift_domain:
            if not self.gifted:
                errors.append("Only a gifted character has a gift domain.")
            if ruleset.get_domain(self.gift_domain) is None:
                errors.append(f"Unknown gift domain {self.gift_domain!r}.")
            elif lin is not None and not lin.gift_domain_scope:
                errors.append(f"The {lin.name} lineage has no gift domain.")
        if self.class_signature:
            sdef = ruleset.get_talent(self.class_signature)
            if sdef is None or sdef.kind != "signature":
                errors.append(f"Class signature {self.class_signature!r} is not a signature.")
        eq = ruleset.equipment
        armor = self.equipped.get("armor") or "none"
        if armor not in eq.armor or armor == "shield":
            errors.append(f"Unknown worn armor {armor!r}.")
        elif armor != "none" and not any(i.armor == armor for i in self.inventory):
            errors.append(f"Wearing {armor} armor that is not in the inventory.")
        if self.equipped.get("shield") and not any(i.armor == "shield" for i in self.inventory):
            errors.append("Carrying a shield that is not in the inventory.")
        wid = self.equipped.get("weapon")
        if wid and self.equipped_weapon() is None:
            errors.append(f"Equipped weapon {wid!r} is not a weapon in the inventory.")
        for i in self.inventory:
            if i.weapon and i.weapon not in eq.weapon_categories:
                errors.append(f"Item {i.id!r} has unknown weapon category {i.weapon!r}.")
        if self.fatigue < 0 or self.sparks < 0 or self.coin < 0:
            errors.append("Fatigue, Sparks and coin cannot be negative.")
        return errors

    def warnings(self, ruleset) -> list[str]:
        """Soft problems a sheet should flag but the engine can play through."""
        out = []
        if self.hp_max_stored is not None and self.hp_max_stored != self.hp_max(ruleset):
            out.append(f"Stored max HP {self.hp_max_stored} differs from the computed "
                       f"{self.hp_max(ruleset)}.")
        if self.slots_free(ruleset) < 0:
            out.append(f"Over-burdened by {-self.slots_free(ruleset)} slot(s).")
        if self.curios_carried() > self.curio_limit(ruleset):
            out.append("Carrying more curios than the limit.")
        return out

    # ------------------------------------------------------------ serialise
    def to_fof(self, module_refs: list[dict], session_id: Optional[str] = None,
               ruleset=None) -> dict:
        """Character .fof v1.0 (DESIGN §3.3)."""
        hp_max = self.hp_max(ruleset) if ruleset is not None else self.hp_max_stored
        hp: dict[str, Any] = {"max": hp_max, "current": self.hp_current}
        if self.hp_gains:
            hp["gains"] = list(self.hp_gains)
        lineage: dict[str, Any] = {"id": self.lineage}
        if self.gifted:
            lineage["gifted"] = True
        elif self.lineage != "human":
            lineage["gifted"] = False
        if self.gift_domain:
            lineage["gift_domain"] = self.gift_domain
        body: dict[str, Any] = {
            "name": self.name,
            "player_name": self.player_name,
            "facet": self.facet,
            "level": self.level,
            "class": _class_block(self),
            "stats": dict(self.stats),
            "hp": hp,
            "knacks": list(self.knacks),
            "specialty": self.specialty,
            "background": dict(self.background),
            "lineage": lineage,
            "talents": [t.to_dict() for t in self.talents],
            "signature": self.signature,
            "magic": self.magic.to_dict() if self.magic else None,
            "inventory": [i.to_dict() for i in self.inventory],
            "equipped": dict(self.equipped),
            "coin": self.coin,
            "fatigue": self.fatigue,
            "wounds": [dict(w) for w in self.wounds],
            "scars": [dict(s) for s in self.scars],
            "sparks": self.sparks,
            "talent_uses": dict(self.talent_uses),
            "notes_player": self.notes_player,
            "notes_mm": self.notes_mm,
        }
        if self.status != "ok":
            body["status"] = self.status
        if self.arcane_mastery_working:
            body["arcane_mastery_working"] = self.arcane_mastery_working
        out: dict[str, Any] = {
            "fof_version": FOF_VERSION,
            "type": "character",
            "id": self.id or _slug(self.name),
            "name": self.name,
            "ruleset": {"modules": list(module_refs)},
        }
        if session_id:
            out["session_id"] = session_id
        out["character"] = body
        return out

    @classmethod
    def from_fof(cls, fof: dict, ruleset=None) -> "Character":
        """Read a character .fof v1.0. A v0.3 file fails with a clear message.

        Raises:
            CharacterFormatError (a ValueError): wrong type, old format, or missing fields.
        """
        if not isinstance(fof, dict) or fof.get("type") != "character":
            raise CharacterFormatError("Not a character file (type: character).")
        c = fof.get("character")
        if not isinstance(c, dict):
            raise CharacterFormatError("Character file has no `character:` block.")
        if str(fof.get("fof_version")) != FOF_VERSION or "attributes" in c or "primary_facet" in c:
            raise CharacterFormatError(
                "This character file uses the retired v0.3 format (nine attributes, skills, "
                "Techniques). Lean Facets v1.0 characters have three stats, a class and "
                "talents: rebuild the character in the app, or see PHB II.1. The old rules "
                "are preserved at git tag `pre-lean-facets`.")
        missing = [k for k in ("name", "facet", "stats") if k not in c]
        if missing:
            raise CharacterFormatError(f"Character file is missing: {', '.join(missing)}.")
        klass = c.get("class") or {}
        hp = c.get("hp") or {}
        lineage = c.get("lineage") or {"id": "human"}
        if isinstance(lineage, str):
            lineage = {"id": lineage}
        equipped = {"weapon": None, "armor": "none", "shield": False}
        equipped.update(c.get("equipped") or {})
        ch = cls(
            id=fof.get("id"),
            name=c["name"],
            player_name=c.get("player_name") or c["name"],
            facet=c["facet"],
            stats={k: int(v) for k, v in (c.get("stats") or {}).items()},
            class_id=klass.get("id"),
            class_name=klass.get("name", ""),
            concept=klass.get("concept", ""),
            custom_class=bool(klass.get("custom", False)),
            class_talents=list(klass.get("talents") or []),
            class_signature=klass.get("signature"),
            level=int(c.get("level", 1)),
            knacks=list(c.get("knacks") or []),
            specialty=c.get("specialty") or "",
            background=dict(c.get("background") or {}),
            lineage=lineage.get("id", "human"),
            gifted=bool(lineage.get("gifted", bool(lineage.get("gift_domain")))),
            gift_domain=lineage.get("gift_domain"),
            talents=[TalentState.from_dict(t) for t in c.get("talents") or []],
            signature=c.get("signature"),
            magic=MagicState.from_dict(c.get("magic")),
            inventory=[InventoryItem.from_dict(i, ruleset) for i in c.get("inventory") or []],
            equipped=equipped,
            coin=int(c.get("coin", 0)),
            fatigue=int(c.get("fatigue", 0)),
            wounds=[_named(w) for w in c.get("wounds") or []],
            scars=[_named(s) for s in c.get("scars") or []],
            sparks=int(c.get("sparks", 3)),
            talent_uses={k: int(v) for k, v in (c.get("talent_uses") or {}).items()},
            hp_current=int(hp.get("current", hp.get("max", 0)) or 0),
            hp_gains=[int(g) for g in hp.get("gains") or []],
            hp_max_stored=hp.get("max"),
            status=c.get("status", "ok"),
            notes_player=c.get("notes_player") or "",
            notes_mm=c.get("notes_mm") or "",
        )
        ch.arcane_mastery_working = c.get("arcane_mastery_working")
        return ch

    def to_client_dict(self, ruleset=None) -> dict:
        """JSON-safe view for clients; derived numbers included when a ruleset is given."""
        d = self.to_fof([], ruleset=ruleset)["character"]
        d["id"] = self.id or _slug(self.name)
        d["status"] = self.status
        if ruleset is not None:
            d["derived"] = {
                "hp_max": self.hp_max(ruleset),
                "slots_total": self.slots_total(ruleset),
                "slots_used": self.slots_used(ruleset),
                "slots_free": self.slots_free(ruleset),
                "armor": self.armor_value(ruleset),
                "weapon_die": self.weapon_die(ruleset),
                "ranged": self.is_ranged(ruleset),
                "damage_bonus": self.damage_bonus(ruleset),
                "curio_limit": self.curio_limit(ruleset),
                "items_to_drop": self.items_to_drop(ruleset),
                "grit_die": self.facet_def(ruleset).grit_die,
                "warnings": self.warnings(ruleset),
            }
        return d


def _class_block(ch: "Character") -> dict:
    d: dict[str, Any] = {"id": ch.class_id, "name": ch.class_name, "concept": ch.concept,
                         "custom": ch.custom_class}
    if ch.class_talents:
        d["talents"] = list(ch.class_talents)
    if ch.class_signature:
        d["signature"] = ch.class_signature
    return d


def planned_signature(ruleset, ch: "Character") -> Optional[str]:
    """The class's level-3 signature: the preset's, or a custom class's stated one."""
    if ch.class_signature:
        return ch.class_signature
    klass = ruleset.get_class(ch.class_id or "") if not ch.custom_class else None
    return klass.signature if klass else None


def _named(entry) -> dict:
    if isinstance(entry, str):
        return {"name": entry}
    return dict(entry)


def _slug(name: str) -> str:
    out = "".join(ch.lower() if ch.isalnum() else "_" for ch in name).strip("_")
    while "__" in out:
        out = out.replace("__", "_")
    return out or "character"


# ---------------------------------------------------------------------------
# Creation
# ---------------------------------------------------------------------------

def _magic_setup_errors(ruleset, character: Character, magic: Optional[dict]) -> list[str]:
    """Validate and install the magic block for a character's casting talent."""
    traditions = character.traditions(ruleset)
    if not traditions:
        if magic:
            return ["Only a character with a casting talent (Thaumaturgy or Invocation) "
                    "has a domain and signature workings."]
        character.magic = None
        return []
    tradition = traditions[0]
    magic = magic or {}
    errors: list[str] = []
    domain = ruleset.get_domain(magic.get("domain") or "")
    if domain is None:
        errors.append(f"A {tradition} caster chooses a domain.")
    elif domain.tradition != tradition or domain.prismatic:
        errors.append(f"{domain.name} is not a non-prismatic {tradition} domain.")
    workings = [w.strip() for w in magic.get("signature_workings") or [] if w and w.strip()]
    need = ruleset.magic.starting_signature_workings
    if len(workings) != need:
        errors.append(f"Name {need} signature workings.")
    if errors:
        return errors
    character.magic = MagicState(tradition=tradition, domains=[domain.id],
                                 signature_workings=workings)
    return []


def roll_starting_coin(ruleset, rng=None) -> int:
    """Starting coin, e.g. '2d6x10'."""
    expr = ruleset.equipment.starting_coin or "0d6"
    mult = 1
    if "x" in expr:
        expr, m = expr.split("x", 1)
        mult = int(m)
    try:
        spec = DiceSpec.parse(expr)
    except ValueError:
        return 0
    r = rng or random
    return spec.total([r.randint(1, spec.sides) for _ in range(spec.count)]) * mult


def _auto_equip(ruleset, character: Character) -> None:
    eq = ruleset.equipment
    weapons = [i for i in character.inventory if i.weapon]
    if weapons:
        best = max(weapons, key=lambda i: eq.weapon_categories[i.weapon].die
                   if i.weapon in eq.weapon_categories else 0)
        character.equipped["weapon"] = best.id
    worn = [i.armor for i in character.inventory if i.armor and i.armor != "shield"]
    if worn:
        character.equipped["armor"] = max(worn, key=lambda a: eq.armor[a].armor)
    character.equipped["shield"] = any(i.armor == "shield" for i in character.inventory)


def create_character(
    ruleset,
    *,
    name: str,
    player_name: str,
    facet: str,
    second_stat: str,
    class_id: Optional[str] = None,
    custom_class: Optional[dict] = None,
    background_id: Optional[str] = None,
    custom_background: Optional[dict] = None,
    lineage: str = "human",
    gifted: Optional[bool] = None,
    gift_domain: Optional[str] = None,
    talent_choices: Optional[dict[str, str]] = None,
    magic: Optional[dict] = None,
    kit: Optional[list[str]] = None,
    coin: Optional[int] = None,
    rng=None,
) -> tuple[Optional[Character], list[str]]:
    """Build a level-1 character from a preset class or a custom one.

    Args:
        facet: body | mind | soul — that stat is +2.
        second_stat: the other stat that is +1 (the third is +0).
        class_id: a preset class of that Facet; or
        custom_class: {name, concept, knack, talents: [2 ids], kit: [item ids]}.
        background_id / custom_background: a listed background, or
            {name, knack, specialty, description}.
        lineage: a lineage id; a gifted lineage adds its gift knack, and one
            with `gift_domain_scope` needs `gift_domain` (Minor workings only).
        gifted: whether this character carries the lineage's gift (default:
            yes, for a gifted lineage). An ungifted member has no gift knack.
        talent_choices: {talent_id: choice} (Weapon Master's kind, Wider Domain's domain).
        magic: {domain, signature_workings: [two]} for a character with a casting talent.
        kit: override the class kit (item ids).
        coin: starting coin; None rolls it.

    Returns:
        (character, []) or (None, errors).
    """
    errors: list[str] = []
    choices = dict(talent_choices or {})
    if not name or not name.strip():
        errors.append("A character needs a name.")
    f = ruleset.get_facet(facet)
    if f is None:
        return None, [f"Unknown Facet {facet!r}."]
    stat_ids = [s.id for s in ruleset.stats]
    rules = ruleset.stat_rules.creation
    if second_stat not in stat_ids or second_stat == f.stat:
        errors.append(f"The second stat must be one of {[s for s in stat_ids if s != f.stat]}.")
    stats = {s: rules.third for s in stat_ids}
    stats[f.stat] = rules.facet_stat
    if second_stat in stats and second_stat != f.stat:
        stats[second_stat] = rules.second

    # --- class
    klass = None
    if class_id and custom_class:
        errors.append("Choose a preset class or write a custom one, not both.")
    if class_id:
        klass = ruleset.get_class(class_id)
        if klass is None:
            return None, errors + [f"Unknown class {class_id!r}."]
        if klass.facet != facet:
            errors.append(f"{klass.name} is a {klass.facet} class.")
        class_name, concept, class_knack = klass.name, klass.concept, klass.knack
        talent_ids = list(klass.talents)
        kit_ids = list(kit if kit is not None else klass.kit)
        custom = False
    elif custom_class:
        class_name = (custom_class.get("name") or "").strip()
        concept = (custom_class.get("concept") or "").strip()
        class_knack = (custom_class.get("knack") or "").strip()
        talent_ids = list(custom_class.get("talents") or [])
        kit_ids = list(kit if kit is not None else custom_class.get("kit") or [])
        custom = True
        planned = custom_class.get("signature")
        if planned:
            sdef = ruleset.get_talent(planned)
            if sdef is None or sdef.kind != "signature" or not sdef.on_menu_of(facet):
                errors.append(f"{planned!r} is not a {facet} signature.")
        if not class_name:
            errors.append("A custom class needs a name.")
        if not concept:
            errors.append("A custom class needs a one-sentence concept.")
        if not class_knack:
            errors.append("A custom class needs a class knack.")
    else:
        return None, errors + ["Choose a preset class or write a custom one."]

    need = ruleset.advancement.starting_talents
    if len(talent_ids) != need or len(set(talent_ids)) != len(talent_ids):
        errors.append(f"A class starts with {need} different talents.")
    talent_states = []
    for tid in talent_ids:
        tdef = ruleset.get_talent(tid)
        if tdef is None:
            errors.append(f"Unknown talent {tid!r}.")
            continue
        if tdef.kind != "talent" or not tdef.on_menu_of(facet):
            errors.append(f"{tdef.name} is not on the {facet} talent menu.")
        if tdef.requires and tdef.requires.any_talent and not set(talent_ids) & set(tdef.requires.any_talent):
            errors.append(f"{tdef.name} requires one of: {', '.join(tdef.requires.any_talent)}.")
        if tid == "weapon_master" and choices.get(tid) not in ruleset.equipment.weapon_kinds:
            errors.append(f"Weapon Master needs a weapon kind: {ruleset.equipment.weapon_kinds}.")
        talent_states.append(TalentState(id=tid, choice=choices.get(tid)))

    # --- background
    if background_id and custom_background:
        errors.append("Choose a listed background or write your own, not both.")
    if background_id:
        bg = ruleset.get_background(background_id)
        if bg is None:
            return None, errors + [f"Unknown background {background_id!r}."]
        background = {"id": bg.id, "name": bg.name, "description": bg.description}
        bg_knack, specialty = bg.knack, bg.specialty
    elif custom_background:
        background = {"id": None, "name": (custom_background.get("name") or "").strip(),
                      "description": (custom_background.get("description") or "").strip()}
        bg_knack = (custom_background.get("knack") or "").strip()
        specialty = (custom_background.get("specialty") or "").strip()
        if not background["name"] or not bg_knack or not specialty:
            errors.append("A custom background needs a name, a knack and a Specialty.")
    else:
        errors.append("Choose a background or write your own.")
        background, bg_knack, specialty = {}, "", ""

    # --- lineage
    lin = ruleset.get_lineage(lineage)
    knacks = [k for k in (class_knack, bg_knack) if k]
    is_gifted = False
    if lin is None:
        errors.append(f"Unknown lineage {lineage!r}.")
    else:
        is_gifted = lin.gifted if gifted is None else bool(gifted)
        if is_gifted and not lin.gifted:
            errors.append(f"The {lin.name} lineage carries no gift.")
            is_gifted = False
        if is_gifted and lin.gift_knack:
            knacks.append(lin.gift_knack)
        if not is_gifted:
            if gift_domain:
                errors.append("Only a gifted character has a gift domain.")
        elif lin.gift_domain_scope:
            dom = ruleset.get_domain(gift_domain or "")
            if dom is None:
                errors.append(f"The {lin.name} gift needs a domain of the player's choice.")
            elif dom.prismatic:
                errors.append("A gift domain cannot be prismatic.")
            elif lin.gift_domains and dom.id not in lin.gift_domains:
                errors.append(f"The {lin.name} gift is one of: {lin.gift_domains}.")
        elif gift_domain:
            errors.append(f"The {lin.name} lineage has no gift domain.")

    if errors:
        return None, errors

    ch = Character(
        name=name.strip(), player_name=player_name, facet=facet, stats=stats,
        class_id=klass.id if klass else _slug(class_name), class_name=class_name,
        concept=concept, custom_class=custom, knacks=knacks, specialty=specialty,
        background=background, lineage=lineage, gifted=is_gifted,
        gift_domain=gift_domain if (is_gifted and lin and lin.gift_domain_scope) else None,
        talents=talent_states, id=_slug(name),
        sparks=ruleset.spark.base_sparks_per_session,
        class_talents=list(talent_ids) if custom else [],
        class_signature=(custom_class or {}).get("signature") if custom else None,
    )
    errors += _magic_setup_errors(ruleset, ch, magic)
    for st in talent_states:
        if st.id == "wider_domain" and ch.magic is not None:
            dom = ruleset.get_domain(st.choice or "")
            if dom is None or dom.tradition != ch.magic.tradition or dom.prismatic \
                    or dom.id in ch.magic.domains:
                errors.append("Wider Domain needs a second non-prismatic domain of your tradition.")
            else:
                ch.magic.domains.append(dom.id)

    for item_id in kit_ids:
        try:
            ch.add_item(ruleset, item_id)
        except ValueError as e:
            errors.append(f"Kit: {e}")
    if errors:
        return None, errors
    _auto_equip(ruleset, ch)
    ch.coin = coin if coin is not None else roll_starting_coin(ruleset, rng)
    if ch.coin < 0:
        return None, ["Coin cannot be negative."]
    ch.hp_current = ch.hp_max(ruleset)
    ch.hp_max_stored = ch.hp_current
    return ch, []
