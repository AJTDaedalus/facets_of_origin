"""Take one turn at a running table. The interface a subagent uses.

    python -m tools.agentic_playtest.play_as Sophia state
    python -m tools.agentic_playtest.play_as Sophia say '{"text": "I go first."}'
    python -m tools.agentic_playtest.play_as Sophia roll_skill \\
        '{"attribute_id": "wisdom", "skill_id": "insight"}'

Every call goes to the broker, which sends it on that actor's own authenticated
socket and returns whatever the engine broadcast back. **You cannot state an
outcome here — only ask for one.** If you want to know what you rolled, roll and
read the answer.

Exit code 0 on success, 2 when the rules refused the action (the refusal text is
on stdout; read it and choose again).
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

SOFTWARE_DIR = Path(__file__).resolve().parents[2]
if str(SOFTWARE_DIR) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_DIR))

#: Written by the broker at start-up so clients need no arguments to find it.
ENDPOINT_FILE = SOFTWARE_DIR / "data" / "agentic_playtest" / "broker.json"


def endpoint() -> str:
    if not ENDPOINT_FILE.exists():
        sys.exit("No table is running. The session host starts one; if you are a "
                 "player, wait to be told the table is open.")
    return json.loads(ENDPOINT_FILE.read_text(encoding="utf-8"))["url"]


def _call(path: str, payload: dict | None = None) -> dict:
    url = f"{endpoint()}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url, data=data, method="POST" if data else "GET",
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read())
    except urllib.error.URLError as e:
        sys.exit(f"The table is not answering ({e}). It may have ended.")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1

    actor, verb = argv[0], argv[1]
    args = {}
    if len(argv) > 2:
        try:
            args = json.loads(argv[2])
        except json.JSONDecodeError as e:
            print(f"Your arguments are not valid JSON: {e}\n"
                  f"Wrap them in single quotes: '{{\"text\": \"hello\"}}'")
            return 2

    if verb == "state":
        print(json.dumps(_call(f"/state?actor={actor}"), indent=2))
        return 0

    response = _call("/turn", {"actor": actor, "verb": verb, "args": args})
    if "refused" in response:
        print(f"REFUSED: {response['refused']}")
        return 2
    print(json.dumps(response.get("result"), indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
