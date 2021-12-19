#!/usr/bin/env python3

import os
import psutil
import pyautogui
import threading
import subprocess

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

def microphone_set_state_icon():
    mic_on = subprocess.check_output(['pulsemixer', '--id', '3', '--get-mute']) == b'0\n'
    file = 'microphone-on.png' if mic_on else 'microphone-off.png'
    key_image(deck, 7, file)

def key_change(deck, key, direction):
    # only operate on key down
    if direction != 1:
        return

    if key == 0:
        pyautogui.hotkey('winleft', '1')
    elif key == 1:
        pyautogui.hotkey('winleft', '4')
    elif key == 7:
        os.system('pulsemixer --id 3 --toggle-mute')
        microphone_set_state_icon()
    elif key == 4:
        os.system('systemctl suspend')

if __name__ == "__main__":
    for index, deck in enumerate(DeviceManager().enumerate()):
        deck.open()
        deck.reset()

        # Set initial screen brightness to 30%.
        deck.set_brightness(50)

        # render keys
        key_image(deck, 0, 'firefox.png')
        key_image(deck, 1, 'vs-code.png')
        key_image(deck, 4, 'power.png')
        microphone_set_state_icon()

        # actions
        deck.set_key_callback(key_change)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()
