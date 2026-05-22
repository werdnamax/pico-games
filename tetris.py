'''
A tetris game implemented in Python for the Raspberry Pi Pico.
The game features a grid where players can move and rotate falling tetrominoes to create complete lines.
The game ends when the stack of tetrominoes reaches the top of the grid.
Players earn points for each completed line, and the game continues until the blocks reach the top of the grid. The game uses an OLED display to show the game state and a rotary encoder for user input.
The code includes functions for handling user input, updating the game state, and rendering the graphics on the screen.

The game uses the rotary encoder for input... 
* Rotate the encoder to move the tetromino left or right.
* Press the encoder button to rotate the tetromino.
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
grid_width = 10
grid_height = 15
cell_size = 4
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
current_piece = None
current_x = 0
current_y = 0
score = 0
level = 1
next_piece = None

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

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Game state
game_state = 'welcome'  # 'welcome' or 'playing'
last_fall_time = 0

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
    global score, level, current_piece, current_x, current_y, grid
    score = 0
    level = 1
    current_piece = None
    current_x = 0
    current_y = 0
    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    new_piece()

def draw_grid():
    """Draws the game grid and current piece on the OLED display."""
    oled.fill(0)
    # Draw a border around the grid
    oled.rect(0, 0, grid_width * cell_size + 2, grid_height * cell_size + 2, 1)
    # Draw the grid
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x]:
                oled.fill_rect(x * cell_size, y * cell_size, cell_size, cell_size, 1)
    # Draw the current piece
    if current_piece:
        for y in range(4):
            for x in range(4):
                if current_piece[y][x]:
                    oled.fill_rect((current_x + x) * cell_size, (current_y + y) * cell_size, cell_size, cell_size, 1)
    # Draw score and level
    oled.text(f'Score:{score}', 70, 0)
    oled.text(f'Level:{level}', 70, 10)
    oled.text('Next:', 70, 20)
    if next_piece:
        for y in range(4):
            for x in range(4):
                if next_piece[y][x]:
                    oled.fill_rect(70 + x * cell_size, 30 + y * cell_size, cell_size, cell_size, 1)
    oled.show()

def update_encoder():
    global current_x, encoder_prev_state, encoder_accum
    current_state = (ang_a_pin.value() << 1) | ang_b_pin.value()
    transition = (encoder_prev_state << 2) | current_state
    delta = ENCODER_DELTA.get(transition, 0)
    moved = False

    if delta:
        encoder_accum += delta
        # Most encoders generate 4 transitions per detent.
        if abs(encoder_accum) >= 4:
            move_steps = encoder_accum // 4
            new_x = current_x + move_steps
            if not check_collision(current_piece, new_x, current_y):
                current_x = new_x
                moved = True
            encoder_accum -= move_steps * 4
            
    encoder_prev_state = current_state
    return moved

def draw_welcome_screen():
    oled.fill(0)
    oled.text('Tetris Game', 15, 20)
    oled.text('Press to Start', 10, 40)
    oled.show()

def draw_game_over_screen():
    oled.fill(0)
    oled.text('Game Over', 25, 20)
    oled.text(f'Score: {score}', 10, 40)
    oled.show()

def _generate_piece():
    """Generates a new random tetromino as a 4x4 grid."""
    shape = random.choice(SHAPES)
    piece = [[0] * 4 for _ in range(4)]
    shape_h = len(shape)
    shape_w = len(shape[0])
    for r in range(shape_h):
        for c in range(shape_w):
            if shape[r][c]:
                piece[r][c] = 1
    return piece

def new_piece():
    """Sets a new piece and generates the next one."""
    global current_piece, next_piece, current_x, current_y, game_state
    
    if next_piece is None:
        current_piece = _generate_piece()
        next_piece = _generate_piece()
    else:
        current_piece = next_piece
        next_piece = _generate_piece()

    current_x = grid_width // 2 - 2
    current_y = 0
    
    if check_collision(current_piece, current_x, current_y):
        game_state = 'game_over'

def check_collision(piece, x, y):
    """Checks if the piece collides with the grid or boundaries."""
    for r in range(4):
        for c in range(4):
            if piece[r][c]:
                # Check boundaries
                if not (0 <= x + c < grid_width and 0 <= y + r < grid_height):
                    return True
                # Check grid collision
                if grid[y + r][x + c]:
                    return True
    return False

def rotate_piece(piece):
    """Rotates a piece 90 degrees clockwise."""
    new_piece = [[0] * 4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            new_piece[c][3 - r] = piece[r][c]
    return new_piece

def lock_piece():
    """Locks the current piece into the grid."""
    global grid
    for r in range(4):
        for c in range(4):
            if current_piece[r][c]:
                grid[current_y + r][current_x + c] = 1
    clear_lines()

def clear_lines():
    """Clears completed lines and updates the score."""
    global grid, score, level
    lines_cleared = 0
    new_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    new_row_idx = grid_height - 1

    for r in range(grid_height - 1, -1, -1):
        if sum(grid[r]) < grid_width:
            new_grid[new_row_idx] = grid[r]
            new_row_idx -= 1
        else:
            lines_cleared += 1
    
    if lines_cleared > 0:
        score += (10 * lines_cleared) * level
        level = score // 50 + 1
        grid = new_grid

reset_game()

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
        moved = update_encoder()
        
        # Handle rotation
        if sw_c_pin.value() == 0:
            rotated = rotate_piece(current_piece)
            if not check_collision(rotated, current_x, current_y):
                current_piece = rotated
                moved = True
            while sw_c_pin.value() == 0:
                time.sleep_ms(10)

        # Gravity
        fall_speed = max(100, 500 - (level - 1) * 50)
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, last_fall_time) > fall_speed:
            if not check_collision(current_piece, current_x, current_y + 1):
                current_y += 1
            else:
                lock_piece()
                new_piece()
            last_fall_time = current_time
            moved = True

        if moved:
            draw_grid()
        
        time.sleep_ms(10)

    elif game_state == 'game_over':
        draw_game_over_screen()
        if is_start_button_pressed():
            wait_for_button_release()
            reset_game()
            game_state = 'playing'
