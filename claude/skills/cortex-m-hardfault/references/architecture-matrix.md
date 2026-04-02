# Architecture Matrix

## Cortex-M0 / Cortex-M0+

Capabilities:

- limited fault diagnostics compared with `M3/M4/M7`
- no full `CFSR/HFSR/MMFAR/BFAR` workflow

Use this path:

- rely on stacked `PC/LR/xPSR`
- inspect `SP`, vector table, startup code, and memory map
- look for bad jumps, stack overflow, invalid interrupt vectors, and illegal memory accesses inferred from code and address map

Do not request unavailable registers as if they were mandatory.

## Cortex-M3 / Cortex-M4

Capabilities:

- standard configurable fault status model
- use `HFSR`, `CFSR`, `MMFAR`, and `BFAR`

Default method:

- decode `FORCED`
- split `CFSR`
- validate fault address registers
- recover stacked `PC`
- map status bits to likely root cause

## Cortex-M7

Extra consideration:

- use `ABFSR` when bus fault origin is unclear
- consider cache, write buffer, and memory system effects when dealing with `IMPRECISERR`

Default additions:

- inspect instruction/data bus path hints from `ABFSR`
- be more cautious about delayed fault visibility than on simpler cores

## Cortex-M33 and similar Armv8-M profiles

Use the standard `HFSR/CFSR/MMFAR/BFAR` process, but also account for:

- security attribution differences when applicable
- MPU/SAU restrictions
- secure vs non-secure transition context if the user provides it

## FPU-enabled cores

Relevant signs:

- `NOCP` when FPU instructions execute before enable/init
- `MLSPERR` or `LSPERR` during lazy stacking

Validation:

- confirm FPU enable sequence
- inspect task context save/restore code
- inspect interrupt nesting and RTOS port layer

## RTOS context

Typical pattern:

- thread mode often runs on `PSP`
- exceptions typically run on `MSP`

Implications:

- a broken task stack may only be visible through `PSP`
- `INVPC`, `UNSTKERR`, or corrupted saved `LR/PC` often implicate context switch code or task stack overwrite

Ask for:

- task stack boundaries
- context switch assembly
- stack watermark or overflow hook data
- whether the crash happens on task switch, ISR exit, or scheduler start

## Confidence Rules

- high confidence: valid fault address plus precise status bits plus mapped stacked `PC`
- medium confidence: stacked `PC` matches suspicious code but status bits are broad
- low confidence: imprecise bus fault or stacking fault with incomplete stack evidence
