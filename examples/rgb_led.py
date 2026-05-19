""" 
A MicroPython script that cycles a single WS2812B NeoPixel
on GPIO 22 through red, green, blue, and white at 600 ms
per color, using the built-in neopixel module.
"""
import machine
import neopixel
import time

# Set up the NeoPixel on GPIO 22 with 1 pixel
np = neopixel.NeoPixel(machine.Pin(22), 1)
# Define the colors to cycle through
colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 255),
]  # Red, Green, Blue, White
while True:
    for color in colors:
        np[0] = color  # Set the color of the single pixel
        np.write()  # Update the NeoPixel to show the new color
        time.sleep(0.6)  # Wait for 600 ms before changing to the next color
