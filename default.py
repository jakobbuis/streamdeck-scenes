#!/usr/bin/env python3

import os
import psutil
import pyautogui
import threading

from PIL import Image, ImageDraw, ImageFont
from src.StreamDeck.DeviceManager import DeviceManager
from src.StreamDeck.ImageHelpers import PILHelper

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

# Global state management
class State:
    microphone = False

state = State()

# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, icon_filename, label_text):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    icon = Image.open(icon_filename)
    margins = [0, 0, 20, 0] if label_text else [5, 5, 5, 5]
    image = PILHelper.create_scaled_image(deck, icon, margins=margins)

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(os.path.join(ASSETS_PATH, 'roboto-regular.ttf'), 14)
    if label_text:
        draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)

def key_image(deck, key, asset, title = None):
    assetpath = os.path.join(ASSETS_PATH, asset)
    image = render_key_image(deck, assetpath, title)
    with deck:
        deck.set_key_image(key, image)

def is_running(program):
    for p in psutil.process_iter(attrs=['pid', 'name']):
        if p.info['name'] == program:
            return True
    return False

def run_if_not(program, command = None):
    if is_running(program) == False:
        os.system(command or program)

def key_change(deck, key, direction):
    # only operate on key down
    if direction != 1:
        return

    if key == 0:
        pyautogui.hotkey('winleft', '1')
    elif key == 1:
        pyautogui.hotkey('winleft', '4')
    elif key == 2:
        pyautogui.hotkey('shift', 'ctrl', 'alt', 'F9') # global ubuntu hotkey mic on/off
        state.microphone = not state.microphone
        key_image(deck, 2, ('microphone-on.png' if state.microphone else 'microphone-off.png'))
    elif key == 4:
        os.system('systemctl suspend')
    elif key == 10:
        run_if_not('spotify')
    elif key == 11:
        pyautogui.hotkey('shift', 'ctrl', 'alt', 'F12') # global ubuntu hotkey play/pause
    elif key == 12:
        pyautogui.hotkey('shift', 'ctrl', 'alt', 'F1') # global ubuntu hotkey next track
    elif key == 13:
        pyautogui.hotkey('shift', 'ctrl', 'alt', 'F8') # global ubuntu hotkey volume down
    elif key == 14:
        pyautogui.hotkey('shift', 'ctrl', 'alt', 'F11') # global ubuntu hotkey volume up

if __name__ == "__main__":
    for index, deck in enumerate(DeviceManager().enumerate()):
        deck.open()
        deck.reset()

        # Set initial screen brightness to 30%.
        deck.set_brightness(50)

        # render keys
        key_image(deck, 0, 'firefox.png')
        key_image(deck, 1, 'vs-code.png')
        key_image(deck, 2, 'microphone-off.png')
        key_image(deck, 4, 'power.png')
        key_image(deck, 10, 'spotify.png')
        key_image(deck, 11, 'play-pause.png')
        key_image(deck, 12, 'next.png')
        key_image(deck, 13, 'volume-down.png')
        key_image(deck, 14, 'volume-up.png')

        # actions
        deck.set_key_callback(key_change)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()
