#!/usr/bin/env python3

#
# Quick way to call specific people
#

import os
import threading

from PIL import Image, ImageDraw, ImageFont
from src.StreamDeck.DeviceManager import DeviceManager
from src.StreamDeck.ImageHelpers import PILHelper

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")


# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, icon_filename, label_text):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_image(deck, icon, margins=[0, 0, 20, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(os.path.join(ASSETS_PATH, 'roboto-regular.ttf'), 14)
    draw.text((image.width / 2, image.height - 5), text=label_text, font=font, anchor="ms", fill="white")

    return PILHelper.to_native_format(deck, image)

def key_image(deck, key, asset, title):
    assetpath = os.path.join(ASSETS_PATH, asset)
    image = render_key_image(deck, assetpath, title)
    with deck:
        deck.set_key_image(key, image)

def key_change(deck, key, state):
    if key == 0:
        # restart vagrant
        # open terminal
        # layout screen
        os.system('firefox')
        os.system('code')
        os.system('terminal')
    elif key == 4:
        os.system('systemctl suspend')

if __name__ == "__main__":
    for index, deck in enumerate(DeviceManager().enumerate()):
        deck.open()
        deck.reset()

        # Set initial screen brightness to 30%.
        deck.set_brightness(50)

        # render keys
        key_image(deck, 0, 'vs-code.png', 'Build')
        key_image(deck, 4, 'pause.png', 'Suspend')

        # actions
        deck.set_key_callback(key_change)

        # Wait until all application threads have terminated (for this example,
        # this is when all deck handles are closed).
        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()
