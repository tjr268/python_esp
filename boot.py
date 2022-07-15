# Complete project details at https://RandomNerdTutorials.com

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network
import time
import creds
import gc
gc.collect()

#### BLINK FUNCTION CONTROLS #####
BLUE_WIFI_LED = Pin(2, Pin.OUT)
BOARD_ADDRESS = "Not Initiated"

def blink(number, delay=300):
  while number > 0:
    BLUE_WIFI_LED.off()
    time.sleep_ms(delay)
    BLUE_WIFI_LED.on()
    time.sleep_ms(delay)
    number -= 1

#### MAIN ####
def boot():
  SSID = creds.SSID
  PASSWORD = creds.PASSWORD

  station = network.WLAN(network.STA_IF)

  station.active(True)
  station.connect(SSID, PASSWORD)

  while station.isconnected() == False:
    pass

  print('Connection successful')
  BOARD_ADDRESS = station.ifconfig()[0]
  print("Board Address: " + BOARD_ADDRESS)

  time.sleep(5)

  # blink last number of ip 
  ip_final = int(BOARD_ADDRESS.split(".")[-1]) + 1
  blink(ip_final, delay=450)

  print("Boot Done")

  # delay for setup
  time.sleep(4)

if __name__ == "__main__":
  boot()