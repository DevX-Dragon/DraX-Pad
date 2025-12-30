# Setup Instructions
## Follow these steps to get your macropad up and running.

### 1. Connect the Hardware
 Plug a USB-C cable from your PC into the macropad. A new external drive (often named RPI-RP2 or similar) should appear on your computer.

### 2. Install CircuitPython
 Download the correct .uf2 file for your board from the CircuitPython website.

Drag and drop the .uf2 file onto the new drive.

The board will automatically reboot, and the drive name will change to CIRCUITPY.

### 3. Flash the Software
Copy all the Python files from this repository directory and paste them directly onto the CIRCUITPY drive.

Note: Ensure code.py is in the root directory of the drive, as this is the file CircuitPython executes on startup.

### 4. Finalize
Unplug the USB-C cable.

Reconnect the cable to initialize the new firmware.

You're now ready to go! Have fun experimenting!
