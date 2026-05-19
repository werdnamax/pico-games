
# my script which prints "Hello CPTR480" to the OLED display
import machine
import time
from ssd1306 import SSD1306_I2C

# sda is GP12 and scl is GP13 on the Pico
i2c = machine.I2C(0, scl=machine.Pin(13), sda=machine.Pin(12))
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("Hello CPTR480", 0, 0)
oled.show()
# comment out to keep the messages on the screen indefinitely
# time.sleep(10)  # Wait for 10 seconds
# oled.poweroff()