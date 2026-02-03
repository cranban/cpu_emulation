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
    opcode=instruction>>4
    operand=instruction&4
    if opcode==nop:
        pass



while running==True:
    break
