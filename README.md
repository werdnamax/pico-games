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

1. Hold the BOOTSEL button while plugging in the Pico.
2. Copy `RPI_PICO-20260409-v1.29.0-preview.32.g8c6dfa5bd4.uf2` onto the mounted Pico drive.
3. The board will reboot into MicroPython after the file finishes copying.

### 2. Connect with Pico VS Code

Use the Pico / Pico-vscode extension in VS Code to connect your editor to the board.

Typical workflow:

1. Open the Pico commands in VS Code.
2. Use the Window to Pico connect option to connect to the board.
3. Upload `tetris.py` to the Pico filesystem.
4. Open a REPL or run the file from the extension.

If you prefer, you can also copy the file directly to the Pico and rename it to `main.py` so it starts automatically after boot.

### 3. Run the game

Once the Pico is connected and the file is on the board, run `tetris.py` from the extension or execute it from the MicroPython REPL.

## Files

- `tetris.py` - Tetris game for the Pico
- `falling.py` - another game/example in this repo
- `examples/` - simple hardware examples for the board and peripherals

## Notes

- Make sure the OLED wiring matches the I2C pins configured in `tetris.py`.
- If the game does not start, check that the `ssd1306` module is installed on the Pico.
- If the controls move the wrong direction, verify the encoder wiring and pin mapping.
