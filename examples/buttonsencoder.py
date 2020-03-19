#!/usr/bin/env python3

# pylint: disable=no-member

from config import *  # pylint: disable=unused-wildcard-import
import RPi.GPIO as GPIO
import time


def ledsEnable():
    GPIO.output(led1, True)
    GPIO.output(led2, True)
    GPIO.output(led3, True)
    GPIO.output(led4, True)


def ledsDisable():
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    GPIO.output(led3, False)
    GPIO.output(led4, False)


def buttonEncoderEnableLeds():
    while GPIO.input(buttonRed) or GPIO.input(buttonGreen):
        GPIO.output(led1, not GPIO.input(encoderLeft))
        GPIO.output(led2, not GPIO.input(encoderRight))
        GPIO.output(led3, not GPIO.input(buttonRed))
        GPIO.output(led4, not GPIO.input(buttonGreen))
    ledsEnable()
    time.sleep(1)
    ledsDisable()


def tests():
    print('\nButtons and encoder test.')
    print('Press the Red and Green buttons togehter to finish the button test.')
    buttonEncoderEnableLeds()


if __name__ == "__main__":
    tests()
    GPIO.cleanup()
