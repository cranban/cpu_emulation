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
    operand=instruction&4
    print(f"opcode:{opcode}")
    print(f"operand:{operand}")
    if opcode==nop:
        pass
    elif opcode==loada:
        reg_a=operand
    elif opcode==loadb:
        reg_b=operand
    elif opcode==storea:
        print(opcode)
    elif opcode==halt:
        running=False

memory[0]=(loada<<4)|0x4
memory[1]=(storea<<4)|(reg_a>>4)
memory[2]=(halt<<4)

while running==True:
    instruction=fetch()
    execute(instruction)
