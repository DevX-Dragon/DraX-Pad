# this code is fully written by me without the use of Ai.
# i have commented out some stuff for ease understanding of others.
# --- DraX Pad V2 Firmware ---
import board, busio, usb_hid, time
import adafruit_ssd1306
import neopixel
from keypad import KeyMatrix
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from game_logic import MacropadGame

# --- Hardware Config ---
pixels = neopixel.NeoPixel(board.D2, 10, brightness=0.2)
i2c = busio.I2C(board.D7, board.D6)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
kbd = Keyboard(usb_hid.devices)

# My matrix 
matrix = KeyMatrix(row_pins=(board.D0, board.D1, board.D3, board.D4), 
                   column_pins=(board.D5, board.D8, board.D9))

# Mode Structures 
MODES = ["MACROS", "RGB", "GAME"]
current_mode_idx = 0
current_preset_idx = 0

# My Presets for now will update with more modes.
PRESETS = [
    {"name": "Work", "keys": {0: [Keycode.A], 1: [Keycode.B], 2: [Keycode.C], 3: [Keycode.D], 4: [Keycode.E], 5: [Keycode.F], 6: [Keycode.G], 7: [Keycode.H], 8: [Keycode.I], 9: [Keycode.J]}},
    {"name": "Gaming", "keys": {0: [Keycode.ONE], 1: [Keycode.TWO], 2: [Keycode.THREE], 3: [Keycode.FOUR], 4: [Keycode.FIVE], 5: [Keycode.SIX], 6: [Keycode.SEVEN], 7: [Keycode.EIGHT], 8: [Keycode.NINE], 9: [Keycode.ZERO]}}
]

game = MacropadGame(display)
key_states = [False] * 12 # Track held keys

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
        
        # Key 9 + Key 0 to Cycle between modes
        if key_states[9] and event.key_number == 0 and event.pressed:
            current_mode_idx = (current_mode_idx + 1) % len(MODES)
            if MODES[current_mode_idx] == "GAME": game.reset()
            update_ui()
            continue

        # Key 9 to Cycle Presets/Options ---
        if event.key_number == 9 and event.pressed and not key_states[0]:
            if MODES[current_mode_idx] == "MACROS":
                current_preset_idx = (current_preset_idx + 1) % len(PRESETS)
                update_ui()
            continue

        # logics for mode 
        if MODES[current_mode_idx] == "MACROS":
            if event.pressed and event.key_number in PRESETS[current_preset_idx]["keys"]:
                kbd.press(*PRESETS[current_preset_idx]["keys"][event.key_number])
                pixels[event.key_number] = (0, 255, 255)
            elif event.released:
                kbd.release_all()
                pixels.fill(0)

        elif MODES[current_mode_idx] == "GAME":
            if event.pressed: game.handle_input(event.key_number)

    if MODES[current_mode_idx] == "GAME":
        game.update()
        game.draw()
        time.sleep(0.05)