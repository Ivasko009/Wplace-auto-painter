#  -------------------
# |Wplace Auto Painter|
# |made by Ivasko009  |
#  -------------------
# 
# Make any changes you want, it's hella fast, so if it's crashing or lagging your computer, slow it down.
# If you're reading this, you probably want to do some changes, so I left some notes on what does what.


import pyautogui
import cv2
import numpy as np
import time
import threading
from pynput import keyboard
import tkinter as tk

TL_X, TL_Y = 109, 187
BR_X, BR_Y = 950, 792
REGION = (TL_X, TL_Y, BR_X - TL_X, BR_Y - TL_Y)

pyautogui.PAUSE = 0                  # Remove the ~0.1s global pause between every pyautogui call
pyautogui.FAILSAFE = False           # Optional: disable failsafe corner check overhead

TOLERANCE = 5                        # Color tolerance. Higher values result in inaccurate clicks.
PICK_DELAY = 0                       # Edit this value to add a delay between picking different colors
PAINT_DELAY = 0                      # Edit this value to add a delay between clicking pixels on the canvas
RUN_SECONDS = 0.3                    # Don't delete this or make this longer, otherwise it will go through the cycle multiple times
HOTKEY = keyboard.Key.alt_gr         # Change this if you don't like the key to activate the script

PALETTE = {                          # Whole Wplace color palette and their corresponding coordinates on the screen.
    (0, 0, 0): (37, 882),            # Change the coords if you have a different resolution than 1920*1080.
    (60, 60, 60): (98, 882),
    (120, 120, 120): (159, 884),
    (170, 170, 170): (218, 881),
    (210, 210, 210): (276, 885),
    (255, 255, 255): (336, 884),
    (96, 0, 24): (396, 883),
    (165, 14, 30): (455, 885),
    (237, 28, 36): (513, 887),
    (250, 128, 114): (575, 883),
    (228, 92, 26): (635, 885),
    (255, 127, 39): (692, 887),
    (246, 170, 9): (753, 884),
    (249, 221, 59): (813, 885),
    (255, 250, 188): (871, 886),
    (156, 132, 49): (930, 884),
    (197, 173, 49): (990, 886),
    (232, 212, 95): (1051, 887),
    (74, 107, 58): (1109, 883),
    (90, 148, 74): (1169, 885),
    (132, 197, 115): (1226, 885),
    (14, 185, 104): (1284, 885),
    (19, 230, 123): (1347, 885),
    (135, 255, 94): (1405, 886),
    (12, 129, 110): (1465, 884),
    (16, 174, 166): (1525, 882),
    (19, 225, 190): (1586, 885),
    (15, 121, 159): (1645, 883),
    (96, 247, 242): (1706, 882),
    (187, 250, 242): (1759, 886),
    (40, 80, 158): (1823, 883),
    (64, 147, 228): (1883, 881),
    (125, 199, 255): (36, 927),
    (77, 49, 184): (97, 926),
    (107, 80, 246): (158, 927),
    (153, 177, 251): (221, 925),
    (74, 66, 132): (275, 929),
    (122, 113, 196): (333, 925),
    (181, 174, 241): (396, 925),
    (120, 12, 153): (454, 925),
    (170, 56, 185): (510, 928),
    (224, 159, 249): (576, 927),
    (203, 0, 122): (633, 928),
    (236, 31, 128): (693, 930),
    (243, 141, 169): (750, 929),
    (155, 82, 73): (811, 929),
    (209, 128, 120): (871, 928),
    (250, 182, 164): (931, 929),
    (104, 70, 52): (988, 929),
    (149, 104, 42): (1051, 929),
    (219, 164, 99): (1107, 927),
    (123, 99, 82): (1172, 927),
    (156, 132, 107): (1233, 929),
    (214, 181, 148): (1287, 923),
    (209, 128, 81): (1346, 930),
    (248, 178, 119): (1408, 931),
    (255, 197, 165): (1464, 929),
    (109, 100, 63): (1527, 927),
    (148, 140, 107): (1584, 927),
    (205, 197, 158): (1643, 929),
    (51, 57, 65): (1705, 928),
    (109, 117, 141): (1762, 928),
    (179, 185, 209): (1821, 929),
} 

running = True
active = False

# I don't recommend changing anything past this point, it's just code for taking the screenshot, analyzing colors and telling your cursor where to click.

def color_mask(img_bgr, rgb, tol):
    bgr = (rgb[2], rgb[1], rgb[0])
    lower = np.array([max(0, c - tol) for c in bgr], dtype=np.uint8)
    upper = np.array([min(255, c + tol) for c in bgr], dtype=np.uint8)
    return cv2.inRange(img_bgr, lower, upper)

def stop_program():
    global running, active
    active = False
    running = False

def on_press(key):
    global active
    if key == HOTKEY and not active:
        active = True
        threading.Timer(RUN_SECONDS, stop_program).start()

def overlay():
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.attributes("-transparentcolor", "black")

    w = BR_X - TL_X
    h = BR_Y - TL_Y
    root.geometry(f"{w}x{h}+{TL_X}+{TL_Y}")

    canvas = tk.Canvas(root, width=w, height=h, bg="black", highlightthickness=0)
    canvas.pack()

    rect = canvas.create_rectangle(
        2, 2, w - 2, h - 2,
        outline="red",
        width=2,
        dash=(6, 4)
    )

    while running:
        canvas.itemconfig(rect, outline="green" if active else "red")
        root.update()
        time.sleep(0.05)

    root.destroy()

keyboard.Listener(on_press=on_press).start()
threading.Thread(target=overlay, daemon=True).start()

while running:
    if not active:
        time.sleep(0.05)
        continue

    screenshot = pyautogui.screenshot(region=REGION)
    img_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    for rgb, pick_xy in PALETTE.items():
        mask = color_mask(img_bgr, rgb, TOLERANCE)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            continue

        pyautogui.click(pick_xy[0], pick_xy[1], _pause=False)
        time.sleep(PICK_DELAY)

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if w >= 1 and h >= 1:
                cx = TL_X + x + w // 2
                cy = TL_Y + y + h // 2
                pyautogui.click(cx, cy, _pause=False)
                time.sleep(PAINT_DELAY)

    active = False
