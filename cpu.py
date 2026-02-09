#instruction set
nop = 0x00 
loada = 0x01
loadb = 0x02
storea = 0x03
storeb = 0x04
addi = 0x05
jmp = 0x06
inp = 0x07
out = 0x08
mov = 0x09
loadi = 0x0a
storei = 0x0b
shiftl = 0x0c
shiftr = 0x0d
jz = 0x0e
sub = 0x0f
halt = 0x10

#registers
reg_a = 0           #id:0x0
reg_b = 0           #id:0x1
inpr = 0            #id:0x2
outr = 0            #id:0x3
indr = 0            #id:0x4
pc = 0              
zf = 0              
nf = 0
running = True
memory = 256 * [0]

#fetch decode and execute
def fetch():
    global pc
    instruction = memory[pc]
    pc= (pc + 1) & 0xff
    return instruction

def execute(instruction):
    global pc, zf, reg_a, reg_b, inpr, outr, indr, running 
    
    opcode = instruction >> 4
    operand = instruction & 0x0f
    
    if opcode == nop:
        pass
    
    elif opcode == loada:
        memory[indr]=reg_a
    
    elif opcode == loadb:
        memory[indr]=reg_b
    
    elif opcode == storea:
        reg_a = memory[indr]
    
    elif opcode == storeb:
        reg_b = memory[indr]
    
    elif opcode == mov:
        origin=operand>>2
        destination=operand&0xf
        if origin==0x0 and destination==0x1:
            reg_b=reg_a
        elif origin==0x0 and destination==0x2:
            inpr=reg_a
        elif origin==0x0 and destination==0x3:
            outr=reg_a
        elif origin==0x0 and destination==0x4:
            indr=reg_a
        elif origin==0x1 and destination==0x0:
            reg_a=reg_b
        elif origin==0x1 and destination==0x2:
            inpr=reg_b
        elif origin==0x1 and destination==0x3:
            outr=reg_b
        elif origin==0x1 and destination==0x4:
            indr=reg_b
        elif origin==0x2 and destination==0x0:
            reg_a=inpr

                
    elif opcode == addi:
        reg_a = (reg_a + reg_b) & 0xff
    
    elif opcode = subi:
        reg_a = (reg_a - reg_b)
        if reg_a==0:
            zf=1
        elif reg_a<0:
            nf=1
    
    elif opcode == jmp:
        pc = operand
    
    elif opcode == inp:
        inpr = int(input()) & 0xff
    
    elif opcode == out:
        outr = memory[indr]
        print(outr)
    
    elif opcode == loadi:
        reg_a = memory[indr]
    
    elif opcode == storei:
        memory[indr] = reg_a
    
    elif opcode == shiftr:
        indr = (indr << operand) & 0xff
    
    elif opcode == shiftl:
        indr = (indr>>operand) & 0xff
    
    elif opcode == jz and zf ==1:
        pc = indr
    
    elif opcode == sub:
        reg a = (reg_a - reg_b) & 0xff
    
    elif opcode==halt:
        running=False

#program
memory[0]=mov|((0x0<<2)|0x1)
while running == True:
    instruction = fetch()
    execute(instruction)
    print(memory)
