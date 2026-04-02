# Root Cause Patterns

## Bad function pointer or branch target

Common evidence:

- `INVSTATE`
- `UNDEFINSTR`
- instruction fetch fault
- stacked `PC` points to SRAM, peripheral, zero, or an even address without Thumb bit semantics

Validation:

- inspect the call site and function pointer source
- check whether the branch target has bit0 set
- inspect memory corruption around the pointer storage

## Stack overflow or stack corruption

Common evidence:

- `MSTKERR`, `MUNSTKERR`, `STKERR`, `UNSTKERR`
- stacked frame is incomplete or implausible
- `PSP/MSP` near or beyond configured stack limit

Validation:

- compare `MSP/PSP` with stack boundaries
- inspect RTOS stack watermark and overflow hooks
- inspect large local arrays, recursion, nested interrupts, and DMA writes into stack memory

## Invalid exception return

Common evidence:

- `INVPC`
- corrupted `EXC_RETURN`
- failure on ISR exit or context switch

Validation:

- inspect saved `LR` and stacked return frame
- inspect RTOS PendSV/SVC context restore path
- inspect manual assembly that edits stack frames

## Invalid data access

Common evidence:

- `DACCVIOL`
- `PRECISERR` with valid `BFAR`
- fault address maps to unmapped or protected region

Validation:

- identify the exact load/store at stacked `PC`
- classify address ownership and alignment
- inspect pointer lifetime and race conditions

## Invalid instruction fetch

Common evidence:

- `IACCVIOL`
- `IBUSERR`
- `VECTTBL`

Validation:

- verify code region is executable
- inspect `VTOR` and vector entries
- inspect boot remap and image placement

## Divide by zero

Common evidence:

- `DIVBYZERO`

Validation:

- inspect `CCR.DIV_0_TRP`
- trace divisor source back to caller state
- add guards around denominator creation

## Unaligned access

Common evidence:

- `UNALIGNED`

Validation:

- inspect `CCR.UNALIGN_TRP`
- inspect packed structs, casts, DMA buffers, and protocol parsers

## FPU or lazy stacking problem

Common evidence:

- `NOCP`
- `MLSPERR`
- `LSPERR`

Validation:

- confirm CPACR/FPU init order
- inspect interrupt nesting and RTOS FPU context save rules
- inspect whether floating-point is used before scheduler/FPU init completes

## Imprecise bus fault

Common evidence:

- `IMPRECISERR`
- stacked `PC` does not obviously access the reported data region

Validation:

- inspect preceding stores
- inspect DMA and cache/write-buffer interactions
- reduce optimization or add targeted barriers/logging to narrow the write window

## Vector table or startup issue

Common evidence:

- `VECTTBL`
- fault immediately after reset or IRQ entry
- ISR entry address invalid or not Thumb

Validation:

- verify vector table location and alignment
- inspect linker placement and remap setup
- inspect startup code copying of vectors or memory regions
