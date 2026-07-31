"""Agentic playtest harness.

See docs/DESIGN_agentic_playtests.md. The load-bearing rule of this package:

    The agent decides. The engine resolves. The agent narrates what it was told.

No module here may contain rule logic. Every mechanical fact comes from
app/game/* and is written to an event log; transcripts are rendered from that
log, never from agent-authored text.
"""
