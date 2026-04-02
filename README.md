# Cortex-M HardFault Skill Pack

<div align="center">

**English** | [**中文**](./README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Codex](https://img.shields.io/badge/Codex-.codex-0A7AFF)](#install)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-.claude-D97706)](#install)
[![Platform](https://img.shields.io/badge/Platform-Cortex--M-0F766E)](#overview)

**Copy-ready Cortex-M HardFault tooling for Codex and Claude Code**

</div>

## Overview

This repository ships two independent deliverables:

- `codex/` for a target project's `.codex/`
- `claude/` for a target project's `.claude/`

Each package is self-contained. Users copy the package they need into their own project and can use it immediately.

## Install

| Target | Copy From This Repo | Copy Into Your Project |
|---|---|---|
| Codex | `codex/` | `.codex/` |
| Claude Code | `claude/` | `.claude/` |

### Codex Layout

Copy the contents of `codex/` into your target project's `.codex/`.

```text
your-project/
└── .codex/
    └── skills/
        └── cortex-m-hardfault/
            ├── SKILL.md
            ├── agents/
            │   └── openai.yaml
            ├── references/
            └── scripts/
```

### Claude Code Layout

Copy the contents of `claude/` into your target project's `.claude/`.

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

## Usage

### Claude Code

```text
/hardfault HFSR=0x40000000 CFSR=0x01008200 BFAR=0x20030000 LR=0xFFFFFFF9 PC=0x08001234
```

### Codex

Use the `cortex-m-hardfault` skill after copying the package into `.codex/skills/`.

Typical evidence the skill is designed to analyze:

```text
HFSR=0x40000000, CFSR=0x01008200, BFAR=0x20030000
LR=0xFFFFFFF9, PC=0x08001234, xPSR=0x21000000
MSP=0x20020000, PSP=0x2001F000
```

## Package Contents

| Package | Entry Point | Includes |
|---|---|---|
| `codex/` | `skills/cortex-m-hardfault/SKILL.md` | Codex skill, UI metadata, references, decode script |
| `claude/` | `commands/hardfault.md` | Claude command, local skill files, references, decode script |

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

- The two folders are intentionally duplicated deliverables, not a shared runtime layout.
- `references/` and `scripts/` exist in both packages on purpose so either package can be copied alone.
- The repository is optimized for distribution clarity, not for minimizing duplicate files.

## License

MIT. See [LICENSE](./LICENSE).
