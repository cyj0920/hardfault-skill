# Cortex-M HardFault Skill Pack

<div align="center">

[**English**](./README.md) | **中文**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Codex](https://img.shields.io/badge/Codex-.codex-0A7AFF)](#安装)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-.claude-D97706)](#安装)
[![Platform](https://img.shields.io/badge/Platform-Cortex--M-0F766E)](#概述)

**面向 Codex 和 Claude Code 的可直接复制 Cortex-M HardFault 工具包**

</div>

## 概述

这个仓库提供两份相互独立、可直接交付的内容：

- `codex/`，用于复制到目标项目的 `.codex/`
- `claude/`，用于复制到目标项目的 `.claude/`

每个包都是自包含的。用户只需要复制自己需要的那一份到工程里，就可以直接使用。

## 安装

| 目标 | 从本仓库复制 | 复制到你的工程 |
|---|---|---|
| Codex | `codex/` | `.codex/` |
| Claude Code | `claude/` | `.claude/` |

### Codex 结构

把 `codex/` 目录中的内容复制到目标项目的 `.codex/` 中。

```text
你的工程/
└── .codex/
    └── skills/
        └── cortex-m-hardfault/
            ├── SKILL.md
            ├── agents/
            │   └── openai.yaml
            ├── references/
            └── scripts/
```

### Claude Code 结构

把 `claude/` 目录中的内容复制到目标项目的 `.claude/` 中。

```text
你的工程/
└── .claude/
    ├── commands/
    │   └── hardfault.md
    └── skills/
        └── cortex-m-hardfault/
            ├── COMMAND.md
            ├── references/
            └── scripts/
```

## 使用方式

### Claude Code

```text
/hardfault HFSR=0x40000000 CFSR=0x01008200 BFAR=0x20030000 LR=0xFFFFFFF9 PC=0x08001234
```

### Codex

把包复制到 `.codex/skills/` 后，直接使用 `cortex-m-hardfault` 这个 skill。

这个 skill 主要面向如下现场信息：

```text
HFSR=0x40000000, CFSR=0x01008200, BFAR=0x20030000
LR=0xFFFFFFF9, PC=0x08001234, xPSR=0x21000000
MSP=0x20020000, PSP=0x2001F000
```

## 包内容

| 包 | 入口文件 | 包含内容 |
|---|---|---|
| `codex/` | `skills/cortex-m-hardfault/SKILL.md` | Codex skill、UI 元数据、参考资料、解码脚本 |
| `claude/` | `commands/hardfault.md` | Claude 命令、本地支撑文件、参考资料、解码脚本 |

## 仓库结构

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

## 说明

- 这两个目录是刻意保持独立的交付物，不是共享运行时目录。
- 两边都保留 `references/` 和 `scripts/`，目的是保证任一目录都能单独复制使用。
- 这个仓库优先优化“分发和复制时易理解”，而不是去消除重复文件。

## License

MIT。见 [LICENSE](./LICENSE)。
