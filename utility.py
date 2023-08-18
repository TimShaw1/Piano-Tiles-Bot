import win32.lib.win32con as win32con
import win32.win32gui as win32gui
import pyautogui
import ctypes
import copy
from PIL import Image
from typing import Union
import numpy
from ctypes import windll
dc= windll.user32.GetDC(0)

ctypes.windll.user32.SetProcessDPIAware()

def get_window_name() -> str:
    """
    Gets the full window name of Bluestacks

    Returns
    ----------
        str
            the name of the Bluestacks window
    """
    windows = pyautogui.getAllWindows()
    for w in windows:
        if "Blue" in w.title:
            return w.title

def get_screenshot(dimensions: list[int] | None = None, window_title: str = get_window_name()) -> Image:
    """
    Gets a screenshot of the given window within the given dimensions

    Parameters
    ----------
        dimensions : tuple[int], optional
            the `[x, y, w, h]` dimensions of where to get the screenshot
        window_title : str, optional
            the title of the window

    Returns
    ----------
        im : Image
            the screenshot of the screen

    Raises
    ----------
        ValueError
            The window title was incorrect or the window was not open
    """
    if window_title:

        hwnd = win32gui.FindWindow(None, get_window_name())
        if hwnd and not dimensions:
            win32gui.SetForegroundWindow(hwnd)
            x, y, x1, y1 = win32gui.GetClientRect(hwnd)
            x, y = win32gui.ClientToScreen(hwnd, (x, y))
            x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
            im = pyautogui.screenshot(region=(x, y, x1, y1))
            return im
        elif dimensions:
            im = pyautogui.screenshot(region=dimensions)
            return im
        else:
            raise ValueError("Window Not found")
    else:
        im = pyautogui.screenshot()
        return im
    
def getpixel(x,y):
    return tuple(int.to_bytes(windll.gdi32.GetPixel(dc,x,y), 3, "little"))
    
def get_dimensions(window_title: str = get_window_name()) -> list[int]:
    """
    Returns the `[x, y, w, h]` dimensions of the window
    
    Parameters
    ----------
    window_title: str, optional
        the name of the window

    Returns
    ----------
    tuple[int]
        the `[x, y, w, h]` dimensions of the window

    Raises
    ----------
    ValueError
        If window is not open or title is incorrect
    """
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetForegroundWindow(hwnd)
        x, y, x1, y1 = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (x, y))
        x1, y1 = win32gui.ClientToScreen(hwnd, (x1 - x, y1 - y))
        return[x,y,x1,y1]
    else:
        raise ValueError("Window Not found")


def get_screen_coords() -> None:
    """
    Utility function that prints the current mouse position indefinitely
    """
    while True:
        print(pyautogui.position(), end='\r')

def get_screen_ratio(dim: list[int]) -> None:
    """
    Utility function that prints the current mouse position as a ratio indefinitely.
    - The ratio is `(window_width / (pos.x - window_x), window_height / (pos.y - window_y))` rounded to the nearest integer
    """
    while True:
        print(round(abs(dim[2] / (pyautogui.position().x - dim[0])), 2), round(abs(dim[3] / (pyautogui.position().y - dim[1])), 2), end='\r')

def get_max_pixel_diff(pixel: tuple[int], col: tuple[int]) -> int:
    """
    Utility function that gets the max difference between two colors
    """
    return max(abs(numpy.subtract(pixel, col)))