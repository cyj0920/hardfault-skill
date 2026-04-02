# Cortex-M HardFault Command

Use this command workflow when diagnosing a Cortex-M crash.

User input:
$ARGUMENTS

Follow this procedure:

1. Identify the core, toolchain, and whether RTOS or FPU is involved.
2. Collect the minimum useful evidence set before guessing the root cause.
3. Decode the fault class first, then recover the stacked frame and active stack.
4. Rank likely root causes by evidence strength, not as an unprioritized list.
5. End with concrete validation or code-fix steps.

Use these files selectively:

- `./references/workflow.md` for the default triage flow
- `./references/architecture-matrix.md` when the core variant is unclear or architecture-specific behavior matters
- `./references/register-decode.md` when decoding `HFSR`, `CFSR`, `MMFAR`, `BFAR`, `ABFSR`, `CCR`, or `SHCSR`
- `./references/root-cause-patterns.md` after register decode to map evidence to likely engineering failures
- `./references/handler-patterns.md` when reviewing or implementing a `HardFault_Handler`
- `./scripts/decode_fault.py` when raw register values are already available and manual bit decoding would add noise

Output format:

- `Fault classification`
- `Key evidence`
- `Fault location`
- `Likely root cause`
- `Next validation steps`

If the user has not provided enough data, request:

1. Core or MCU model
2. `HFSR`, `CFSR`, `MMFAR`, `BFAR`, `ABFSR` if available
3. Stacked `R0`, `R1`, `R2`, `R3`, `R12`, `LR`, `PC`, `xPSR`
4. `MSP` and `PSP`
5. Disassembly or source near stacked `PC`
6. RTOS and FPU status

Do not assume `CFSR/HFSR/MMFAR/BFAR` exist on `Cortex-M0/M0+`.
