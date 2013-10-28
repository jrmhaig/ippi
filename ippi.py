#!/usr/bin/python

from piface.pfio import *
from sys import argv, exit

# This file determines whether or not to run the script
# If it does not exist at the start then the script exits immediately
# If it is deleted then the script exists the next time a button is pressed
go_file = '/home/pi/ippi/go'

# Display a number (between 0 and 255) on the 8 LEDs
def showNumber(n):
    for i in range(7, -1, -1):
        if (2**i <= n):
            n = n - 2**i
            digital_write(i,1)
        else:
            digital_write(i,0)

# Flash all the lights n times
def alert(n):
    for i in range(n):
        showNumber(255)
        sleep(0.2)
        showNumber(0)
        sleep(0.2)

# Flash all the lights forever to indicate a fault
def fail():
    while True:
        alert(1)
        sleep(2)

# Test for existance of the 'go' file
def check_file():
    try:
        open(go_file)
        return True
    except IOError:
        return False

# Only carry on if the 'go' file exists
if not check_file():
    exit(0)

# Start piface
init()

# The script must be called as:
#    ./ippi.py <ip address>
if len(argv)<2:
    print "No argument given"
    fail()

# Argument is expected to be an IP address
# <ip address> must be four integers separated by dots
bytes = argv[1].split(".")
if len(bytes) != 4:
    print "Could not understand argument"
    fail()

# Convert to integers
for i in range(4):
    try:
        bytes[i] = int(bytes[i])
    except:
        print bytes[i] + " is not an integer"
        fail()

# Alert that we are awake
alert(3)

# Show the first byte
showNumber(bytes[0])

while check_file():
    # Wait until the button has been released (since last time)
    event = read_input()
    while event != 0:
        event = read_input()
        sleep(0.001)

    # Wait for a button to be pressed
    while event == 0:
        event = read_input()

    # Display the byte corresponding to the button pressed
    showNumber(bytes[get_pin_number(event)])

# Clean up
showNumber(0)
deinit()
