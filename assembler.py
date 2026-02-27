import cpu
import sys

def get_opcodes():
    instructions = [
        'lda', 'ldb', 'ldc', 'ldi', 'sta', 'stb', 'stc', 'sti',
        'mov', 'add', 'sub', 'mul', 'div', 'gand', 'gor', 'gxor',
        'shl', 'shr', 'cmp', 'dec', 'inc', 'jmp', 'jz', 'jnz',
        'jn', 'jc', 'push', 'pop', 'call', 'ret', 'nop', 'halt', 'swp'
    ]
    mapping = {}
    for name in instructions:
        if hasattr(cpu, name):
            mapping[name] = getattr(cpu, name)
    return mapping

def assemble(input_file, output_file):
    opcodes = get_opcodes()
    symbol_table = {}
    lines_to_process = []
    address_counter = 0

    with open(input_file, 'r') as f:
        for line in f:
            clean_line = line.split(';')[0].strip()
            if not clean_line:
                continue

            if clean_line.endswith(':'):
                label_name = clean_line[:-1].lower()
                symbol_table[label_name] = address_counter
            else:
                lines_to_process.append(clean_line)
                address_counter += 3

    binary_result = bytearray()

    for line in lines_to_process:
        parts = line.split()
        mnemonic = parts[0].lower()

        raw_operand = parts[1] if len(parts) > 1 else "0"

        if raw_operand.lower() in symbol_table:
            operand_value = symbol_table[raw_operand.lower()]
        else:
            operand_value = int(raw_operand, 0)

        if mnemonic in opcodes:
            opcode_value = opcodes[mnemonic]
            binary_result.append(opcode_value)
            binary_result.append(operand_value & 0xFF)
            binary_result.append((operand_value >> 8) & 0xFF)

    with open(output_file, 'wb') as f:
        f.write(binary_result)

if __name__ == "__main__":
    assemble("program.asm", "program.bin")
