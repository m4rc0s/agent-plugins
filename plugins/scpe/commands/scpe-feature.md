---
description: Open a feature (index.md, feat_roadmap.md, quick_status.md, epics/)
argument-hint: <feature-slug> "<Title>"
---

Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/scpe/scripts/scpe.py" feature $ARGUMENTS
```

Then co-write `features/<slug>/index.md` with the user (Upstream wave): goal, users,
bounded context, business value, scope — per `${CLAUDE_PLUGIN_ROOT}/skills/scpe/SKILL.md`
§1–2. Keep this to the single most critical feature; do not map the whole system.
