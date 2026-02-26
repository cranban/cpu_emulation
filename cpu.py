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
swp=0x20
memory=[0]*65536

#registers           register id:

reg_a=0              #0x1
reg_b=0              #0x2
reg_c=0              #0x3
reg_out=0            #0x4
zero_flag=0          #0x5
negative_flag=0      #0x6
carry_flag=0         #0x7
program_counter=0    #0x8
stack_pointer=0      #0x9
reg_instruction=0    #0xa
reg_index=0          #0xb
running=True         #0xc

def fetch():
    global program_counter
    opcode=memory[program_counter]
    lowbyte=memory[(program_counter+1)&0xffff]
    highbyte=memory[(program_counter+2)&0xffff]
    operand=(highbyte<<8)|lowbyte
    program_counter=(program_counter+3)&0xffff
    return opcode,operand

def execute(opcode,operand):
    global reg_a,reg_b,reg_c,reg_out,zero_flag,negative_flag
    global carry_flag,program_counter,stack_pointer,reg_instruction
    global reg_index,running
    
    if opcode==lda:
        reg_a=memory[operand]
    
    elif opcode==ldb:
        reg_b=memory[operand]
    
    elif opcode==ldc:
        reg_c=memory[operand]
    
    elif opcode==ldi:
        reg_a=operand
    
    elif opcode==sta:
        memory[operand]=reg_a
    
    elif opcode==stb:
        memory[operand]=reg_b
    
    elif opcode==stc:
        memory[operand]=reg_c
    
    elif opcode==sti:
        #placeholder
        return
    
    elif opcode==mov:
        source=operand>>8
        destination=operand&0xff
        val=0
        if source==0x1: val=reg_a
        elif source==0x2: val=reg_b
        elif source==0x3: val=reg_c
        elif source==0x4: val=reg_out
        elif source==0x5: val=zero_flag
        elif source==0x6: val=negative_flag
        elif source==0x7: val=carry_flag
        elif source==0x8: val=program_counter
        elif source==0x9: val=stack_pointer
        elif source==0xa: val=reg_instruction
        elif source==0xb: val=reg_index
        
        if destination==0x1: reg_a=val
        elif destination==0x2: reg_b=val
        elif destination==0x3: reg_c=val
        elif destination==0x4: reg_out=val
        elif destination==0x5: zero_flag=val
        elif destination==0x6: negative_flag=val
        elif destination==0x7: carry_flag=val
        elif destination==0x8: program_counter=val
        elif destination==0x9: stack_pointer=val
        elif destination==0xa: reg_instruction=val
        elif destination==0xb: reg_index=val
    
    elif opcode==add:
        result=reg_b+reg_c
        carry_flag=1 if result>0xffff else 0
        reg_a=result&0xffff
        zero_flag=1 if reg_a==0 else 0
        negative_flag=1 if (reg_a&0x8000) else 0
    
    elif opcode==sub:
        result=reg_b-reg_c
        carry_flag=1 if reg_b<reg_c else 0
        reg_a=result&0xffff
        zero_flag=1 if reg_a==0 else 0
        negative_flag=1 if (reg_a&0x8000) else 0
    
    elif opcode==gand:
        reg_a= (reg_b&reg_c)&0xffff
        zero_flag=1 if reg_a==0 else 0
        negative_flag=1 if (reg_a&0x8000) else 0
        carry_flag=0
    
    elif opcode==gor:
        reg_a=(reg_b|reg_c)&0xffff
        zero_flag=1 if reg_a==0 else 0
        negative_flag=1 if (reg_a&0x8000) else 0
        carry_flag=0
    
    elif opcode==gxor:
        reg_a=(reg_b^reg_c)&0xffff
        zero_flag=1 if reg_a==0 else 0
        negative_flag=1 if (reg_a&0x8000) else 0
        carry_flag=0
        return
    
    elif opcode==shl:
        #placeholder
        return
    
    elif opcode==shr:
        #placeholder
        return
    
    elif opcode==cmp:
        result=reg_b-reg_c
        carry_flag=1 if reg_b<reg_c else 0
        zero_flag=1 if (result&0xffff)==0 else 0
        negative_flag=1 if (result&0x8000) else 0
    
    elif opcode==inc:
        #placeholder
        return
    
    elif opcode==dec:
        #placeholder
        return
    
    elif opcode==jmp:
        #placeholder
        return
    
    elif opcode==jz:
        #placeholder
        return
    
    elif opcode==jnz:
        #placeholder
        return
    
    elif opcode==jn:
        #placeholder
        return
    
    elif opcode==jc:
        #placeholder
        return
    
    elif opcode==push:
        #placeholder
        return
    
    elif opcode==pop:
        #placeholder
        return
    
    elif opcode==call:
        #placeholder
        return
    
    elif opcode==ret:
        #placeholder
        return
    
    elif opcode==nop:
        return
    
    elif opcode==halt:
        running=False
        
while running==True:
    opcode,operand=fetch()
    execute(opcode,operand)
