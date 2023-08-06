.. contents:: Table of Contents:

About
-----

USBdev is a USB device recognition tool on Linux.

How works
---------

The tool compares the USB devices that are connected before and after.

USBdev use `linux-usb.org <http://www.linux-usb.org/usb-ids.html>`_ repository to get
data devices.

 
Install
-------

.. code-block:: bash

    $ pip install USBdev
    
    or

    $ pip install USBdev-<version>.tar.gz


Uninstall
---------

.. code-block:: bash

    $ pip uninstall USBdev


Usage
-----

.. code-block:: bash

    $ usbdev
    Plugin USB device(s) now .......Done
    Found: Vendor(s)                    Device(s)
    1:     Kingston Technology (0951)   DataTraveler 100 (1607)

    
    
    Using the time to connect and recognize multiple devices.
    
    $ usbdev --time 10
    Plugin USB device(s) now .......Done
    Found: Vendor(s)                   Device(s)
    1:     Kingston Technology (0951)  DataTraveler 100 (1607)
    2:     Logitech, Inc. (046d)       Unifying Receiver (c52b)
    3:     Alcor Micro Corp. (058f)    Flash Drive (1234)

Asciicast
---------

.. image:: https://gitlab.com/dslackw/images/raw/master/USBdev/usbdev_asciicast.png
    :target: http://asciinema.org/a/18905
   
CLI
---

.. code-block:: bash

    USBdev is a tool recognition of USB devices

    Optional  arguments:
      -h, --help               display this help and exit
      -v, --version            print program version and exit
      -t, --time [sec]         waiting time before plugin


Copyright 
---------

- Copyright © Dimitris Zlatanidis
- Linux is a Registered Trademark of Linus Torvalds.
