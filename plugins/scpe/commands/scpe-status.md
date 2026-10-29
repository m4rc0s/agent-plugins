---
description: Show the product-wide panel of every feature, its state, and task progress
argument-hint: "[--write]"
---

Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/scpe/scripts/scpe.py" status $ARGUMENTS
```

Show the panel to the user. With `--write`, it synchronizes the root `roadmap.md` — confirm that happened.
