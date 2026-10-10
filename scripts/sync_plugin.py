#!/usr/bin/env python3
"""Sync canonical skills/<name> into plugins/<name>/skills/<name>.

Claude Code plugins are copied to an isolated cache directory on install, so a
plugin cannot reference files outside its own folder by relative path. The
canonical skill lives once at skills/<name>/ in this repo; this script is the
only thing that copies it into each plugin package, so there is a single
source of truth and no manual drift.

The per-plugin agents/*.md wrappers (e.g. plugins/scpe/agents/senior-developer.md)
are NOT overwritten here: they intentionally differ from the canonical
agents/*.md (Claude-specific frontmatter, ${CLAUDE_PLUGIN_ROOT} paths instead of
.agents/skills/... paths), so they are maintained by hand, not synced.

Usage: python3 scripts/sync_plugin.py [plugin_name ...]
       (no args = sync every plugin under plugins/)
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
PLUGINS_DIR = ROOT / "plugins"


def sync_one(plugin_dir: Path) -> None:
    plugin_name = plugin_dir.name
    skill_src = SKILLS_DIR / plugin_name
    if not skill_src.is_dir():
        print(f"skip {plugin_name}: no skills/{plugin_name}/ to sync")
        return

    skill_dst = plugin_dir / "skills" / plugin_name
    if skill_dst.exists():
        shutil.rmtree(skill_dst)
    shutil.copytree(
        skill_src,
        skill_dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    print(f"synced skills/{plugin_name} -> plugins/{plugin_name}/skills/{plugin_name}")


def main(argv: list[str]) -> int:
    names = argv or [p.name for p in PLUGINS_DIR.iterdir() if p.is_dir()]
    for name in names:
        plugin_dir = PLUGINS_DIR / name
        if not plugin_dir.is_dir():
            print(f"error: no plugins/{name}/", file=sys.stderr)
            return 1
        sync_one(plugin_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
