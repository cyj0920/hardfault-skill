# 🐛 Cortex-M HardFault Diagnostic Skill

<div align="center">

**[🇨🇳 中文](./README.zh-CN.md)** | **English**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Cortex-M](https://img.shields.io/badge/Platform-Cortex--M-informational)](https://developer.arm.com/architectures/cpu-architecture/a-profile)

**A specialized skill for diagnosing Cortex-M series crashes**

[Quick Start](#-quick-start) • [Features](#-features) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 Overview

> "Stop guessing, start analyzing with evidence."

This skill provides systematic diagnosis for **HardFault**, **MemManage**, **BusFault**, and **UsageFault** exceptions across the entire Cortex-M family. It helps embedded developers analyze register dumps, exception stack frames, disassembly, and map files to pinpoint fault locations and root causes with precision.

## ✨ Features

<div align="center">

| Feature | Description |
|:-------:|-------------|
| 🔍 | **Comprehensive Fault Analysis** - HardFault, MemManage, BusFault, UsageFault |
| 🎯 | **Multi-Core Support** - M0/M0+, M3, M4, M7, M33, and FPU variants |
| 📊 | **Evidence-Based Approach** - Structured workflow, prioritize evidence over speculation |
| 🏗️ | **Architecture-Aware** - Respects capability differences across variants |
| 🔧 | **Toolchain Agnostic** - Keil, IAR, GCC, STM32CubeIDE, J-Link, OpenOCD |
| ⚙️ | **RTOS Support** - Both bare-metal and RTOS contexts with MSP/PSP analysis |
| 🚀 | **Automated Decoding** - Python script for rapid register bit decoding |

</div>

## 🚀 Quick Start

### 1️⃣ Analyze a Crash

Simply provide the crash evidence:

```bash
HFSR=0x40000000, CFSR=0x01008200, BFAR=0x20030000
LR=0xFFFFFFF9, PC=0x08001234, xPSR=0x21000000
MSP=0x20020000, PSP=0x2001F000
```

### 2️⃣ Use the Decode Script

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

### 3️⃣ Implement HardFault Handler

> See `references/handler-patterns.md` for production-ready handler implementations that capture crash data without causing secondary faults.

## 📁 Project Structure

```
cortex-m-hardfault/
├── 📄 SKILL.md                          # Main skill definition
├── 🤖 agents/
│   └── openai.yaml                   # Agent configuration
├── 📚 references/
│   ├── workflow.md                   # Standard diagnostic flow
│   ├── register-decode.md            # HFSR/CFSR/MMFAR/BFAR decoding
│   ├── architecture-matrix.md        # Core capability differences
│   ├── root-cause-patterns.md        # Common failure modes
│   └── handler-patterns.md           # Handler implementation guide
└── 🔧 scripts/
    └── decode_fault.py               # Automated register decoder
```

## 🔄 Core Workflow

<div align="center">

```mermaid
graph LR
    A[1. Identify Core] --> B[2. Collect Evidence]
    B --> C[3. Decode Registers]
    C --> D[4. Recover Context]
    D --> E[5. Locate Fault]
    E --> F[6. Root Cause Analysis]
    F --> G[7. Propose Next Steps]

    style A fill:#e1f5fe
    style B fill:#e1f5fe
    style C fill:#fff3e0
    style D fill:#fff3e0
    style E fill:#f3e5f5
    style F fill:#f3e5f5
    style G fill:#e8f5e9
```

</div>

| Step | Description |
|:----:|-------------|
| 1️⃣ | **Identify Core** - Determine Cortex-M variant and capabilities |
| 2️⃣ | **Collect Evidence** - Gather fault status registers and stacked frame |
| 3️⃣ | **Decode Registers** - Parse HFSR, CFSR, MMFAR, BFAR, ABFSR |
| 4️⃣ | **Recover Context** - Interpret EXC_RETURN to select MSP vs PSP |
| 5️⃣ | **Locate Fault** - Map stacked PC to source code or disassembly |
| 6️⃣ | **Root Cause Analysis** - Rank likely causes with evidence |
| 7️⃣ | **Propose Next Steps** - Provide concrete validation actions |

## 📋 Minimum Required Evidence

> 💡 **Tip**: Having this information ready will speed up your diagnosis significantly.

- ✅ Core/MCU model (e.g., M0+, M4F, M7)
- ✅ HFSR, CFSR, MMFAR, BFAR (if available)
- ✅ Stacked R0-R3, R12, LR, PC, xPSR
- ✅ MSP and PSP values
- ✅ Disassembly or source line near faulting PC
- ✅ RTOS and FPU status

## 🎮 Supported Cores

| Core | Fault Support | Special Considerations |
|:----:|:-------------:|:----------------------|
| **M0/M0+** | Basic only | Limited registers, rely on stacked PC |
| **M3** | Full | Standard HFSR/CFSR/MMFAR/BFAR |
| **M4/M4F** | Full | Add FPU lazy stacking checks |
| **M7** | Full + ABFSR | Check auxiliary bus fault register |
| **M33** | Full | Security-aware analysis |

## ⚠️ Common Failure Modes

<div align="center">

| Category | Issues |
|:--------:|--------|
| 🎯 **Pointer Issues** | Wild pointer, function pointer corruption |
| 📚 **Stack Issues** | Stack overflow, stack corruption, RTOS task stack corruption |
| 🔄 **Return Issues** | Corrupted exception return |
| 📍 **Access Issues** | Unaligned access, illegal peripheral access, bus errors |
| 🔢 **Math Issues** | Division by zero |
| 🚫 **Execution Issues** | Execution in non-executable memory |
| 📋 **Vector Issues** | Interrupt vector table errors |
| ⚙️ **FPU Issues** | FPU lazy stacking issues |

</div>

## 📚 Documentation

- **[📄 SKILL.md](cortex-m-hardfault/SKILL.md)** - Main skill definition and usage
- **[📐 Design Document](hardfault-skill-design.md)** - Detailed design rationale
- **[📖 References](cortex-m-hardfault/references/)** - Comprehensive technical documentation

## 📦 Requirements

- **Python** 3.6+ (for decode script)
- **Target Platform**: Cortex-M series microcontrollers
- **Debug Interface**: J-Link, ST-Link, OpenOCD, or equivalent

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please ensure:

- ✅ Evidence-based approach in all analysis
- ✅ Respect for core capability differences
- ✅ Clear documentation of assumptions
- ✅ Testing across multiple Cortex-M variants

## 🙏 Acknowledgments

Based on [Cortex-M3/M4/M7 Fault Analysis Principles and Practice](https://yuxxxxxxxxxx.github.io/2024/10/07/Cortex-M3-M4-M7-%E8%8A%AF%E7%89%87-Fault-%E5%88%86%E6%9E%90%E5%8E%9F%E7%90%86%E4%B8%8E%E5%AE%9E%E6%88%98/) and Arm CMSIS documentation.

---

<div align="center">

**Made with ❤️ for embedded developers**

[⬆ Back to Top](#-cortex-m-hardfault-diagnostic-skill)

</div>