---
description: Open an epic in Draft and co-write its plan.md
argument-hint: <feature-slug> <epic-slug> "<Title>"
---

Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/scpe/scripts/scpe.py" epic $ARGUMENTS
```

Then co-write `features/<feature>/epics/<epic>/plan.md` with the user (Upstream wave):
rules (`R#`), Given/When/Then examples (`S#`, one `When` each), vertical slices citing
the `S#`/`R#` they deliver, and any open questions — per
`${CLAUDE_PLUGIN_ROOT}/skills/scpe/SKILL.md` §6. Terms in the Domain Model must exist as
`##` headings in `glossary.md`. The epic stays `Draft` until a human runs `/scpe-gate`.
