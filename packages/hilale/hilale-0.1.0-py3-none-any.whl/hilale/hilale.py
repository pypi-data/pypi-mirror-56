import pyautogui as pg
import random
from datetime import datetime
from time import sleep
import os

offset = 10
pg.PAUSE = 2.5
pg.FAILSAFE = False
screenWidth, screenHeight = pg.size()


def run():
    print("Hilale: Keeps the mouse running...")

    try:
        while True:
            rand_width = random.randint(offset, screenWidth - offset)
            rand_height = random.randint(offset, screenHeight - offset)
            pg.moveTo(rand_width, rand_height, 2, pg.easeInElastic)
            print((rand_width, rand_height))
            now = datetime.now()
            if now.minute % 5 == 0:
                print("Mouse Click & Sleep")
                pg.click(screenWidth / 2, screenHeight / 2)
                sleep(30)
    except KeyboardInterrupt:
        print("Over!!!\n")

    os.system("pause")
