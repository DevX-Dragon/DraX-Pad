# this code is fully written by me without the use of Ai.
# i have commented out some stuff for ease understanding of others.
# --- DraX Pad V2 Firmware ---
import board, busio, usb_hid, time
import adafruit_ssd1306
import neopixel
from keypad import KeyMatrix
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
# Ensure game_logic.py is present on your CIRCUITPY drive
try:
    from game_logic import MacropadGame
except ImportError:
    MacropadGame = None

# --- Hardware Config (Updated for Final Schematic) ---

# 1. NeoPixels: Using GP2 (Pin 9). 
# Brightness restricted to 0.15 since the capacitor was removed to prevent power spikes.
pixels = neopixel.NeoPixel(board.GP2, 10, brightness=0.15, auto_write=True)

# 2. OLED Display: Now using Hardware I2C on Pins 5 & 6 (GP6/GP7)
# This is much more stable than bit-banging or using the previous noisy pins.
i2c = busio.I2C(board.GP7, board.GP6) # SCL, SDA
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# 3. HID Keyboard
kbd = Keyboard(usb_hid.devices)

# 4. Key Matrix (Updated to match the 4x3 layout with GP29)
# Rows: GP29 (Pin 4), GP0 (Pin 7), GP1 (Pin 8), GP7 (Pin 6)
# Columns: GP26 (Pin 1), GP27 (Pin 2), GP28 (Pin 3)
matrix = KeyMatrix(row_pins=(board.GP29, board.GP0, board.GP1, board.GP7), 
                   column_pins=(board.GP26, board.GP27, board.GP28))

# --- Mode Structures ---
MODES = ["MACROS", "RGB", "GAME"]
current_mode_idx = 0
current_preset_idx = 0

PRESETS = [
    {"name": "Work", "keys": {0: [Keycode.A], 1: [Keycode.B], 2: [Keycode.C], 3: [Keycode.D], 4: [Keycode.E], 5: [Keycode.F], 6: [Keycode.G], 7: [Keycode.H], 8: [Keycode.I], 9: [Keycode.J]}},
    {"name": "Gaming", "keys": {0: [Keycode.ONE], 1: [Keycode.TWO], 2: [Keycode.THREE], 3: [Keycode.FOUR], 4: [Keycode.FIVE], 5: [Keycode.SIX], 6: [Keycode.SEVEN], 7: [Keycode.EIGHT], 8: [Keycode.NINE], 9: [Keycode.ZERO]}}
]

if MacropadGame:
    game = MacropadGame(display)
key_states = [False] * 12 

def update_ui():
    display.fill(0)
    display.text(f"MODE: {MODES[current_mode_idx]}", 0, 10, 1)
    if MODES[current_mode_idx] == "MACROS":
        display.text(f"Preset: {PRESETS[current_preset_idx]['name']}", 0, 30, 1)
    display.show()

update_ui()

while True:
    event = matrix.events.get()
    if event:
        key_states[event.key_number] = event.pressed
        
        # Mode Cycling Logic
        if key_states[9] and event.key_number == 0 and event.pressed:
            current_mode_idx = (current_mode_idx + 1) % len(MODES)
            if MODES[current_mode_idx] == "GAME" and MacropadGame: 
                game.reset()
            update_ui()
            continue

        # Preset Cycling Logic
        if event.key_number == 9 and event.pressed and not key_states[0]:
            if MODES[current_mode_idx] == "MACROS":
                current_preset_idx = (current_preset_idx + 1) % len(PRESETS)
                update_ui()
            continue

        # Mode Specific Logic
        if MODES[current_mode_idx] == "MACROS":
            if event.pressed and event.key_number in PRESETS[current_preset_idx]["keys"]:
                kbd.press(*PRESETS[current_preset_idx]["keys"][event.key_number])
                pixels[event.key_number] = (0, 255, 255) # Cyan flash
            elif event.released:
                kbd.release_all()
                pixels.fill(0)

        elif MODES[current_mode_idx] == "GAME" and MacropadGame:
            if event.pressed: 
                game.handle_input(event.key_number)

    if MODES[current_mode_idx] == "GAME" and MacropadGame:
        game.update()
        game.draw()

    time.sleep(0.01) # Reduced sleep for better responsiveness
