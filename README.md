# vulture-skills

A general-purpose [Agent Skills](https://agentskills.io/specification) repository.
Skills here are tool-agnostic, but the primary consumer is **Vulture**, which
installs each skill as a zip.

## Layout

```
/
├── skills/                  ← one directory per skill
│   └── <name>/
│       ├── SKILL.md         ← required: frontmatter (name, description) + instructions
│       ├── scripts/         ← optional bundled scripts
│       └── reference.md     ← optional progressive-disclosure docs
├── template/SKILL.md        ← starting point for a new skill
├── scripts/build-skill-zip.sh
├── dist/                    ← built zips (gitignored)
└── docs/agents/             ← repo conventions consumed by engineering skills
```

Each skill is self-contained under `skills/<name>/`. The directory name must match
the `name:` field in its `SKILL.md`. This is the canonical `{name}/SKILL.md` shape
that round-trips through Vulture's `build_anthropic_export_zip`.

## Adding a skill

```bash
cp -r template skills/<name>
$EDITOR skills/<name>/SKILL.md   # set name: and description:
```

Use the `skill-creator` (or `write-a-skill`) skill for the structured workflow.

## Building for Vulture

```bash
scripts/build-skill-zip.sh <name>   # → dist/<name>.zip
```

The zip contains `<name>/SKILL.md` at its root. Install it into Vulture via the
zip-upload / zip-URL flow.

## Conventions

Repo-level conventions (issue tracker, triage labels, domain docs) live in
[`docs/agents/`](docs/agents/) and are described in [`CLAUDE.md`](CLAUDE.md).
