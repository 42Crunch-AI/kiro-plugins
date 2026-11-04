#!/usr/bin/env python3
"""Build and check the Kiro plugin.

Reference documents are edited once, in shared/references/. Each skill must
carry its own copy of every reference it uses: the Agent Plugins format does not
guarantee that files outside skills/ survive installation, and a skill imported
on its own only gets its own folder. This script copies each skill's references
into its references/ folder and checks the plugin.

Usage:
  python3 tools/build.py           # copy shared references into the skills, then check
  python3 tools/build.py --check   # check only; exit 1 if anything is stale or invalid (CI)

Checks:
  * every skill's references/ matches shared/references/ exactly (no stale or extra files)
  * every reference a skill mentions is present in its folder
  * no wording from other AI assistants (tool names, product names, attribution)
  * SKILL.md frontmatter follows Kiro's rules (name matches folder, description length)
  * plugin.json has the Agent Plugins 1.0.0 shape
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "shared" / "references"
PLUGIN = ROOT / "plugins" / "42crunch-api-security-testing"
SCHEMA_URL = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"

# Wording that belongs to other assistants and must never ship in the Kiro plugin.
FORBIDDEN = [
    (re.compile(r"AskUserQuestion|\bAskQuestion\b"), "another assistant's question tool"),
    (re.compile(r"`(Bash|Edit|Write|Read|StrReplace)` tool"), "another assistant's tool name"),
    (re.compile(r"\b(bash_tool|str_replace_editor|create_file)\b"), "another assistant's tool name"),
    (re.compile(r"CLAUDE_PLUGIN_ROOT|\$\{?PLUGIN_ROOT"), "another host's plugin-root variable"),
    (re.compile(r"\.\./\.\./references/"), "shared references path (skills must use references/)"),
    (re.compile(r"\?source=(?!kiro\b)\w+"), "Free Trial attribution other than source=kiro"),
    (re.compile(r"\b(Copilot|Claude|Codex|Cursor)\b"), "another assistant's product name"),
]

SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PLUGIN_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9]|[.-](?=[a-z0-9])){0,63}$")
PLUGIN_KEYS = {"$schema", "name", "version", "description", "author", "homepage",
               "repository", "license", "keywords", "extensions"}
MD_NAME = re.compile(r"[A-Za-z0-9_-]+\.md")


def references_for(skill_md):
    """Shared references a skill needs: those its SKILL.md mentions, followed transitively."""
    available = {p.name for p in SHARED.glob("*.md")}
    needed, queue = set(), [skill_md.read_text()]
    while queue:
        for name in MD_NAME.findall(queue.pop()):
            if name in available and name not in needed:
                needed.add(name)
                queue.append((SHARED / name).read_text())
    return needed


def build():
    for skill_md in sorted(PLUGIN.glob("skills/*/SKILL.md")):
        refs_dir = skill_md.parent / "references"
        needed = references_for(skill_md)
        if needed:
            refs_dir.mkdir(exist_ok=True)
        for name in needed:
            (refs_dir / name).write_bytes((SHARED / name).read_bytes())
        for stale in (refs_dir.glob("*.md") if refs_dir.exists() else []):
            if stale.name not in needed:
                stale.unlink()
        if refs_dir.exists() and not any(refs_dir.iterdir()):
            refs_dir.rmdir()


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fields, key = {}, None
    for line in (m.group(1).splitlines() if m else []):
        top = re.match(r"^([A-Za-z-]+):\s*(.*)$", line)
        if top:
            key = top.group(1)
            fields[key] = "" if top.group(2) in (">", "|", ">-", "|-") else top.group(2)
        elif key:
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields


def check():
    errors = []

    for skill_md in sorted(PLUGIN.glob("skills/*/SKILL.md")):
        skill = skill_md.parent
        refs_dir = skill / "references"
        needed = references_for(skill_md)
        present = {p.name for p in refs_dir.glob("*.md")} if refs_dir.exists() else set()
        for name in sorted(needed - present):
            errors.append(f"{skill.name}: missing references/{name} (run tools/build.py)")
        for name in sorted(present - needed):
            errors.append(f"{skill.name}: references/{name} is not used by this skill (run tools/build.py)")
        for name in sorted(needed & present):
            if (refs_dir / name).read_bytes() != (SHARED / name).read_bytes():
                errors.append(f"{skill.name}: references/{name} differs from shared/references/ "
                              "(edit shared/references/, then run tools/build.py)")

        fm = frontmatter(skill_md.read_text())
        if fm.get("name") != skill.name:
            errors.append(f"{skill.name}/SKILL.md: name {fm.get('name')!r} must match the folder name")
        if not SKILL_NAME.match(skill.name) or len(skill.name) > 64:
            errors.append(f"{skill.name}: skill names use lowercase letters, numbers and hyphens (max 64)")
        if not fm.get("description") or len(fm["description"]) > 1024:
            errors.append(f"{skill.name}/SKILL.md: description is missing or over 1024 characters")

    for path in sorted(PLUGIN.rglob("*.md")) + sorted(SHARED.glob("*.md")) + [PLUGIN / "plugin.json"]:
        for lineno, line in enumerate(path.read_text().splitlines(), 1):
            for pattern, why in FORBIDDEN:
                if pattern.search(line):
                    errors.append(f"{path.relative_to(ROOT)}:{lineno}: {why}: {line.strip()[:100]}")

    manifest = json.loads((PLUGIN / "plugin.json").read_text())
    if manifest.get("$schema") != SCHEMA_URL:
        errors.append(f"plugin.json: $schema must be {SCHEMA_URL}")
    if not PLUGIN_NAME.match(manifest.get("name", "")):
        errors.append("plugin.json: name must be lowercase letters, digits, dots or hyphens")
    for key in sorted(set(manifest) - PLUGIN_KEYS):
        errors.append(f"plugin.json: unknown top-level key {key!r}")
    if set(manifest.get("author", {})) - {"name", "email", "url"}:
        errors.append("plugin.json: author may only contain name, email and url")
    if not all(isinstance(k, str) for k in manifest.get("keywords", [])):
        errors.append("plugin.json: keywords must be strings")
    for key in ("version", "description", "license", "keywords"):
        if not manifest.get(key):
            errors.append(f"plugin.json: {key} is required for the Kiro powers catalog")

    return errors


def main():
    if "--check" not in sys.argv:
        build()
    errors = check()
    if errors:
        print("plugin check failed:", *errors, sep="\n  ", file=sys.stderr)
        return 1
    print("plugin check passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
