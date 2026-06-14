#!/usr/bin/env python3
# ybmc.py - Viper language compiler for YBM-16
import sys, re

KEY_CONSTANTS = {
    'KEY_A':4,'KEY_B':5,'KEY_C':6,'KEY_D':7,'KEY_E':8,'KEY_F':9,
    'KEY_G':10,'KEY_H':11,'KEY_I':12,'KEY_J':13,'KEY_K':14,'KEY_L':15,
    'KEY_M':16,'KEY_N':17,'KEY_O':18,'KEY_P':19,'KEY_Q':20,'KEY_R':21,
    'KEY_S':22,'KEY_T':23,'KEY_U':24,'KEY_V':25,'KEY_W':26,'KEY_X':27,
    'KEY_Y':28,'KEY_Z':29,
    'KEY_1':30,'KEY_2':31,'KEY_3':32,'KEY_4':33,'KEY_5':34,
    'KEY_6':35,'KEY_7':36,'KEY_8':37,'KEY_9':38,'KEY_0':39,
    'KEY_ENTER':40,'KEY_ESC':41,'KEY_BACKSPACE':42,'KEY_TAB':43,
    'KEY_SPACE':44,'KEY_LEFT':80,'KEY_RIGHT':79,'KEY_UP':82,'KEY_DOWN':81,
    'KEY_LSHIFT':225,'KEY_RSHIFT':229,
    'KEY_F1':58,'KEY_F2':59,'KEY_F3':60,'KEY_F4':61,
}

FONT_ROWS = {
    ' ':["     ","     ","     ","     ","     "],
    '!':["  X  ","  X  ","  X  ","     ","  X  "],
    '"':[" X X "," X X ","     ","     ","     "],
    '#':[" X X ","XXXXX"," X X ","XXXXX"," X X "],
    '$':[" XXXX","X X  "," XXX ","  X X","XXXX "],
    '%':["X   X","   X ","  X  "," X   ","X   X"],
    '&':[" XX  ","X  X ","X XX ","X  X "," XX X"],
    "'":[" X   "," X   ","     ","     ","     "],
    '(':["  XX "," X   "," X   "," X   ","  XX "],
    ')':["XX   ","   X ","   X ","   X ","XX   "],
    '*':["     ","X X X"," XXX ","X X X","     "],
    '+':["     ","  X  ","XXXXX","  X  ","     "],
    ',':["     ","     ","     ","  X  "," X   "],
    '-':["     ","     ","XXXXX","     ","     "],
    '.':["     ","     ","     ","     ","  X  "],
    '/':["    X","   X ","  X  "," X   ","X    "],
    '0':[" XXX ","X   X","X   X","X   X"," XXX "],
    '1':["  X  "," XX  ","  X  ","  X  "," XXX "],
    '2':[" XXX ","X   X","  XX "," X   ","XXXXX"],
    '3':["XXXX ","    X"," XXX ","    X","XXXX "],
    '4':["   X ","  XX "," X X ","XXXXX","   X "],
    '5':["XXXXX","X    ","XXXX ","    X","XXXX "],
    '6':[" XXX ","X    ","XXXX ","X   X"," XXX "],
    '7':["XXXXX","    X","   X ","  X  ","  X  "],
    '8':[" XXX ","X   X"," XXX ","X   X"," XXX "],
    '9':[" XXX ","X   X"," XXXX","    X"," XXX "],
    ':':["     ","  X  ","     ","  X  ","     "],
    ';':["     ","  X  ","     ","  X  "," X   "],
    '<':["   X ","  X  "," X   ","  X  ","   X "],
    '=':["     ","XXXXX","     ","XXXXX","     "],
    '>':["X    "," X   ","  X  "," X   ","X    "],
    '?':[" XXX ","X   X","  XX ","     ","  X  "],
    '@':[" XXX ","X   X","X XXX","X    "," XXX "],
    'A':[" XXX ","X   X","XXXXX","X   X","X   X"],
    'B':["XXXX ","X   X","XXXX ","X   X","XXXX "],
    'C':[" XXX ","X   X","X    ","X   X"," XXX "],
    'D':["XXXX ","X   X","X   X","X   X","XXXX "],
    'E':["XXXXX","X    ","XXX  ","X    ","XXXXX"],
    'F':["XXXXX","X    ","XXX  ","X    ","X    "],
    'G':[" XXX ","X    ","X  XX","X   X"," XXX "],
    'H':["X   X","X   X","XXXXX","X   X","X   X"],
    'I':[" XXX ","  X  ","  X  ","  X  "," XXX "],
    'J':["  XXX","   X ","   X ","X  X "," XX  "],
    'K':["X   X","X  X ","XX   ","X  X ","X   X"],
    'L':["X    ","X    ","X    ","X    ","XXXXX"],
    'M':["X   X","XX XX","X X X","X   X","X   X"],
    'N':["X   X","XX  X","X X X","X  XX","X   X"],
    'O':[" XXX ","X   X","X   X","X   X"," XXX "],
    'P':["XXXX ","X   X","XXXX ","X    ","X    "],
    'Q':[" XXX ","X   X","X X X","X  XX"," XXXX"],
    'R':["XXXX ","X   X","XXXX ","X  X ","X   X"],
    'S':[" XXXX","X    "," XXX ","    X","XXXX "],
    'T':["XXXXX","  X  ","  X  ","  X  ","  X  "],
    'U':["X   X","X   X","X   X","X   X"," XXX "],
    'V':["X   X","X   X","X   X"," X X ","  X  "],
    'W':["X   X","X   X","X X X","XX XX","X   X"],
    'X':["X   X"," X X ","  X  "," X X ","X   X"],
    'Y':["X   X"," X X ","  X  ","  X  ","  X  "],
    'Z':["XXXXX","   X ","  X  "," X   ","XXXXX"],
    '[':["  XX "," X   "," X   "," X   ","  XX "],
}

def char_to_cols(rows):
    cols = []
    for c in range(5):
        val = 0
        for r in range(5):
            row = rows[r] if r < len(rows) else "     "
            px = 1 if c < len(row) and row[c] == 'X' else 0
            val |= px << (4 - r)
        cols.append(val)
    return cols

def make_font_dw():
    lines = []
    for code in range(32, 92):
        ch = chr(code)
        rows = FONT_ROWS.get(ch, FONT_ROWS[' '])
        cols = char_to_cols(rows)
        lines.append('.dw ' + ' '.join(f'0x{v:02X}' for v in cols))
    return lines


INT_TO_STR_ASM = """; --- int to string converter ---
__int_to_str:
    push r2
    push r3
    push r4
    push r5
    push r6
    mov r6 r2
    cmpr r1 r0
    jnz its_nonzero
    ldi r5 1
    stind r5 r2
    inc r2
    inc r2
    ldi r5 48
    stind r5 r2
    mov r1 r6
    jmp its_done
its_nonzero:
    ldi r5 0x7FE0
    ldi r4 0
its_extract:
    cmpr r1 r0
    jz its_extracted
    ldi r3 10
    mod r3 r1 r3
    ldi r2 48
    add r3 r3 r2
    stind r3 r5
    inc r5
    inc r5
    inc r4
    ldi r3 10
    div r1 r1 r3
    jmp its_extract
its_extracted:
    mov r2 r6
    stind r4 r2
    inc r2
    inc r2
    dec r5
    dec r5
its_copy:
    ldind r3 r5
    stind r3 r2
    inc r2
    inc r2
    dec r5
    dec r5
    dec r4
    jnz its_copy
    mov r1 r6
its_done:
    pop r6
    pop r5
    pop r4
    pop r3
    pop r2
    ret
"""

TEXT_RENDERER_ASM = """; --- text renderer ---
__text_renderer:
    push r1
    push r2
    push r3
    push r4
    push r5
    push r6
    push r7
    push r8
    push r9
    push r10
    push r11
    push r12
    push r13
    push r14
    ld r1 0x7FF0
    ld r2 0x7FF2
    ld r3 0x7FF4
    ld r4 0x7FF6
    ldind r5 r1
    inc r1
    inc r1
    ldi r6 0
__tr_char:
    cmpr r6 r5
    jge __tr_done
    ldind r7 r1
    inc r1
    inc r1
    ldi r8 97
    cmpr r7 r8
    jc __tr_no_lower
    ldi r8 32
    sub r7 r7 r8
__tr_no_lower:
    ldi r8 32
    sub r7 r7 r8
    ldi r8 59
    cmpr r7 r8
    jle __tr_in_range
    ldi r7 0
__tr_in_range:
    ldi r8 10
    mul r9 r7 r8
    ldi r8 __font_data
    add r9 r9 r8
    ldi r10 0
__tr_col:
    ldi r11 2
    mul r11 r10 r11
    add r11 r11 r9
    ldind r11 r11
    ldi r12 0
__tr_row:
    ldi r13 4
    sub r13 r13 r12
    ldi r14 1
    shl r14 r14 r13
    gand r14 r14 r11
    cmpr r14 r0
    jz __tr_no_px
    ldi r14 128
    add r13 r3 r12
    mul r13 r13 r14
    add r14 r2 r10
    add r13 r13 r14
    pixel r4 r13
__tr_no_px:
    inc r12
    ldi r13 5
    cmpr r12 r13
    jnz __tr_row
    inc r10
    ldi r13 5
    cmpr r10 r13
    jnz __tr_col
    ldi r13 6
    add r2 r2 r13
    inc r6
    jmp __tr_char
__tr_done:
    pop r14
    pop r13
    pop r12
    pop r11
    pop r10
    pop r9
    pop r8
    pop r7
    pop r6
    pop r5
    pop r4
    pop r3
    pop r2
    pop r1
    ret
"""

# Frame layout in RAM:
#   0x4FFC  FRAME_PTR   — base of the current call's frame
#   0x4FFE  FRAME_ALLOC — next free byte in frame area (grows upward)
#   0x5000+ frame area  — each call allocates N*2 bytes here for its params
#
# On every call:
#   - old FRAME_PTR is pushed to the hardware stack
#   - FRAME_ALLOC becomes the new FRAME_PTR
#   - args are written at [FRAME_PTR+0], [FRAME_PTR+2], ...
#   - FRAME_ALLOC is bumped past them
#
# On return:
#   - FRAME_ALLOC is reset to FRAME_PTR (free our frame)
#   - old FRAME_PTR is popped and restored
#
# This means every recursive call has its own independent param slots.

FRAME_PTR   = 0x4FFC
FRAME_ALLOC = 0x4FFE
FRAME_BASE  = 0x5000

TOKEN_TYPES = [
    ('NUMBER',   r'0x[0-9a-fA-F]+|0b[01]+|\d+'),
    ('STRING',   r'"[^"]*"'),
    ('IDENT',    r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LE',       r'<='),('GE',r'>='),('EQ',r'=='),('NEQ',r'!='),
    ('ASSIGN',   r'='),('PLUS',r'\+'),('MINUS',r'-'),
    ('STAR',     r'\*'),('SLASH',r'/'),('PERCENT',r'%'),
    ('LT',       r'<'),('GT',r'>'),
    ('LPAREN',   r'\('),('RPAREN',r'\)'),
    ('LBRACE',   r'\{'),('RBRACE',r'\}'),
    ('LBRACKET', r'\['),('RBRACKET',r'\]'),
    ('COMMA',    r','),
    ('SKIP',     r'[ \t\r\n]+'),
    ('COMMENT',  r'#[^\n]*'),
]

def tokenize(source):
    source = source.replace('\u2018',"'").replace('\u2019',"'")
    source = source.replace('\u201c','"').replace('\u201d','"')
    source = source.replace('\uff5b','{').replace('\uff5d','}')
    source = source.replace('{',' { ').replace('}',' } ')
    tokens = []
    pos = 0
    line = 1
    while pos < len(source):
        matched = False
        for typ, pattern in TOKEN_TYPES:
            m = re.match(pattern, source[pos:])
            if m:
                if typ == 'SKIP': line += m.group().count('\n')
                elif typ != 'COMMENT': tokens.append((typ, m.group(), line))
                pos += m.end()
                matched = True
                break
        if not matched:
            raise SyntaxError(f"line {line}: unknown character {source[pos]!r}")
    tokens.append(('EOF','',line))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self): return self.tokens[self.pos]

    def consume(self, typ=None):
        tok = self.tokens[self.pos]
        if typ and tok[0] != typ:
            raise SyntaxError(f"line {tok[2]}: expected {typ}, got {tok[1]!r}")
        self.pos += 1
        return tok

    def parse_program(self):
        stmts = []
        while self.peek()[0] != 'EOF':
            if self.peek()[0] == 'IDENT' and self.peek()[1] == 'func':
                stmts.append(self.parse_func())
            else:
                stmts.append(self.parse_stmt())
        return ('program', stmts)

    def parse_func(self):
        self.consume('IDENT')
        name = self.consume('IDENT')[1]
        self.consume('LPAREN')
        params = []
        if self.peek()[0] != 'RPAREN':
            params.append(self.consume('IDENT')[1])
            while self.peek()[0] == 'COMMA':
                self.consume('COMMA')
                params.append(self.consume('IDENT')[1])
        self.consume('RPAREN')
        self.consume('LBRACE')
        body = []
        while self.peek()[0] != 'RBRACE':
            body.append(self.parse_stmt())
        self.consume('RBRACE')
        return ('func', name, params, body)

    def parse_stmt(self):
        tok = self.peek()
        if tok[0] == 'IDENT' and tok[1] == 'var':    return self.parse_var_decl()
        if tok[0] == 'IDENT' and tok[1] == 'if':     return self.parse_if()
        if tok[0] == 'IDENT' and tok[1] == 'while':  return self.parse_while()
        if tok[0] == 'IDENT' and tok[1] == 'return': return self.parse_return()
        if tok[0] == 'IDENT' and tok[1] in ('pixel','vsync','halt','text','sound'):
            return self.parse_builtin_stmt()
        if tok[0] == 'IDENT':
            name = self.consume('IDENT')[1]
            if self.peek()[0] == 'LPAREN':
                self.consume('LPAREN')
                args = []
                if self.peek()[0] != 'RPAREN':
                    args.append(self.parse_expr())
                    while self.peek()[0] == 'COMMA':
                        self.consume('COMMA')
                        args.append(self.parse_expr())
                self.consume('RPAREN')
                return ('call_stmt', name, args)
            if self.peek()[0] == 'LBRACKET':
                self.consume('LBRACKET')
                idx = self.parse_expr()
                self.consume('RBRACKET')
                self.consume('ASSIGN')
                return ('list_set', name, idx, self.parse_expr())
            self.consume('ASSIGN')
            return ('assign', name, self.parse_expr())
        raise SyntaxError(f"line {tok[2]}: unexpected {tok[1]!r}")

    def parse_return(self):
        self.consume('IDENT')
        if self.peek()[0] in ('NUMBER','STRING','IDENT','LPAREN','MINUS'):
            return ('return', self.parse_expr())
        return ('return', None)

    def parse_var_decl(self):
        self.consume('IDENT')
        name = self.consume('IDENT')[1]
        self.consume('ASSIGN')
        if self.peek()[0] == 'IDENT' and self.peek()[1] == 'list':
            self.consume('IDENT')
            self.consume('LPAREN')
            size = int(self.consume('NUMBER')[1])
            self.consume('RPAREN')
            return ('var_list', name, size)
        return ('var_init', name, self.parse_expr())

    def parse_if(self):
        self.consume('IDENT')
        cond = self.parse_cond()
        self.consume('LBRACE')
        body = []
        while self.peek()[0] != 'RBRACE': body.append(self.parse_stmt())
        self.consume('RBRACE')
        else_body = []
        if self.peek()[0] == 'IDENT' and self.peek()[1] == 'else':
            self.consume('IDENT')
            self.consume('LBRACE')
            while self.peek()[0] != 'RBRACE': else_body.append(self.parse_stmt())
            self.consume('RBRACE')
        return ('if', cond, body, else_body)

    def parse_while(self):
        self.consume('IDENT')
        cond = self.parse_cond()
        self.consume('LBRACE')
        body = []
        while self.peek()[0] != 'RBRACE': body.append(self.parse_stmt())
        self.consume('RBRACE')
        return ('while', cond, body)

    def parse_builtin_stmt(self):
        name = self.consume('IDENT')[1]
        self.consume('LPAREN')
        args = []
        if self.peek()[0] != 'RPAREN':
            args.append(self.parse_expr())
            while self.peek()[0] == 'COMMA':
                self.consume('COMMA')
                args.append(self.parse_expr())
        self.consume('RPAREN')
        return ('builtin', name, args)

    def parse_cond(self):
        left = self.parse_expr()
        tok = self.peek()
        if tok[0] in ('EQ','NEQ','LT','GT','LE','GE'):
            self.consume()
            return ('cmp', tok[0], left, self.parse_expr())
        return ('cmp', 'NEQ', left, ('num', 0))

    def parse_expr(self):  return self.parse_add()

    def parse_add(self):
        left = self.parse_mul()
        while self.peek()[0] in ('PLUS','MINUS'):
            op = self.consume()[0]
            left = ('binop', op, left, self.parse_mul())
        return left

    def parse_mul(self):
        left = self.parse_unary()
        while self.peek()[0] in ('STAR','SLASH','PERCENT'):
            op = self.consume()[0]
            left = ('binop', op, left, self.parse_unary())
        return left

    def parse_unary(self):
        if self.peek()[0] == 'MINUS':
            self.consume()
            return ('neg', self.parse_primary())
        return self.parse_primary()

    def parse_primary(self):
        tok = self.peek()
        if tok[0] == 'NUMBER':
            self.consume()
            v = tok[1]
            if v.startswith(('0x','0X')): return ('num', int(v,16))
            if v.startswith(('0b','0B')): return ('num', int(v,2))
            return ('num', int(v))
        if tok[0] == 'STRING':
            self.consume()
            return ('string_lit', tok[1][1:-1])
        if tok[0] == 'IDENT':
            name = tok[1]
            if name in KEY_CONSTANTS:
                self.consume()
                return ('num', KEY_CONSTANTS[name])
            self.consume()
            if self.peek()[0] == 'LPAREN':
                self.consume('LPAREN')
                args = []
                if self.peek()[0] != 'RPAREN':
                    args.append(self.parse_expr())
                    while self.peek()[0] == 'COMMA':
                        self.consume('COMMA')
                        args.append(self.parse_expr())
                self.consume('RPAREN')
                return ('call', name, args)
            if self.peek()[0] == 'LBRACKET':
                self.consume('LBRACKET')
                idx = self.parse_expr()
                self.consume('RBRACKET')
                return ('list_get', name, idx)
            return ('var_ref', name)
        if tok[0] == 'LPAREN':
            self.consume()
            e = self.parse_expr()
            self.consume('RPAREN')
            return e
        raise SyntaxError(f"line {tok[2]}: unexpected {tok[1]!r} in expression")

class Compiler:
    def __init__(self):
        self.vars = {}
        self.next_var = 0x8000
        self.label_n = 0
        self.out = []
        self.str_data = []
        self.strings = {}
        self.reg = 0
        self.uses_text = False
        self.str_buf_next = 0x7F00
        self.func_defs = {}
        self.current_epilogue = None
        self.in_func = False

    def emit(self, s):    self.out.append(s)
    def label(self):
        self.label_n += 1
        return f'__L{self.label_n}'

    def alloc_var(self, name):
        self.vars[name] = self.next_var
        self.next_var += 2
        return self.vars[name]

    def alloc_reg(self):
        self.reg += 1
        if self.reg > 12:
            raise RuntimeError("expression too complex — use intermediate variables")
        return self.reg

    def free_reg(self): self.reg -= 1
    def reset_regs(self): self.reg = 0

    def intern_str(self, s):
        if s not in self.strings:
            label = f'__str_{len(self.strings)}'
            self.strings[s] = label
            self.str_data.append(f'{label}:')
            self.str_data.append(f'.dw {len(s)}')
            for ch in s:
                self.str_data.append(f'.dw {ord(ch)}')
        return self.strings[s]

    def emit_load_param(self, slot, r_dst):
        """Load param at frame slot i into r_dst using FRAME_PTR."""
        rt = self.alloc_reg()
        self.emit(f'    ld r{rt} {FRAME_PTR:#06x}')
        if slot == 0:
            self.emit(f'    ldind r{r_dst} r{rt}')
        else:
            ro = self.alloc_reg()
            self.emit(f'    ldi r{ro} {2 * slot}')
            self.emit(f'    add r{rt} r{rt} r{ro}')
            self.emit(f'    ldind r{r_dst} r{rt}')
            self.free_reg()
        self.free_reg()

    def emit_store_param(self, slot, r_val):
        """Store r_val into frame slot i using FRAME_PTR."""
        rt = self.alloc_reg()
        self.emit(f'    ld r{rt} {FRAME_PTR:#06x}')
        if slot == 0:
            self.emit(f'    stind r{r_val} r{rt}')
        else:
            ro = self.alloc_reg()
            self.emit(f'    ldi r{ro} {2 * slot}')
            self.emit(f'    add r{rt} r{rt} r{ro}')
            self.emit(f'    stind r{r_val} r{rt}')
            self.free_reg()
        self.free_reg()

    def compile_func_def(self, name, params, body_stmts):
        label    = f'__func_{name}'
        epilogue = f'__func_{name}_ep'
        n        = len(params)

        if n > 12:
            raise RuntimeError(f"function '{name}': too many parameters (max 12)")

        saved_out      = self.out
        saved_vars     = self.vars
        saved_reg      = self.reg
        saved_epilogue = self.current_epilogue
        saved_in_func  = self.in_func

        self.out           = []
        self.reg           = 0
        self.current_epilogue = epilogue
        self.in_func       = True

        # Function scope: global vars remain visible; params are frame-relative.
        self.vars = dict(saved_vars)
        for i, p in enumerate(params):
            self.vars[p] = ('frame', i)

        self.emit(f'{label}:')

        # Prologue:
        # 1. Save old FRAME_PTR on hardware stack (so we can restore it on exit).
        self.emit(f'    ld r14 {FRAME_PTR:#06x}')
        self.emit(f'    push r14')
        # 2. FRAME_ALLOC is our new frame base. Publish it as FRAME_PTR.
        self.emit(f'    ld r14 {FRAME_ALLOC:#06x}')
        self.emit(f'    st r14 {FRAME_PTR:#06x}')
        # 3. Store incoming args into our frame slots.
        if n >= 1:
            self.emit(f'    stind r1 r14')
        for i in range(1, n):
            self.emit(f'    ldi r13 {2 * i}')
            self.emit(f'    add r13 r14 r13')
            self.emit(f'    stind r{i + 1} r13')
        # 4. Bump the allocator past our frame.
        if n > 0:
            self.emit(f'    ldi r13 {n * 2}')
            self.emit(f'    add r13 r14 r13')
            self.emit(f'    st r13 {FRAME_ALLOC:#06x}')

        for s in body_stmts:
            self.stmt(s)

        # Epilogue: free our frame, restore caller's FRAME_PTR, return.
        self.emit(f'{epilogue}:')
        self.emit(f'    ld r14 {FRAME_PTR:#06x}')
        self.emit(f'    st r14 {FRAME_ALLOC:#06x}')
        self.emit(f'    pop r14')
        self.emit(f'    st r14 {FRAME_PTR:#06x}')
        self.emit('    ret')

        block = list(self.out)

        self.out           = saved_out
        self.vars          = saved_vars
        self.reg           = saved_reg
        self.current_epilogue = saved_epilogue
        self.in_func       = saved_in_func
        return block

    def expr(self, node):
        k = node[0]
        if k == 'num':
            r = self.alloc_reg()
            self.emit(f'    ldi r{r} {node[1]}')
            return r
        if k == 'var_ref':
            name = node[1]
            info = self.vars.get(name)
            if info is None:
                raise NameError(f"undefined variable: {name!r}")
            r = self.alloc_reg()
            if isinstance(info, tuple):
                self.emit_load_param(info[1], r)
            else:
                self.emit(f'    ld r{r} {info:#06x}')
            return r
        if k == 'neg':
            r = self.expr(node[1])
            self.emit(f'    neg r{r}')
            return r
        if k == 'binop':
            _, op, left, right = node
            rl = self.expr(left)
            rr = self.expr(right)
            mn = {'PLUS':'add','MINUS':'sub','STAR':'mul','SLASH':'div','PERCENT':'mod'}[op]
            self.emit(f'    {mn} r{rl} r{rl} r{rr}')
            self.free_reg()
            return rl
        if k == 'string_lit':
            label = self.intern_str(node[1])
            r = self.alloc_reg()
            self.emit(f'    ldi r{r} {label}')
            return r
        if k == 'list_get':
            name, idx_node = node[1], node[2]
            info = self.vars.get(name)
            if info is None: raise NameError(f"undefined variable: {name!r}")
            rb = self.alloc_reg()
            self.emit(f'    ld r{rb} {info:#06x}')
            ri = self.expr(idx_node)
            rt = self.alloc_reg()
            self.emit(f'    ldi r{rt} 2')
            self.emit(f'    mul r{ri} r{ri} r{rt}')
            self.emit(f'    add r{rb} r{rb} r{ri}')
            self.emit(f'    ldind r{rb} r{rb}')
            self.free_reg()
            self.free_reg()
            return rb
        if k == 'call':
            name, args = node[1], node[2]

            if name == 'key':
                if len(args) != 1: raise TypeError("key(scancode) takes 1 argument")
                r = self.expr(args[0])
                r2 = self.alloc_reg()
                self.emit(f'    ldi r{r2} 0xFF00')
                self.emit(f'    add r{r} r{r} r{r2}')
                self.emit(f'    ldind r{r} r{r}')
                self.emit(f'    ldi r{r2} 0x00FF')
                self.emit(f'    gand r{r} r{r} r{r2}')
                self.free_reg()
                return r

            if name == 'timer':
                if len(args) != 0: raise TypeError("timer() takes no arguments")
                r = self.alloc_reg()
                self.emit(f'    ld r{r} 0xFEF2')
                return r

            if name == 'random':
                if len(args) != 0: raise TypeError("random() takes no arguments")
                r = self.alloc_reg()
                self.emit(f'    ld r{r} 0xFEF4')
                return r

            if name == 'str':
                if len(args) != 1: raise TypeError("str(n) takes 1 argument")
                self.uses_text = True
                buf_addr = self.str_buf_next
                self.str_buf_next += 14
                r = self.expr(args[0])
                self.emit(f'    mov r1 r{r}')
                self.emit(f'    ldi r2 {buf_addr:#06x}')
                self.emit(f'    call __int_to_str')
                rd = self.alloc_reg()
                self.emit(f'    mov r{rd} r1')
                if r != 1: self.free_reg()
                return rd

            if name in self.func_defs:
                fd = self.func_defs[name]
                nparams = len(fd['params'])
                if len(args) != nparams:
                    raise TypeError(f"'{name}' expects {nparams} argument(s), got {len(args)}")

                # Caller-save: push any live registers so the callee doesn't clobber them.
                live = self.reg
                for i in range(1, live + 1):
                    self.emit(f'    push r{i}')

                # Evaluate args fresh — sequential alloc puts arg0→r1, arg1→r2, etc.
                self.reg = 0
                for arg in args:
                    self.expr(arg)

                self.emit(f'    call {fd["label"]}')

                # Move return value (r1) to the next free slot before restoring.
                self.reg = live
                rd = self.alloc_reg()
                if rd != 1:
                    self.emit(f'    mov r{rd} r1')

                for i in range(live, 0, -1):
                    self.emit(f'    pop r{i}')

                return rd

            raise NameError(f"unknown function: {name!r}")
        raise RuntimeError(f"unknown expr node: {k}")

    def cond_jump(self, cond, lbl_false):
        self.reset_regs()
        _, op, left, right = cond
        rl = self.expr(left)
        rr = self.expr(right)
        self.emit(f'    cmpr r{rl} r{rr}')
        if   op == 'EQ':  self.emit(f'    jnz {lbl_false}')
        elif op == 'NEQ': self.emit(f'    jz {lbl_false}')
        elif op == 'LT':  self.emit(f'    jge {lbl_false}')
        elif op == 'GE':  self.emit(f'    jc {lbl_false}')
        elif op == 'GT':  self.emit(f'    jle {lbl_false}')
        elif op == 'LE':
            lok = self.label()
            self.emit(f'    jle {lok}')
            self.emit(f'    jmp {lbl_false}')
            self.emit(f'{lok}:')

    def stmt(self, node):
        k = node[0]
        if k == 'var_init':
            addr = self.alloc_var(node[1])
            self.reset_regs()
            r = self.expr(node[2])
            self.emit(f'    st r{r} {addr:#06x}')
        elif k == 'var_list':
            _, name, size = node
            ptr = self.alloc_var(name)
            data = self.next_var
            self.next_var += size * 2
            self.emit(f'    ldi r1 {data:#06x}')
            self.emit(f'    st r1 {ptr:#06x}')
        elif k == 'assign':
            name = node[1]
            self.reset_regs()
            r = self.expr(node[2])
            info = self.vars.get(name)
            if info is None:
                raise NameError(f"undefined variable: {name!r}")
            if isinstance(info, tuple):
                self.emit_store_param(info[1], r)
            else:
                self.emit(f'    st r{r} {info:#06x}')
        elif k == 'list_set':
            _, name, idx_node, val_node = node
            info = self.vars.get(name)
            if info is None: raise NameError(f"undefined variable: {name!r}")
            self.reset_regs()
            rb = self.alloc_reg()
            self.emit(f'    ld r{rb} {info:#06x}')
            ri = self.expr(idx_node)
            rt = self.alloc_reg()
            self.emit(f'    ldi r{rt} 2')
            self.emit(f'    mul r{ri} r{ri} r{rt}')
            self.emit(f'    add r{rb} r{rb} r{ri}')
            rv = self.expr(val_node)
            self.emit(f'    stind r{rv} r{rb}')
        elif k == 'if':
            _, cond, body, else_body = node
            lf = self.label()
            le = self.label()
            self.cond_jump(cond, lf)
            for s in body: self.stmt(s)
            if else_body: self.emit(f'    jmp {le}')
            self.emit(f'{lf}:')
            for s in else_body: self.stmt(s)
            if else_body: self.emit(f'{le}:')
        elif k == 'while':
            _, cond, body = node
            lt = self.label()
            le = self.label()
            self.emit(f'{lt}:')
            self.cond_jump(cond, le)
            for s in body: self.stmt(s)
            self.emit(f'    jmp {lt}')
            self.emit(f'{le}:')
        elif k == 'call_stmt':
            _, name, args = node
            self.reset_regs()
            self.expr(('call', name, args))
            self.reset_regs()
        elif k == 'return':
            if self.current_epilogue is None:
                raise RuntimeError("'return' used outside of a function")
            self.reset_regs()
            if node[1] is not None:
                r = self.expr(node[1])
                if r != 1: self.emit(f'    mov r1 r{r}')
            self.emit(f'    jmp {self.current_epilogue}')
        elif k == 'builtin':
            _, name, args = node
            self.reset_regs()
            if name == 'vsync':
                self.emit('    vsync')
            elif name == 'halt':
                self.emit('    halt')
            elif name == 'pixel':
                if len(args) != 2: raise TypeError("pixel(color, address)")
                rc = self.expr(args[0])
                ra = self.expr(args[1])
                self.emit(f'    pixel r{rc} r{ra}')
            elif name == 'text':
                if len(args) != 4: raise TypeError("text(string, x, y, color)")
                self.uses_text = True
                r = self.expr(args[0]); self.emit(f'    st r{r} 0x7FF0')
                self.reset_regs()
                r = self.expr(args[1]); self.emit(f'    st r{r} 0x7FF2')
                self.reset_regs()
                r = self.expr(args[2]); self.emit(f'    st r{r} 0x7FF4')
                self.reset_regs()
                r = self.expr(args[3]); self.emit(f'    st r{r} 0x7FF6')
                self.emit('    call __text_renderer')
            elif name == 'sound':
                if len(args) != 1: raise TypeError("sound(freq) takes 1 argument")
                r = self.expr(args[0])
                self.emit(f'    st r{r} 0xFEF0')
            else:
                raise NameError(f"unknown builtin: {name!r}")

    def compile(self, ast):
        _, stmts = ast

        for s in stmts:
            if s[0] == 'func':
                _, name, params, _ = s
                if name in self.func_defs:
                    raise NameError(f"function '{name}' defined more than once")
                self.func_defs[name] = {'params': params, 'label': f'__func_{name}'}

        for s in stmts:
            if s[0] != 'func':
                self.stmt(s)

        func_blocks = []
        for s in stmts:
            if s[0] == 'func':
                _, name, params, body = s
                func_blocks.append(self.compile_func_def(name, params, body))

        lines = ['; compiled by viper / ybmc']
        needs_preamble = self.uses_text or bool(self.strings) or bool(func_blocks)

        if needs_preamble:
            lines.append('    jmp __start')
            if self.uses_text or bool(self.strings):
                lines.append('__font_data:')
                lines.extend(make_font_dw())
                lines.append(TEXT_RENDERER_ASM)
                lines.append(INT_TO_STR_ASM)
            for block in func_blocks:
                lines.extend(block)
            if self.str_data:
                lines.append('; --- string data ---')
                lines.extend(self.str_data)
            lines.append('__start:')

        if func_blocks:
            lines.append(f'    ldi r1 {FRAME_BASE:#06x}')
            lines.append(f'    st r1 {FRAME_ALLOC:#06x}')
            lines.append(f'    st r1 {FRAME_PTR:#06x}')

        lines.extend(self.out)
        lines.append('    halt')

        return '\n'.join(lines)

if len(sys.argv) < 3:
    print("usage: python ybmc.py input.ybm output.asm")
    sys.exit(1)

with open(sys.argv[1]) as f:
    source = f.read()

try:
    tokens = tokenize(source)
    ast = Parser(tokens).parse_program()
    asm = Compiler().compile(ast)
    with open(sys.argv[2], 'w') as f:
        f.write(asm)
    print(f"compiled {sys.argv[1]} -> {sys.argv[2]}")
except (SyntaxError, NameError, TypeError, RuntimeError) as e:
    print(f"error: {e}")
    sys.exit(1)
