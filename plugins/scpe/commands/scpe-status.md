---
description: Show the product-wide panel of every epic, its state, and task progress
argument-hint: "[--write]"
---

Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/scpe/scripts/scpe.py" status $ARGUMENTS
```

Show the panel to the user. With `--write`, it also refreshes the `<!-- scpe:status:start
-->` block in the root `quick_status.md` — confirm that happened.
