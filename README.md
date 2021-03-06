ippi
====

If you have your Raspberry Pi set up to use DHCP and you connect it to a new
network you have the problem of how to log into it remotely. If you are able
to connect a monitor then you can see it displayed on the screen but what
happens if it is headless?

The [PiFace](http://pi.cs.man.ac.uk/interface.htm) is an add-on board that
provides 8 digital outputs, 8 digital inputs and 2 relays. Additionally, there
are 8 LEDs linked to the outputs and 4 buttons linked to the first four of the
inputs. This is perfect for displaying an IPv4 IP address, made up of four
integers between 0 and 255. Each number can be represented in binary by the
eight LEDs and each of the numbers can be selected by pressing one of the four
buttons.

Running ippi
------------

ippi will only run if an input is on at the start - i.e., at least one of the
buttons is pressed. This is so that it can be used as required on boot (see
below).

Copy ippi.py into /home/pi/ippi/ and execute it as:

    $ /home/pi/ippi/ippi.py 10.3.192.1

Where '10.3.192.1' is the IP address to display. All LEDs should flash three
times and then display the first number (10) in binary (00001010). Press the
second button, S2, and the LEDs will change to display the second number (3)
in binary (00000011). Likewise, S3 and S4 will display the third and fourth
numbers respectively.

To exit ippi (without pressing Ctrl-C) press two buttons simultaneously.

If there is an error then all eight lights will flash slowly until the ippi is
killed with Ctrl-C.

Run ippi on boot
----------------

Modify /etc/rc.local to look like:

    #!/bin/sh -e
    #
    # rc.local
    #
    # This script is executed at the end of each multiuser runlevel.
    # Make sure that the script will "exit 0" on success or any other
    # value on error.
    #
    # In order to enable or disable this script just change the execution
    # bits.
    #
    # By default this script does nothing.
    
    # Try to find the IP address
    # Try 10 time to take account of slow DHCP
    N=0
    while [ ! "$_IP" -a $N -lt 10 ]
    do
      _IP=$(hostname -I) || true
      N=$((N+1))
      sleep 1
    done

    # Print the IP address
    if [ "$_IP" ]; then
      printf "My IP address is %s\n" "$_IP"
    fi

    # Use the PiFace to display the IP address
    python3 /home/pi/ippi/ippi.py $_IP &
    
    exit 0

When you want ippi to run on boot, hold down any of the buttons during boot up
until the LEDs flash three times.

Install on new image
--------------------

If you have a new SD card and want to use ippi you will need to set it up while it is mounted on another computer. A relatively recent version of Raspbian has all the necessary python modules already installed and so the set up is relatively straightforward.

Find the root partition (usually the second partition) and copy ippi.py to:

    <root partition mount>/home/pi/ippi/ippi.py

You will need to create the directory `<root partition mount>/home/pi/ippi` first. Then find

    <root partition mount>/etc/rc.local

and modify it as shown in the "Run ippi on boot" section above.

Finally, edit the file:

    <root partition mount>/modprobe.d/raspi-blacklist.conf

and remove the line:

    blacklist spi-bcm2708

This will enable the SPI kernel module, which is required for the PiFace Digital.

Reboot and hold one of the PiFace buttons pressed until the LEDs flash.

Some useful numbers in binary
-----------------------------

Local networks usually have IP addresses in one of three formats:

* 10.x.x.x
* 172.16.x.x to 172.31.x.x
* 192.168.x.x

First, check the first byte:

| Decimal |  Binary  |
| ------- | -------- |
| 10      | 00001010 |
| 172     | 10101100 |
| 192     | 11000000 |

If the first byte is 10 then the remaining bytes may have any value.

If the first byte is 172 then the second byte should be between 16 and 31:

| Decimal |  Binary  |
| ------- | -------- |
| 16      | 00010000 |
| 17      | 00010001 |
| 18      | 00010010 |
| 19      | 00010011 |
| 20      | 00010100 |
| 21      | 00010101 |
| 22      | 00010110 |
| 23      | 00010111 |
| 24      | 00011000 |
| 25      | 00011001 |
| 26      | 00011010 |
| 27      | 00011011 |
| 28      | 00011100 |
| 29      | 00011101 |
| 30      | 00011110 |
| 31      | 00011111 |

The remaining two bytes may have any value.

If the first byte is 192 then the second byte should be 168:

| Decimal |  Binary  |
| ------- | -------- |
| 168     | 10101000 |

The remaining two bytes may have any value.

To do
-----

* Put all the functions in a module to tidy up the code.
 * Then create a new module for PiFace Control and Display. (Other boards?)
* Detect IP address rather than require it to be passed in as an argument.
