#!/usr/bin/env python3
import argparse
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class DecodeResult:
    title: str
    details: List[str]


def parse_int(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    return int(value, 0)


def format_hex(value: Optional[int]) -> str:
    return "n/a" if value is None else f"0x{value:08X}"


def add_flag(results: List[DecodeResult], title: str, *details: str) -> None:
    results.append(DecodeResult(title=title, details=[d for d in details if d]))


def decode_hfsr(hfsr: Optional[int]) -> List[DecodeResult]:
    results: List[DecodeResult] = []
    if hfsr is None:
        return results
    if hfsr & (1 << 30):
        add_flag(results, "HFSR.FORCED", "Configurable fault escalated into HardFault.", "Decode CFSR next.")
    if hfsr & (1 << 1):
        add_flag(results, "HFSR.VECTTBL", "Fault occurred during vector table read.", "Check VTOR, remap, and ISR vector entries.")
    if not results:
        add_flag(results, "HFSR", "No decoded FORCED/VECTTBL bits set in the supplied value.")
    return results


def decode_cfsr(cfsr: Optional[int]) -> List[DecodeResult]:
    results: List[DecodeResult] = []
    if cfsr is None:
        return results

    mmfsr = cfsr & 0xFF
    bfsr = (cfsr >> 8) & 0xFF
    ufsr = (cfsr >> 16) & 0xFFFF

    mmfsr_bits: Dict[int, str] = {
        0: "IACCVIOL: instruction access violation",
        1: "DACCVIOL: data access violation",
        3: "MUNSTKERR: fault during exception return unstack",
        4: "MSTKERR: fault during exception entry stacking",
        5: "MLSPERR: fault during FP lazy state preservation",
        7: "MMARVALID: MMFAR is valid",
    }
    bfsr_bits: Dict[int, str] = {
        0: "IBUSERR: instruction bus error",
        1: "PRECISERR: precise data bus fault",
        2: "IMPRECISERR: imprecise data bus fault",
        3: "UNSTKERR: bus fault during unstack",
        4: "STKERR: bus fault during stack push",
        5: "LSPERR: bus fault during FP lazy state preservation",
        7: "BFARVALID: BFAR is valid",
    }
    ufsr_bits: Dict[int, str] = {
        0: "UNDEFINSTR: undefined instruction",
        1: "INVSTATE: invalid EPSR/T-bit state",
        2: "INVPC: invalid PC or EXC_RETURN usage",
        3: "NOCP: coprocessor disabled",
        8: "UNALIGNED: unaligned access trap",
        9: "DIVBYZERO: divide-by-zero trap",
    }

    for bit, text in mmfsr_bits.items():
        if mmfsr & (1 << bit):
            add_flag(results, "MMFSR", text)
    for bit, text in bfsr_bits.items():
        if bfsr & (1 << bit):
            add_flag(results, "BFSR", text)
    for bit, text in ufsr_bits.items():
        if ufsr & (1 << bit):
            add_flag(results, "UFSR", text)

    if not results:
        add_flag(results, "CFSR", "No known MMFSR/BFSR/UFSR bits set in the supplied value.")
    return results


def decode_exc_return(lr: Optional[int]) -> DecodeResult:
    if lr is None:
        return DecodeResult("EXC_RETURN", ["Not provided."])
    details: List[str] = [f"LR(EXC_RETURN)={format_hex(lr)}"]
    if (lr & 0xFF000000) != 0xFF000000:
        details.append("Value does not look like EXC_RETURN. It may be a normal LR instead.")
        return DecodeResult("EXC_RETURN", details)

    if lr & (1 << 2):
        details.append("Return will use PSP.")
    else:
        details.append("Return will use MSP.")

    if lr & (1 << 3):
        details.append("Exception interrupted thread mode.")
    else:
        details.append("Exception interrupted handler mode.")

    if lr & (1 << 4):
        details.append("Basic stack frame expected.")
    else:
        details.append("Extended FP stack frame expected.")

    return DecodeResult("EXC_RETURN", details)


def summarize(core: str, hfsr: Optional[int], cfsr: Optional[int]) -> str:
    if core in {"m0", "m0+"}:
        return "Core has limited fault status support; prioritize stacked PC/LR/xPSR and memory map validation."
    if hfsr is not None and (hfsr & (1 << 30)) and cfsr:
        if cfsr & 0xFF:
            return "Likely HardFault escalated from MemManage fault."
        if cfsr & 0xFF00:
            return "Likely HardFault escalated from BusFault."
        if cfsr & 0xFFFF0000:
            return "Likely HardFault escalated from UsageFault."
    return "Use the decoded bits plus stacked PC and address registers to rank the root cause."


def main() -> None:
    parser = argparse.ArgumentParser(description="Decode common Cortex-M fault registers.")
    parser.add_argument("--core", required=True, choices=["m0", "m0+", "m3", "m4", "m7", "m33"])
    parser.add_argument("--hfsr")
    parser.add_argument("--cfsr")
    parser.add_argument("--mmfar")
    parser.add_argument("--bfar")
    parser.add_argument("--abfsr")
    parser.add_argument("--lr")
    parser.add_argument("--pc")
    parser.add_argument("--xpsr")
    parser.add_argument("--msp")
    parser.add_argument("--psp")
    args = parser.parse_args()

    hfsr = parse_int(args.hfsr)
    cfsr = parse_int(args.cfsr)
    mmfar = parse_int(args.mmfar)
    bfar = parse_int(args.bfar)
    abfsr = parse_int(args.abfsr)
    lr = parse_int(args.lr)
    pc = parse_int(args.pc)
    xpsr = parse_int(args.xpsr)
    msp = parse_int(args.msp)
    psp = parse_int(args.psp)

    print(f"Core: {args.core}")
    print(f"HFSR: {format_hex(hfsr)}")
    print(f"CFSR: {format_hex(cfsr)}")
    print(f"MMFAR: {format_hex(mmfar)}")
    print(f"BFAR: {format_hex(bfar)}")
    print(f"ABFSR: {format_hex(abfsr)}")
    print(f"PC: {format_hex(pc)}")
    print(f"xPSR: {format_hex(xpsr)}")
    print(f"MSP: {format_hex(msp)}")
    print(f"PSP: {format_hex(psp)}")
    print()

    print("Summary:")
    print(f"- {summarize(args.core, hfsr, cfsr)}")
    print()

    print("Decoded flags:")
    for item in decode_hfsr(hfsr) + decode_cfsr(cfsr) + [decode_exc_return(lr)]:
        print(f"- {item.title}")
        for detail in item.details:
            print(f"  * {detail}")

    if args.core == "m7" and abfsr is None:
        print("- ABFSR")
        print("  * M7 target detected. Consider capturing ABFSR if the bus fault origin is unclear.")

    print()
    print("Next checks:")
    print("- Map the stacked PC to source/disassembly.")
    print("- Trust MMFAR/BFAR only when MMARVALID/BFARVALID are set in CFSR.")
    print("- Re-check stack integrity first if stacking/unstacking bits are set.")
    print("- Downgrade PC confidence when IMPRECISERR is present.")


if __name__ == "__main__":
    main()
