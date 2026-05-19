'''
Falling Object Game for Raspberry Pi Pico with OLED Display using MicroPython
The game displays a falling object on an OLED screen, and the player must use the rotary encoder 
to move a catcher at the bottom of the screen to catch the object which will spawn at the top at random positions.
The player scores points for each successful catch, and the score resets if they miss.
as the level increases, the speed of the falling object increases, making it more challenging to catch.
'''

import machine
import time
from ssd1306 import SSD1306_I2C
import random

# Set up I2C for OLED display
i2c = machine.I2C(0, scl=machine.Pin(13), sda=machine.Pin(12))
oled = SSD1306_I2C(128, 64, i2c)

# Set up rotary encoder pins
btn_pin = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)  
sw_c_pin = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
ang_a_pin = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)
ang_b_pin = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP)
counter = 0

# Previous state of the encoder
prev_a = ang_a_pin.value()
prev_b = ang_b_pin.value()

# Game variables
catcher_x = 64
catcher_width = 20
score = 0
level = 1
falling_object_x = 0
falling_object_y = 0

# Rotary encoder state
last_a = ang_a_pin.value()

# Game state
game_state = 'welcome'  # 'welcome' or 'playing'

# Triple-press detection
last_press_time = 0
press_count = 0

def reset_game():
    """Resets the game variables to their initial state."""
    global score, level, falling_object_x, falling_object_y, catcher_x
    score = 0
    level = 1
    falling_object_x = random.randint(0, 127)
    falling_object_y = 0
    catcher_x = 64

def encoder_interrupt(pin):
    global catcher_x, last_a
    current_a = ang_a_pin.value()
    if current_a != last_a:
        if ang_b_pin.value() != current_a:
            # Counter-clockwise
            catcher_x = max(catcher_width // 2, min(127 - catcher_width // 2, catcher_x + 5))
        else:
            # Clockwise
            catcher_x = max(catcher_width // 2, min(127 - catcher_width // 2, catcher_x - 5))
        last_a = current_a

# Attach interrupt to pin A
ang_a_pin.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=encoder_interrupt)

def draw_welcome_screen():
    oled.fill(0)
    oled.text('Falling Game', 15, 20)
    oled.text('Press to Start', 10, 40)
    oled.show()

def draw_game():
    oled.fill(0)  # Clear the screen
    # Draw falling object
    oled.fill_rect(falling_object_x, falling_object_y, 5, 5, 1)
    # Draw catcher
    oled.fill_rect(catcher_x - catcher_width // 2, 60, catcher_width, 4, 1)
    # Draw score and level
    oled.text(f'Score: {score}', 0, 0)
    oled.text(f'Level: {level}', 80, 0)
    oled.show()

reset_game()

while True:
    if game_state == 'welcome':
        draw_welcome_screen()
        if not btn_pin.value():
            reset_game()
            game_state = 'playing'
            time.sleep(0.2)  # Debounce
    
    elif game_state == 'playing':
        # Check for button press (for exiting)
        current_time = time.ticks_ms()
        if not btn_pin.value():
            if time.ticks_diff(current_time, last_press_time) > 300:
                press_count = 1
            else:
                press_count += 1
            last_press_time = current_time
            
            if press_count >= 3:
                game_state = 'welcome'
                press_count = 0
            
            while not btn_pin.value():
                pass  # Wait for release

        # Move the falling object down
        falling_object_y += level

        # Check for catch or miss
        if falling_object_y >= 60:
            if abs(falling_object_x - catcher_x) <= catcher_width // 2:
                score += 1
            else:
                score = 0
            level = score // 5 + 1
            falling_object_x = random.randint(0, 127)
            falling_object_y = 0

        draw_game()
        time.sleep(0.1)

