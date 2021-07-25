import os
import pyautogui
import time

# Folder location of image assets used by this example.
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

TIMEOUT=2

# open teams
pyautogui.press('winleft');
time.sleep(TIMEOUT)
pyautogui.write('teams');
time.sleep(TIMEOUT)
pyautogui.press('enter');

# wait for search GUI to be ready
search_oracle = os.path.join(ASSETS_PATH, 'teams-search-bar-start.png')
search = pyautogui.locateOnScreen(search_oracle, grayscale=True)
while search == None:
    search = pyautogui.locateOnScreen(search_oracle, grayscale=True)

# focus search, and select first result
pyautogui.hotkey('ctrl', 'e');
time.sleep(TIMEOUT)
pyautogui.write('Kelvin');
time.sleep(TIMEOUT)
pyautogui.press('down');
time.sleep(TIMEOUT)
pyautogui.press('enter');
time.sleep(TIMEOUT)

# tab left to defocus the message box
pyautogui.press('tab')
# video call hotkey
pyautogui.hotkey('ctrlleft', 'shiftleft', 'u')

