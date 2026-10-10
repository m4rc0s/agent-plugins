---
description: Create a new SCPE product workspace and run the first Upstream round
argument-hint: <product-name> [path] [--app name:type]...
---

Run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/scpe/scripts/scpe.py" init $ARGUMENTS
```

Parse `$ARGUMENTS` for the product name, an optional destination path, and any
`--app name:type` pairs — pass them straight through to the command above.

After the workspace is created, follow `${CLAUDE_PLUGIN_ROOT}/skills/scpe/SKILL.md` §0–1:
read the scaffolded `index.md`, then interview the user to fill in `product_vision.md`,
`glossary.md` and `technical_deal.md`, and the manifest for each `apps/<app>/app.md`.
Propose the single most critical feature for `roadmap.md` → **Now** and offer the first
commit. Do not invent business answers — ask.
