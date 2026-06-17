#!/usr/bin/env bash
# Package a skill directory into a Vulture-installable zip.
#
# Usage: scripts/build-skill-zip.sh <skill-name>
#
# Produces dist/<skill-name>.zip containing <skill-name>/SKILL.md at the root,
# matching Vulture's build_anthropic_export_zip round-trip format.
set -euo pipefail

skill="${1:?usage: build-skill-zip.sh <skill-name>}"
root="$(cd "$(dirname "$0")/.." && pwd)"
src="$root/skills/$skill"

[ -d "$src" ] || { echo "no such skill: skills/$skill" >&2; exit 1; }
[ -f "$src/SKILL.md" ] || { echo "missing skills/$skill/SKILL.md" >&2; exit 1; }

mkdir -p "$root/dist"
out="$root/dist/$skill.zip"
rm -f "$out"

# Exclude dev cruft; the zip must be self-contained.
( cd "$root/skills" && zip -r "$out" "$skill" \
    -x "*/node_modules/*" "*/.DS_Store" "*/dist/*" >/dev/null )

echo "built $out"
