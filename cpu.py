import tkinter as tk
#instructions
lda = 0x00
ldb = 0x01
ldc = 0x02
ldi = 0x03
sta = 0x04
stb = 0x05
stc = 0x06
sti = 0x07
mov = 0x08
add = 0x09
sub = 0x0a
mul = 0x0b
div = 0x0c
gand = 0x0d
gor = 0x0e
gxor = 0x0f
shl = 0x10
shr = 0x11
cmp = 0x12
dec =0x13
inc =0x14
jmp = 0x15
jz = 0x16
jnz = 0x17
jn = 0x18
jc = 0x19
push = 0x1a
pop = 0x1b
call = 0x1c
ret = 0x1d
nop = 0x1e
halt = 0x1f
swp = 0x20
stiv = 0x21
memory = [0] * 65536
vram = 4096 * [0]
#registers           register id:

reg_a = 0              #0x1
reg_b = 0              #0x2
reg_c = 0              #0x3
reg_out = 0            #0x4
zero_flag = 0          #0x5
negative_flag = 0      #0x6
carry_flag = 0         #0x7
program_counter = 0    #0x8
stack_pointer = 0xffff #0x9
reg_instruction = 0    #0xa
reg_index = 0          #0xb
running = True         #0xc

def fetch():
    global program_counter
    opcode = memory[program_counter]
    lowbyte = memory[(program_counter + 1) & 0xffff]
    highbyte = memory[(program_counter + 2) & 0xffff]
    operand = (highbyte << 8 ) | lowbyte
    program_counter = (program_counter + 3) & 0xffff
    return opcode, operand

def execute(opcode, operand):
    global reg_a, reg_b, reg_c, reg_out, zero_flag, negative_flag
    global carry_flag, program_counter, stack_pointer, reg_instruction
    global reg_index, running
    
    if opcode == lda:
        reg_a = memory[operand]
    
    elif opcode == ldb:
        reg_b = memory[operand]
    
    elif opcode == ldc:
        reg_c = memory[operand]
    
    elif opcode == ldi:
        reg_a = operand
    
    elif opcode == sta:
        memory[operand] = reg_a
    
    elif opcode == stb:
        memory[operand] = reg_b
    
    elif opcode == stc:
        memory[operand] = reg_c
    
    elif opcode == sti:
        memory[reg_index & 0xffff] = reg_a
    
    elif opcode == mov:
        source = operand >> 8
        destination = operand & 0xff
        val = 0
        if source == 0x1: val = reg_a
        elif source == 0x2: val = reg_b
        elif source == 0x3: val = reg_c
        elif source == 0x4: val = reg_out
        elif source == 0x5: val = zero_flag
        elif source == 0x6: val = negative_flag
        elif source == 0x7: val = carry_flag
        elif source == 0x8: val = program_counter
        elif source == 0x9: val = stack_pointer
        elif source == 0xa: val = reg_instruction
        elif source == 0xb: val = reg_index
        
        if destination == 0x1: reg_a = val
        elif destination == 0x2: reg_b = val
        elif destination == 0x3: reg_c = val
        elif destination == 0x4: reg_out = val
        elif destination == 0x5: zero_flag = val
        elif destination == 0x6: negative_flag = val
        elif destination == 0x7: carry_flag = val
        elif destination == 0x8: program_counter = val
        elif destination == 0x9: stack_pointer = val
        elif destination == 0xa: reg_instruction = val
        elif destination == 0xb: reg_index = val
    
    elif opcode == add:
        result = reg_b + reg_c
        carry_flag = 1 if result > 0xffff else 0
        reg_a = result & 0xffff
        zero_flag = 1 if reg_a == 0 else 0
        negative_flag = 1 if (reg_a & 0x8000) else 0
    
    elif opcode == sub:
        result = reg_b - reg_c
        carry_flag = 1 if reg_b < reg_c else 0
        reg_a = result & 0xffff
        zero_flag = 1 if reg_a == 0 else 0
        negative_flag = 1 if (reg_a & 0x8000) else 0
    
    elif opcode == gand:
        reg_a = (reg_b & reg_c) & 0xffff
        zero_flag = 1 if reg_a == 0 else 0
        negative_flag = 1 if (reg_a & 0x8000) else 0
        carry_flag = 0
    
    elif opcode == gor:
        reg_a = (reg_b | reg_c) & 0xffff
        zero_flag = 1 if reg_a == 0 else 0
        negative_flag = 1 if (reg_a & 0x8000) else 0
        carry_flag = 0
    
    elif opcode == gxor:
        reg_a = (reg_b ^ reg_c) & 0xffff
        zero_flag = 1 if reg_a == 0 else 0
        negative_flag = 1 if (reg_a & 0x8000) else 0
        carry_flag = 0
    
    elif opcode == shl:
        reg_a = (reg_b << reg_c) & 0xffff
        zero_flag = 1 if reg_a == 0 else 0
        negative_flag = 1 if (reg_a & 0x8000) else 0
        carry_flag = 1 if (reg_b << reg_c) > 0xffff else 0
    
    elif opcode == shr:
        reg_a = (reg_b >> reg_c) & 0xffff
        zero_flag = 1 if reg_a == 0 else 0
        negative_flag = 1 if (reg_a & 0x8000) else 0
        carry_flag = reg_b & 0x1 if reg_c > 0 else 0 
    
    elif opcode == cmp:
        result = reg_b - reg_c
        carry_flag = 1 if reg_b < reg_c else 0
        zero_flag = 1 if (result & 0xffff) == 0 else 0
        negative_flag = 1 if (result & 0x8000) else 0
    
    elif opcode == inc:
        reg_a = (reg_a + 1) & 0xffff
        zero_flag = 1 if reg_a == 0 else 0
        negative_flag = 1 if (reg_a & 0x8000) else 0
    
    elif opcode == dec:
        reg_a = (reg_a - 1) & 0xffff
        zero_flag = 1 if reg_a == 0 else 0
        negative_flag = 1 if (reg_a & 0x8000) else 0
    
    elif opcode == jmp:
        program_counter = operand
    
    elif opcode == jz:
        if zero_flag == 1:
            program_counter = operand
    
    elif opcode == jnz:
        if zero_flag == 0:
            program_counter = operand
        
    elif opcode == jn:
        if negative_flag == 1:
            program_counter = operand
    
    elif opcode == jc:
        if carry_flag == 1:
            program_counter = operand
    
    elif opcode == push:
        stack_pointer = (stack_pointer - 1) & 0xffff
        memory[stack_pointer] = reg_a
    
    elif opcode == pop:
        reg_a = memory[stack_pointer]
        stack_pointer = (stack_pointer + 1) & 0xffff
    
    elif opcode == call:
        stack_pointer = (stack_pointer - 1) & 0xffff
        memory[stack_pointer] = program_counter
        program_counter = operand
    
    elif opcode == ret:
        program_counter = memory[stack_pointer]
        stack_pointer = (stack_pointer + 1) & 0xffff

    elif opcode == swp:
        reg_b, reg_c = reg_c, reg_b

    elif opcode == stiv:
        target_pixel = (reg_index + operand) % 4096
        vram[target_pixel] = reg_a & 0xffff
    
    elif opcode == nop:
        return
    
    elif opcode == halt:
        running = False

def load_bin(filename):
    with open(filename, "rb") as f:
        data = f.read()
        for i, byte in enumerate(data):
            if i < 65536:
                memory[i] = byte
root = tk.Tk()
root.title("SCREEN")
scale = 8
canvas = tk.Canvas(root, width=512, height=512, bg="black", highlightthickness=0)
canvas.pack()

pixels = []
for i in range(4096):
    x, y = (i%64)*scale, (i//64)*scale
    p=canvas.create_rectangle(x,y,x+scale,y+scale,fill="#000000", outline="")
    pixels.append(p)

def run_cpu():
    global running
    if running:
        for _ in range(500):
            opcode, operand = fetch()
            execute(opcode,operand)
            if not running: break
        for i, val in enumerate(vram):
            r, g, b = ((val >> 5) & 0x07) * 36, ((val >> 2) & 0x07) * 36, (val & 0x03) *85
            canvas.itemconfig(pixels[i], fill=f'#{r:02x}{g:02x}{b:02x}')
        root.after(1, run_cpu)

if __name__ == "__main__":
    load_bin("program.bin")
    run_cpu()
    root.mainloop()


