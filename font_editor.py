import tkinter as tk
from tkinter import messagebox, filedialog
import os

# ── Constants ─────────────────────────────────────────────────────────────────
CHAR_COUNT   = 128       # ASCII 0–127
CHAR_W       = 8
CHAR_H       = 8
CELL_SIZE    = 40        # pixels per bit cell in the editor grid
PREVIEW_SCALE = 3        # scale for the preview panel characters
COLS         = 16        # characters per row in the charset overview
ROWS         = 8

# Colours
BG           = "#0a0f0c"
BG2          = "#0d1510"
PANEL        = "#101a14"
BORDER       = "#1a3328"
BORDER2      = "#224433"
GREEN        = "#00e676"
GREEN2       = "#00c853"
GREEN_DIM    = "#00e67620"
TEXT         = "#c8e6c9"
TEXT_DIM     = "#6a9b7a"
TEXT_MUTE    = "#3a5a48"
AMBER        = "#ffb300"
PIXEL_ON     = "#00e676"
PIXEL_OFF    = "#0d1a13"
PIXEL_HOVER  = "#005533"

# ── Font data ─────────────────────────────────────────────────────────────────
# 128 characters × 8 rows × 8 bits, stored as list of lists of lists
font_data = [[[0]*CHAR_W for _ in range(CHAR_H)] for _ in range(CHAR_COUNT)]

# Seed some basic ASCII characters so the editor isn't totally blank
BUILTIN = {
    ord('A'): [0x3C,0x42,0x42,0x7E,0x42,0x42,0x42,0x00],
    ord('B'): [0x7C,0x42,0x42,0x7C,0x42,0x42,0x7C,0x00],
    ord('C'): [0x3C,0x42,0x40,0x40,0x40,0x42,0x3C,0x00],
    ord('D'): [0x78,0x44,0x42,0x42,0x42,0x44,0x78,0x00],
    ord('E'): [0x7E,0x40,0x40,0x7C,0x40,0x40,0x7E,0x00],
    ord('F'): [0x7E,0x40,0x40,0x7C,0x40,0x40,0x40,0x00],
    ord('G'): [0x3C,0x42,0x40,0x4E,0x42,0x42,0x3C,0x00],
    ord('H'): [0x42,0x42,0x42,0x7E,0x42,0x42,0x42,0x00],
    ord('I'): [0x7E,0x18,0x18,0x18,0x18,0x18,0x7E,0x00],
    ord('J'): [0x1E,0x06,0x06,0x06,0x06,0x46,0x3C,0x00],
    ord('K'): [0x42,0x44,0x48,0x70,0x48,0x44,0x42,0x00],
    ord('L'): [0x40,0x40,0x40,0x40,0x40,0x40,0x7E,0x00],
    ord('M'): [0x42,0x66,0x5A,0x42,0x42,0x42,0x42,0x00],
    ord('N'): [0x42,0x62,0x52,0x4A,0x46,0x42,0x42,0x00],
    ord('O'): [0x3C,0x42,0x42,0x42,0x42,0x42,0x3C,0x00],
    ord('P'): [0x7C,0x42,0x42,0x7C,0x40,0x40,0x40,0x00],
    ord('Q'): [0x3C,0x42,0x42,0x42,0x4A,0x44,0x3A,0x00],
    ord('R'): [0x7C,0x42,0x42,0x7C,0x48,0x44,0x42,0x00],
    ord('S'): [0x3C,0x42,0x40,0x3C,0x02,0x42,0x3C,0x00],
    ord('T'): [0x7E,0x18,0x18,0x18,0x18,0x18,0x18,0x00],
    ord('U'): [0x42,0x42,0x42,0x42,0x42,0x42,0x3C,0x00],
    ord('V'): [0x42,0x42,0x42,0x42,0x42,0x24,0x18,0x00],
    ord('W'): [0x42,0x42,0x42,0x42,0x5A,0x66,0x42,0x00],
    ord('X'): [0x42,0x42,0x24,0x18,0x24,0x42,0x42,0x00],
    ord('Y'): [0x42,0x42,0x24,0x18,0x18,0x18,0x18,0x00],
    ord('Z'): [0x7E,0x02,0x04,0x18,0x20,0x40,0x7E,0x00],
    ord('0'): [0x3C,0x42,0x46,0x4A,0x52,0x62,0x3C,0x00],
    ord('1'): [0x18,0x28,0x08,0x08,0x08,0x08,0x3E,0x00],
    ord('2'): [0x3C,0x42,0x02,0x0C,0x30,0x40,0x7E,0x00],
    ord('3'): [0x3C,0x42,0x02,0x1C,0x02,0x42,0x3C,0x00],
    ord('4'): [0x04,0x0C,0x14,0x24,0x7E,0x04,0x04,0x00],
    ord('5'): [0x7E,0x40,0x7C,0x02,0x02,0x42,0x3C,0x00],
    ord('6'): [0x1C,0x20,0x40,0x7C,0x42,0x42,0x3C,0x00],
    ord('7'): [0x7E,0x02,0x04,0x08,0x10,0x10,0x10,0x00],
    ord('8'): [0x3C,0x42,0x42,0x3C,0x42,0x42,0x3C,0x00],
    ord('9'): [0x3C,0x42,0x42,0x3E,0x02,0x04,0x38,0x00],
    ord(' '): [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],
    ord('.'): [0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x00],
    ord('!'): [0x18,0x18,0x18,0x18,0x18,0x00,0x18,0x00],
    ord('?'): [0x3C,0x42,0x02,0x0C,0x18,0x00,0x18,0x00],
    ord(':'): [0x00,0x18,0x18,0x00,0x18,0x18,0x00,0x00],
    ord('-'): [0x00,0x00,0x00,0x7E,0x00,0x00,0x00,0x00],
    ord('+'): [0x00,0x18,0x18,0x7E,0x18,0x18,0x00,0x00],
    ord('='): [0x00,0x00,0x7E,0x00,0x7E,0x00,0x00,0x00],
    ord('/'): [0x02,0x04,0x08,0x10,0x20,0x40,0x00,0x00],
    ord('*'): [0x00,0x42,0x24,0x18,0x24,0x42,0x00,0x00],
    ord(','): [0x00,0x00,0x00,0x00,0x18,0x18,0x08,0x10],
    ord(';'): [0x00,0x18,0x18,0x00,0x18,0x18,0x08,0x10],
    ord('('): [0x08,0x10,0x20,0x20,0x20,0x10,0x08,0x00],
    ord(')'): [0x20,0x10,0x08,0x08,0x08,0x10,0x20,0x00],
    ord('_'): [0x00,0x00,0x00,0x00,0x00,0x00,0x7E,0x00],
    ord('#'): [0x24,0x24,0x7E,0x24,0x7E,0x24,0x24,0x00],
    ord('@'): [0x3C,0x42,0x4E,0x52,0x4E,0x40,0x3C,0x00],
    ord('&'): [0x30,0x48,0x48,0x30,0x4A,0x44,0x3A,0x00],
    ord('%'): [0x62,0x64,0x08,0x10,0x26,0x46,0x00,0x00],
    ord('"'): [0x24,0x24,0x24,0x00,0x00,0x00,0x00,0x00],
    ord("'"): [0x18,0x18,0x10,0x20,0x00,0x00,0x00,0x00],
    ord('<'): [0x04,0x08,0x10,0x20,0x10,0x08,0x04,0x00],
    ord('>'): [0x20,0x10,0x08,0x04,0x08,0x10,0x20,0x00],
    ord('['): [0x3C,0x20,0x20,0x20,0x20,0x20,0x3C,0x00],
    ord(']'): [0x3C,0x04,0x04,0x04,0x04,0x04,0x3C,0x00],
    ord('^'): [0x18,0x24,0x42,0x00,0x00,0x00,0x00,0x00],
    ord('~'): [0x00,0x00,0x32,0x4C,0x00,0x00,0x00,0x00],
    ord('`'): [0x10,0x08,0x00,0x00,0x00,0x00,0x00,0x00],
    ord('|'): [0x18,0x18,0x18,0x18,0x18,0x18,0x18,0x00],
    ord('\\'): [0x40,0x20,0x10,0x08,0x04,0x02,0x00,0x00],
    ord('{'): [0x0C,0x10,0x10,0x20,0x10,0x10,0x0C,0x00],
    ord('}'): [0x30,0x08,0x08,0x04,0x08,0x08,0x30,0x00],
}

for char_code, rows in BUILTIN.items():
    for row_idx, byte in enumerate(rows):
        for bit_idx in range(8):
            font_data[char_code][row_idx][7 - bit_idx] = (byte >> bit_idx) & 1


class FontEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("FONT EDITOR — 8x8 BITMAP")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.current_char = ord('A')
        self.drawing = False
        self.draw_value = 1
        self.dirty = False

        self._build_ui()
        self._load_char(self.current_char)
        self._refresh_overview()

    # ── UI construction ────────────────────────────────────────────────────────
    def _build_ui(self):
        # Title bar
        title_frame = tk.Frame(self.root, bg=BG, pady=8)
        title_frame.pack(fill='x', padx=16, pady=(12,0))

        tk.Label(title_frame, text="▶ FONT EDITOR", font=("Courier", 10, "bold"),
                 fg=GREEN, bg=BG).pack(side='left')

        self.status_label = tk.Label(title_frame, text="", font=("Courier", 9),
                                      fg=TEXT_DIM, bg=BG)
        self.status_label.pack(side='right')

        # Separator
        tk.Frame(self.root, bg=BORDER2, height=1).pack(fill='x', padx=0, pady=4)

        # Main layout
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill='both', expand=True, padx=16, pady=8)

        # Left — editor grid + controls
        left = tk.Frame(main, bg=BG)
        left.pack(side='left', padx=(0, 16))

        self._build_char_info(left)
        self._build_grid(left)
        self._build_tools(left)

        # Right — charset overview
        right = tk.Frame(main, bg=BG)
        right.pack(side='left', fill='both')

        self._build_overview(right)
        self._build_file_controls(right)

    def _build_char_info(self, parent):
        frame = tk.Frame(parent, bg=PANEL, bd=0, highlightthickness=1,
                         highlightbackground=BORDER2)
        frame.pack(fill='x', pady=(0, 8))

        inner = tk.Frame(frame, bg=PANEL, padx=12, pady=8)
        inner.pack(fill='x')

        tk.Label(inner, text="EDITING CHARACTER", font=("Courier", 7),
                 fg=TEXT_MUTE, bg=PANEL).pack(anchor='w')

        self.char_display = tk.Label(inner, text="A", font=("Courier", 28, "bold"),
                                      fg=GREEN, bg=PANEL)
        self.char_display.pack(anchor='w')

        self.char_info = tk.Label(inner, text="ASCII 65  |  0x41",
                                   font=("Courier", 9), fg=TEXT_DIM, bg=PANEL)
        self.char_info.pack(anchor='w')

        # Nav buttons
        nav = tk.Frame(inner, bg=PANEL)
        nav.pack(anchor='w', pady=(6,0))

        btn_style = dict(font=("Courier", 9), fg=GREEN, bg=BG2, relief='flat',
                         bd=0, padx=8, pady=4, cursor='hand2',
                         activeforeground=GREEN, activebackground=BORDER2)

        tk.Button(nav, text="◀ PREV", command=self._prev_char, **btn_style).pack(side='left', padx=(0,4))
        tk.Button(nav, text="NEXT ▶", command=self._next_char, **btn_style).pack(side='left')

        # ASCII jump
        jump = tk.Frame(inner, bg=PANEL)
        jump.pack(anchor='w', pady=(6,0))
        tk.Label(jump, text="JUMP TO:", font=("Courier", 8), fg=TEXT_MUTE, bg=PANEL).pack(side='left')
        self.jump_entry = tk.Entry(jump, font=("Courier", 9), fg=GREEN, bg=BG2,
                                    insertbackground=GREEN, relief='flat', width=6,
                                    highlightthickness=1, highlightbackground=BORDER2)
        self.jump_entry.pack(side='left', padx=4)
        self.jump_entry.bind('<Return>', self._jump_to_char)

    def _build_grid(self, parent):
        label = tk.Frame(parent, bg=BG)
        label.pack(anchor='w', pady=(4,2))
        tk.Label(label, text="PIXEL GRID  (click or drag to draw)",
                 font=("Courier", 7), fg=TEXT_MUTE, bg=BG).pack(side='left')

        frame = tk.Frame(parent, bg=BORDER2, bd=1, relief='flat')
        frame.pack()

        self.grid_canvas = tk.Canvas(frame,
                                      width=CHAR_W * CELL_SIZE,
                                      height=CHAR_H * CELL_SIZE,
                                      bg=PIXEL_OFF, highlightthickness=0)
        self.grid_canvas.pack()

        self.cells = []
        for row in range(CHAR_H):
            row_cells = []
            for col in range(CHAR_W):
                x1 = col * CELL_SIZE + 1
                y1 = row * CELL_SIZE + 1
                x2 = x1 + CELL_SIZE - 2
                y2 = y1 + CELL_SIZE - 2
                rect = self.grid_canvas.create_rectangle(x1, y1, x2, y2,
                                                          fill=PIXEL_OFF, outline=BORDER)
                row_cells.append(rect)
            self.cells.append(row_cells)

        self.grid_canvas.bind('<Button-1>',       self._grid_press)
        self.grid_canvas.bind('<B1-Motion>',      self._grid_drag)
        self.grid_canvas.bind('<ButtonRelease-1>',self._grid_release)
        self.grid_canvas.bind('<Motion>',         self._grid_hover)
        self.grid_canvas.bind('<Leave>',          self._grid_unhover)
        self._hover_cell = None

    def _build_tools(self, parent):
        frame = tk.Frame(parent, bg=BG, pady=8)
        frame.pack(fill='x')

        btn_style = dict(font=("Courier", 8), fg=TEXT_DIM, bg=PANEL, relief='flat',
                         bd=0, padx=10, pady=6, cursor='hand2',
                         activeforeground=GREEN, activebackground=BORDER2,
                         highlightthickness=1, highlightbackground=BORDER)

        tk.Button(frame, text="CLEAR", command=self._clear_char, **btn_style).pack(side='left', padx=(0,4))
        tk.Button(frame, text="INVERT", command=self._invert_char, **btn_style).pack(side='left', padx=4)
        tk.Button(frame, text="SHIFT ▲", command=lambda: self._shift('up'), **btn_style).pack(side='left', padx=4)
        tk.Button(frame, text="SHIFT ▼", command=lambda: self._shift('down'), **btn_style).pack(side='left', padx=4)
        tk.Button(frame, text="◀", command=lambda: self._shift('left'), **btn_style).pack(side='left', padx=4)
        tk.Button(frame, text="▶", command=lambda: self._shift('right'), **btn_style).pack(side='left', padx=4)

        # Byte preview
        byte_frame = tk.Frame(parent, bg=PANEL, highlightthickness=1,
                               highlightbackground=BORDER2, padx=12, pady=8)
        byte_frame.pack(fill='x', pady=(4,0))
        tk.Label(byte_frame, text="ROW BYTES (hex)", font=("Courier", 7),
                 fg=TEXT_MUTE, bg=PANEL).pack(anchor='w')
        self.byte_labels = []
        for r in range(CHAR_H):
            lbl = tk.Label(byte_frame, text=f"row {r}: 0x00",
                           font=("Courier", 9), fg=GREEN2, bg=PANEL, anchor='w')
            lbl.pack(anchor='w')
            self.byte_labels.append(lbl)

    def _build_overview(self, parent):
        tk.Label(parent, text="CHARACTER SET OVERVIEW", font=("Courier", 7),
                 fg=TEXT_MUTE, bg=BG).pack(anchor='w', pady=(0,4))

        frame = tk.Frame(parent, bg=BORDER2, bd=1)
        frame.pack()

        cell_px = PREVIEW_SCALE * CHAR_W + 2
        ov_w = COLS * cell_px
        ov_h = ROWS * (PREVIEW_SCALE * CHAR_H + 2)

        self.overview_canvas = tk.Canvas(frame, width=ov_w, height=ov_h,
                                          bg=BG2, highlightthickness=0)
        self.overview_canvas.pack()
        self.overview_canvas.bind('<Button-1>', self._overview_click)
        self.ov_rects = {}   # char_code -> list of pixel rects
        self.ov_sel   = None # selection highlight rect

        for c in range(CHAR_COUNT):
            col = c % COLS
            row = c // COLS
            ox  = col * cell_px
            oy  = row * (PREVIEW_SCALE * CHAR_H + 2)
            rects = []
            for py in range(CHAR_H):
                for px in range(CHAR_W):
                    x1 = ox + px * PREVIEW_SCALE
                    y1 = oy + py * PREVIEW_SCALE
                    r  = self.overview_canvas.create_rectangle(
                        x1, y1, x1+PREVIEW_SCALE, y1+PREVIEW_SCALE,
                        fill=PIXEL_OFF, outline='')
                    rects.append(r)
            self.ov_rects[c] = rects

        # Selection highlight
        self.ov_sel = self.overview_canvas.create_rectangle(0,0,0,0,
                                                             outline=AMBER, fill='',
                                                             width=2)
        self._update_ov_selection()

    def _build_file_controls(self, parent):
        frame = tk.Frame(parent, bg=BG, pady=12)
        frame.pack(fill='x')

        btn_style = dict(font=("Courier", 9, "bold"), relief='flat', bd=0,
                         padx=14, pady=8, cursor='hand2')

        tk.Button(frame, text="SAVE FONT", command=self._save,
                  fg=BG, bg=GREEN2, activebackground=GREEN,
                  activeforeground=BG, **btn_style).pack(side='left', padx=(0,8))

        tk.Button(frame, text="LOAD FONT", command=self._load,
                  fg=GREEN, bg=PANEL, activebackground=BORDER2,
                  activeforeground=GREEN, highlightthickness=1,
                  highlightbackground=BORDER2, **btn_style).pack(side='left')

        self.save_status = tk.Label(parent, text="", font=("Courier", 8),
                                     fg=TEXT_DIM, bg=BG)
        self.save_status.pack(anchor='w')

    # ── Grid interaction ───────────────────────────────────────────────────────
    def _cell_at(self, x, y):
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        if 0 <= col < CHAR_W and 0 <= row < CHAR_H:
            return row, col
        return None

    def _grid_press(self, event):
        pos = self._cell_at(event.x, event.y)
        if pos:
            row, col = pos
            # toggle value becomes opposite of what was there
            self.draw_value = 1 - font_data[self.current_char][row][col]
            self.drawing = True
            self._set_pixel(row, col, self.draw_value)

    def _grid_drag(self, event):
        if self.drawing:
            pos = self._cell_at(event.x, event.y)
            if pos:
                self._set_pixel(pos[0], pos[1], self.draw_value)

    def _grid_release(self, event):
        self.drawing = False

    def _grid_hover(self, event):
        pos = self._cell_at(event.x, event.y)
        if pos != self._hover_cell:
            if self._hover_cell:
                r, c = self._hover_cell
                val = font_data[self.current_char][r][c]
                self.grid_canvas.itemconfig(self.cells[r][c],
                                             fill=PIXEL_ON if val else PIXEL_OFF)
            self._hover_cell = pos
            if pos:
                r, c = pos
                val = font_data[self.current_char][r][c]
                self.grid_canvas.itemconfig(self.cells[r][c],
                                             fill=PIXEL_ON if val else PIXEL_HOVER)

    def _grid_unhover(self, event):
        if self._hover_cell:
            r, c = self._hover_cell
            val = font_data[self.current_char][r][c]
            self.grid_canvas.itemconfig(self.cells[r][c],
                                         fill=PIXEL_ON if val else PIXEL_OFF)
        self._hover_cell = None

    def _set_pixel(self, row, col, value):
        font_data[self.current_char][row][col] = value
        self.grid_canvas.itemconfig(self.cells[row][col],
                                     fill=PIXEL_ON if value else PIXEL_OFF)
        self._update_byte_labels()
        self._update_overview_char(self.current_char)
        self.dirty = True

    # ── Character navigation ───────────────────────────────────────────────────
    def _load_char(self, code):
        self.current_char = code
        char = chr(code) if 32 <= code <= 126 else f'#{code}'
        self.char_display.config(text=char if len(char) == 1 else '·')
        self.char_info.config(text=f"ASCII {code}  |  0x{code:02X}  |  '{char}'")

        data = font_data[code]
        for row in range(CHAR_H):
            for col in range(CHAR_W):
                val = data[row][col]
                self.grid_canvas.itemconfig(self.cells[row][col],
                                             fill=PIXEL_ON if val else PIXEL_OFF)
        self._update_byte_labels()
        self._update_ov_selection()
        self.status_label.config(text=f"char {code} / 127")

    def _prev_char(self):
        self._load_char((self.current_char - 1) % CHAR_COUNT)

    def _next_char(self):
        self._load_char((self.current_char + 1) % CHAR_COUNT)

    def _jump_to_char(self, event=None):
        val = self.jump_entry.get().strip()
        try:
            if val.startswith('0x') or val.startswith('0X'):
                code = int(val, 16)
            elif len(val) == 1:
                code = ord(val)
            else:
                code = int(val)
            if 0 <= code < CHAR_COUNT:
                self._load_char(code)
                self.jump_entry.delete(0, 'end')
        except ValueError:
            pass

    # ── Edit tools ────────────────────────────────────────────────────────────
    def _clear_char(self):
        for r in range(CHAR_H):
            for c in range(CHAR_W):
                font_data[self.current_char][r][c] = 0
        self._load_char(self.current_char)
        self._update_overview_char(self.current_char)
        self.dirty = True

    def _invert_char(self):
        for r in range(CHAR_H):
            for c in range(CHAR_W):
                font_data[self.current_char][r][c] ^= 1
        self._load_char(self.current_char)
        self._update_overview_char(self.current_char)
        self.dirty = True

    def _shift(self, direction):
        d = font_data[self.current_char]
        if direction == 'up':
            d.append(d.pop(0))
        elif direction == 'down':
            d.insert(0, d.pop())
        elif direction == 'left':
            for r in range(CHAR_H):
                d[r].append(d[r].pop(0))
        elif direction == 'right':
            for r in range(CHAR_H):
                d[r].insert(0, d[r].pop())
        self._load_char(self.current_char)
        self._update_overview_char(self.current_char)
        self.dirty = True

    # ── Overview ──────────────────────────────────────────────────────────────
    def _refresh_overview(self):
        for c in range(CHAR_COUNT):
            self._update_overview_char(c)

    def _update_overview_char(self, code):
        rects = self.ov_rects[code]
        data  = font_data[code]
        idx   = 0
        for py in range(CHAR_H):
            for px in range(CHAR_W):
                val = data[py][px]
                self.overview_canvas.itemconfig(rects[idx],
                                                 fill=GREEN if val else BG2)
                idx += 1

    def _update_ov_selection(self):
        c   = self.current_char
        col = c % COLS
        row = c // COLS
        cell_px = PREVIEW_SCALE * CHAR_W + 2
        x1  = col * cell_px - 1
        y1  = row * (PREVIEW_SCALE * CHAR_H + 2) - 1
        x2  = x1 + cell_px + 1
        y2  = y1 + PREVIEW_SCALE * CHAR_H + 3
        self.overview_canvas.coords(self.ov_sel, x1, y1, x2, y2)

    def _overview_click(self, event):
        cell_px  = PREVIEW_SCALE * CHAR_W + 2
        cell_py  = PREVIEW_SCALE * CHAR_H + 2
        col = event.x // cell_px
        row = event.y // cell_py
        code = row * COLS + col
        if 0 <= code < CHAR_COUNT:
            self._load_char(code)

    # ── Byte labels ───────────────────────────────────────────────────────────
    def _update_byte_labels(self):
        data = font_data[self.current_char]
        for r in range(CHAR_H):
            byte = 0
            for c in range(CHAR_W):
                byte = (byte << 1) | data[r][c]
            self.byte_labels[r].config(text=f"row {r}:  0x{byte:02X}  ({byte:08b})")

    # ── File I/O ──────────────────────────────────────────────────────────────
    def _save(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".bin",
            filetypes=[("Binary font file", "*.bin"), ("All files", "*.*")],
            initialfile="font.bin",
            title="Save Font ROM"
        )
        if not path:
            return
        data = bytearray()
        for code in range(CHAR_COUNT):
            for row in range(CHAR_H):
                byte = 0
                for col in range(CHAR_W):
                    byte = (byte << 1) | font_data[code][row][col]
                data.append(byte)
        with open(path, 'wb') as f:
            f.write(data)
        self.dirty = False
        self.save_status.config(text=f"✓ saved {len(data)} bytes → {os.path.basename(path)}",
                                 fg=GREEN2)
        self.root.after(4000, lambda: self.save_status.config(text=""))

    def _load(self):
        path = filedialog.askopenfilename(
            filetypes=[("Binary font file", "*.bin"), ("All files", "*.*")],
            title="Load Font ROM"
        )
        if not path:
            return
        with open(path, 'rb') as f:
            raw = f.read()
        for code in range(min(CHAR_COUNT, len(raw) // CHAR_H)):
            for row in range(CHAR_H):
                byte = raw[code * CHAR_H + row]
                for col in range(CHAR_W):
                    font_data[code][row][7 - col] = (byte >> col) & 1
        self._load_char(self.current_char)
        self._refresh_overview()
        self.dirty = False
        self.save_status.config(text=f"✓ loaded {os.path.basename(path)}", fg=GREEN2)
        self.root.after(4000, lambda: self.save_status.config(text=""))


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = FontEditor(root)
    root.mainloop()
