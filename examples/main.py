#!/usr/bin/env python3

import os

import RPi.GPIO as GPIO

import buttonsencoder
import buzzer
import leds
import thermometers
import ws2812
import oled
import rfid


def main():
    print('The whole device test.')
    if os.getuid() == 0:
        ws2812.test()
    else:
        print("WS2812 test ommited - root/sudo privileges demanded.")
    buzzer.test()
    oled.test()
    leds.tests()
    buttonsencoder.tests()
    thermometers.test()
    rfid.test()

    GPIO.cleanup()  # pylint: disable=no-member


if __name__ == "__main__":
    main()
