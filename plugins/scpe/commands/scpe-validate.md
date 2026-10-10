---
description: Check workspace structure, epic states, and spec-to-code traceability
argument-hint: "[--strict]"
---

Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/scpe/scripts/scpe.py" validate $ARGUMENTS
```

Report every error and warning to the user as-is. With `--strict`, warnings are errors
and every example of a `Done` epic must have a `<epic>#S#` test — do not soften that.
