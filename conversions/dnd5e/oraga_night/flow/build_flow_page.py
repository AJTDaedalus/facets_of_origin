"""Build the Oraga Night 5e flow page from flow.json.

Usage (from this folder): python build_flow_page.py
Writes oraga_night_flow.html beside the template. Never edit the output by hand.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent


def build() -> Path:
    flow = json.loads((HERE / "flow.json").read_text(encoding="utf-8"))
    ids = {n["id"] for n in flow["nodes"]}
    phases = {p["id"] for p in flow["phases"]}
    bad_phase = [n["id"] for n in flow["nodes"] if n["phase"] not in phases]
    dangling = [e for e in flow["edges"] if e["from"] not in ids or e["to"] not in ids]
    if bad_phase or dangling:
        raise SystemExit(f"flow.json invalid: unknown phases {bad_phase}, dangling edges {dangling}")
    data = json.dumps(flow, ensure_ascii=False).replace("</", "<\\/")
    page = (HERE / "flow_page.template.html").read_text(encoding="utf-8")
    out = HERE / "oraga_night_flow.html"
    out.write_text(page.replace("/*FLOW_DATA*/null", data), encoding="utf-8")
    return out


if __name__ == "__main__":
    print(build())
