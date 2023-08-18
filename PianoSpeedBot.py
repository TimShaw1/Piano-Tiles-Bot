import pyautogui
from utility import *
import keyboard
import time
import mouse
import array as arr
import msvcrt

pyautogui.PAUSE = 0
dim = get_dimensions()

def move_mouse(x, y):
    mouse.move(x, y, absolute=True)

x1 = dim[0] + round(dim[2] / 6)
x2 = dim[0] + round(dim[2] / 2.6)
x3 = dim[0] + round(dim[2] / 2)
x4 = dim[0] + round(dim[2] / 1.4)
y = dim[1] + round(dim[3] / 1.4)

offset = 0.32
x_list = arr.array("i", [x1, x2, x3, x4])

start_col = (49, 158, 198)
black = (0,0,0)
hold_col = (0, 130, 222)

for i in range(4):
    pixel = getpixel(x_list[i], y)
    if get_max_pixel_diff(pixel, start_col) < 3:
        pyautogui.click(x_list[i], y)

y = dim[1] + round(dim[3] / 2)

hold_flag = False
hold_i = -1

is_down = False
click_ctr = 1
offset = 0 # pixels

# Main loop
while not keyboard.is_pressed("`"):
    if click_ctr > 100:
        click_ctr = 1
        offset += 2
    for i in range(4):
        pixel = getpixel(x_list[i], y)
        if get_max_pixel_diff(pixel, black) < 30:
            move_mouse(x_list[i], y + offset)
            mouse.click()
            click_ctr += 1