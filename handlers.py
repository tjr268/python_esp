'''LED HANDLERS
This script contains all handler functions for the LED BAR. Each project will
have a different handlers file but use the common main.py and boot.py file. 

Define functions to control board/hardware here then add an entry in the 
HANDLER_TABLE dict to specify the key word to invoke the function via
HTTP. 

When the board receives a GET request it parses the URI and the first entry
will be matched to the HANDLER_TABLE to determine which function should be 
invoked then any further entries in the URI will be appended to a list 
and passed to the handler function as a list.

Example: if the URI is /rgb/255/255/255 then the list ['255', '255', '255]
will be passed to whatever function is mapped to the "rgb" endpoint in 
HANDLERS_TABLE.

Note all handlers must return a tuple: (bool, string) where the boolean 
value is False if operation failed and True if operation succeeded. The string 
should be a description which will be sent to the client in the response body.
'''


from machine import Pin
import neopixel
import time
import color_dict

# CONSTANTS
TEST_LED_PIN = 2
NUMBER_OF_LEDS = 60 # for my tube light
LED_STRIP_PIN = 14


def test_led_handler(values):
    # do operation return success string
    # values is alwasy a list
    value = values[0]
    test_led = Pin(TEST_LED_PIN, Pin.OUT)
    if int(value) == 1:
        test_led.value(0)
        return (True, "TestLED command received. Blue LED: ON")
    elif int(value) == 0:
        test_led.value(1)
        return (True, "TestLED command received. Blue LED: OFF")
    else:
        return (False, "Failed: Must be 0 or 1")
   

def rgb_handler(values):
    # do operation return success string
    # values is alwasy a list
    # NOTE values is r,g,b in order
    output_tuple = (False, "No operation attempted")
    try: 
        for color_string in values:
            if int(color_string) not in range(256):
                output_tuple = (False, "Failed: rgb values must be between 0, 255")
                return output_tuple
        pin = Pin(LED_STRIP_PIN, Pin.OUT)
        pixels = neopixel.NeoPixel(pin, NUMBER_OF_LEDS, bpp=3, timing=1)
        r = int(values[0])
        g = int(values[1])
        b = int(values[2])
        pixels.fill((r, g, b))
        pixels.write()
        output_tuple = (True, "RGB command reveived. RGB: " + ", ".join(values))
    except Exception as e:
        output_tuple = (False, "Failed: must have 3 inputs, all integers")

    return output_tuple

def color_handler(values):
    # do operation return success string
    # values is alwasys a list
    color_name = values[0]
    if color_name not in color_dict.COLOR_DICT.keys():
        output_tuple = (False, "Failed: color not found")
        return output_tuple
    pin = Pin(LED_STRIP_PIN, Pin.OUT)
    pixels = neopixel.NeoPixel(pin, NUMBER_OF_LEDS, bpp=3, timing=1)
    rgb = color_dict.COLOR_DICT[color_name]
    pixels.fill(tuple(rgb))
    pixels.write()
    output_tuple = (True, "Color command reveived. Color: " + color_name)

    return output_tuple


HANDLER_TABLE = {
    "testled": test_led_handler,
    "color": color_handler,
    "rgb": rgb_handler
}