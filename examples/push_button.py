"""
"Write a MicroPython script for an RP2040 that reads a quadrature
rotary encoder on GPIO 18 (A) and GPIO 17 (B), printing a counter
on each detent. Also detect a push button on GPIO 21 and a center
click on GPIO 5, printing a message when each is pressed. Use internal pull-ups."
"""

import machine
# Set up GPIO pins
btn_pin = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)  
sw_c_pin = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
ang_a_pin = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
ang_b_pin = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
counter = 0
# Previous state of the encoder
prev_a = ang_a_pin.value()
prev_b = ang_b_pin.value()
while True:
    # Check for button press
    if not btn_pin.value():
        print("Button pressed!")
        while not btn_pin.value():  # Wait for button release
            pass

    # Check for center click
    if not sw_c_pin.value():
        print("Center click detected!")
        while not sw_c_pin.value():  # Wait for button release
            pass

    # Read the current state of the encoder
    a = ang_a_pin.value()
    b = ang_b_pin.value()

    # Detect rotation (use positive for clockwise, negative for counterclockwise)
    if (prev_a, prev_b) == (0, 0):
        if (a, b) == (0, 1):
            counter -= 1  # Clockwise 
            print(f"Counter: {counter}")
        elif (a, b) == (1, 0):
            counter += 1  # Counterclockwise
            print(f"Counter: {counter}")

    prev_a, prev_b = a, b