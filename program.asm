ldi 0           ; Initialize color to 0
mov 0x0104      ; Store color in reg_out (temporary storage)
ldi 0           ; Initialize pixel index to 0
mov 0x010B      ; Set reg_index = 0

DRAW_LOOP:
mov 0x0401      ; Copy reg_out (color) back to reg_a
stiv 0          ; VRAM[reg_index] = reg_a

; Increment Color
inc 0           ; reg_a = reg_a + 1
mov 0x0104      ; Save new color in reg_out

; Increment Pixel Index
mov 0x0B01      ; reg_a = reg_index
inc 0           ; reg_a = reg_a + 1
mov 0x010B      ; reg_index = reg_a

; Check if we finished 4096 pixels (0x1000)
ldb 0x1000      ; Load 4096 into reg_b
mov 0x0B03      ; Load current index into reg_c
cmp 0           ; Compare reg_b and reg_c
jnz DRAW_LOOP   ; If index != 4096, repeat

halt 0          ; Finish

