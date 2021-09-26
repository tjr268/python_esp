## CHANGE HANDLERS AND HANDLER TABLE HERE DONT TOUCH MAIN

from machine import Pin
import neopixel
import time
import color_dict

# CONSTANTS
TEST_LED_PIN = 2
NUMBER_OF_LEDS = 60 # for my tube light
LED_STRIP_PIN = 14


# Handlers should take two inputs command and values
    # command is a string -> first thing after ip in url
    # values is a list of strings -> all things after ip sep by "/"

def test_led_handler(command, values):
    # do operation return success string
    # values is alwasy a list
    value = values[0]
    test_led = Pin(TEST_LED_PIN, Pin.OUT)
    if int(value) == 1:
        test_led.value(0)
        return "Success"
    elif int(value) == 0:
        test_led.value(1)
        return "Success"
    else:
        return "Failed: Must be 0 or 1"
   

def rgb_handler(command, values):
    # do operation return success string
    # values is alwasy a list
    # NOTE values is r,g,b in order
    output_string = "Nothing happended"
    try: 
        for color_string in values:
            if int(color_string) not in range(256):
                output_string = "Failed: rgb values must be between 0, 255"
                return output_string
        pin = Pin(LED_STRIP_PIN, Pin.OUT)
        pixels = neopixel.NeoPixel(pin, NUMBER_OF_LEDS, bpp=3, timing=1)
        r = int(values[0])
        g = int(values[1])
        b = int(values[2])
        pixels.fill((r, g, b))
        pixels.write()
        output_string = "Success"
    except Exception as e:
        output_string = "Failed: must have 3 inputs, all integers"
    
    return output_string

def color_handler(command, values):
    # do operation return success string
    # values is alwasys a list
    color_name = values[0]
    if color_name not in color_dict.COLOR_DICT.keys():
        output_string = "Failed: color not found"
        return output_string
    pin = Pin(LED_STRIP_PIN, Pin.OUT)
    pixels = neopixel.NeoPixel(pin, NUMBER_OF_LEDS, bpp=3, timing=1)
    rgb = color_dict.COLOR_DICT[color_name]
    pixels.fill(tuple(rgb))
    pixels.write()
    output_string = "Success"

    return output_string


HANDLER_TABLE = {
    "testled": test_led_handler,
    "color": color_handler,
    "rgb": rgb_handler
}