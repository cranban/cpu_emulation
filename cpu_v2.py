import tkinter as tk
#instructions:

#memory
ld = 0x00
st = 0x01
ldi = 0x02
ldind = 0x03
stind = 0x04

#register
mov = 0x05

#Arithmetic
add = 0x06
sub = 0x07
mul = 0x08
div = 0x09
inc = 0x0a
dec = 0x0b
neg = 0x0c
mod = 0x0d

#bitwise
gand = 0x0e
gor = 0x0f
gxor = 0x10
gnot = 0x11
shl = 0x12
shr = 0x13

#comparison
cmpr = 0x14

#jumps
jmp = 0x15
jz = 0x16
jnz = 0x17
jn = 0x18
jc = 0x19
jge = 0x1a
jle = 0x1b

#stack
push = 0x1c
pop = 0x1d
call = 0x1e
ret = 0x1f

#display
pixel = 0x20

#misc
nop = 0x21
halt = 0x22

#registers
r0 = 0               #0x00
r1 = 0               #0x01
r2 = 0               #0x02
r3 = 0               #0x03
r4 = 0               #0x04
r5 = 0               #0x05
r6 = 0               #0x06
r7 = 0               #0x07
r8 = 0               #0x08
r9 = 0               #0x09
r10 = 0              #0x0a
r11 = 0              #0x0b
r12 = 0              #0x0c
r13 = 0              #0x0d
r14 = 0              #0x0e
idx = 0              #0x0f
sp = 0xffff          #0x10

#flags
zero_flag = 0        #0x11
carry_flag = 0       #0x12
negative_flag = 0    #0x13

#running
program_counter = 0  #0x14
running = True
#memory
ram = 65536 * [0]
vram = 16384 * [0]
rom = 1024 * [0]

def fetch():
    global program_counter
    opcode = ram[program_counter]
    byte2 = ram[(program_counter + 1) & 0xffff]
    byte3 = ram[(program_counter + 2) & 0xffff]
    byte4 = ram[(program_counter + 3) & 0xffff]
    program_counter = (program_counter + 4) & 0xffff
    return opcode, byte2 ,byte3 ,byte4

def execute(opcode, byte2, byte3, byte4):
    global r1, r2, r3 ,r4 ,r5 ,r6 ,r7 ,r8 , r9, r10, r11, r12, r13, r14, idx, sp
    global zero_flag, carry_flag, negative_flag
    global running, program_counter

    if opcode == ld:
        reg_id = byte2
        address = (byte3 << 8) | byte4
        value = ram[address]
        set_reg(reg_id, value)

    elif opcode == st:
        reg_id = byte2
        address = (byte3 << 8) | byte4
        ram[address] = get_reg(reg_id)

    elif opcode == ldi:
        reg_id = byte2
        value = (byte3 << 8) | byte4
        set_reg(reg_id, value)

    elif opcode==ldind:
        dst_reg = byte2 >> 4
        addr_reg = byte2 & 0x0f
        address = get_reg(addr_reg)
        set_reg(dst_reg, ram[address])

    elif opcode == stind:
        value_reg = byte2 >> 4
        address_reg = byte2 & 0x0f
        ram[get_reg(address_reg)] = get_reg(value_reg)

    elif opcode == mov:
        destination = byte2 >> 4
        source = byte2 & 0x0f
        set_reg(destination, get_reg(source))

    elif opcode == add:
        destination = byte2 >> 4
        source1 = byte2 & 0x0f
        source2 = byte3 >> 4
        result = get_reg(source1) + get_reg(source2)
        carry_flag = 1 if result > 0xffff else 0
        zero_flag = 1 if (result & 0xffff) == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(destination, result)

    elif opcode == sub:
        destination = byte2 >> 4
        source1 = byte2 & 0x0f
        source2 = byte3 >> 4
        result = get_reg(source1) - get_reg(source2)
        carry_flag = 1 if get_reg(source1) < get_reg(source2) else 0
        zero_flag = 1 if (result & 0xffff) == 0 else 0
        negative_flag =1 if (result & 0x8000) else 0
        set_reg(destination, result)

    elif opcode == mul:
        destination = byte2 >> 4
        source1 = byte2 & 0x0f
        source2 = byte3 >> 4
        result = get_reg(source1) * get_reg(source2)
        carry_flag = 1 if result > 0xffff else 0
        zero_flag = 1 if (result&0xffff) == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(destination, result)

    elif opcode == div:
        destination = byte2 >> 4
        source1 = byte2 & 0x0f
        source2 = byte3 >> 4
        if get_reg(source2) == 0:
            carry_flag = 1
        else:
            result = get_reg(source1) // get_reg(source2)
            carry_flag = 0
            zero_flag =1 if result == 0 else 0
            negative_flag = 1 if (result & 0x8000) else 0
            set_reg(destination, result)

    elif opcode == inc:
        reg_id = byte2 >> 4
        result = (get_reg(reg_id) + 1) & 0xffff
        zero_flag = 1 if result == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(reg_id, result)

    elif opcode == dec:
        reg_id = byte2 >> 4
        result = (get_reg(reg_id) - 1) & 0xffff
        zero_flag = 1 if result == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(reg_id, result)

    elif opcode == neg:
        reg_id = byte2 >> 4
        result = (~get_reg(reg_id) + 1) & 0xffff
        zero_flag = 1 if result == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(reg_id, result)

    elif opcode == mod:
        destination = byte2 >> 4
        source1 = byte2 & 0x0f
        source2 = byte3 >> 4
        if get_reg(source2) == 0:
            carry_flag = 1
        else:
            result = get_reg(source1) % get_reg(source2)
            carry_flag = 0
            zero_flag = 1 if (result & 0xffff) == 0 else 0
            negative_flag = 1 if (result & 0x8000) else 0
            set_reg(destination, result)

    elif opcode == gand:
        destination = byte2 >> 4
        source1 = byte2 & 0x0f
        source2 = byte3 >> 4
        result = get_reg(source1) & get_reg(source2)
        carry_flag = 0
        zero_flag = 1 if result == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(destination, result)

    elif opcode == gor:
        destination = byte2 >> 4
        source1 = byte2 & 0x0f
        source2 = byte3 >> 4
        result = get_reg(source1) | get_reg(source2)
        carry_flag = 0
        zero_flag = 1 if result == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(destination, result)

    elif opcode == gxor:
        destination = byte2 >> 4
        source1 = byte2 & 0x0f
        source2 = byte3 >> 4
        result = get_reg(source1) ^ get_reg(source2)
        carry_flag = 0
        zero_flag = 1 if result == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(destination, result)

    elif opcode == gnot:
        reg_id = byte2 >> 4
        result = (~get_reg(reg_id)) & 0xffff
        carry_flag = 0
        zero_flag = 1 if result == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(reg_id, result)

    elif opcode == shl:
        destination = byte2 >> 4
        source1 = byte2 & 0x0f
        source2 = byte3 >> 4
        raw = get_reg(source1) << get_reg(source2)
        carry_flag = 1 if raw > 0xffff else 0
        result = raw & 0xffff
        zero_flag = 1 if result == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(destination, result)

    elif opcode == shr:
        destination = byte2 >> 4
        source1 = byte2 & 0x0f
        source2 = byte3 >> 4
        val = get_reg(source1)
        shift = get_reg(source2)
        carry_flag = (val >> (shift - 1)) & 1 if shift > 0 else 0
        result = val >> shift
        zero_flag = 1 if result == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
        set_reg(destination, result)

    elif opcode == cmpr:
        source1 = byte2 >> 4
        source2 = byte2 & 0x0f
        result = get_reg(source1) - get_reg(source2)
        carry_flag = 1 if get_reg(source1) < get_reg(source2) else 0
        zero_flag = 1 if (result & 0xffff) == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0

    elif opcode == jmp:
        program_counter = (byte3 << 8) | byte4

    elif opcode == jz:
        if zero_flag == 1:
            program_counter = (byte3 << 8) | byte4

    elif opcode == jnz:
        if zero_flag == 0:
            program_counter = (byte3 << 8) | byte4

    elif opcode == jn:
        if negative_flag == 1:
            program_counter = (byte3 << 8) | byte4

    elif opcode == jc:
        if carry_flag == 1:
            program_counter = (byte3 << 8) | byte4

    elif opcode == jge:
        if carry_flag == 0:
            program_counter = (byte3 << 8) | byte4

    elif opcode == jle:
        if negative_flag == 1  or zero_flag == 1:
            program_counter = (byte3 << 8) | byte4

    elif opcode == push:
        reg_id = byte2 >> 4
        val = get_reg(reg_id)
        sp = (sp - 1) & 0xffff
        ram[sp] = (val >> 8) & 0xff
        sp = (sp - 1) & 0xffff
        ram[sp] = val & 0xff

    elif opcode == pop:
        reg_id = byte2 >> 4
        low = ram[sp]
        sp = (sp + 1) & 0xffff
        high = ram[sp]
        sp = (sp + 1) & 0xffff
        set_reg(reg_id, (high << 8) | low)

    elif opcode == call:
        address = (byte3 << 8) | byte4
        sp = (sp - 1) & 0xffff
        ram[sp] = (program_counter >> 8) & 0xff
        sp = (sp - 1) & 0xffff
        ram[sp] = program_counter & 0xff
        program_counter = address

    elif opcode == ret:
        low  = ram[sp]
        sp = (sp + 1) & 0xffff
        high = ram[sp]
        sp = (sp + 1) & 0xffff
        program_counter = (high << 8) | low

    elif opcode == pixel:
        color_reg = byte2 >> 4
        addr_reg = byte2 & 0x0f
        address = get_reg(addr_reg)
        if 0 <= address < 16384:
            vram[address] = get_reg(color_reg) & 0x0f

    elif opcode == nop:
        return

    elif opcode == halt:
        running = False

def get_reg(reg_id):
    if reg_id == 0x00: return 0
    if reg_id == 0x01: return r1
    if reg_id == 0x02: return r2
    if reg_id == 0x03: return r3
    if reg_id == 0x04: return r4
    if reg_id == 0x05: return r5
    if reg_id == 0x06: return r6
    if reg_id == 0x07: return r7
    if reg_id == 0x08: return r8
    if reg_id == 0x09: return r9
    if reg_id == 0x0a: return r10
    if reg_id == 0x0b: return r11
    if reg_id == 0x0c: return r12
    if reg_id == 0x0d: return r13
    if reg_id == 0x0e: return r14
    if reg_id == 0x0f: return idx
    if reg_id == 0x10: return sp
    if reg_id == 0x11: return zero_flag
    if reg_id == 0x12: return carry_flag
    if reg_id == 0x13: return negative_flag
    return 0

def set_reg(reg_id, value):
    global r1, r2, r3 ,r4 ,r5 ,r6 ,r7 ,r8 , r9, r10, r11, r12, r13, r14, idx, sp
    value = value & 0xffff
    if reg_id == 0x00: return
    elif reg_id == 0x01: r1 = value
    elif reg_id == 0x02: r2 = value
    elif reg_id == 0x03: r3 = value
    elif reg_id == 0x04: r4 = value
    elif reg_id == 0x05: r5 = value
    elif reg_id == 0x06: r6 = value
    elif reg_id == 0x07: r7 = value
    elif reg_id == 0x08: r8 = value
    elif reg_id == 0x09: r9 = value
    elif reg_id == 0x0a: r10 = value
    elif reg_id == 0x0b: r11 = value
    elif reg_id == 0x0c: r12 = value
    elif reg_id == 0x0d: r13 = value
    elif reg_id == 0x0e: r14 = value
    elif reg_id == 0x0f: idx = value
    elif reg_id == 0x10: sp = value

