import sys
import math

opcodes = {
    "ld":    0x00,
    "st":    0x01,
    "ldi":   0x02,
    "ldind": 0x03,
    "stind": 0x04,
    "mov":   0x05,
    "add":   0x06,
    "sub":   0x07,
    "mul":   0x08,
    "div":   0x09,
    "inc":   0x0a,
    "dec":   0x0b,
    "neg":   0x0c,
    "mod":   0x0d,
    "gand":  0x0e,
    "gor":   0x0f,
    "gxor":  0x10,
    "gnot":  0x11,
    "shl":   0x12,
    "shr":   0x13,
    "cmpr":  0x14,
    "jmp":   0x15,
    "jz":    0x16,
    "jnz":   0x17,
    "jng":   0x18,
    "jc":    0x19,
    "jge":   0x1a,
    "jle":   0x1b,
    "push":  0x1c,
    "pop":   0x1d,
    "call":  0x1e,
    "ret":   0x1f,
    "pixel": 0x20,
    "nop":   0x21,
    "halt":  0x22,
    "vsync": 0x23,  # FIX: added vsync
}

registers = {
    "r0":  0x00,
    "r1":  0x01,
    "r2":  0x02,
    "r3":  0x03,
    "r4":  0x04,
    "r5":  0x05,
    "r6":  0x06,
    "r7":  0x07,
    "r8":  0x08,
    "r9":  0x09,
    "r10": 0x0a,
    "r11": 0x0b,
    "r12": 0x0c,
    "r13": 0x0d,
    "r14": 0x0e,
    "idx": 0x0f,
    "sp":  0x10,
}

def parse_int(s):
    if s.startswith("0x") or s.startswith("0X"):
        return int(s, 16)
    elif s.startswith("0b") or s.startswith("0B"):
        return int(s, 2)
    else:
        return int(s)

def assemble(source):
    lines = source.splitlines()
    labels = {}
    cleaned = []

    for line in lines:
        line = line.split(";")[0].strip()
        if not line:
            continue
        cleaned.append(line)

    # pass 1 - find labels and record addresses
    address = 0
    tokens_list = []
    for line in cleaned:
        if line.endswith(":"):
            labels[line[:-1]] = address
        else:
            tokens = line.split()
            op = tokens[0].lower()
            if op == ".dw":
                address += 2 * (len(tokens) - 1)
            elif op == ".sinetable":
                address += 512
            else:
                address += 4
            tokens_list.append(tokens)

    # pass 2 - assemble
    output = []
    for tokens in tokens_list:
        op = tokens[0].lower()
        args = tokens[1:]

        if op == ".dw":
            for val in args:
                v = parse_int(val) if val not in labels else labels[val]
                v = v & 0xffff
                output.append(v & 0xff)
                output.append((v >> 8) & 0xff)
            continue

        if op == ".sinetable":
            for i in range(256):
                angle = 2 * math.pi * i / 256
                val = int(math.sin(angle) * 127) + 128
                val = val & 0xffff
                output.append(val & 0xff)
                output.append((val >> 8) & 0xff)
            continue

        if op not in opcodes:
            print(f"unknown instruction: {op}")
            sys.exit(1)

        opcode = opcodes[op]
        byte2 = 0
        byte3 = 0
        byte4 = 0

        if op in ("ld", "st"):
            reg = registers[args[0]]
            addr = parse_int(args[1]) if args[1] not in labels else labels[args[1]]
            byte2 = reg
            byte3 = (addr >> 8) & 0xff
            byte4 = addr & 0xff

        elif op == "ldi":
            reg = registers[args[0]]
            val = parse_int(args[1]) if args[1] not in labels else labels[args[1]]
            byte2 = reg
            byte3 = (val >> 8) & 0xff
            byte4 = val & 0xff

        elif op == "ldind":
            dst = registers[args[0]]
            src = registers[args[1]]
            byte2 = (dst << 4) | src

        elif op == "stind":
            val = registers[args[0]]
            addr = registers[args[1]]
            byte2 = (val << 4) | addr

        elif op == "mov":
            dst = registers[args[0]]
            src = registers[args[1]]
            byte2 = (dst << 4) | src

        elif op in ("add", "sub", "mul", "div", "mod", "gand", "gor", "gxor", "shl", "shr"):
            dst = registers[args[0]]
            s1 = registers[args[1]]
            s2 = registers[args[2]]
            byte2 = (dst << 4) | s1
            byte3 = s2 << 4

        elif op in ("inc", "dec", "neg", "gnot"):
            reg = registers[args[0]]
            byte2 = reg << 4

        elif op == "cmpr":
            s1 = registers[args[0]]
            s2 = registers[args[1]]
            byte2 = (s1 << 4) | s2

        elif op in ("jmp", "jz", "jnz", "jng", "jc", "jge", "jle", "call"):
            addr = parse_int(args[0]) if args[0] not in labels else labels[args[0]]
            byte3 = (addr >> 8) & 0xff
            byte4 = addr & 0xff

        elif op == "push":
            reg = registers[args[0]]
            byte2 = reg << 4

        elif op == "pop":
            reg = registers[args[0]]
            byte2 = reg << 4

        elif op == "pixel":
            color = registers[args[0]]
            addr = registers[args[1]]
            byte2 = (color << 4) | addr

        # FIX: explicit no-arg instructions — ret, nop, halt, vsync
        # byte2/byte3/byte4 stay 0, which is correct
        elif op in ("ret", "nop", "halt", "vsync"):
            pass

        output += [opcode, byte2, byte3, byte4]

    return bytes(output)

if len(sys.argv) < 3:
    print("usage: python assembler.py input.asm output.bin")
    sys.exit(1)

with open(sys.argv[1], "r") as f:
    source = f.read()

binary = assemble(source)

with open(sys.argv[2], "wb") as f:
    f.write(binary)

print(f"assembled {len(binary)} bytes -> {sys.argv[2]}")
