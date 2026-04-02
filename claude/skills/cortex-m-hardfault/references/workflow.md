# Workflow

## Quick Triage

Use this order unless there is a strong reason to deviate:

1. Confirm the core.
   - Ask whether the target is `M0/M0+`, `M3/M4`, `M7`, `M33`, and whether it has FPU.
   - Ask whether the fault happens in thread context, interrupt context, boot, or low-power resume.
2. Capture the minimal crash record.
   - `HFSR`
   - `CFSR`
   - `MMFAR`
   - `BFAR`
   - `ABFSR` for `M7`
   - `LR`, stacked `PC`, `xPSR`
   - `MSP` and `PSP`
3. Decode `HardFault` first.
   - If `HFSR.FORCED=1`, treat the `HardFault` as a wrapper around `MemManage`, `BusFault`, or `UsageFault`.
   - If `HFSR.VECTTBL=1`, suspect vector table location, VTOR configuration, boot remap, or invalid ISR entry.
4. Decode `CFSR`.
   - Split it into `MMFSR`, `BFSR`, and `UFSR`.
   - Check valid bits before trusting fault address registers.
5. Reconstruct the faulting context.
   - Use `LR(EXC_RETURN)` to identify the active stack.
   - Recover stacked `R0/R1/R2/R3/R12/LR/PC/xPSR`.
   - Map stacked `PC` to disassembly and source.
6. Rank root causes.
   - Prefer a short ranked list backed by evidence.
   - Avoid broad speculation without concrete status bits or addresses.
7. Propose next validation.
   - Ask for exactly the missing artifact that will reduce uncertainty fastest.

## Full Procedure

### 1. Identify architecture and runtime context

Check:

- core variant
- toolchain and optimization level
- RTOS presence
- FPU presence
- recent code changes around interrupts, DMA, startup, memory protection, or context switching

### 2. Read the top-level fault source

Start with `HFSR`:

- `FORCED`: configurable fault escalated into `HardFault`
- `VECTTBL`: fault while reading the vector table

If `FORCED` is set, continue with `CFSR` immediately. Do not stop at “HardFault happened”.

### 3. Decode configurable fault status

Split `CFSR` into:

- `MMFSR` bits `[7:0]`
- `BFSR` bits `[15:8]`
- `UFSR` bits `[31:16]`

Then:

- trust `MMFAR` only when `MMARVALID=1`
- trust `BFAR` only when `BFARVALID=1`
- treat stacking and unstacking bits as stack-path problems first, code-path problems second
- treat `IMPRECISERR` as delayed write visibility, not proof that stacked `PC` is the store instruction

### 4. Recover the stack frame

Interpret `EXC_RETURN` from `LR`:

- use `PSP` when the return pattern says the exception interrupted thread mode using process stack
- otherwise use `MSP`

Recover the hardware-saved frame in this order:

1. `R0`
2. `R1`
3. `R2`
4. `R3`
5. `R12`
6. saved `LR`
7. saved `PC`
8. saved `xPSR`

If the frame looks corrupt, immediately reconsider stack overflow, invalid stack pointer, bad exception return, or lazy stacking issues.

### 5. Map PC and memory addresses

Use the stacked `PC` and valid fault address registers to answer:

- which function was executing
- whether the address belongs to flash, SRAM, peripheral, system control space, or an unmapped region
- whether the instruction is a load, store, branch, or return
- whether the address is aligned and executable for the core configuration

### 6. Decide whether PC is the cause or only the observation point

Treat stacked `PC` as a strong clue, but downgrade its confidence when these bits appear:

- `IMPRECISERR`
- `STKERR`
- `UNSTKERR`
- `MSTKERR`
- `MUNSTKERR`
- `MLSPERR`
- `LSPERR`

In those cases, inspect earlier instructions, stack boundaries, DMA side effects, and recent context switches.

### 7. Produce the answer

Use this shape:

- `Fault classification`
- `Evidence`
- `Likely root cause`
- `Open uncertainty`
- `Next validation steps`
- `Likely fix directions`

## Minimum Crash Record Checklist

```text
core=
rtos=
fpu=
HFSR=
CFSR=
MMFAR=
BFAR=
ABFSR=
MSP=
PSP=
LR(EXC_RETURN)=
stacked R0=
stacked R1=
stacked R2=
stacked R3=
stacked R12=
stacked LR=
stacked PC=
stacked xPSR=
source/disassembly near PC=
```
