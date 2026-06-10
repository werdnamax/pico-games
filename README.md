# pico-games

MicroPython games for the RP2040 Pico family, built for a custom board interface used with the Walla Walla University intro to CAD student hardware.

This repository currently includes a Tetris game for a Raspberry Pi Pico with:

- an OLED display over I2C
- a rotary encoder for left and right movement
- the encoder button, or a dedicated button, for rotate and start

## Tetris

`tetris.py` is a playable Tetris clone that runs on MicroPython. The game shows the board, score, level, and next piece on a 128x64 SSD1306 OLED display.

### Controls

- Rotate the encoder left or right to move the piece
- Press the encoder button to rotate the piece
- Press the start button, or the encoder center switch, to start and restart

### Hardware

The current Tetris build expects:

- Raspberry Pi Pico or another RP2040 board running MicroPython
- SSD1306 OLED display on I2C0
- Rotary encoder wired to the pins used in `tetris.py`
- The `ssd1306` MicroPython driver available on the board

The pin assignments in the game are defined in `tetris.py` and should match your board wiring before you run it.

## Getting Started

### 1. Flash MicroPython to the Pico

If your Pico is not already running MicroPython, flash the included UF2 file:

1. Hold the BOOTSEL button and rest while plugging in the Pico. Then release the reset button. The Pico should mount as a USB drive on your computer.
2. Copy `RPI_PICO-20260409-v1.29.0-preview.32.g8c6dfa5bd4.uf2` onto the mounted Pico drive.
3. The board will reboot into MicroPython after the file finishes copying.

### 2. Connect with Pico VS Code

Use the Pico / Pico-vscode extension in VS Code to connect your editor to the board.

Typical workflow:

1. Open the Pico commands in VS Code. (press `Ctrl+Shift+P` and search for "Pico")
2. Use the Window to Pico connect option to connect to the board. Select the opetion that says "MicroPico: Connect" 
3. Some green text should appear in the terminal indicating a successful connection.

If you prefer, you can also copy the file directly to the Pico and rename it to `main.py` so it starts automatically after boot.

### 3. Install the SSD1306 driver

using the Pico extension, upload `ssd1306.py` to the Pico filesystem if it's not already there. This driver is required for the OLED display to work.

* With the Pico connected, right-click on `ssd1306.py` in the VS Code file explorer and select "Upload to Pico". This will copy the file to the board's filesystem.
* alternatively, you can use the Pico REPL to copy the file contents and create it directly on the board.
* Note that unless you delete the file after uploading, it will remain on the Pico and be available for future use.

### 4. Run the game

Once the Pico is connected and the driver is installed, you can run `tetris.py`: 
1. Open `tetris.py` in VS Code.
2. With the Pico connected, right-click on `tetris.py` and select "Run on Pico". This will execute the game on the board and you should see it start on the OLED display. Or you can click the "Run" button in the top left of the editor window while `tetris.py` is open and the Pico is connected.

## Files

- `tetris.py` - Tetris game for the Pico
- `falling.py` - another game/example in this repo
- `examples/` - simple hardware examples for the board and peripherals
- `RPI_PICO-20260409-v1.29.0-preview.32.g8c6dfa5bd4.uf2` - MicroPython firmware for the Pico
- `ssd1306.py` - MicroPython driver for the SSD1306 OLED display

## Notes

- Make sure the OLED wiring matches the I2C pins configured in `tetris.py`.
- If the game does not start, check that the `ssd1306` module is installed on the Pico.
- If the controls move the wrong direction, verify the encoder wiring and pin mapping.

For more information on the hardware of the walla walla board see the Walla Walla University intro to CAD course materials.
Github: https://github.com/frohro/Intro-to-CAD-2026.git

For a more detailed hardware analysis see [Hardware.md](./hardware.md) in this repository.