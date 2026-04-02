# Handler Patterns

## Goals

Design the handler to preserve evidence first and avoid making the crash worse.

## Minimum capture set

Capture as early as possible:

- stacked `R0/R1/R2/R3/R12/LR/PC/xPSR`
- `MSP`
- `PSP`
- `LR(EXC_RETURN)`
- `HFSR`
- `CFSR`
- `MMFAR`
- `BFAR`
- `ABFSR` on `M7`
- optional `SHCSR` and `CCR`

## Stack selection

Use `EXC_RETURN` from `LR` to determine which stack pointer was active before the exception.

Practical rule:

- if the return encoding indicates thread mode with process stack, inspect `PSP`
- otherwise inspect `MSP`

## Debug build behavior

Prefer:

- capture registers into a static crash record
- trigger `BKPT` after capture
- halt in a tight loop only after evidence is preserved

Avoid:

- `printf`
- heap usage
- complex peripheral I/O
- any code path that depends on interrupts or RTOS services

## Production build behavior

Prefer:

- write a compact crash record into reserved RAM or retention memory
- optionally store a reboot reason and reset counter
- reset cleanly after capture if the product requires recovery

Keep the record small and fixed-size to reduce the chance of secondary faults.

## Implementation guidance

- keep the naked assembly wrapper minimal
- pass the selected stack pointer into a small C helper
- read `SCB` registers immediately in the C helper
- mark crash record storage `volatile` if needed to prevent optimization loss
- avoid any nonessential function calls before capture completes

## Review checklist

When reviewing a user handler, check for:

- wrong `MSP/PSP` selection logic
- failure to capture `EXC_RETURN`
- reading `MMFAR/BFAR` without checking validity bits in later analysis
- logging mechanisms that can fault again
- missing `ABFSR` capture on `M7`
- FPU context not considered on FPU-enabled parts
