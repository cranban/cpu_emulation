#define SDL_MAIN_HANDLED
#include <cstdint>
#include <SDL2/SDL.h>

//memory
const uint8_t ld = 0x00;
const uint8_t st = 0x01;
const uint8_t ldi = 0x02;
const uint8_t ldind = 0x03;
const uint8_t stind = 0x04;
//register
const uint8_t mov = 0x05;
//arithmetic
const uint8_t add = 0x06;
const uint8_t sub = 0x07;
const uint8_t mul = 0x08;
const uint8_t gdiv = 0x09;
const uint8_t inc = 0x0a;
const uint8_t dec = 0x0b;
const uint8_t neg = 0x0c;
const uint8_t mod = 0x0d;
//bitwise
const uint8_t gand = 0x0e;
const uint8_t gor = 0x0f;
const uint8_t gxor = 0x10;
const uint8_t gnot = 0x11;
const uint8_t shl = 0x12;
const uint8_t shr = 0x13;
//comparison
const uint8_t cmpr = 0x14;
//jumps
const uint8_t jmp = 0x15;
const uint8_t jz = 0x16;
const uint8_t jnz = 0x17;
const uint8_t jng = 0x18;
const uint8_t jc = 0x19;
const uint8_t jge = 0x1a;
const uint8_t jle = 0x1b;
//stack
const uint8_t push = 0x1c;
const uint8_t pop = 0x1d;
const uint8_t call = 0x1e;
const uint8_t ret = 0x1f;
//display
const uint8_t pixel = 0x20;
//misc
const uint8_t nop = 0x21;
const uint8_t halt = 0x22;
const uint8_t vsync = 0x23;

// hardware I/O addresses
const uint16_t ADDR_SOUND = 0xFEF0;  // write: frequency in Hz (0 = stop)
const uint16_t ADDR_TIMER = 0xFEF2;  // read:  ms since startup (wraps at 65535)
const uint16_t ADDR_RAND  = 0xFEF4;  // read:  new random 16-bit value each read

//registers
uint16_t r1 = 0;
uint16_t r2 = 0;
uint16_t r3 = 0;
uint16_t r4 = 0;
uint16_t r5 = 0;
uint16_t r6 = 0;
uint16_t r7 = 0;
uint16_t r8 = 0;
uint16_t r9 = 0;
uint16_t r10 = 0;
uint16_t r11 = 0;
uint16_t r12 = 0;
uint16_t r13 = 0;
uint16_t r14 = 0;
uint16_t idx = 0;
uint16_t sp = 0xFEFF;

//flags
uint8_t zero_flag = 0;
uint8_t carry_flag = 0;
uint8_t negative_flag = 0;

//running
uint16_t program_counter = 0;
bool running = true;
bool vsync_pending = false;

//memory
uint8_t ram[65536] = {};
uint16_t vram[16384] = {};

// sound state — written by main thread, read by audio callback
volatile uint16_t sound_freq = 0;
uint32_t audio_phase = 0;

// xorshift32 RNG
uint32_t rng_state = 0;
uint16_t next_rand() {
    rng_state ^= rng_state << 13;
    rng_state ^= rng_state >> 17;
    rng_state ^= rng_state << 5;
    return (uint16_t)(rng_state & 0xFFFF);
}

// SDL audio callback — generates a square wave at sound_freq
void audio_callback(void* userdata, Uint8* stream, int len) {
    Sint16* buf = (Sint16*)stream;
    int samples = len / 2;
    for (int i = 0; i < samples; i++) {
        uint16_t freq = sound_freq;
        if (freq == 0) {
            buf[i] = 0;
            audio_phase = 0;
        } else {
            // phase accumulator: increment = freq/samplerate * 2^16
            audio_phase += (uint32_t)freq * 65536 / 44100;
            buf[i] = (audio_phase & 0x8000) ? 20000 : -20000;
        }
    }
}

uint16_t get_reg(uint8_t reg_id) {
    if (reg_id == 0x00) return 0;
    if (reg_id == 0x01) return r1;
    if (reg_id == 0x02) return r2;
    if (reg_id == 0x03) return r3;
    if (reg_id == 0x04) return r4;
    if (reg_id == 0x05) return r5;
    if (reg_id == 0x06) return r6;
    if (reg_id == 0x07) return r7;
    if (reg_id == 0x08) return r8;
    if (reg_id == 0x09) return r9;
    if (reg_id == 0x0a) return r10;
    if (reg_id == 0x0b) return r11;
    if (reg_id == 0x0c) return r12;
    if (reg_id == 0x0d) return r13;
    if (reg_id == 0x0e) return r14;
    if (reg_id == 0x0f) return idx;
    if (reg_id == 0x10) return sp;
    if (reg_id == 0x11) return zero_flag;
    if (reg_id == 0x12) return carry_flag;
    if (reg_id == 0x13) return negative_flag;
    return 0;
}

void set_reg(uint8_t reg_id, uint16_t value) {
    value = value & 0xffff;
    if (reg_id == 0x00) return;
    else if (reg_id == 0x01) r1 = value;
    else if (reg_id == 0x02) r2 = value;
    else if (reg_id == 0x03) r3 = value;
    else if (reg_id == 0x04) r4 = value;
    else if (reg_id == 0x05) r5 = value;
    else if (reg_id == 0x06) r6 = value;
    else if (reg_id == 0x07) r7 = value;
    else if (reg_id == 0x08) r8 = value;
    else if (reg_id == 0x09) r9 = value;
    else if (reg_id == 0x0a) r10 = value;
    else if (reg_id == 0x0b) r11 = value;
    else if (reg_id == 0x0c) r12 = value;
    else if (reg_id == 0x0d) r13 = value;
    else if (reg_id == 0x0e) r14 = value;
    else if (reg_id == 0x0f) idx = value;
    else if (reg_id == 0x10) sp = value;
}

// memory-mapped read — intercepts hardware registers
uint16_t mem_read(uint16_t address) {
    if (address == ADDR_TIMER)
        return (uint16_t)(SDL_GetTicks() & 0xFFFF);
    if (address == ADDR_RAND)
        return next_rand();
    return ram[address] | (ram[(address + 1) & 0xffff] << 8);
}

// memory-mapped write — intercepts hardware registers
void mem_write(uint16_t address, uint16_t val) {
    if (address == ADDR_SOUND) {
        sound_freq = val;
        return;
    }
    ram[address] = val & 0xff;
    ram[(address + 1) & 0xffff] = (val >> 8) & 0xff;
}

void fetch(uint8_t& opcode, uint8_t& byte2, uint8_t& byte3, uint8_t& byte4) {
    opcode = ram[program_counter];
    byte2 = ram[(program_counter + 1) & 0xffff];
    byte3 = ram[(program_counter + 2) & 0xffff];
    byte4 = ram[(program_counter + 3) & 0xffff];
    program_counter = (program_counter + 4) & 0xffff;
}

void execute(uint8_t opcode, uint8_t byte2, uint8_t byte3, uint8_t byte4) {

    if (opcode == ld) {
        uint8_t reg_id = byte2;
        uint16_t address = (byte3 << 8) | byte4;
        set_reg(reg_id, mem_read(address));
    }

    else if (opcode == st) {
        uint8_t reg_id = byte2;
        uint16_t address = (byte3 << 8) | byte4;
        mem_write(address, get_reg(reg_id));
    }

    else if (opcode == ldi) {
        uint8_t reg_id = byte2;
        uint16_t value = (byte3 << 8) | byte4;
        set_reg(reg_id, value);
    }

    else if (opcode == ldind) {
        uint8_t dst_reg = byte2 >> 4;
        uint8_t addr_reg = byte2 & 0x0f;
        uint16_t address = get_reg(addr_reg);
        set_reg(dst_reg, mem_read(address));
    }

    else if (opcode == stind) {
        uint8_t value_reg = byte2 >> 4;
        uint8_t address_reg = byte2 & 0x0f;
        uint16_t address = get_reg(address_reg);
        mem_write(address, get_reg(value_reg));
    }

    else if (opcode == mov) {
        uint8_t destination = byte2 >> 4;
        uint8_t source = byte2 & 0x0f;
        set_reg(destination, get_reg(source));
    }

    //arithmetic

    else if (opcode == add) {
        uint8_t destination = byte2 >> 4;
        uint8_t source1 = byte2 & 0x0f;
        uint8_t source2 = byte3 >> 4;
        uint32_t result = get_reg(source1) + get_reg(source2);
        carry_flag = result > 0xffff ? 1 : 0;
        zero_flag = (result & 0xffff) == 0 ? 1 : 0;
        negative_flag = (result & 0x8000) ? 1 : 0;
        set_reg(destination, result);
    }

    else if (opcode == sub) {
        uint8_t destination = byte2 >> 4;
        uint8_t source1 = byte2 & 0x0f;
        uint8_t source2 = byte3 >> 4;
        uint32_t result = get_reg(source1) - get_reg(source2);
        carry_flag = get_reg(source1) < get_reg(source2) ? 1 : 0;
        zero_flag = (result & 0xffff) == 0 ? 1 : 0;
        negative_flag = (result & 0x8000) ? 1 : 0;
        set_reg(destination, result);
    }

    else if (opcode == mul) {
        uint8_t destination = byte2 >> 4;
        uint8_t source1 = byte2 & 0x0f;
        uint8_t source2 = byte3 >> 4;
        uint32_t result = get_reg(source1) * get_reg(source2);
        carry_flag = result > 0xffff ? 1 : 0;
        zero_flag = (result & 0xffff) == 0 ? 1 : 0;
        negative_flag = (result & 0x8000) ? 1 : 0;
        set_reg(destination, result);
    }

    else if (opcode == gdiv) {
        uint8_t destination = byte2 >> 4;
        uint8_t source1 = byte2 & 0x0f;
        uint8_t source2 = byte3 >> 4;
        if (get_reg(source2) == 0) {
            carry_flag = 1; zero_flag = 1; negative_flag = 0;
            set_reg(destination, 0);
        } else {
            uint16_t result = get_reg(source1) / get_reg(source2);
            carry_flag = 0;
            zero_flag = result == 0;
            negative_flag = (result & 0x8000) != 0;
            set_reg(destination, result);
        }
    }

    else if (opcode == inc) {
        uint8_t reg_id = byte2 >> 4;
        uint32_t raw = get_reg(reg_id) + 1;
        carry_flag = raw > 0xFFFF;
        uint16_t result = raw & 0xFFFF;
        zero_flag = result == 0;
        negative_flag = (result & 0x8000) != 0;
        set_reg(reg_id, result);
    }

    else if (opcode == dec) {
        uint8_t reg_id = byte2 >> 4;
        uint16_t val = get_reg(reg_id);
        carry_flag = (val == 0);
        uint16_t result = (val - 1) & 0xFFFF;
        zero_flag = result == 0;
        negative_flag = (result & 0x8000) != 0;
        set_reg(reg_id, result);
    }

    else if (opcode == neg) {
        uint8_t reg_id = byte2 >> 4;
        uint16_t val = get_reg(reg_id);
        carry_flag = (val != 0);
        uint16_t result = (~val + 1) & 0xFFFF;
        zero_flag = result == 0;
        negative_flag = (result & 0x8000) != 0;
        set_reg(reg_id, result);
    }

    else if (opcode == mod) {
        uint8_t destination = byte2 >> 4;
        uint8_t source1 = byte2 & 0x0f;
        uint8_t source2 = byte3 >> 4;
        if (get_reg(source2) == 0) {
            carry_flag = 1; zero_flag = 1; negative_flag = 0;
            set_reg(destination, 0);
        } else {
            uint16_t result = get_reg(source1) % get_reg(source2);
            carry_flag = 0;
            zero_flag = result == 0;
            negative_flag = (result & 0x8000) != 0;
            set_reg(destination, result);
        }
    }

    //bitwise

    else if (opcode == gand) {
        uint8_t destination = byte2 >> 4;
        uint8_t source1 = byte2 & 0x0f;
        uint8_t source2 = byte3 >> 4;
        uint16_t result = get_reg(source1) & get_reg(source2);
        carry_flag = 0;
        zero_flag = result == 0 ? 1 : 0;
        negative_flag = (result & 0x8000) ? 1 : 0;
        set_reg(destination, result);
    }

    else if (opcode == gor) {
        uint8_t destination = byte2 >> 4;
        uint8_t source1 = byte2 & 0x0f;
        uint8_t source2 = byte3 >> 4;
        uint16_t result = get_reg(source1) | get_reg(source2);
        carry_flag = 0;
        zero_flag = result == 0 ? 1 : 0;
        negative_flag = (result & 0x8000) ? 1 : 0;
        set_reg(destination, result);
    }

    else if (opcode == gxor) {
        uint8_t destination = byte2 >> 4;
        uint8_t source1 = byte2 & 0x0f;
        uint8_t source2 = byte3 >> 4;
        uint16_t result = get_reg(source1) ^ get_reg(source2);
        carry_flag = 0;
        zero_flag = result == 0 ? 1 : 0;
        negative_flag = (result & 0x8000) ? 1 : 0;
        set_reg(destination, result);
    }

    else if (opcode == gnot) {
        uint8_t reg_id = byte2 >> 4;
        uint16_t result = (~get_reg(reg_id)) & 0xffff;
        carry_flag = 0;
        zero_flag = result == 0 ? 1 : 0;
        negative_flag = (result & 0x8000) ? 1 : 0;
        set_reg(reg_id, result);
    }

    else if (opcode == shl) {
        uint8_t destination = byte2 >> 4;
        uint8_t source1 = byte2 & 0x0f;
        uint8_t source2 = byte3 >> 4;
        uint16_t shift = get_reg(source2) & 0x0F;
        uint32_t raw = get_reg(source1) << shift;
        carry_flag = raw > 0xFFFF;
        uint16_t result = raw & 0xFFFF;
        zero_flag = result == 0;
        negative_flag = (result & 0x8000) != 0;
        set_reg(destination, result);
    }

    else if (opcode == shr) {
        uint8_t destination = byte2 >> 4;
        uint8_t source1 = byte2 & 0x0f;
        uint8_t source2 = byte3 >> 4;
        uint16_t val = get_reg(source1);
        uint16_t shift = get_reg(source2) & 0x0f;
        carry_flag = shift > 0 ? (val >> (shift - 1)) & 1 : 0;
        uint16_t result = val >> shift;
        zero_flag = result == 0 ? 1 : 0;
        negative_flag = (result & 0x8000) ? 1 : 0;
        set_reg(destination, result);
    }

    //comparison

    else if (opcode == cmpr) {
        uint8_t source1 = byte2 >> 4;
        uint8_t source2 = byte2 & 0x0f;
        uint32_t result = get_reg(source1) - get_reg(source2);
        carry_flag = get_reg(source1) < get_reg(source2) ? 1 : 0;
        zero_flag = (result & 0xffff) == 0 ? 1 : 0;
        negative_flag = (result & 0x8000) ? 1 : 0;
    }

    //jumps

    else if (opcode == jmp) {
        program_counter = ((byte3 << 8) | byte4) & 0xFFFC;
    }

    else if (opcode == jz) {
        if (zero_flag == 1)
            program_counter = ((byte3 << 8) | byte4) & 0xFFFC;
    }

    else if (opcode == jnz) {
        if (zero_flag == 0)
            program_counter = ((byte3 << 8) | byte4) & 0xFFFC;
    }

    else if (opcode == jng) {
        if (negative_flag == 1)
            program_counter = ((byte3 << 8) | byte4) & 0xFFFC;
    }

    else if (opcode == jc) {
        if (carry_flag == 1)
            program_counter = ((byte3 << 8) | byte4) & 0xFFFC;
    }

    else if (opcode == jge) {
        if (carry_flag == 0)
            program_counter = ((byte3 << 8) | byte4) & 0xFFFC;
    }

    else if (opcode == jle) {
        if (carry_flag == 1 || zero_flag == 1)
            program_counter = ((byte3 << 8) | byte4) & 0xFFFC;
    }

    //stack

    else if (opcode == push) {
        uint8_t reg_id = byte2 >> 4;
        uint16_t val = get_reg(reg_id);
        if (sp < 2) { running = false; return; }
        sp = (sp - 1) & 0xffff;
        ram[sp] = (val >> 8) & 0xff;
        sp = (sp - 1) & 0xffff;
        ram[sp] = val & 0xff;
    }

    else if (opcode == pop) {
        uint8_t reg_id = byte2 >> 4;
        if (sp > 0xFEFD) { running = false; return; }
        uint8_t low = ram[sp];
        sp = (sp + 1) & 0xffff;
        uint8_t high = ram[sp];
        sp = (sp + 1) & 0xffff;
        set_reg(reg_id, (high << 8) | low);
    }

    else if (opcode == call) {
        uint16_t address = ((byte3 << 8) | byte4) & 0xFFFC;
        if (sp < 2) { running = false; return; }
        sp = (sp - 1) & 0xffff;
        ram[sp] = (program_counter >> 8) & 0xff;
        sp = (sp - 1) & 0xffff;
        ram[sp] = program_counter & 0xff;
        program_counter = address;
    }

    else if (opcode == ret) {
        if (sp > 0xFEFD) { running = false; return; }
        uint8_t low = ram[sp];
        sp = (sp + 1) & 0xffff;
        uint8_t high = ram[sp];
        sp = (sp + 1) & 0xffff;
        program_counter = (high << 8) | low;
    }

    //display

    else if (opcode == pixel) {
        uint8_t color_reg = byte2 >> 4;
        uint8_t addr_reg = byte2 & 0x0f;
        uint16_t address = get_reg(addr_reg);
        if (address < 16384)
            vram[address] = get_reg(color_reg);
    }

    //misc

    else if (opcode == nop) {
        return;
    }

    else if (opcode == vsync) {
        vsync_pending = true;
    }

    else if (opcode == halt) {
        running = false;
    }

    else {
        running = false;
    }
}

int main() {
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO) != 0) return 1;

    // seed RNG from startup time
    rng_state = SDL_GetTicks();
    if (rng_state == 0) rng_state = 0xDEAD;

    // open audio device
    SDL_AudioSpec want = {};
    want.freq     = 44100;
    want.format   = AUDIO_S16SYS;
    want.channels = 1;
    want.samples  = 512;
    want.callback = audio_callback;
    SDL_AudioSpec got = {};
    SDL_AudioDeviceID audio_dev = SDL_OpenAudioDevice(NULL, 0, &want, &got, 0);
    if (audio_dev) SDL_PauseAudioDevice(audio_dev, 0);  // start playing

    FILE* f = fopen("program.bin", "rb");
    if (f) {
        fread(ram, 1, 65536, f);
        fclose(f);
    }

    SDL_Window* window = SDL_CreateWindow("YBM-16", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 1024, 1024, 0);
    if (!window) return 1;
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) return 1;
    SDL_Texture* texture = SDL_CreateTexture(renderer, SDL_PIXELFORMAT_RGB565, SDL_TEXTUREACCESS_STREAMING, 128, 128);
    if (!texture) return 1;

    uint32_t last_frame = SDL_GetTicks();
    bool halted = false;
    bool quit = false;

    while (!quit) {
        if (!halted && !vsync_pending) {
            uint8_t opcode, byte2, byte3, byte4;
            fetch(opcode, byte2, byte3, byte4);
            execute(opcode, byte2, byte3, byte4);
            if (!running) halted = true;
        }

        uint32_t now = SDL_GetTicks();
        if (now - last_frame >= 16) {
            last_frame = now;
            vsync_pending = false;

            SDL_UpdateTexture(texture, NULL, vram, 128 * sizeof(uint16_t));
            SDL_RenderClear(renderer);
            SDL_RenderCopy(renderer, texture, NULL, NULL);
            SDL_RenderPresent(renderer);

            SDL_Event event;
            while (SDL_PollEvent(&event)) {
                if (event.type == SDL_QUIT) quit = true;
            }

            const uint8_t* keys = SDL_GetKeyboardState(NULL);
            for (int i = 0; i < 256; i++) {
                ram[0xFF00 + i] = keys[i];
            }
        }
    }

    if (audio_dev) SDL_CloseAudioDevice(audio_dev);
    SDL_DestroyTexture(texture);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
