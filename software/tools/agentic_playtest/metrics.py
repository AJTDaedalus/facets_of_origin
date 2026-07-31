"""Behavioural metrics, computed from the event log.

None of these ask an agent how it felt. Absolute self-report is worthless here —
agreeable models rate everything highly — so the primary instruments are things
you can count in a transcript: who got the spotlight, who sat idle, whether
proposals shrank as the session went on, how many exchanges passed with nobody
rolling.

`proposal_length_trend` is the one to watch. A player whose contributions get
steadily shorter is the closest behavioural proxy for disengagement available
without asking.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field

from tools.agentic_playtest.events import EventLog

#: Events that represent a player choosing to do something.
ACTION_KINDS = {
    "roll_result", "saving_throw_result", "cast_result", "strike_result",
    "react_result", "support_result", "maneuver_result", "posture_declared",
    "skill_point_spent", "technique_selected",
}
#: Events that are a person talking.
SPEECH_KINDS = {"say", "say_ooc", "scene"}
#: Events that consumed dice.
DICE_KINDS = {
    "roll_result", "saving_throw_result", "cast_result", "strike_result",
    "react_result", "support_result", "maneuver_result", "contested_roll_result",
}


@dataclass
class PlayerMetrics:
    player: str
    actions: int = 0
    lines: int = 0
    words: int = 0
    rolls: int = 0
    sparks_earned: int = 0
    sparks_spent: int = 0
    longest_idle_beats: int = 0
    proposal_length_trend: float = 0.0
    luck: float = 0.0


@dataclass
class SessionMetrics:
    session_id: str
    arm: str
    beats: int
    players: list[PlayerMetrics] = field(default_factory=list)
    spotlight_spread: float = 0.0
    decision_to_roll_ratio: float = 0.0
    ooc_to_ic_ratio: float = 0.0
    lateral_solutions: int = 0
    callbacks: int = 0
    zero_dice_exchanges: int = 0
    total_exchanges: int = 0
    rules_gaps: int = 0
    refusals: int = 0
    enemy_attacks: int = 0
    enemy_attacks_softened: int = 0

    def to_dict(self) -> dict:
        d = asdict(self)
        d["players"] = [asdict(p) for p in self.players]
        return d


def _words(event) -> int:
    text = event.data.get("text") or event.data.get("summary") or ""
    return len(str(text).split())


def proposal_length_trend(word_counts: list[int]) -> float:
    """Change in mean contribution length, last third vs first third.

    Negative means the player's turns are getting shorter — the disengagement
    proxy. Returns 0.0 when there is too little to compare.
    """
    if len(word_counts) < 6:
        return 0.0
    third = len(word_counts) // 3
    first = word_counts[:third]
    last = word_counts[-third:]
    if not first or not last:
        return 0.0
    first_mean = sum(first) / len(first)
    last_mean = sum(last) / len(last)
    if first_mean == 0:
        return 0.0
    return (last_mean - first_mean) / first_mean


def spotlight_spread(action_counts: list[int]) -> float:
    """Gap between the busiest and quietest player, as a share of the total.

    0.0 is a perfectly even table; 1.0 is one player doing everything. Simpler
    than a Gini coefficient and easier to read in a report.
    """
    if not action_counts or sum(action_counts) == 0:
        return 0.0
    return (max(action_counts) - min(action_counts)) / sum(action_counts)


def _longest_idle(log: EventLog, player: str, beats: int) -> int:
    active = {e.beat for e in log if e.actor == player}
    longest = current = 0
    for beat in range(1, beats + 1):
        if beat in active:
            current = 0
        else:
            current += 1
            longest = max(longest, current)
    return longest


def _luck(log: EventLog, player: str) -> float:
    """Mean roll total minus the 2d6 expectation of 7.

    Reported so the analysis can cross-reference an unlucky player against their
    engagement trend — the variance-concentration question in DESIGN §5.
    """
    totals = [e.data["roll"]["dice_sum"] for e in log
              if e.actor == player and e.data.get("roll")]
    return (sum(totals) / len(totals)) - 7.0 if totals else 0.0


def compute(log: EventLog, players: list[str]) -> SessionMetrics:
    metrics = SessionMetrics(session_id=log.session_id, arm=log.arm, beats=log.beat)

    speech_by_player: dict[str, list[int]] = defaultdict(list)
    actions = Counter()
    lines = Counter()
    words = Counter()
    rolls = Counter()

    for event in log:
        if event.kind in SPEECH_KINDS:
            lines[event.actor] += 1
            n = _words(event)
            words[event.actor] += n
            speech_by_player[event.actor].append(n)
        if event.kind in ACTION_KINDS:
            actions[event.actor] += 1
        if event.kind in DICE_KINDS and event.data.get("roll"):
            rolls[event.actor] += 1

    sparks_earned = Counter(
        e.data.get("player") for e in log.of_kind("spark_earned"))
    sparks_spent = Counter()
    for event in log:
        roll = event.data.get("roll")
        if roll and roll.get("sparks_spent"):
            sparks_spent[event.actor] += roll["sparks_spent"]

    for player in players:
        metrics.players.append(PlayerMetrics(
            player=player,
            actions=actions[player],
            lines=lines[player],
            words=words[player],
            rolls=rolls[player],
            sparks_earned=sparks_earned.get(player, 0),
            sparks_spent=sparks_spent.get(player, 0),
            longest_idle_beats=_longest_idle(log, player, log.beat),
            proposal_length_trend=proposal_length_trend(speech_by_player[player]),
            luck=_luck(log, player),
        ))

    metrics.spotlight_spread = spotlight_spread([p.actions for p in metrics.players])

    total_rolls = sum(rolls.values())
    total_actions = sum(actions.values())
    metrics.decision_to_roll_ratio = (total_actions / total_rolls) if total_rolls else 0.0

    ooc = len(log.of_kind("say_ooc"))
    ic = len(log.of_kind("say")) + len(log.of_kind("scene"))
    metrics.ooc_to_ic_ratio = (ooc / ic) if ic else 0.0

    # A Maneuver is the system's own "solve it another way" verb; a scene that
    # ends while enemies are still standing is the other shape of it.
    metrics.lateral_solutions = len(log.of_kind("maneuver_result"))

    metrics.callbacks = _count_callbacks(log)

    metrics.total_exchanges = len(log.of_kind("exchange_ended"))
    metrics.zero_dice_exchanges = _zero_dice_exchanges(log)

    metrics.rules_gaps = len(log.of_kind("rules_gap"))
    metrics.refusals = len(log.of_kind("refused"))

    attacks = log.of_kind("condition_applied")
    metrics.enemy_attacks = len(attacks)
    metrics.enemy_attacks_softened = sum(
        1 for e in attacks if e.data.get("arm_softened"))

    return metrics


def _zero_dice_exchanges(log: EventLog) -> int:
    """Exchanges in which nobody rolled anything.

    The direct measure for DESIGN §5: with fixed enemy severity and a PC who
    Absorbs, an exchange can resolve with no dice thrown by anyone.
    """
    boundaries = [e.seq for e in log.of_kind("exchange_ended")]
    if not boundaries:
        return 0
    start = 0
    zero = 0
    for end in boundaries:
        window = [e for e in log if start <= e.seq < end]
        if not any(e.kind in DICE_KINDS and e.data.get("roll") for e in window):
            zero += 1
        start = end
    return zero


def _count_callbacks(log: EventLog) -> int:
    """Speech that refers back to something from an earlier beat.

    A crude investment proxy: proper nouns and distinctive phrases reappearing
    later in the session. Counts references, not their quality.
    """
    seen_terms: set[str] = set()
    callbacks = 0
    for event in log:
        if event.kind not in SPEECH_KINDS:
            continue
        text = str(event.data.get("text", ""))
        terms = {w.strip(".,!?\"'") for w in text.split()
                 if len(w) > 4 and w[0].isupper()}
        callbacks += len(terms & seen_terms)
        seen_terms |= terms
    return callbacks


def summarise(metrics: SessionMetrics) -> str:
    lines = [
        f"Session {metrics.session_id} (arm {metrics.arm}) — {metrics.beats} beats",
        f"  spotlight spread      {metrics.spotlight_spread:.2f}  (0 = even, 1 = one player)",
        f"  decisions per roll    {metrics.decision_to_roll_ratio:.2f}",
        f"  OOC : IC              {metrics.ooc_to_ic_ratio:.2f}",
        f"  lateral solutions     {metrics.lateral_solutions}",
        f"  callbacks             {metrics.callbacks}",
        f"  zero-dice exchanges   {metrics.zero_dice_exchanges} / {metrics.total_exchanges}",
        f"  enemy attacks         {metrics.enemy_attacks}"
        + (f" ({metrics.enemy_attacks_softened} softened)"
           if metrics.enemy_attacks_softened else ""),
        f"  rules gaps            {metrics.rules_gaps}",
        f"  refused actions       {metrics.refusals}",
        "",
        f"  {'player':<12}{'acts':>5}{'rolls':>7}{'words':>7}{'idle':>6}"
        f"{'trend':>8}{'luck':>7}",
    ]
    for p in metrics.players:
        lines.append(
            f"  {p.player:<12}{p.actions:>5}{p.rolls:>7}{p.words:>7}"
            f"{p.longest_idle_beats:>6}{p.proposal_length_trend:>+8.2f}{p.luck:>+7.2f}")
    return "\n".join(lines)
