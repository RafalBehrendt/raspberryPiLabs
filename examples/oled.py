#!/usr/bin/env python3

import os
import time
import traceback

from PIL import Image, ImageDraw, ImageFont

import config
import lib.oled.config as oledconfig
import lib.oled.SSD1331 as SSD1331


def oledtest():
    disp = SSD1331.SSD1331()

    # Initialize library.
    disp.Init()
    # Clear display.
    disp.clear()

    # Create blank image for drawing.
    image1 = Image.new("RGB", (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    fontLarge = ImageFont.truetype('./lib/oled/Font.ttf', 20)
    fontSmall = ImageFont.truetype('./lib/oled/Font.ttf', 13)
    print("- draw line")
    draw.line([(0, 0), (0, 63)], fill="BLUE", width=5)
    draw.line([(0, 0), (95, 0)], fill="BLUE", width=5)
    draw.line([(0, 63), (95, 63)], fill="BLUE", width=5)
    draw.line([(95, 0), (95, 63)], fill="BLUE", width=5)
    print("- draw rectangle")
    draw.rectangle([(5, 5), (90, 30)], fill="BLUE")

    print("- draw text")
    draw.text((8, 0), u'ąćęńł', font=fontLarge, fill="WHITE")
    draw.text((12, 40), 'Hello!!!', font=fontSmall, fill="BLUE")

    # image1 = image1.rotate(45)
    disp.ShowImage(image1, 0, 0)
    time.sleep(2)

    print("- draw image")
    image = Image.open('./lib/oled/pic.jpg')
    disp.ShowImage(image, 0, 0)
    time.sleep(2)

    disp.clear()
    disp.reset()


def test():
    print('\nOLED screen test.')
    oledtest()


if __name__ == "__main__":
    test()
