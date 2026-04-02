# Register Decode

## HFSR

### FORCED

Meaning:

- A configurable fault escalated into `HardFault`.

Implication:

- Always decode `CFSR` next.
- The useful root cause is usually in `MMFSR`, `BFSR`, or `UFSR`, not in `HFSR` alone.

Common causes:

- Bus fault disabled or not handled
- Usage fault escalated during invalid instruction or bad return
- Memory management fault escalated by protection or bad access

### VECTTBL

Meaning:

- Fault during vector fetch.

Common causes:

- bad `VTOR`
- bad boot remap
- invalid ISR entry address
- vector table placed in inaccessible memory

Validation:

- inspect `VTOR`
- check reset and ISR vectors for Thumb bit
- verify vector table memory permissions and remap state

## CFSR

Interpret `CFSR` as three logical groups.

### MMFSR bits `[7:0]`

#### IACCVIOL

- instruction fetch from a forbidden region
- suspect bad function pointer, jumped data, MPU/SAU/XN restrictions

#### DACCVIOL

- data access violation
- suspect invalid pointer, MPU/SAU restriction, or bad peripheral address

#### MUNSTKERR

- fault while unstacking on exception return
- treat stack pointer corruption or stack boundary failure as primary suspects

#### MSTKERR

- fault while stacking during exception entry
- suspect overflowed stack, invalid `MSP/PSP`, or memory protection on stack region

#### MLSPERR

- fault during floating-point lazy state preservation
- only relevant on FPU-enabled cores

#### MMARVALID

- `MMFAR` contains a valid address for this event
- use it only when this bit is set

### BFSR bits `[15:8]`

#### IBUSERR

- instruction bus error
- suspect invalid code fetch, flash access issue, remap issue, or bad branch target

#### PRECISERR

- precise data bus fault
- the fault is usually associated closely with the current instruction
- prefer `BFAR` when `BFARVALID=1`

#### IMPRECISERR

- imprecise data bus fault
- the fault may be reported later than the causative write
- inspect recent stores, DMA, caches, write buffers, and peripheral side effects

#### UNSTKERR

- bus fault during exception return unstack
- suspect broken stack frame or invalid stack address

#### STKERR

- bus fault during exception entry stack push
- suspect stack overflow, invalid stack pointer, or stack region access issue

#### LSPERR

- bus fault during floating-point lazy state preservation
- inspect FPU context stacking path

#### BFARVALID

- `BFAR` is valid for this event
- use it to classify memory region and ownership

### UFSR bits `[31:16]`

#### UNDEFINSTR

- undefined instruction
- suspect corrupted code, branched into data, bad image, or wrong ISA state

#### INVSTATE

- invalid EPSR/T-bit state
- strongly suspect a branch target without Thumb bit set or corrupted stacked state

#### INVPC

- invalid `EXC_RETURN` or invalid PC on exception return
- suspect corrupted stack frame, bad manual stack edits, or RTOS context corruption

#### NOCP

- coprocessor instruction used without coprocessor enabled
- common on FPU instructions when FPU is disabled or not initialized

#### UNALIGNED

- unaligned access trap
- only occurs when alignment trap is enabled
- inspect `CCR.UNALIGN_TRP`

#### DIVBYZERO

- divide-by-zero trap
- only occurs when divide-by-zero trap is enabled
- inspect `CCR.DIV_0_TRP`

## MMFAR and BFAR

Use address registers carefully:

- Ignore `MMFAR` if `MMARVALID=0`.
- Ignore `BFAR` if `BFARVALID=0`.
- Once valid, classify the address by region: flash, SRAM, peripheral, PPB/system, external memory, or unmapped.
- A valid address often narrows the issue faster than the stacked `PC` alone.

## ABFSR (`M7`)

Use `ABFSR` when `M7` bus fault origin is unclear.

Typical use:

- determine whether the fault came from instruction or data path and which bus interface reported it
- separate core-local execution issues from memory system or bus matrix issues

## CCR

### DIV_0_TRP

- if enabled, integer divide-by-zero raises `UFSR.DIVBYZERO`
- if disabled, division still happens with architecture-defined result behavior instead of trapping

### UNALIGN_TRP

- if enabled, unaligned accesses raise `UFSR.UNALIGNED`
- if disabled, many unaligned accesses complete, so do not assume absence of `UNALIGNED` means alignment is clean

## SHCSR

Use `SHCSR` to confirm which faults are enabled, active, or pending.

Helpful checks:

- whether `MemManage`, `BusFault`, or `UsageFault` handlers are enabled
- whether a configurable fault likely escalated because its dedicated handler path is unavailable

## Interpretation Rules

- Treat `FORCED + CFSR!=0` as “decode CFSR first”.
- Treat stacking and unstacking bits as stack-path evidence before code-path evidence.
- Treat `INVSTATE` with an odd/even branch target mismatch as a strong indicator of bad function pointer or bad return address.
- Treat `IMPRECISERR` as low-confidence `PC` evidence.
