nop = 0x0 
loada = 0x1
loadb = 0x2
storea = 0x3
storeb = 0x4
add = 0x5
jmp = 0x6
halt = 0xf

reg_a=0
reg_b=0
pc=0
running=True
memory=256*[0]
print(memory)

def fetch():
    global pc
    instruction=memory[pc]
    pc=(pc+1)&0xff
    return instruction

def execute(instruction):
    global pc, reg_a, reg_b , running 
    print(f"instruction:{instruction}")
    opcode=instruction>>4
    operand=instruction & 0x0f
    print(f"opcode:{opcode}")
    print(f"operand:{operand}")
    if opcode==nop:
        pass
    elif opcode==loada:
        reg_a=operand
    elif opcode==loadb:
        reg_b=operand
    elif opcode==storea:
        memory[operand]=reg_a
    elif opcode==storeb:
        memory[operand]=reg_b
    elif opcode==add:
        reg_a=reg_a+reg_b
        print(f"sum:{reg_a}")
    elif opcode==jmp:
        pc=operand
    elif opcode==halt:
        running=False

memory[0]=(loada<<4)|0x4
memory[1]=(loadb<<4)|0x8
memory[2]=(add<<4)|0x0
memory[3]=(storea<<4)|0x9
memory[4]=(halt<<4)|0x0

while running==True:
    instruction=fetch()
    execute(instruction)
