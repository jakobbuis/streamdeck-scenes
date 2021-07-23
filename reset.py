#!/usr/bin/env python3

#
# Reset all attached decks
#
from src.StreamDeck.DeviceManager import DeviceManager

if __name__ == "__main__":
    streamdecks = DeviceManager().enumerate()

    for index, deck in enumerate(streamdecks):
        deck.open()
        deck.reset()
        deck.set_brightness(100)
        deck.close()
        print("Reset Streamdeck {}".format(deck.id()))
