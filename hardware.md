# Hardware Analysis

The games in this repository are designed to run on a Walla Walla University walla walla board, which is based on the Raspberry Pi Pico microcontroller. The hardware setup for the games includes:
- A Raspberry Pi Pico or compatible RP2040 board running MicroPython
- An SSD1306 OLED display connected over I2C for visual output
- A rotary encoder for user input, allowing for left and right movement as well as a button press for actions like rotation and starting the game
The pin assignments for the OLED display and rotary encoder are defined in the game code (e.g., `tetris.py`) and should be matched to your specific hardware wiring. The SSD1306 driver must also be installed on the Pico for the display to function correctly.

## Pins used in tetris.py:
- OLED SCL: GPIO 15
- OLED SDA: GPIO 14
- Encoder A: GPIO 16
- Encoder B: GPIO 17
- Encoder Button: GPIO 18
- Start Button: GPIO 19

## Troubleshooting
- If the display does not show anything, check the I2C connections and ensure the `ssd1306` driver is properly installed on the Pico.
- If the encoder does not respond, verify the wiring and pin assignments for the encoder in the code match your hardware setup.
