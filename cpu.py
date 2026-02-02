instruction_set="""
instruction    opcode
nop            00000
load           00001
store          00010
mov            00011
add            00100
sub            00101
and            00110
or             00111
xor            01000
not            01001
shr            01010
shl            01011
cmp            01100
lmp            01101
beq            01110
rst            01111
in             10000
"""
print(instruction_set)

def g_not(a):
    return a^1

def g_and(a, b):
    return a & b

def g_or(a, b):
    return a | b

def g_xor(a, b):
    return a ^ b

def g_nor(a, b):
    return (a | b)^1

def g_nand(a, b):
    return (a & b)^1

def g_xnor(a, b):
    return (a ^ b)^1

def store(a):
    return

def nop():
    pass

def input_(a):
    memory.append(a)
    return

def load(index,register):
    if register == 0:
        reg_a=memory[index]
        return
    
    elif register == 1:
        reg_b=memory[index]
        return
    
    elif register == 2:
        reg_c=memory[index]
        return

def add(dest):
    global reg_a
    global reg_b
    global reg_c
    
    if dest == 0:
        reg_a = reg_b+reg_c
        print(reg_a)
        return
    
    elif dest == 1:
        reg_b = reg_a+reg_c
        print(reg_b)
        return
    
    elif dest == 2:
        reg_c = reg_a+reg_b
        print(reg_c)
        return

memory=[]
reg_a=0
reg_b=0
reg_c=0

while True:
    usr = input("\n")

    if usr == "exit":
        break

    x = usr.split()

    a = int(x[0])
    b = int(x[1])
    c = int(x[2])
    instruction = x[3]

    if instruction == "nop":
        nop()

    elif instruction == "in":
        input_(a)

    elif instruction == "load":
        load(a,b)

    elif instruction == "store":
        print(g_xor(a, b))

    elif instruction == "nor":
        print(g_nor(a, b))

    elif instruction == "nand":
        print(g_nand(a, b))

    elif instruction == "xnor":
        print(g_xnor(a, b))
    
    elif instruction == "add":
        add(a)
