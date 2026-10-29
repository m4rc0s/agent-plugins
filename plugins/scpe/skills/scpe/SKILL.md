---
name: scpe
description: >-
  SCPE (Spec-Compiled Product Engineering) method and tooling. Use whenever work happens in an
  SCPE product workspace (a folder with product_vision.md, glossary.md, features/ and apps/), or
  when the user wants to start a new product, write a product vision or glossary, open a feature
  or epic, write or review a plan.md (rules R#, Given/When/Then examples S#, vertical slices),
  run the Readiness Gate, change an epic state (Draft, Ready, WIP, Blocked, Done, Stale), handle
  spec drift, or compile a Ready epic into tasks.md, code and tests in apps/.
---

# SCPE — Spec-Compiled Product Engineering

Living Markdown documentation is the contract; code in `apps/` is its consequence.
**Humans decide, agents execute.** The full method is in `references/SCPE_METHOD.md`;
checklists for each wave are in `references/checklists.md`.

## 0. Find the workspace

The workspace is the folder containing `product_vision.md` and `features/` (or `$SCPE_WORKSPACE`).

```bash
python3 "<SKILL_DIR>/scripts/scpe.py" status
```

`<SKILL_DIR>` is the folder containing this `SKILL.md` (when running as the Claude Code
plugin, that's `${CLAUDE_PLUGIN_ROOT}/skills/scpe`).

No workspace yet → create one with `init` (see §5). Your scope is that folder only. Before any
work, read `index.md`, `product_vision.md`, `glossary.md`, `architecture.md` and `technical_deal.md`.

## 1. Workspace layout

```text
<product>/
├── index.md  product_vision.md  roadmap.md  glossary.md  architecture.md
├── technical_deal.md  team_playbook.md  AGENTS.md  CLAUDE.md
├── assets/
├── apps/<app>/app.toml          # typed manifest + boundaries (or legacy app.md)
└── features/
    └── 00X-<slug>/              # flat, sequential feature folder
        ├── plan.md              # intent, rules (R#), examples (S#), slices
        └── tasks.toml           # state, slices, task graph, temporal log
```

Formats are in `references/SCPE_METHOD.md` §5; the scaffolds in `templates/` follow them.
Machine metadata, manifests, and task execution graphs use TOML (`app.toml`, `tasks.toml`), while domain modeling remains living Markdown (`plan.md`, `glossary.md`).

### Compact layout ("tiny SCPE")

A smaller product may flatten the tree. The tooling detects this and adapts; no
flag or config is involved.

```text
<product>/
├── index.md  product_vision.md  roadmap.md  glossary.md  architecture.md
├── technical_deal.md  team_playbook.md  AGENTS.md  CLAUDE.md
├── app.toml                    # the manifest at root: no apps/ folder
├── adr.md                      # one section per decision: no adr/ folder
└── features/
    └── 00X-<slug>/             # plan.md + tasks.toml
```

A workspace is compact when `app.toml` (or `app.md`) exists at its root and there is no `apps/`
folder. In that mode: `apps/` and `assets/` are not required, each feature consists of
`plan.md` and `tasks.toml`, and the root `roadmap.md` is auto-synced via `scpe roadmap --sync`.

Because compact workspaces usually sit beside the code rather than containing
it, `validate --strict` looks for `<epic>#S#` tests under the path named by
`- **source:** <path>` in `app.md` (relative to the workspace), falling back to
the workspace's parent directory.

**Slicing in compact workspaces.** The *feature* must be a vertical slice: on
its own it delivers something a user can use. An *epic* need not be. This is the
one deliberate trade against §4.2.1 of the method, and it buys smaller epics: an
epic may be a shared capability that several epics of the same feature build on,
as long as the feature around it still delivers value. Epics keep their
`## Slices`, and an epic with no user-facing behaviour of its own says so there.

## 2. Wave pipeline

| Wave | Who | You do |
|---|---|---|
| **Upstream** | Developers + agent as co-pilot | Draft vision, glossary terms, and feature `plan.md`. Ask; never settle business questions yourself. Feature stays `Draft`. |
| **Readiness Gate** | Tech Lead (a human) | Run `gate-check`, present results, compile initial `tasks.toml`, wait for explicit human approval, then record `Ready`. |
| **Downstream (JIT)** | Agent, reviewed by Developers | Only on `Ready` features: Compile slice with `scpe pack <feat> <slice_id>`. Implement code and tests slice by slice inside app boundaries. |
| **Audit & Sync** | Everyone | Log learnings in `tasks.toml`; sync product roadmap with `scpe roadmap --sync`. |

Incremental Feature Discovery: open only the most critical feature now; do not map the whole system.
Vertical slicing is the default: each slice cuts through every layer and gives a user something real.

## 3. Feature / Epic states

Declared in `tasks.toml` under `[state]`. Allowed transitions (enforced by `set-state`):

| From | To | Set by |
|---|---|---|
| `Draft` | `Ready` | Tech Lead, after the gate |
| `Ready` | `WIP` / `Blocked` | Agent / Agent or Developer |
| `WIP` | `Done` / `Blocked` | Agent, after Developer review / Agent or Developer |
| `Blocked` | `Ready` / `Draft` | whoever resolves it (Draft when the model must be reworked) |
| `Done` | `Stale` | automatic on any edit to `plan.md` |
| `Stale` | `Ready` / `Done` | Tech Lead: Re-execute / Accept the drift (with a note) |

**Never** set `Ready` yourself and never approve your own work. Always change state through
`set-state` so the log and roadmap stay in sync.

## 4. Downstream protocol

1. Confirm the feature is `Ready`; `set-state <feature> WIP --by agent`.
2. **JIT Context Compilation Invariant (Do NOT dump raw markdowns):**
   - Run `python3 "$S" pack <feature> <slice_id>` to compile the exact slice context (< 1k tokens).
   - This payload contains ONLY the slice's `R#` rules, `S#` scenarios, relevant domain terms from `glossary.md`, and application commands/boundaries from `app.toml`.
   - Use `python3 "$S" term <word>` for instant definition lookups if needed.
3. Build slice by slice in `apps/<app>/`, strictly adhering to `app.toml` boundaries and `technical_deal.md` standards.
4. Name at least one test per example `<feature>#S#` (e.g. `001-pix-payment#S2 expired charge can be recreated`).
5. Log dated learnings in `tasks.toml` under `[[log]]`. Blocked → `set-state … Blocked`.
6. **Immediate Task Completion (Strict Invariant):**
   - **Always mark tasks as done immediately upon completing and verifying each task.**
   - Never proceed to the next task leaving completed tasks pending.
   - Use `python3 "$S" complete-task <feature> <task_id>` or update `tasks.toml`.
   - When all tasks are checked off, ask a Developer to review, then `set-state … Done`.
7. **Roadmap Sync:** Run `python3 "$S" roadmap --sync` to update the product-wide `roadmap.md`.
8. Commits: `docs:` for specification, `feat:`/`fix:`/`test:` for code — never mixed.

Found a gap in the plan while building? Stop and ask. Do not silently change `plan.md` or code around it.

## 5. Scripts

`S="<SKILL_DIR>/scripts/scpe.py"` — Python 3 standard library only (see §0 for `<SKILL_DIR>`).

| Action | Command |
|---|---|
| New product workspace | `python3 "$S" init <name> [--path DIR] [--app NAME:TYPE]... [--no-git]` |
| New feature (auto 00X) | `python3 "$S" feature "<Title>" [--branch]` |
| Compile slice context (JIT) | `python3 "$S" pack <feature> <slice_id> [--json]` |
| Glossary term lookup | `python3 "$S" term <word>` |
| Sync product roadmap | `python3 "$S" roadmap [--sync]` |
| Complete task in feature | `python3 "$S" complete-task <feature> <task_id>` |
| Readiness Gate lint | `python3 "$S" gate-check <feature>` |
| Change state | `python3 "$S" set-state <feature> <State> --by "<who>" [--note "..."]` |
| Validate workspace | `python3 "$S" validate [--strict]` |
| Status panel | `python3 "$S" status [--json] [--write]` |
| Status panel | `python3 "$S" status [--json] [--write]` |

Scaffolds never overwrite: they abort if the target exists. `validate --strict` also requires a
`<epic>#S#` test for every example of a `Done` epic and turns warnings into errors.

## 6. Writing a good plan.md

- One `When` per example; `Then` is observable by a user or another system.
- If you cannot write the example, the decision has not been made — add an Open Question.
- Open questions block the gate unless marked `(non-blocking)` or `[resolved]`.
- Terms in **Domain Model** must exist as `##` headings in `glossary.md`.
- Slices list the `S#`/`R#` they deliver; if not vertical, say why.
