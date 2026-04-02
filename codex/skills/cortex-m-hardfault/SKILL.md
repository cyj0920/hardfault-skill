---
name: cortex-m-hardfault
description: Diagnose Cortex-M HardFault, MemManage, BusFault, and UsageFault crashes from register dumps, stacked exception frames, map files, disassembly, startup code, RTOS context, or HardFault handler code. Use when Codex needs to decode HFSR/CFSR/MMFAR/BFAR/ABFSR, interpret EXC_RETURN and MSP/PSP selection, locate the faulting PC, distinguish Cortex-M0/M0+ from M3/M4/M7/M33 fault capabilities, or propose next debugging steps and handler improvements.
---
# Codex Entry

This file is the Codex-specific integration layer for the `cortex-m-hardfault` skill.

## Workflow

Follow this skill when diagnosing a Cortex-M crash. Start by identifying the core, then collect the smallest useful evidence set, decode fault status registers, recover the stacked frame, and only then rank likely root causes.

Use the references selectively:

- Read [../references/workflow.md](../references/workflow.md) first for the default triage flow.
- Read [../references/architecture-matrix.md](../references/architecture-matrix.md) when the core variant is unclear or the target is `M0/M0+`, `M7`, `M33`, or FPU-enabled.
- Read [../references/register-decode.md](../references/register-decode.md) when decoding `HFSR`, `CFSR`, `MMFAR`, `BFAR`, `ABFSR`, `CCR`, or `SHCSR`.
- Read [../references/root-cause-patterns.md](../references/root-cause-patterns.md) after the register decode to map the evidence to concrete engineering failure modes.
- Read [../references/handler-patterns.md](../references/handler-patterns.md) when the user needs to implement or improve a `HardFault_Handler`.
- Run [../scripts/decode_fault.py](../scripts/decode_fault.py) when the user provides raw register values and repeated bit decoding would add noise.

## Default Procedure

1. Identify the core and environment.
   - Ask for the MCU or CPU core, toolchain, and whether an RTOS or FPU is in use.
   - Do not assume `CFSR/HFSR/MMFAR/BFAR` exist on `Cortex-M0/M0+`.
2. Collect the minimum evidence set.
   - Prefer `HFSR`, `CFSR`, `MMFAR`, `BFAR`, `ABFSR` when applicable.
   - Collect stacked `R0/R1/R2/R3/R12/LR/PC/xPSR` and both `MSP` and `PSP` if available.
   - Ask for the faulting disassembly line, map file symbol, linker script, or startup code when `PC` cannot be mapped directly.
3. Decode fault class before guessing the root cause.
   - Check whether `HardFault` is forced from a configurable fault.
   - Split `CFSR` into `MMFSR`, `BFSR`, and `UFSR`.
   - Trust `MMFAR` or `BFAR` only when their valid bits are set.
4. Recover the active stack and stacked `PC`.
   - Decode `EXC_RETURN` from `LR` to decide between `MSP` and `PSP`.
   - Treat `PC` as the main observation point, not automatically as the root cause.
   - Be cautious when `IMPRECISERR`, `STKERR`, `UNSTKERR`, `MSTKERR`, or `MUNSTKERR` are set.
5. Rank likely root causes and propose validation.
   - State the most likely explanation first.
   - List the evidence supporting it.
   - State what is still uncertain.
   - End with concrete next actions such as extra logs, breakpoint placement, stack watermark checks, or code fixes.

## Output Format

Keep the response structured and evidence-driven:

- `Fault classification`: direct `HardFault` vs escalated `MemManage/BusFault/UsageFault`
- `Key evidence`: the status bits, stacked registers, and addresses that matter
- `Fault location`: stacked `PC`, likely source line, and whether `MSP` or `PSP` was active
- `Likely root cause`: ranked explanations, not an unprioritized list
- `Next validation steps`: what to inspect, log, patch, or re-run

## Minimum Data Request Template

Use this template when the user does not yet have enough crash evidence:

```text
Please provide:
1. Core/MCU model (for example M0+, M4F, M7)
2. HFSR, CFSR, MMFAR, BFAR, ABFSR (if available)
3. Stacked R0, R1, R2, R3, R12, LR, PC, xPSR
4. MSP and PSP
5. The disassembly or source line near stacked PC
6. Whether an RTOS is running and whether FPU is enabled
```

## Handling Core Differences

Treat core capability differences as a first-class decision point:

- For `M0/M0+`, fall back to stacked `PC/LR/xPSR`, vector table checks, memory map validation, and stack integrity.
- For `M3/M4`, use the standard `HFSR/CFSR/MMFAR/BFAR` path.
- For `M7`, check `ABFSR` when the bus fault cause is ambiguous.
- For FPU-enabled cores, consider lazy stacking faults before assuming a generic stack corruption.

## Using the Decode Script

Run the helper script when register values are already known:

```powershell
python .\scripts\decode_fault.py --core m7 --hfsr 0x40000000 --cfsr 0x00008200 --bfar 0x20030000 --lr 0xFFFFFFF9 --pc 0x08001234 --xpsr 0x21000000
```

Use the script output as a first-pass decode. Still verify the conclusions against the code, memory map, and execution context.

## Handler Guidance

When the user needs a handler implementation or review:

- Extract the stacked frame without corrupting it further.
- Capture `SCB` registers early.
- Differentiate debug and production behavior.
- Avoid heavy logging, dynamic allocation, or peripheral access that can fault again inside the handler.
- Prefer writing minimal crash records into reserved RAM, then reset or halt.

