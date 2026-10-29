---
description: Open a flat sequential feature (plan.md and tasks.toml)
argument-hint: "<Title>" [--branch]
---

Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/scpe/scripts/scpe.py" feature $ARGUMENTS
```

Then co-write `features/00X-<slug>/plan.md` with the user (Upstream wave): intent, domain model,
rules (R#), Given/When/Then scenarios (S#), and vertical slices per `${CLAUDE_PLUGIN_ROOT}/skills/scpe/SKILL.md`.
Keep this to the single most critical feature; do not map the whole system.
