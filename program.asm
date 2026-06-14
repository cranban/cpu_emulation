; compiled by viper / ybmc
__L1:
    ldi r1 1
    ldi r2 0
    cmpr r1 r2
    jz __L2
    ldi r1 20
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L3
    ldi r1 190
    st r1 0xFEF0
__L3:
    ldi r1 26
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L5
    ldi r1 232
    st r1 0xFEF0
__L5:
    ldi r1 8
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L7
    ldi r1 244
    st r1 0xFEF0
__L7:
    ldi r1 21
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L9
    ldi r1 256
    st r1 0xFEF0
__L9:
    ldi r1 23
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L11
    ldi r1 268
    st r1 0xFEF0
__L11:
    ldi r1 28
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L13
    ldi r1 280
    st r1 0xFEF0
__L13:
    ldi r1 24
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L15
    ldi r1 292
    st r1 0xFEF0
__L15:
    ldi r1 12
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L17
    ldi r1 304
    st r1 0xFEF0
__L17:
    ldi r1 18
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L19
    ldi r1 316
    st r1 0xFEF0
__L19:
    ldi r1 19
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L21
    ldi r1 328
    st r1 0xFEF0
__L21:
    ldi r1 4
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L23
    ldi r1 340
    st r1 0xFEF0
__L23:
    ldi r1 22
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L25
    ldi r1 352
    st r1 0xFEF0
__L25:
    ldi r1 7
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L27
    ldi r1 364
    st r1 0xFEF0
__L27:
    ldi r1 9
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L29
    ldi r1 376
    st r1 0xFEF0
__L29:
    ldi r1 10
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L31
    ldi r1 388
    st r1 0xFEF0
__L31:
    ldi r1 11
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L33
    ldi r1 400
    st r1 0xFEF0
__L33:
    ldi r1 13
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L35
    ldi r1 412
    st r1 0xFEF0
__L35:
    ldi r1 14
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L37
    ldi r1 424
    st r1 0xFEF0
__L37:
    ldi r1 15
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 0
    cmpr r1 r2
    jz __L39
    ldi r1 436
    st r1 0xFEF0
__L39:
    ldi r1 20
    ldi r2 0xFF00
    add r1 r1 r2
    ldind r1 r1
    ldi r2 0x00FF
    gand r1 r1 r2
    ldi r2 26
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 8
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 21
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 23
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 28
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 24
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 12
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 18
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 19
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 4
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 22
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 7
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 9
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 10
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 11
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 13
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 14
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    ldi r2 15
    ldi r3 0xFF00
    add r2 r2 r3
    ldind r2 r2
    ldi r3 0x00FF
    gand r2 r2 r3
    add r1 r1 r2
    st r1 0x8000
    ld r1 0x8000
    ldi r2 0
    cmpr r1 r2
    jnz __L41
    ldi r1 0
    st r1 0xFEF0
__L41:
    vsync
    jmp __L1
__L2:
    halt