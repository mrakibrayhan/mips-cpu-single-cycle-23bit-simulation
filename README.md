# 23-Bit Single-Cycle MIPS CPU

A custom single-cycle CPU designed and implemented in **Logisim**, built around a self-defined 23-bit MIPS-inspired Instruction Set Architecture (ISA). Developed for **CSE332 — Computer Organization and Architecture** (North South University, Summer 2024, Section 04, Group 9). Includes the complete datapath, control unit, ALU control logic, and a custom Python assembler that translates assembly programs into hex machine code loadable into the Logisim instruction memory.

## Overview

This project implements a fully functional CPU capable of fetching, decoding, and executing instructions from memory sequentially. The design is inspired by the IAS (Institute for Advanced Study) architecture and follows a modular approach, integrating:

- **Register File** — stores intermediate data and results
- **ALU** — performs arithmetic and logical operations
- **Control Unit** — decodes instructions and generates control signals
- **ALU Control Unit** — derives the specific ALU operation from `ALUOp` and `funct`
- **Instruction & Data Memory** — holds the program and associated data

The ISA supports 15 operations assigned per the course specification, across three instruction formats (R-type, I-type, J-type), encoded in **23 bits**.

## Instruction Set Architecture

### Bit Breakdown

| Format | Op (3) | Rs (5) | Rt (5) | Rd (5) | Shamt (2) | Funct (3) |
|---|---|---|---|---|---|---|
| **R-type** | 22–20 | 19–15 | 14–10 | 9–5 | 4–3 | 2–0 |

| Format | Op (3) | Rs (5) | Rt (5) | Immediate (10) |
|---|---|---|---|---|
| **I-type** | 22–20 | 19–15 | 14–10 | 9–0 |

| Format | Op (3) | Address (20) |
|---|---|---|
| **J-type** | 22–20 | 19–0 |

### Opcode Table

| Instruction | Type | Opcode |
|---|---|---|
| All R-type | R-type | `000` |
| LW | I-type | `001` |
| ADDi | I-type | `010` |
| BEQ | I-type | `011` |
| BNE | I-type | `100` |
| SW | I-type | `101` |
| JMP | J-type | `110` |
| NOP | — | `111` |

### Function Table (R-type)

| Instruction | Funct | Description |
|---|---|---|
| ADD | `000` | Add |
| SUB | `001` | Subtract |
| AND | `010` | Logical AND |
| OR | `011` | Logical OR |
| NOR | `100` | Logical NOR |
| SLT | `101` | Set Less Than |
| SLL | `110` | Shift Left Logical |
| SRL | `111` | Shift Right Logical |

### Control Signals

| Instruction | Type | RegDst | RegWrite | ALUSrc | MemRead | MemWrite | MemToReg | Branch | Jump | ALUOp |
|---|---|---|---|---|---|---|---|---|---|---|
| LW | I | 0 | 1 | 1 | 1 | 0 | 1 | 0 | 0 | 00 |
| ADDi | I | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 00 |
| NOP | — | X | X | X | X | X | X | X | X | XX |
| NOR | R | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| BEQ | I | X | 0 | 0 | 0 | 0 | X | 1 | 0 | 01 |
| OR | R | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| ADD | R | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| BNE | I | X | 0 | 0 | 0 | 0 | X | 1 | 0 | 01 |
| SRL | R | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| SW | I | X | 0 | 1 | 0 | 1 | X | 0 | 0 | 00 |
| SLT | R | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| SLL | R | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| SUB | R | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |
| JMP | J | X | 0 | X | 0 | 0 | X | 0 | 1 | XX |
| AND | R | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 10 |

Full ALU control derivation (ALUOp + funct → ALU control output), K-map work, and the detailed control-unit design are documented in `CSE332 Project Tables.xlsx` and `Project Report.pdf`.

## Repository Contents

| File / Folder | Description |
|---|---|
| `Project Report.pdf` / `.docx` | Full project report: introduction, ISA description, control unit table, ALU control table |
| `CSE332 Project Tables.xlsx` | Working design tables — bit breakdown, control unit table, opcode table, ALU control table (with K-map derivation), function table |
| `cover.pdf` | Original course assignment guideline (CSE332, instructor: Tanjila Farah) |
| `circuit/NEW Project 4.1.circ` | Final Logisim datapath file — complete CPU design (register file, ALU, control unit, ALU control, instruction & data memory) |
| `Assembler/assemblerMy.py` | Final custom assembler matching the submitted 23-bit ISA — converts assembly source into hex machine code |
| `Assembler/assembler.py`, `Assembler/assemblerAfsana.py` | Earlier/reference assembler versions developed during the design process |
| `Assembler/inputs` | Sample assembly program |
| `Assembler/outputs` | Sample assembled hex output (generated from `inputs`) |
| `references/` | Supplementary MIPS ISA reference material (not authored as part of this project) |

## Running the Assembler

The assembler scripts read a file literally named `inputs` and write to a file literally named `outputs` in the same directory — rename your own program to `inputs` before running, or edit the hardcoded filenames in the script.

```bash
cd Assembler
python3 assemblerMy.py
```

Example (`inputs`):
```
addi $r1 $r1 9
addi $r2 $r2 6
addi $r3 $r3 1
sub $r4 $r1 $r2
add $r5 $r4 $r3
```

Produces (`outputs`, loadable directly into the Logisim ROM):
```
v2.0 raw
208409
210806
218C01
008881
020CA0
```

## Opening the Circuit

1. Install [Logisim](http://www.cburch.com/logisim/) (this project was built with Logisim 2.7.1).
2. Open `circuit/NEW Project 4.1.circ`.
3. Load an assembled hex program (from `Assembler/outputs`) into the instruction memory ROM.
4. Step or run the clock to execute instructions.

## Authors

- **Mohd Atik Akbar Rahat** (2211757042)
- **Rakib Rayhan** (2132332642)

Group 9 — CSE332.4, North South University, Summer 2024
Instructor: Tanjila Farah (TnF)

## Notes

- `Assembler/assembler.py` and `Assembler/assemblerAfsana.py` are earlier development iterations kept for reference; `assemblerMy.py` reflects the final 23-bit ISA as submitted.
- Only the final circuit revision (`4.1`) is included here; earlier iterations (`3.1`, `4.0`) were part of the design process and are not included.
