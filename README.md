# 🧩 agent-plugins

**This is where my AI agents live.**

[![Agent Plugins](https://img.shields.io/badge/protocol-Agent%20Plugins%20v1.0.0-6366f1)](https://agent-plugins.org)
[![Agent Skills](https://img.shields.io/badge/standard-Agent%20Skills-10b981)](https://agentskills.io)
[![Client](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20CLI%20%7C%20Antigravity-000000)](#-installing-a-plugin)

A growing monorepo of specialized agents and the skills that back them, packaged
as plugins that follow the open **[Agent Plugins](https://agent-plugins.org)
v1.0.0** protocol — so they aren't locked into one vendor's assistant — plus a
thin Claude Code marketplace layer on top for the plugins that need one.

---

## 🤖 What's in here right now

The first resident is **`scpe`** ([Spec-Compiled Product Engineering](plugins/scpe/skills/scpe/references/SCPE_METHOD.md)),
a product-engineering method where living Markdown is the contract and code is
its consequence. It ships seven specialized agents, each with full working
knowledge of the method and a distinct, non-overlapping mandate:

| | Agent | Specialty | Owns |
|---|---|---|---|
| 📋 | [`product-manager`](plugins/scpe/agents/product-manager.md) | Product Engineering | Vision, roadmap, feature discovery, `plan.md` (rules, examples, slices); marks Ready/Done |
| 🏛️ | [`software-architect`](plugins/scpe/agents/software-architect.md) | Software & Solution Architecture | `architecture.md`, `technical_deal.md`, `app.toml` boundaries, ADRs |
| 🎨 | [`senior-fullstack-product-designer`](plugins/scpe/agents/senior-fullstack-product-designer.md) | Fullstack Product Design | `design_system.md`, design direction for UI-facing `R#`/`S#`; marks its own features Ready/Done |
| ⚙️ | [`senior-backend-developer`](plugins/scpe/agents/senior-backend-developer.md) | Senior Backend Engineering | `tasks.toml`, `scpe pack` execution, business logic, persistence/migrations, service boundaries |
| 🖥️ | [`senior-frontend-developer`](plugins/scpe/agents/senior-frontend-developer.md) | Senior Frontend Engineering | `tasks.toml`, `scpe pack` execution, components, client state, routing/data loading, accessibility |
| 🔬 | [`ux-researcher`](plugins/scpe/agents/ux-researcher.md) | User Behavior & Product Analytics | What to instrument to validate or falsify a plan's Riskiest Assumption; usage data as evidence |
| 🔎 | [`ux-specialist`](plugins/scpe/agents/ux-specialist.md) | Browser-based UX/UI Audit | Visual hierarchy, navigation, filtering and consistency reviews of the running UI |

More skills and agents will land here over time, each following the same shape.

---

## 🧠 Why this shape

Two open standards compose here instead of a bespoke format:

- **[Agent Skills](https://agentskills.io)** 📚 — a folder with `SKILL.md` +
  `scripts/` + `references/` + `assets/`. The portable unit of capability. Read
  natively by Claude Code, Codex CLI, and Gemini CLI / Antigravity.
- **[Agent Plugins](https://agent-plugins.org) v1.0.0** 📦 — the packaging layer
  on top of Agent Skills (and, optionally, MCP servers), backed by Amazon,
  Cursor, Microsoft, OpenAI, and Vercel. A plugin is a directory with a root
  `plugin.json` manifest plus fixed component locations (`skills/`, `mcp.json`).
  Distribution and installation stay client-specific by design — the protocol
  only standardizes the portable parts.

There is deliberately **no second, "canonical" copy** of a skill outside its
plugin. A plugin directory is already self-contained and loadable by path, so
`plugins/<name>/` is the single source of truth: no sync step, no drift. Only
the client-specific component types that the protocol doesn't cover
(`agents/`, `commands/`) live alongside the portable core, where their client
expects them. 🔓

---

## 🗂️ Repo layout

```text
.
├── plugins/<name>/                   # self-contained, Agent Plugins-compliant package — the single source of truth
│   ├── plugin.json                   # Agent Plugins protocol manifest (portable, v1.0.0)
│   ├── skills/<name>/                # Agent Plugins "skills/" fixed location: SKILL.md, scripts/, references/, templates/
│   ├── .claude-plugin/plugin.json    # Claude Code's own manifest (not part of the open protocol)
│   ├── commands/*.md                 # Claude Code-specific slash commands
│   └── agents/<name>.md              # Claude Code-specific subagents (not a protocol component type)
└── .claude-plugin/marketplace.json   # lets `/plugin marketplace add` install from this repo in Claude Code
```

> 🤔 **Why two `plugin.json` files per plugin?** Agent Plugins v1.0.0 requires its
> manifest at the plugin *root* (`plugin.json`, with a specific `$schema` and a
> closed set of top-level fields). Claude Code's own plugin system is a
> separate, earlier convention that requires its manifest at
> `.claude-plugin/plugin.json` instead. Both coexist in the same folder without
> conflict because they use different filenames.

> 🤔 **Why are `agents/` and `commands/` in there at all?** Agent Plugins v1.0.0
> defines exactly two portable component types — `skills/` and `mcp.json`.
> Subagents, slash commands and hooks are outside its scope, so there is no
> standard-compliant way to ship a persona; the spec's own answer is that
> clients extend the package (its example uses a reverse-domain namespace like
> `com.example.client/`). Claude Code predates that convention and reads
> `agents/` and `commands/` from the plugin root instead. A client that doesn't
> implement them simply doesn't look there, so the portable core stays clean.

---

## 📦 Installing a plugin

- **✅ Any Agent Plugins-compliant client** — point it directly at a plugin's
  own directory, e.g. `plugins/scpe/`: each one is self-contained and loadable
  by path. The protocol defines no marketplace layer; that's left to the client.
- **🧪 Claude Code, dev/local testing** — `claude --plugin-dir plugins/scpe`
  loads a single plugin directly, without a marketplace.
- **🚀 Claude Code, normal install** — marketplaces are a Claude Code-specific
  concept layered on top, scoped to the whole repo (not a single plugin
  subpath):

  ```text
  /plugin marketplace add <path or git remote of this repo>
  /plugin install scpe@agent-plugins
  ```

---

## 🧵 Using a skill directly (no packaging)

Point any tool at `plugins/<name>/skills/<name>/` (or copy that folder into a
product workspace's `.agents/skills/<name>/`, the path Antigravity and a growing
set of agents read natively). No installation step required — it's plain
Markdown, Python (standard library only), and templates. ✨

---

## 🔁 Adding or updating a skill

1. Edit `plugins/<name>/skills/<name>/` directly — that's the single source of
   truth, and nothing needs to be copied anywhere afterwards.
2. `agents/*.md` and `commands/*.md` are hand-maintained Claude Code components;
   keep their mandates non-overlapping when you add one.
3. Keep the plugin's root `plugin.json` (Agent Plugins manifest) in sync by hand
   with `.claude-plugin/plugin.json` — `name`, `version`, `description` should
   mirror each other — and mirror the description into
   `.claude-plugin/marketplace.json` at the repo root.

---

📖 See `plugins/scpe/skills/scpe/SKILL.md` and
`plugins/scpe/skills/scpe/references/SCPE_METHOD.md` for the full SCPE method —
the first skill/plugin in this repo.
