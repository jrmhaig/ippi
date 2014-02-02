#!/usr/bin/python3

import pifacedigitalio
import time
import sys

# This file determines whether or not to run the script
# If it does not exist at the start then the script exits immediately
# If it is deleted then the script exists the next time a button is pressed
go_file = '/home/pi/ippi/go'

# Start piface
try:
    pfd = pifacedigitalio.PiFaceDigital()
except:
    print("No PiFaceDigital")
    sys.exit(0)

def showNumber(n):
    """Display a number (between 0 and 255) on the 8 LEDs"""
    for i in range(7, -1, -1):
        if (2**i <= n):
            n = n - 2**i
            pfd.leds[i].turn_on()
        else:
            pfd.leds[i].turn_off()

def alert(n):
    """Flash all the lights n times"""
    for i in range(n):
        showNumber(255)
        time.sleep(0.2)
        showNumber(0)
        time.sleep(0.2)

def fail():
    """Flash all the lights forever to indicate a fault"""
    while True:
        alert(1)
        time.sleep(2)

def check_file():
    """Test for existance of the 'go' file"""
    try:
        open(go_file)
        return True
    except IOError:
        return False

def pin_number(mask):
    """Determine which pin has been pressed by the mask

    If multiple buttons are pressed return the highest pin

    """
    for i in range(7, -1, -1):
        if mask >= 2**i:
            return i

    return None

# Only carry on if the 'go' file exists
if not check_file():
    sys.exit(0)

# The script must be called as:
#    ./ippi.py <ip address>
if len(sys.argv)<2:
    print("No argument given")
    fail()

# Argument is expected to be an IP address
# <ip address> must be four integers separated by dots
bytes = sys.argv[1].split(".")
if len(bytes) != 4:
    print("Could not understand argument")
    fail()

# Convert to integers
for i in range(4):
    try:
        bytes[i] = int(bytes[i])
    except:
        print(bytes[i], "is not an integer")
        fail()

# Alert that we are awake
alert(3)

# Show the first byte
showNumber(bytes[0])

while check_file():
    # Wait until the button has been released (since last time)
    event = pfd.input_port.value
    while event != 0:
        event = pfd.input_port.value
        time.sleep(0.001)

    # Wait for a button to be pressed
    while event == 0:
        event = pfd.input_port.value

    print(event)
    # Display the byte corresponding to the button pressed
    showNumber(bytes[pin_number(event)])

# Clean up
showNumber(0)
deinit()
