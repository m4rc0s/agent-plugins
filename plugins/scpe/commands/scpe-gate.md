---
description: Run the Readiness Gate lint for one epic and record the Tech Lead's decision
argument-hint: <feature-slug>/<epic-slug>
---

Run the lint (never changes state):

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/scpe/scripts/scpe.py" gate-check $ARGUMENTS
```

Present the full output to the user. Then **stop and wait** — do not proceed on your own:

- If the lint fails, list what must change in `plan.md` before re-running the gate.
- If the lint passes, ask the user, acting as Tech Lead, whether they approve the epic.
  Only on their explicit approval, run:

  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT}/skills/scpe/scripts/scpe.py" set-state $ARGUMENTS Ready --by "<their name>"
  ```

You must never mark an epic `Ready` yourself and never approve your own work — this
command exists to get a human decision, not to automate it away.
