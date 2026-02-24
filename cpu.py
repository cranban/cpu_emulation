#instructions
lda=0x00
ldb=0x01
ldc=0x02
ldi=0x03
sta=0x04
stb=0x05
stc=0x06
sti=0x07
mov=0x08
add=0x09
sub=0x0a
mul=0x0b
div=0x0c
gand=0x0d
gor=0x0e
gxor=0x0f
shl=0x10
shr=0x11
cmp=0x12
dec=0x13
inc=0x14
jmp=0x15
jz=0x16
jnz=0x17
jn=0x18
jc=0x19
push=0x1a
pop=0x1b
call=0x1c
ret=0x1d
nop=0x1e
halt=0x1f
memory=[0]*65536
#registers
reg_a=0
reg_b=0
reg_c=0
reg_out=0
zero_flag=0
negative_flag=0
carry_flag=0
program_counter=0
stack_pointer=0
reg_instruction=0
reg_index=0
running=True

def fetch(opcode,operand):
    global program_counter
    opcode=memory[program_counter]
    lowbyte=memory[program_counter+1]
    highbyte=memory[program_counter+2]
    operand=(highbyte<<8)|lowbyte
    program_counter=(program_counter+3)&0xffff
    return opcode,operand

def execute(opcode,operand):
    global reg_a,reg_b,reg_c,reg_out,zero_flag,negative_flag,
    carry_flag,program_counter,stack_pointer,reg_instruction,
    reg_index,running
    
    if opcode==lda:
        reg_a=memory[reg_index]
    elif opcode==ldb:
        reg_b=memory[reg_index]
    elif opcode==ldc:
        reg_c=memory[reg_index]
    elif opcode==ldi:
        reg_a=operand

while running==True:
    opcode,operand=fetch(opcode,operand)
    execute(opcode,operand)
