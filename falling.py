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

# Game variables
catcher_x = 64
catcher_width = 20
score = 0
level = 1
falling_object_x = 0
falling_object_y = 0

# Rotary encoder state
encoder_prev_state = (ang_a_pin.value() << 1) | ang_b_pin.value()
encoder_accum = 0

# Valid quadrature transitions mapped to movement deltas.
ENCODER_DELTA = {
    0b0001: -1,
    0b0111: -1,
    0b1110: -1,
    0b1000: -1,
    0b0010: 1,
    0b1011: 1,
    0b1101: 1,
    0b0100: 1,
}

# Game state
game_state = 'welcome'  # 'welcome' or 'playing'

# Triple-press detection
last_press_time = 0
press_count = 0

def is_start_button_pressed():
    """Accept either the dedicated button or encoder center click as start/exit input."""
    return (btn_pin.value() == 0) or (sw_c_pin.value() == 0)

def wait_for_button_release():
    """Block until both buttons are released to avoid repeated triggers."""
    while is_start_button_pressed():
        time.sleep_ms(5)

def reset_game():
    """Resets the game variables to their initial state."""
    global score, level, falling_object_x, falling_object_y, catcher_x
    score = 0
    level = 1
    falling_object_x = random.randint(0, 127)
    falling_object_y = 0
    catcher_x = 64

def update_encoder():
    global catcher_x, encoder_prev_state, encoder_accum
    current_state = (ang_a_pin.value() << 1) | ang_b_pin.value()
    transition = (encoder_prev_state << 2) | current_state
    delta = ENCODER_DELTA.get(transition, 0)
    moved = False

    if delta:
        encoder_accum += delta
        # Most encoders generate 4 transitions per detent.
        if encoder_accum >= 4:
            catcher_x = max(catcher_width // 2, min(127 - catcher_width // 2, catcher_x + 5))
            encoder_accum = 0
            moved = True
        elif encoder_accum <= -4:
            catcher_x = max(catcher_width // 2, min(127 - catcher_width // 2, catcher_x - 5))
            encoder_accum = 0
            moved = True

    encoder_prev_state = current_state
    return moved

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
last_fall_time = time.ticks_ms()

while True:
    if game_state == 'welcome':
        draw_welcome_screen()
        if is_start_button_pressed():
            time.sleep_ms(30)
            if not is_start_button_pressed():
                continue
            reset_game()
            game_state = 'playing'
            wait_for_button_release()
    
    elif game_state == 'playing':
        moved_catcher = update_encoder()

        # Check for button press (for exiting)
        current_time = time.ticks_ms()
        if is_start_button_pressed():
            time.sleep_ms(30)
            if not is_start_button_pressed():
                continue
            if time.ticks_diff(current_time, last_press_time) > 300:
                press_count = 1
            else:
                press_count += 1
            last_press_time = current_time
            
            if press_count >= 3:
                game_state = 'welcome'
                press_count = 0
            
            wait_for_button_release()

        frame_due = False
        if time.ticks_diff(current_time, last_fall_time) >= 100:
            frame_due = True
            last_fall_time = current_time

            # Move the falling object down on a fixed interval.
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

        if moved_catcher or frame_due:
            draw_game()

        time.sleep_ms(5)

