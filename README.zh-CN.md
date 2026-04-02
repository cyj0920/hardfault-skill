# Cortex-M HardFault Skill Pack

这个仓库现在只提供两份可直接交付的内容：

- `codex/`，用于复制到目标项目的 `.codex/`
- `claude/`，用于复制到目标项目的 `.claude/`

目标很直接：用户不需要理解仓库内部结构，只需要复制对应目录内容到自己的工程里，就能立即使用。

## 安装

### Codex

把 `codex/` 目录中的内容复制到目标项目的 `.codex/` 中。

目标项目中的结果结构：

```text
你的工程/
└── .codex/
    └── skills/
        └── cortex-m-hardfault/
            ├── SKILL.md
            ├── agents/
            ├── references/
            └── scripts/
```

### Claude Code

把 `claude/` 目录中的内容复制到目标项目的 `.claude/` 中。

目标项目中的结果结构：

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

然后直接调用：

```text
/hardfault HFSR=0x40000000 CFSR=0x01008200 BFAR=0x20030000 LR=0xFFFFFFF9 PC=0x08001234
```

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

- 这两个目录是刻意做成相互独立的交付物。
- `codex/` 是标准 Codex skill 包。
- `claude/` 是 Claude 命令加本地支撑文件。
- `references/` 和 `scripts/` 故意各自保留一份，保证任一目录都能单独复制使用。

## License

MIT。见 `LICENSE`。
