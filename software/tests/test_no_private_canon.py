"""Guard: private setting canon must never appear in a tracked file.

The owner's private canon notes (the references/ folder that git ignores, and the
setting author's own corpus) hold names the published books deliberately never say.
Twice in September 2026 a design or review document quoted them and was pushed. This
test fails the suite if any tracked text file contains one of those words again.

The denylist is stored as SHA-256 hashes of the lowercased words, so this file does
not leak what it protects. To add a word, append its hash:
    python -c "import hashlib; print(hashlib.sha256(b'word').hexdigest())"
"""
import hashlib
import re
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

PRIVATE_WORD_HASHES = frozenset({
    "5eee0b0154283d29b5498220fe32f8f35abc91c49d8d03f10c64179b1fcca81e",
    "9666a980423aa4530f5bff2cafa496efdd91db8cec479bb421fa6a5f8a5eb26c",
    "895406b73cb9076f1d811f1d400cae2b290fead2aa36c5a25872a45c930d3253",
    "5388a5a5ac0868b9e3b94ffeebe2b0b6b2173805cbe40b3199a2a7d6102f30a3",
    "249b2f4fe2c25fc2d3d5f546106b9a0e7c1f8b0ff31a73b9a018eb2e1bd4a2ec",
    "1c522f5504b3b5480402e08cb6c18201e44953172bcab420b8a491bf10192496",
    "cd0b9452fc376fc4c35a60087b366f70d883fc901524daf1f122fbd319384f6a",
    "18ec4ef8f04bd2da93a3c3ef188cb926a85344c356c460699320c7f3b6188282",
})

WORD = re.compile(r"[A-Za-z]+")


def find_private_words(text: str, hashes=PRIVATE_WORD_HASHES) -> list[tuple[int, str]]:
    """Return (line number, word) for every word whose lowercase hash is denied."""
    hits = []
    for number, line in enumerate(text.splitlines(), 1):
        for word in WORD.findall(line):
            if hashlib.sha256(word.lower().encode()).hexdigest() in hashes:
                hits.append((number, word))
    return hits


def tracked_text_files() -> list[Path]:
    out = subprocess.run(["git", "-C", str(REPO_ROOT), "ls-files"],
                         capture_output=True, text=True, check=True).stdout
    files = []
    for rel in out.splitlines():
        path = REPO_ROOT / rel
        if not path.is_file():
            continue
        head = path.read_bytes()[:4096]
        if b"\0" in head:          # binary
            continue
        files.append(path)
    return files


def test_no_tracked_file_names_private_canon():
    offenders = []
    for path in tracked_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for number, word in find_private_words(text):
            offenders.append(f"{path.relative_to(REPO_ROOT)}:{number}: {word}")
    assert not offenders, "Private canon in tracked files:\n" + "\n".join(offenders)


def test_detector_flags_a_denied_word():
    planted = {hashlib.sha256(b"zzsecret").hexdigest()}
    assert find_private_words("an ordinary line\nthe Zzsecret spoke", planted) == [(2, "Zzsecret")]


def test_detector_catches_words_inside_paths_and_filenames():
    planted = {hashlib.sha256(b"zzsecret").hexdigest()}
    text = "see /root/zzsecret/lore.md and ZZSECRET_NOTES.md"
    assert [w for _, w in find_private_words(text, planted)] == ["zzsecret", "ZZSECRET"]


def test_detector_ignores_words_that_merely_contain_a_denied_word():
    planted = {hashlib.sha256(b"zzsecret").hexdigest()}
    assert find_private_words("zzsecrets and prezzsecret are different words", planted) == []


def test_denylist_is_hashes_only():
    assert all(re.fullmatch(r"[0-9a-f]{64}", h) for h in PRIVATE_WORD_HASHES)
