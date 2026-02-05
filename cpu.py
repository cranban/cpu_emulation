nop = 0x0 
loada = 0x1
loadb = 0x2
storea = 0x3
storeb = 0x4
add = 0x5
jmp = 0x6
inp = 0x7
out = 0x8
mov = 0x9
halt = 0xf

reg_a=0
reg_b=0
inpr=0
outr=0
par=0x00
pc=0
running=True
memory=256*[0]


def fetch():
    global pc
    instruction=memory[pc]
    pc=(pc+1)&0xff
    return instruction

def execute(instruction):
    global pc, reg_a, reg_b, inpr, outr, par, running 
    
    opcode=instruction>>4
    operand=instruction&0x0f
    
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
    elif opcode==mov:
        memory[operand]
    elif opcode==add:
        reg_a=reg_a+reg_b
    elif opcode==jmp:
        pc=operand
    elif opcode==inp:
        inpr=int(input())
    elif opcode==out:
        outr=memory[par]
        print(outr)
    elif opcode==halt:
        running=False


memory[0]=(loada<<4)|0x4
memory[1]=(loadb<<4)|0x8
memory[2]=(add<<4)|0x0
memory[3]=(storea<<4)|0xf
memory[4]=(halt<<4)|0x0

while running==True:
    instruction=fetch()
    execute(instruction)
    print(memory)
