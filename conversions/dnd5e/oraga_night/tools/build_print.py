#!/usr/bin/env python3
"""Build the print packets for Oraga Night, 5e edition (three-player pass, T9.6–T9.12).

    python tools/build_print.py              # four standalone HTML files in print/
    python tools/build_print.py --pdf        # and a PDF of each, with page counts
    python tools/build_print.py --out DIR    # somewhere else

The packets:

- **dm_packet.html**: the DM sheet (each of its two pages on a sheet of its own), the
  palace keyed with the five maps, the Snake Tracker and the Midnight Tracker. Landscape.
- **player_packet.html**: Player Handouts 1–5, one to a page, with the DM's italic lines
  stripped and cut lines round the invitation and each agenda card.
- **card_deck.html**: fight cards S1–S14, one card to a page, each followed by the stat
  blocks of chapter X that it names in bold.
- **pregen_sheets.html**: the five pregenerated characters, each standalone: chapter XI's
  shared preamble merged in, trackers, one line per spell and an "on your turn" line.

Everything is the standard library. The Markdown converter handles the subset the book
uses (headings, paragraphs, tables, block quotes, lists, images, bold, italics, code).
PDFs come from the browser's own print: `--pdf` drives headless Chromium through
Playwright if it is installed, or WeasyPrint; without either, print the HTML from a browser.

Every packet is checked before it is written: no repository paths, no INVENTIONS
references, no private-canon word (the hashed denylist in
software/tests/test_no_private_canon.py), and, for player material, no DM-only names or
DM text. A packet that fails is not written. The output folder is generated and git-ignored.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html as _html
import importlib.util
import re
import sys
from pathlib import Path

MODULE = Path(__file__).resolve().parent.parent
REPO = MODULE.parents[2]
OUT = MODULE / "print"
DENYLIST = REPO / "software" / "tests" / "test_no_private_canon.py"


# --------------------------------------------------------------------------- inline

_CODE = re.compile(r"`([^`]+)`")
_IMG = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLDITAL = re.compile(r"\*\*\*(?!\s)(.+?)(?<!\s)\*\*\*")
_BOLD = re.compile(r"\*\*(?!\s)(.+?)(?<!\s)\*\*")
_ITAL = re.compile(r"(?<![\w*])\*(?![\s*])(.+?)(?<![\s*])\*(?![\w*])")


def inline(text: str) -> str:
    """Inline Markdown to HTML: code, images, links, bold italics, bold, italics."""
    codes: list[str] = []

    def keep(m):
        codes.append(m.group(1))
        return f"\x00{len(codes) - 1}\x00"

    s = _CODE.sub(keep, text)
    s = _html.escape(s, quote=False)
    s = _IMG.sub(lambda m: f'<img alt="{m.group(1)}" src="{m.group(2)}">', s)
    s = _LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = _BOLDITAL.sub(r"<strong><em>\1</em></strong>", s)
    s = _BOLD.sub(r"<strong>\1</strong>", s)
    s = _ITAL.sub(r"<em>\1</em>", s)
    return re.sub("\x00(\\d+)\x00", lambda m: f"<code>{_html.escape(codes[int(m.group(1))], quote=False)}</code>", s)


# --------------------------------------------------------------------------- blocks

_HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_RULE = re.compile(r"^\s*(?:-{3,}|\*{3,})\s*$")
_ITEM = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
_TSEP = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
_FIG = re.compile(r"^!\[([^\]]*)\]\(([^)\s]+)\)\s*$")


def slug(text: str) -> str:
    s = re.sub(r"<[^>]+>|[*`_]", "", text).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def _cells(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _starts_block(line: str) -> bool:
    s = line.lstrip()
    return bool(_HEAD.match(line) or _RULE.match(line) or s.startswith(">") or s.startswith("|")
                or _ITEM.match(line) or _FIG.match(line))


def _list(lines: list[str], i: int) -> tuple[str, int]:
    m = _ITEM.match(lines[i])
    base, ordered = len(m.group(1)), m.group(2)[0].isdigit()
    items: list[list[str]] = []
    n = len(lines)
    while i < n:
        ln = lines[i]
        mm = _ITEM.match(ln)
        if mm and len(mm.group(1)) == base and mm.group(2)[0].isdigit() == ordered:
            items.append([mm.group(3)])
            i += 1
        elif not ln.strip():
            j = i + 1
            while j < n and not lines[j].strip():
                j += 1
            nxt = _ITEM.match(lines[j]) if j < n else None
            if j < n and ((nxt and len(nxt.group(1)) == base) or _indent(lines[j]) > base):
                items[-1].append("")
                i += 1
            else:
                break
        elif _indent(ln) > base:
            items[-1].append(ln[min(_indent(ln), base + 2):])
            i += 1
        elif items[-1][-1].strip() and not _starts_block(ln):
            items[-1].append(ln)          # a lazy continuation line
            i += 1
        else:
            break
    out = []
    for body in items:
        inner = _blocks(body)
        if inner.startswith("<p>") and inner.count("<p>") == 1:
            inner = inner[3:].replace("</p>", "", 1)
        out.append(f"<li>{inner}</li>")
    tag = "ol" if ordered else "ul"
    return f"<{tag}>{''.join(out)}</{tag}>", i


def _blocks(lines: list[str], images=None) -> str:
    out: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        m = _HEAD.match(ln)
        if m:
            level, text = len(m.group(1)), m.group(2)
            out.append(f'<h{level} id="{slug(text)}">{inline(text)}</h{level}>')
            i += 1
            continue
        if _RULE.match(ln):
            out.append("<hr>")
            i += 1
            continue
        if ln.lstrip().startswith(">"):
            quote = []
            while i < n and lines[i].lstrip().startswith(">"):
                s = lines[i].lstrip()[1:]
                quote.append(s[1:] if s.startswith(" ") else s)
                i += 1
            out.append(f"<blockquote>{_blocks(quote)}</blockquote>")
            continue
        if ln.lstrip().startswith("|") and i + 1 < n and _TSEP.match(lines[i + 1].strip()):
            head = _cells(ln)
            i += 2
            rows = []
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append(_cells(lines[i]))
                i += 1
            th = "".join(f"<th>{inline(c)}</th>" for c in head)
            body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                           for r in rows)
            out.append(f"<table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>")
            continue
        m = _FIG.match(ln)
        if m:
            alt, src = m.group(1), m.group(2)
            out.append(f'<figure><img alt="{_html.escape(alt)}" src="{src}">'
                       f"<figcaption>{inline(alt)}</figcaption></figure>")
            i += 1
            continue
        if _ITEM.match(ln):
            html, i = _list(lines, i)
            out.append(html)
            continue
        para = [ln.strip()]
        i += 1
        while i < n and lines[i].strip() and not _starts_block(lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append(f"<p>{inline(' '.join(para))}</p>")
    return "".join(out)


def md_to_html(text: str) -> str:
    """Markdown (the book's subset) to an HTML fragment."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return _blocks(text.split("\n"))


# --------------------------------------------------------------------------- sections

def section(text: str, heading: str) -> str:
    """The section whose heading starts with `heading`, down to the next heading of the
    same or a higher level. KeyError if there is none."""
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        m = _HEAD.match(ln)
        if m and m.group(2).startswith(heading):
            level = len(m.group(1))
            j = i + 1
            while j < len(lines):
                mm = _HEAD.match(lines[j])
                if mm and len(mm.group(1)) <= level:
                    break
                j += 1
            return "\n".join(lines[i:j]) + "\n"
    raise KeyError(heading)


# --------------------------------------------------------------------------- safety

_PATH = re.compile(
    r"`[^`]*(?:/|\.(?:md|py|ya?ml|json|svg|png|html|txt))[^`]*`"
    r"|(?<![\w/:.])(?:\.\./)*(?:[\w-]+/)+(?:[\w.-]+)?(?![\w/])"
    r"|\b[\w-]+\.(?:md|py|ya?ml|json|txt)\b")
_DATA = re.compile(r"data:[\w/+.-]+;base64,[A-Za-z0-9+/=]+")
_INVENT = re.compile(r"\bINVENTIONS\w*")

# names and words that belong to the DM alone; none may reach player material
DM_ONLY = [r"\bUninvited\b", r"\bNamak", r"\bthe Attendant\b", r"\b[Tt]he Radiant\b", r"\bthe Wept\b",
           r"\bthe Hollow\b", r"\bmidwife\b", r"\bpregnan", r"\bheir\b", r"\bnursery\b",
           r"\bSecond Clause\b", r"\bthe Root\b", r"\bVell\b", r"\bDM Note\b", r"\bDM only\b",
           r"\bDM ONLY\b", r"\bDM truth\b", r"\bRead this when\b", r"\bSidebar —",
           r"\bTroubleshooting —", r"⟨If History Breaks⟩"]


def _private_hashes():
    if not DENYLIST.exists():
        return frozenset()
    spec = importlib.util.spec_from_file_location("_private_canon_guard", DENYLIST)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return frozenset(mod.PRIVATE_WORD_HASHES)


PRIVATE = _private_hashes()


def strip_repo_paths(text: str) -> str:
    """Remove repository paths, file names and INVENTIONS references (data URIs are kept)."""
    keep: list[str] = []

    def hold(m):
        keep.append(m.group(0))
        return f"\x01{len(keep) - 1}\x01"

    s = _DATA.sub(hold, text)
    s = _INVENT.sub("", _PATH.sub("", s))
    return re.sub("\x01(\\d+)\x01", lambda m: keep[int(m.group(1))], s)


def strip_dm_lines(text: str) -> str:
    """Drop every paragraph that is wholly in italics and outside a block quote: in the
    handouts, those are the DM's lines (when to hand it over, how to print it)."""
    paras = re.split(r"\n\s*\n", text)
    kept = []
    for p in paras:
        s = p.strip()
        if (s.startswith("*") and not s.startswith("**") and s.endswith("*")
                and not s.endswith("**") and not s.startswith(">")):
            continue
        kept.append(p)
    return "\n\n".join(kept)


def safety_problems(text: str, player: bool = False, hashes=None) -> list[str]:
    """What must not be printed: repo paths, INVENTIONS, private-canon words, and (for
    player material) DM-only names and DM text. An empty list means safe."""
    hashes = PRIVATE if hashes is None else hashes
    s = _DATA.sub(" ", text)
    probs = [f"repo path: {m.group(0)!r}" for m in _PATH.finditer(s)
             if not m.group(0).startswith(("http", "//"))]
    probs += [f"inventions: {m.group(0)!r}" for m in _INVENT.finditer(s)]
    for w in re.findall(r"[A-Za-z]+", s):
        if hashlib.sha256(w.lower().encode()).hexdigest() in hashes:
            probs.append("private word")
    if player:
        for rx in DM_ONLY:
            for m in re.finditer(rx, s):
                probs.append(f"DM-only: {m.group(0)!r}")
    return probs


# --------------------------------------------------------------------------- page

CSS = """
:root { --ink: #1f1c18; --soft: #5f584e; --rule: #8a8273; --tint: #f3efe6; }
* { box-sizing: border-box; }
body { margin: 0; color: var(--ink); background: #fff;
       font: 10.5pt/1.38 Georgia, 'DejaVu Serif', 'Times New Roman', serif; }
main { max-width: 7.4in; margin: 0 auto; padding: 0.3in 0; }
h1 { font-size: 18pt; margin: 0 0 6pt; }
h2 { font-size: 14pt; margin: 12pt 0 4pt; border-bottom: 1px solid var(--rule); }
h3 { font-size: 12pt; margin: 10pt 0 3pt; }
h4 { font-size: 10.5pt; margin: 8pt 0 2pt; }
p { margin: 0 0 5pt; }
ul, ol { margin: 0 0 5pt; padding-left: 16pt; }
li { margin: 0 0 1.5pt; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0 8pt; font-size: 9pt; }
th, td { border: 0.6pt solid var(--rule); padding: 2pt 4pt; vertical-align: top; text-align: left; }
th { background: var(--tint); }
blockquote { margin: 5pt 0; padding: 4pt 8pt; border-left: 2.5pt solid var(--rule);
             background: var(--tint); }
figure { margin: 6pt 0; text-align: center; break-inside: avoid; }
figure img { max-width: 100%; max-height: 8.2in; }
figcaption { font-style: italic; color: var(--soft); font-size: 9pt; }
code { font-family: inherit; }
hr { border: 0; border-top: 0.6pt solid var(--rule); margin: 8pt 0; }
.page, .card, .pregen, .sheet-page, .map-page { break-before: page; }
.page:first-of-type, .card:first-of-type, .pregen:first-of-type, .sheet-page.first { break-before: auto; }
.cut { position: relative; border: 1.2pt dashed var(--ink); padding: 10pt 12pt 8pt;
       margin: 12pt 0; break-inside: avoid; }
.cut .scissors { position: absolute; top: -9pt; left: 8pt; background: #fff; padding: 0 4pt;
                 font-size: 10pt; color: var(--soft); }
.blocks h2 { border: 0; font-size: 11pt; margin-top: 10pt; }
.statblock { border-top: 2pt solid var(--rule); margin-top: 8pt; padding-top: 4pt;
             font-size: 9pt; }
.statblock h3 { break-after: avoid; }
.deck { font-size: 9.8pt; }
.sheets { font-size: 9.6pt; }
.sheets table { font-size: 9pt; }
.track { font-size: 10.5pt; letter-spacing: 1pt; }
.turn { border: 1pt solid var(--ink); padding: 5pt 8pt; margin: 6pt 0; background: var(--tint); }
.dm .sheet-page { font-size: 7pt; line-height: 1.12; }
.dm .sheet-page table { font-size: 6.7pt; margin: 2pt 0 3pt; }
.dm .sheet-page th, .dm .sheet-page td { padding: 0.5pt 2.5pt; }
.dm .sheet-page h2 { font-size: 10pt; margin: 0 0 1pt; border: 0; }
.dm .sheet-page h3 { font-size: 8.6pt; margin: 2pt 0 1pt; }
.dm .sheet-page p, .dm .sheet-page li { margin-bottom: 1.5pt; }
.dm .sheet-page ul { padding-left: 11pt; margin-bottom: 2pt; }
.dm .map-page figure img { max-height: 7.1in; }
.dm main { max-width: 10in; }
@media screen { main { padding: 0.4in 0.3in; } .page, .card, .pregen, .sheet-page, .map-page {
  border-top: 1px solid #ccc; margin-top: 0.3in; padding-top: 0.2in; } }
"""


def page(title: str, body: str, landscape: bool = False, extra_css: str = "",
         cls: str = "") -> str:
    """A standalone HTML document with the print stylesheet."""
    size = "Letter landscape" if landscape else "Letter"
    margin = "0.3in 0.35in" if landscape else "0.6in 0.65in"
    css = CSS + f"\n@page {{ size: {size}; margin: {margin}; }}\n" + extra_css
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            f"<title>{_html.escape(title)}</title>\n<style>{css}</style>\n</head>\n"
            f"<body class=\"{cls}\">\n<main>\n{body}\n</main>\n</body>\n</html>\n")


def cut(inner: str, label: str = "cut along the line") -> str:
    """Wrap a piece of a handout in a dashed cut line."""
    return (f'<div class="cut"><span class="scissors">✂ {_html.escape(label)}</span>'
            f"{inner}</div>")


# --------------------------------------------------------------------------- data

def stat_blocks(bestiary: str) -> dict[str, str]:
    """Chapter X's blocks by name: every ### section from "The Blocks, A to Z" to the end of
    "If It Comes to It" (Master Vell lives there), each down to the next heading."""
    out: dict[str, str] = {}
    lines = bestiary.split("\n")
    on = False
    cur, buf = None, []
    for ln in lines:
        m = _HEAD.match(ln)
        if m and len(m.group(1)) <= 2:
            if cur:
                out[cur] = "\n".join(buf) + "\n"
                cur, buf = None, []
            on = m.group(2).startswith(("The Blocks", "If It Comes to It"))
            continue
        if not on:
            continue
        if m and len(m.group(1)) == 3:
            if cur:
                out[cur] = "\n".join(buf) + "\n"
            cur, buf = m.group(2).strip(), [ln]
        elif cur:
            buf.append(ln)
    if cur:
        out[cur] = "\n".join(buf) + "\n"
    return out


def fight_cards(snakes: str) -> dict[str, str]:
    """Chapter IX's fight cards, S1 to S14, by ID."""
    out: dict[str, str] = {}
    for m in re.finditer(r"^## (S\d+)\. .*?(?=^## |\Z)", snakes, flags=re.M | re.S):
        out[m.group(1)] = m.group(0)
    return out


def _singular(word: str) -> str:
    word = word.strip().rstrip(".:,")
    if word.endswith("Knives"):
        return word[:-6] + "Knife"
    if word.endswith("men"):
        return word[:-3] + "man"
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith(("ss", "'s")):
        return word[:-1]
    return word


def _candidates(raw: str) -> list[str]:
    words = raw.split()
    out = [raw]
    for i in range(len(words)):
        out.append(" ".join(words[:i] + [_singular(words[i])] + words[i + 1:]))
    return out + ["The " + c for c in out]


def card_blocks(card: str, blocks: dict[str, str]) -> list[str]:
    """The chapter X blocks a card names in bold, in the order it first names them."""
    found: list[str] = []
    for m in re.finditer(r"\*\*([^*]{3,60}?)\*\*", card):
        raw = " ".join(m.group(1).split()).rstrip(".:,")
        for cand in _candidates(raw):
            if cand in blocks:
                if cand not in found:
                    found.append(cand)
                break
    return found


def pregen_sheets_md(pregens: str) -> dict[str, str]:
    """Chapter XI's five sheets, each with the shared preamble merged in after its header."""
    try:
        common = section_par(pregens, "**Common to all five.**")
        masks = section_par(pregens, "**Masks.**")
    except KeyError:
        common = masks = ""
    out: dict[str, str] = {}
    for m in re.finditer(r"^## (.+?)\n(.*?)(?=^## |\Z)", pregens, flags=re.M | re.S):
        title, body = m.group(1), m.group(2)
        if " — " not in title:
            continue
        body = re.sub(r"\n---\s*$", "\n", body.rstrip()) + "\n"
        name = title.split(" — ")[0].strip()
        pre = "\n\n".join(p for p in (common, masks) if p)
        out[name] = f"## {title}\n\n{pre}\n\n{body}" if pre else f"## {title}\n{body}"
    return out


def section_par(text: str, opener: str) -> str:
    """The paragraph that starts with `opener`. KeyError if none."""
    for p in re.split(r"\n\s*\n", text):
        if p.strip().startswith(opener):
            return p.strip()
    raise KeyError(opener)


def _boxes(n: int) -> str:
    return "☐" * n


def trackers(sheet: str) -> str:
    """Markdown tracker lines for one sheet: Hit Points, Hit Dice, slots, limited uses,
    Inspiration, the crystal charge and Death Saving Throws."""
    lines = []
    hp = re.search(r"\*\*Hit Points\*\* (\d+)", sheet)
    if hp:
        lines.append(f"**Hit Points** ______ of {hp.group(1)} · **Temporary** ______")
    hd = re.search(r"\*\*Hit Dice\*\* (\d+)(d\d+)", sheet)
    if hd:
        lines.append(f"**Hit Dice** ({hd.group(2)}) {_boxes(int(hd.group(1)))}")
    slots = re.search(r"\*Slots:\*\s*([^\n]+)", sheet)
    if slots:
        for lvl, cnt in re.findall(r"(\d)(?:st|nd|rd|th) ×(\d)", slots.group(1)):
            suffix = {"1": "st", "2": "nd", "3": "rd"}.get(lvl, "th")
            lines.append(f"**{lvl}{suffix}-level slots** {_boxes(int(cnt))}")
    for m in re.finditer(r"\*\*([A-Z][\w' ]+?)\*\* \((\d+) uses?", sheet):
        lines.append(f"**{m.group(1)}** {_boxes(int(m.group(2)))}")
    for m in re.finditer(r"\*\*([A-Z][\w' ]+?)\*\* \((\d+) use per", sheet):
        lines.append(f"**{m.group(1)}** {_boxes(int(m.group(2)))}")
    for m in re.finditer(r"\*\*([A-Z][\w' ]+?)\*\* \(once per", sheet):
        lines.append(f"**{m.group(1)}** {_boxes(1)}")
    if re.search(r"crystal\s+charge", sheet):
        lines.append("**Crystal charge** ☐ released")
    lines.append("**Inspiration** ☐")
    lines.append("**Death Saving Throws** successes ☐☐☐ · failures ☐☐☐")
    return "\n".join(f"- {l}" for l in lines)


# One line per spell, from the SRD 5.1 (CC BY 4.0) text (2014 conversion), cut to what a
# player needs at the table. A pregen naming a spell that is not here fails the build
# (spell_lines).
SPELLS = {
    "Aid": "Up to three creatures within 30 ft. each gain 5 to their Hit Point maximum and current Hit Points for 8 hours.",
    "Bless": "Up to three creatures within 30 ft. add 1d4 to attack rolls and saving throws for up to 1 minute (Concentration).",
    "Calm Emotions": "Each humanoid in a 20-ft.-radius sphere within 60 ft. makes a Charisma save (it can choose to fail); for up to 1 minute (Concentration) you suppress anything charming or frightening it, or make it indifferent toward creatures you choose.",
    "Charm Person": "One humanoid within 30 ft. makes a Wisdom save (with Advantage if you or your companions are fighting it) or is Charmed by you for 1 hour, or until you or your companions harm it; it knows afterward.",
    "Command": "One creature within 60 ft. that understands you makes a Wisdom save or obeys a one-word command (Approach, Drop, Flee, Grovel, Halt) on its next turn.",
    "Comprehend Languages": "Ritual: for 1 hour you understand the literal meaning of any spoken language you hear, and written language you touch.",
    "Cure Wounds": "A creature you touch regains 1d8 + your spellcasting modifier Hit Points.",
    "Darkness": "Magical darkness fills a 15-ft.-radius sphere within 60 ft. for up to 10 minutes (Concentration); darkvision can't see through it and ordinary light can't light it.",
    "Detect Magic": "Ritual: for up to 10 minutes (Concentration) you sense magic within 30 ft., and can use your action to see a faint aura round a visible creature or object that bears it.",
    "Disguise Self": "You look different, clothes and gear included, for 1 hour; a creature that uses its action to inspect you sees through it on an Intelligence (Investigation) check against your save DC.",
    "Fire Bolt": "Ranged spell attack, 120 ft.: 1d10 Fire damage; a flammable object it hits catches fire.",
    "Guidance": "Touch a willing creature: once within the next minute (Concentration) it adds 1d4 to one ability check of its choice.",
    "Guiding Bolt": "Ranged spell attack, 120 ft.: 4d6 Radiant damage, and the next attack roll against the target before the end of your next turn has Advantage.",
    "Healing Word": "Bonus Action: a creature you can see within 60 ft. regains 1d4 + your spellcasting modifier Hit Points.",
    "Hideous Laughter": "One creature within 30 ft. makes a Wisdom save or falls Prone and is Incapacitated, laughing, for up to 1 minute (Concentration); it repeats the save at the end of each of its turns and when it takes damage. A creature of Intelligence 4 or less is unaffected.",
    "Hold Person": "One humanoid within 60 ft. makes a Wisdom save or is Paralyzed for up to 1 minute (Concentration); it repeats the save at the end of each of its turns.",
    "Identify": "Ritual: touch an object for 1 minute and learn its magical properties and how to use them.",
    "Lesser Restoration": "Touch a creature and end one disease, or one condition on it: Blinded, Deafened, Paralyzed or Poisoned.",
    "Light": "An object you touch sheds bright light in a 20-ft. radius and dim light for 20 ft. more, for 1 hour.",
    "Mage Armor": "A creature you touch that wears no armor has a base AC of 13 + its Dexterity modifier for 8 hours.",
    "Mage Hand": "A spectral hand appears within 30 ft. for 1 minute; as your action you move it 30 ft. and use it to handle an object, open a door or carry up to 10 lb.",
    "Magic Missile": "Three darts, each striking a creature you can see within 120 ft. for 1d4 + 1 Force damage; they never miss.",
    "Mending": "Repair one break or tear in an object you touch, no larger than 1 ft. in any dimension.",
    "Message": "Whisper to a creature within 120 ft.; only it hears, and it can whisper back.",
    "Minor Illusion": "A sound, or the image of an object no larger than a 5-ft. cube, within 30 ft. for 1 minute; a creature that uses its action to examine it sees through it on an Intelligence (Investigation) check against your save DC.",
    "Misty Step": "Bonus Action: teleport up to 30 ft. to an unoccupied space you can see.",
    "Prayer of Healing": "Over 10 minutes, up to six creatures you can see within 30 ft. each regain 2d8 + your spellcasting modifier Hit Points.",
    "Prestidigitation": "A small trick within 10 ft.: a harmless sensory effect, light or snuff a candle, clean or soil a small object, chill, warm or flavor food, or a brief mark or trinket-sized illusion.",
    "Ray of Frost": "Ranged spell attack, 60 ft.: 1d8 Cold damage, and the target's speed drops by 10 ft. until the start of your next turn.",
    "Resistance": "Touch a willing creature: once within the next minute (Concentration) it adds 1d4 to one saving throw of its choice.",
    "Sacred Flame": "One creature within 60 ft. makes a Dexterity save or takes 1d8 Radiant damage; cover doesn't help it.",
    "Sanctuary": "Bonus Action: ward a creature within 30 ft. for 1 minute; anyone who targets it with an attack or a harmful spell makes a Wisdom save or must pick a new target. It ends if the warded creature attacks or casts a spell that affects an enemy.",
    "Shield": "Reaction, when you are hit by an attack or targeted by *Magic Missile*: +5 AC until the start of your next turn, including against that attack.",
    "Shield of Faith": "Bonus Action: a creature within 60 ft. gains +2 AC for up to 10 minutes (Concentration).",
    "Silent Image": "The image of an object, creature or other visible thing, no larger than a 15-ft. cube, within 60 ft. for up to 10 minutes (Concentration); your action moves it; a creature that uses its action to examine it sees through it on an Intelligence (Investigation) check.",
    "Sleep": "Roll 5d8: creatures within 20 ft. of a point within 90 ft. fall Unconscious for 1 minute, lowest current Hit Points first, until the total is spent; damage or a shake wakes them.",
    "Spare the Dying": "Touch a living creature that has 0 Hit Points: it becomes stable.",
    "Spiritual Weapon": "Bonus Action: a floating spectral weapon within 60 ft. for 1 minute makes a melee spell attack for 1d8 + your spellcasting modifier Force damage; a Bonus Action on later turns moves it 20 ft. and repeats the attack.",
    "Suggestion": "One creature within 30 ft. that can hear and understand you makes a Wisdom save or follows a reasonable course of action you describe in a sentence or two, for up to 8 hours (Concentration).",
    "Vicious Mockery": "One creature within 60 ft. that can hear you makes a Wisdom save or takes 1d4 Psychic damage and has Disadvantage on its next attack roll.",
}

# What a new player does on their turn, drawn from each sheet's own features.
ON_YOUR_TURN = {
    "Serane Vaskarin": "Move, then one action: talk, *Vicious Mockery*, or a spell (*Hideous Laughter* and *Suggestion* end trouble without a blade). A Bonus Action gives a friend Bardic Inspiration or casts *Healing Word*. Your Reaction is Cutting Words.",
    "Pello": "Move, then attack with a dagger; add Sneak Attack once a turn when you have Advantage or an ally beside the target. A Bonus Action is the second dagger, Cunning Action (Dash, Disengage, Hide), or Fast Hands.",
    "Andra Tessarin": "Move, then one action: *Fire Bolt* or *Ray of Frost*, or a spell (*Sleep*, *Magic Missile*, *Darkness*). *Misty Step* is a Bonus Action; *Shield* is your Reaction when you are hit.",
    "Dassa": "Move, then attack once with the longsword; you score a critical hit on a 19 or 20. Once a Short Rest, Action Surge gives you a second action. Second Wind is a Bonus Action that heals you.",
    "Ilesse Kethaun": "Move, then one action: *Sacred Flame*, *Guiding Bolt* or a healing spell. A Bonus Action casts *Healing Word*, *Shield of Faith* or *Spiritual Weapon*. Channel Divinity heals in a hurry (Preserve Life).",
}


def spell_lines(sheet: str) -> list[str]:
    """One Markdown line per spell the sheet can cast tonight (cantrips, prepared and
    always-prepared spells, and rituals from a spellbook). KeyError for a spell with no line."""
    names: list[str] = []
    for m in re.finditer(r"^- \*(Cantrips|Prepared|Always prepared[^:]*|The lattice)?[^\n]*$"
                         r"(?:\n  [^\n]*)*", sheet, flags=re.M):
        block = m.group(0)
        head = re.match(r"^- \*(?:\*)?([^:*]+)", block)
        kind = head.group(1).strip().lower() if head else ""
        if not kind.startswith(("cantrips", "prepared", "spells known", "always prepared", "the lattice")):
            continue
        body = block.split(":", 1)[1] if ":" in block else block
        for sm in re.finditer(r"\*([A-Z][A-Za-z' ]+?)\*(?: \(ritual\))?", body):
            name = sm.group(1).strip()
            if name in ("1st", "2nd", "3rd") or name.endswith(("level", "Domain)")):
                continue
            ritual = sm.group(0).endswith("(ritual)")
            if kind.startswith("the lattice") and not ritual:
                continue
            if name not in names:
                names.append(name)
    return [f"*{n}*. {SPELLS[n]}" for n in names]


# --------------------------------------------------------------------------- images

def data_uri(path: Path) -> str:
    mime = {"svg": "image/svg+xml", "png": "image/png"}[path.suffix.lstrip(".").lower()]
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def embed_images(md: str, base: Path) -> str:
    """Point every relative image at a data URI, so the HTML stands alone."""
    def rep(m):
        src = m.group(2)
        if src.startswith(("data:", "http")):
            return m.group(0)
        return f"![{m.group(1)}]({data_uri((base / src).resolve())})"
    return _IMG.sub(rep, md)


def _read(module: Path, name: str) -> str:
    return (Path(module) / name).read_text(encoding="utf-8")


# --------------------------------------------------------------------------- packets

def build_dm_packet(module: Path = MODULE) -> str:
    """The DM sheet, the palace keyed with its maps, the Snake Tracker and the Midnight
    Tracker, landscape."""
    module = Path(module)
    ch8 = _read(module, "08_Handouts.md")
    sheet = section(ch8, "The DM Sheet")
    p1, p2 = section(sheet, "Page One"), section(sheet, "Page Two")
    keyed = embed_images(section(ch8, "The Palace, Keyed"), module)
    def sheet_page(md, first=False):
        md = re.sub(r"\n---\s*$", "\n", md.rstrip()) + "\n"
        cls = "sheet-page first" if first else "sheet-page"
        return f'<section class="{cls}">{md_to_html(strip_repo_paths(md))}</section>'

    parts = [sheet_page(p1, first=True), sheet_page(p2)]
    # the keyed palace: its text, then one map to a page
    figs = re.findall(r"^!\[[^\]]*\]\([^)]+\)\s*$", keyed, flags=re.M)
    text = re.sub(r"^!\[[^\]]*\]\([^)]+\)\s*$", "", keyed, flags=re.M)
    parts.append(f'<section class="page">{md_to_html(strip_repo_paths(text))}</section>')
    for f in figs:
        parts.append(f'<section class="map-page">{md_to_html(f)}</section>')
    for title in ("The Snake Tracker", "The Midnight Tracker"):
        parts.append(sheet_page(section(ch8, title)))
    return page("Oraga Night — DM Packet", "\n".join(parts), landscape=True, cls="dm")


def build_player_packet(module: Path = MODULE) -> str:
    """Player Handouts 1–5, one to a page, DM lines stripped, cut lines marked."""
    module = Path(module)
    ch8 = _read(module, "08_Handouts.md")
    handouts = section(ch8, "Player Handouts")
    parts = []
    for m in re.finditer(r"^### (Player Handout \d+: .+?)\n(.*?)(?=^### |\Z)", handouts,
                         flags=re.M | re.S):
        title, body = m.group(1), m.group(2)
        body = re.sub(r"\n---\s*$", "\n", body.rstrip()) + "\n"
        body = strip_dm_lines(embed_images(body, module))
        if "Agenda Cards" in title:
            cards = re.split(r"\n\s*\n(?=\*\*\d+\. )", body.strip())
            inner = "".join(cut(md_to_html(c)) for c in cards if c.strip())
        elif "Invitation" in title:
            inner = cut(md_to_html(body), label="cut out the invitation")
        else:
            inner = md_to_html(body)
        parts.append(f'<section class="page"><h2>{inline(title)}</h2>{inner}</section>')
    return page("Oraga Night — Player Handouts", "\n".join(parts))


def build_card_deck(module: Path = MODULE) -> str:
    """Fight cards S1–S14, one to a page, each with the blocks it names appended."""
    module = Path(module)
    cards = fight_cards(_read(module, "09_The_Snakes.md"))
    blocks = stat_blocks(_read(module, "10_Bestiary.md"))
    parts = []
    for cid, md in cards.items():
        names = card_blocks(md, blocks)
        stats = "".join(f'<div class="statblock" data-block="{_html.escape(n, quote=False).replace(chr(34), "&quot;")}">'
                        f"{md_to_html(strip_repo_paths(blocks[n]))}</div>" for n in names)
        parts.append(f'<section class="card" id="{cid.lower()}">'
                     f"{md_to_html(strip_repo_paths(md))}"
                     f'<div class="blocks"><h2>Stat blocks for {cid} (chapter X)</h2>{stats}</div>'
                     "</section>")
    return page("Oraga Night — Fight Cards", "\n".join(parts), cls="deck")


def build_pregen_sheets(module: Path = MODULE) -> str:
    """The five pregenerated characters, each a standalone sheet."""
    module = Path(module)
    sheets = pregen_sheets_md(_read(module, "11_Pregenerated_Characters.md"))
    parts = []
    for name, md in sheets.items():
        turn = ON_YOUR_TURN[name]
        spells = spell_lines(md)
        box = f'<div class="turn"><strong>On your turn.</strong> {inline(turn)}</div>'
        extra = f'<h3>Trackers</h3><div class="track">{md_to_html(trackers(md))}</div>'
        if spells:
            extra += ("<h3>Spells, one line each</h3>"
                      + md_to_html("\n".join(f"- {s}" for s in spells)))
        body = md_to_html(strip_repo_paths(md)).replace("</h2>", "</h2>" + box, 1)
        parts.append(f'<section class="pregen">{body}{extra}{SRD_NOTE}</section>')
    return page("Oraga Night — Pregenerated Characters", "\n".join(parts), cls="sheets")


SRD_NOTE = ('<p class="srd"><em>This sheet includes material taken from the System '
            "Reference Document 5.1 by Wizards of the Coast LLC, licensed under the Creative "
            "Commons Attribution 4.0 International License.</em></p>")


BUILDERS = {
    "dm_packet": ("build_dm_packet", False),
    "player_packet": ("build_player_packet", True),
    "card_deck": ("build_card_deck", False),
    "pregen_sheets": ("build_pregen_sheets", True),
}


def _visible(html: str) -> str:
    html = _DATA.sub(" ", html)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    return _html.unescape(re.sub(r"<[^>]+>", " ", html))


def build_all(module: Path = MODULE, out: Path = OUT, pdf: bool = False) -> dict[str, Path]:
    """Build every packet into `out`. Raises ValueError, writing nothing, if any packet
    fails its safety check."""
    module, out = Path(module), Path(out)
    built = {}
    for name, (fn, player) in BUILDERS.items():
        html = getattr(sys.modules[__name__], fn)(module)
        probs = safety_problems(_visible(html), player=player)
        if probs:
            raise ValueError(f"{name}: not safe to print: " + "; ".join(probs[:8]))
        built[name] = html
    out.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, html in built.items():
        path = out / f"{name}.html"
        path.write_text(html, encoding="utf-8")
        paths[name] = path
        if pdf:
            render_pdf(path, path.with_suffix(".pdf"))
    return paths


# --------------------------------------------------------------------------- pdf

def render_pdf(html_path: Path, pdf_path: Path) -> Path:
    """Print the HTML to PDF with headless Chromium (Playwright) or WeasyPrint."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sync_playwright = None
    if sync_playwright:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            pg = browser.new_page()
            pg.goto(Path(html_path).resolve().as_uri())
            pg.pdf(path=str(pdf_path), prefer_css_page_size=True, print_background=True)
            browser.close()
        return pdf_path
    try:
        import weasyprint
    except ImportError as e:
        raise RuntimeError("no PDF renderer: install playwright or weasyprint, or print the "
                           "HTML from a browser") from e
    weasyprint.HTML(filename=str(html_path)).write_pdf(str(pdf_path))
    return pdf_path


def pdf_pages(pdf_path: Path) -> int:
    """Page count of a PDF (the /Type /Page objects)."""
    data = Path(pdf_path).read_bytes()
    return len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", data))


# --------------------------------------------------------------------------- main

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the Oraga Night print packets")
    ap.add_argument("--out", default=str(OUT), help="output folder (default: print/)")
    ap.add_argument("--pdf", action="store_true", help="also print each packet to PDF")
    a = ap.parse_args(argv)
    paths = build_all(MODULE, Path(a.out), pdf=a.pdf)
    for name, path in paths.items():
        line = str(path)
        if a.pdf:
            line += f"  ({pdf_pages(path.with_suffix('.pdf'))} pages as PDF)"
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
