
# Prerequisites

`ATMO-VENT` software installation must be done on a RPI3 or higher in order for the alarm system to work. If you choose to use a different system make sure you have an alarm system implemented and change the "RPi.GPIO" library to the corresponding one. The prerequisites packages are the following:

1. Installation must be done on a Raspberry Pi 3 or higher
2. `python3.6 or higher` (`$ sudo apt-get install python3.6`)
3. Intall the python packages listed in `requirements.txt` (`$ pip install -r requirements.txt`)

# Installation

### Let's hope everything is installed correctly and working:

First, make sure you cloned/downloaded the repository:

```
$ git clone link_to_this_repository
```
Second, before trying to run the program make sure the libraries are correctly installed:

```
$ python3
>>> import pyqtgraph as pg
>>> import serial
>>> import time
>>> import _thread
>>> import subprocess
>>> from PyQt5 import QtCore, QtGui, QtWidgets
>>> from PyQt5.QtCore import QThread, pyqtSignal
>>> from PyQt5.QtGui import *
>>> from PyQt5.QtWidgets import *
>>> from PyQt5.QtCore import *
>>> import traceback, sys
>>> import numpy as np
>>> from random import randint
>>> import RPi.GPIO as GPIO
```
If the previous steps were succesfull, you are almost ready to execute the program.
Change directories into the repository folder, edit the main.py file changing the varialbe "self.arduino_id" with the ID of the arduino you are using. Then, you are ready to run the main program:
```
$ cd ATMO-VENT/
$ nano main.py
#change the "self.arduino_id" variable with the ID of the Arduino being used.
$ python3 main.py
```
