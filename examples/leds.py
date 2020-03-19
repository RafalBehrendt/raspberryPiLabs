#!/usr/bin/env python3

# pylint: disable=no-member

from config import *  # pylint: disable=unused-wildcard-import
import RPi.GPIO as GPIO
import time


def ledsDisable():
    GPIO.output(led1, False)
    GPIO.output(led2, False)
    GPIO.output(led3, False)
    GPIO.output(led4, False)


def simpleLedTest():
    ledsDisable()

    GPIO.output(led1, True)
    time.sleep(0.5)
    GPIO.output(led2, True)
    time.sleep(0.5)
    GPIO.output(led3, True)
    time.sleep(0.5)
    GPIO.output(led4, True)
    time.sleep(1)

    ledsDisable()


def pwmTest():
    diode1 = GPIO.PWM(led1, 50)  # Nowa instancja PWM
    diode2 = GPIO.PWM(led2, 50)  # Nowa instancja PWM
    init = 1
    wypelnienie = init  # Wypełnienie sygnału PWM
    diode1.start(wypelnienie)  # Uruchomienie sygnału PWM
    diode2.start(wypelnienie)  # Uruchomienie sygnału PWM

    while True:
        wypelnienie *= 1.1
        if wypelnienie > 100:
            #wypelnienie = init
            break
        # Ustaw nową wartość wypełnienia
        diode1.ChangeDutyCycle(wypelnienie)
        diode2.ChangeDutyCycle(wypelnienie)
        time.sleep(0.02)

    diode1.stop()
    diode2.stop()


def tests():
    print('\nLED test.')
    simpleLedTest()
    pwmTest()


if __name__ == "__main__":
    tests()
    GPIO.cleanup()
