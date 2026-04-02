# Cortex-M HardFault Skill Pack

This repository ships two copy-ready deliverables:

- `codex/` for a target project's `.codex/`
- `claude/` for a target project's `.claude/`

The goal is simple: users should copy one folder's contents into their own project and use it immediately, without understanding this repository's internal packaging.

## Install

### Codex

Copy the contents of `codex/` into your target project's `.codex/`.

Resulting layout in the target project:

```text
your-project/
└── .codex/
    └── skills/
        └── cortex-m-hardfault/
            ├── SKILL.md
            ├── agents/
            ├── references/
            └── scripts/
```

### Claude Code

Copy the contents of `claude/` into your target project's `.claude/`.

Resulting layout in the target project:

```text
your-project/
└── .claude/
    ├── commands/
    │   └── hardfault.md
    └── skills/
        └── cortex-m-hardfault/
            ├── COMMAND.md
            ├── references/
            └── scripts/
```

Then invoke:

```text
/hardfault HFSR=0x40000000 CFSR=0x01008200 BFAR=0x20030000 LR=0xFFFFFFF9 PC=0x08001234
```

## Repository Layout

```text
codex/
└── skills/
    └── cortex-m-hardfault/
        ├── SKILL.md
        ├── agents/
        │   └── openai.yaml
        ├── references/
        └── scripts/

claude/
├── commands/
│   └── hardfault.md
└── skills/
    └── cortex-m-hardfault/
        ├── COMMAND.md
        ├── references/
        └── scripts/
```

## Notes

- The two folders are intentionally independent deliverables.
- `codex/` contains a standard Codex skill package.
- `claude/` contains a Claude command plus its local support files.
- References and scripts are duplicated on purpose so each folder can be copied alone.

## License

MIT. See `LICENSE`.
