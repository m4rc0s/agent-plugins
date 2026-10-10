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

The first resident is **`scpe`** ([Spec-Compiled Product Engineering](skills/scpe/references/SCPE_METHOD.md)),
a product-engineering method where living Markdown is the contract and code is
its consequence. It ships three specialized agents, each with full working
knowledge of the method and a distinct, non-overlapping mandate:

| | Agent | Specialty | Owns |
|---|---|---|---|
| 📋 | [`product-manager`](agents/product-manager.md) | Product Engineering | Vision, roadmap, feature discovery, epic `plan.md` (rules, examples, slices) |
| 🏛️ | [`software-architect`](agents/software-architect.md) | Software & Solution Architecture | `architecture.md`, `technical_deal.md`, app boundaries, ADRs |
| 🛠️ | [`senior-developer`](agents/senior-developer.md) | Senior Software Engineering | `tasks.md`, implementation and tests, slice by slice |

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

On top of both, this repo adds one convention of its own: the canonical,
unpackaged skill source lives once at `skills/<name>/`; each `plugins/<name>/`
folder is a self-contained, protocol-compliant *package* of that skill, built by
`scripts/sync_plugin.py`. That way nothing here is tied to a single client —
today it's Claude Code, tomorrow it could be any Agent Plugins-compliant tool. 🔓

---

## 🗂️ Repo layout

```text
.
├── skills/<name>/                   # canonical skill source: SKILL.md, scripts/, references/, templates/
├── agents/<name>.md                 # canonical persona, agent-agnostic
├── plugins/<name>/                  # self-contained, Agent Plugins-compliant package
│   ├── plugin.json                  # Agent Plugins protocol manifest (portable, v1.0.0)
│   ├── skills/<name>/               # Agent Plugins "skills/" fixed location — synced from ../../../skills/<name>
│   ├── .claude-plugin/plugin.json   # Claude Code's own manifest (not part of the open protocol)
│   ├── commands/*.md                # Claude Code-specific slash commands
│   └── agents/<name>.md             # Claude Code-specific agent wrapper (hand-maintained, not synced)
├── .claude-plugin/marketplace.json  # lets `/plugin marketplace add` install from this repo in Claude Code
└── scripts/sync_plugin.py           # copies skills/<name> into plugins/<name>/skills/<name>
```

> 🤔 **Why two `plugin.json` files per plugin?** Agent Plugins v1.0.0 requires its
> manifest at the plugin *root* (`plugin.json`, with a specific `$schema` and a
> closed set of top-level fields). Claude Code's own plugin system is a
> separate, earlier convention that requires its manifest at
> `.claude-plugin/plugin.json` instead. Both coexist in the same folder without
> conflict because they use different filenames. `commands/` and `agents/` are
> Claude Code-specific component types — the Agent Plugins spec only defines
> `skills/` and `mcp.json` as fixed locations in v1 and requires conformant
> clients to ignore component types they don't implement, so these extra
> folders are harmless to any other protocol client.

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

Point any tool at `skills/<name>/` (or copy it into a product workspace's
`.agents/skills/<name>/`, the path Antigravity and a growing set of agents read
natively). No installation step required — it's plain Markdown, Python (standard
library only), and templates. ✨

---

## 🔁 Adding or updating a skill

1. Edit `skills/<name>/` directly — that's the single source of truth.
2. If a plugin wraps it, run `python3 scripts/sync_plugin.py <name>` to refresh
   `plugins/<name>/skills/<name>/` before testing or publishing.
3. A plugin's `.claude-plugin/plugin.json`, `commands/*.md`, and Claude-specific
   `agents/<name>.md` are hand-maintained, not synced.
4. Keep the plugin's root `plugin.json` (Agent Plugins manifest) in sync by hand
   too — `name`, `version`, `description` should mirror `.claude-plugin/plugin.json`.

---

📖 See `skills/scpe/SKILL.md` and `skills/scpe/references/SCPE_METHOD.md` for
the full SCPE method — the first skill/plugin in this repo.
