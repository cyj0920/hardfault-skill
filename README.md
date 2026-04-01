# Cortex-M HardFault Diagnostic Skill

**[🇨🇳 中文](./README.zh-CN.md)** | **English**

A specialized skill for diagnosing Cortex-M series crashes including HardFault, MemManage, BusFault, and UsageFault. This tool helps embedded developers analyze register dumps, exception stack frames, disassembly, and map files to pinpoint fault locations and root causes.

## Features

- **Comprehensive Fault Analysis**: Supports diagnosis of HardFault, MemManage, BusFault, and UsageFault exceptions
- **Multi-Core Support**: Handles Cortex-M0/M0+, M3, M4, M7, M33, and FPU-enabled variants
- **Evidence-Based Approach**: Structured workflow that prioritizes evidence over speculation
- **Architecture-Aware**: Respects capability differences across Cortex-M variants
- **Toolchain Agnostic**: Works with Keil, IAR, GCC, STM32CubeIDE, J-Link, OpenOCD, etc.
- **RTOS Support**: Handles both bare-metal and RTOS contexts with MSP/PSP analysis
- **Automated Decoding**: Includes Python script for rapid register bit decoding

## Quick Start

### 1. Analyze a Crash

Provide the crash evidence:

```
HFSR=0x40000000, CFSR=0x01008200, BFAR=0x20030000
LR=0xFFFFFFF9, PC=0x08001234, xPSR=0x21000000
MSP=0x20020000, PSP=0x2001F000
```

### 2. Use the Decode Script

```bash
python ./scripts/decode_fault.py \
  --core m7 \
  --hfsr 0x40000000 \
  --cfsr 0x00008200 \
  --bfar 0x20030000 \
  --lr 0xFFFFFFF9 \
  --pc 0x08001234 \
  --xpsr 0x21000000
```

### 3. Implement HardFault Handler

See `references/handler-patterns.md` for production-ready handler implementations that capture crash data without causing secondary faults.

## Project Structure

```
cortex-m-hardfault/
├── SKILL.md                          # Main skill definition
├── agents/
│   └── openai.yaml                   # Agent configuration
├── references/
│   ├── workflow.md                   # Standard diagnostic flow
│   ├── register-decode.md            # HFSR/CFSR/MMFAR/BFAR decoding
│   ├── architecture-matrix.md        # Core capability differences
│   ├── root-cause-patterns.md        # Common failure modes
│   └── handler-patterns.md           # Handler implementation guide
└── scripts/
    └── decode_fault.py               # Automated register decoder
```

## Core Workflow

1. **Identify Core**: Determine Cortex-M variant and capabilities
2. **Collect Evidence**: Gather fault status registers and stacked frame
3. **Decode Registers**: Parse HFSR, CFSR, MMFAR, BFAR, ABFSR
4. **Recover Context**: Interpret EXC_RETURN to select MSP vs PSP
5. **Locate Fault**: Map stacked PC to source code or disassembly
6. **Root Cause Analysis**: Rank likely causes with evidence
7. **Propose Next Steps**: Provide concrete validation actions

## Minimum Required Evidence

- Core/MCU model (e.g., M0+, M4F, M7)
- HFSR, CFSR, MMFAR, BFAR (if available)
- Stacked R0-R3, R12, LR, PC, xPSR
- MSP and PSP values
- Disassembly or source line near faulting PC
- RTOS and FPU status

## Supported Cores

| Core | Fault Support | Special Considerations |
|------|---------------|----------------------|
| M0/M0+ | Basic only | Limited registers, rely on stacked PC |
| M3 | Full | Standard HFSR/CFSR/MMFAR/BFAR |
| M4/M4F | Full | Add FPU lazy stacking checks |
| M7 | Full + ABFSR | Check auxiliary bus fault register |
| M33 | Full | Security-aware analysis |

## Common Failure Modes

- Wild pointer / function pointer corruption
- Stack overflow / stack corruption
- Corrupted exception return
- Unaligned access
- Division by zero
- Execution in non-executable memory
- Illegal peripheral access / bus errors
- Interrupt vector table errors
- RTOS task stack corruption
- FPU lazy stacking issues

## Documentation

- **[SKILL.md](cortex-m-hardfault/SKILL.md)** - Main skill definition and usage
- **[Design Document](hardfault-skill-design.md)** - Detailed design rationale
- **[References](cortex-m-hardfault/references/)** - Comprehensive technical documentation

## Requirements

- Python 3.6+ (for decode script)
- Target platform: Cortex-M series microcontrollers
- Debug interface: J-Link, ST-Link, OpenOCD, or equivalent

## License

MIT License

## Contributing

Contributions are welcome! Please ensure:

- Evidence-based approach in all analysis
- Respect for core capability differences
- Clear documentation of assumptions
- Testing across multiple Cortex-M variants

## Acknowledgments

Based on [Cortex-M3/M4/M7 Fault Analysis Principles and Practice](https://yuxxxxxxxxxx.github.io/2024/10/07/Cortex-M3-M4-M7-%E8%8A%AF%E7%89%87-Fault-%E5%88%86%E6%9E%90%E5%8E%9F%E7%90%86%E4%B8%8E%E5%AE%9E%E6%88%98/) and Arm CMSIS documentation.