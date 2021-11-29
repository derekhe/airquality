from machine import UART
from color_setup import ssd
from gui.core.nanogui import refresh  # Color LUT is updated now.
from gui.fonts import arial35
from gui.widgets.label import Label
from gui.widgets.dial import Dial, Pointer

refresh(ssd, True)  # Initialise and clear display.

# Now import other modules
import cmath
import utime
from gui.core.writer import CWriter

# Font for CWriter
import gui.fonts.arial10 as arial10
from gui.core.colors import *

uart = UART(1, 9600)

while True:
    c = uart.read(2)
    if c == b'BM':
        buff = []
        while len(buff) < 30:
            b = uart.read(1)
            if b is not None:
                buff.append(b[0])
        pm1_0 = (buff[8] << 8) + buff[9]
        pm2_5 = (buff[10] << 8) + buff[11]
        pm10 = (buff[12] << 8) + buff[13]
        pmmax = max(pm2_5, pm10)
        color = BLACK
        quality = ""
        if pmmax < 50:
            color = GREEN
            quality = "Good"
        elif pmmax < 100:
            color = YELLOW
            quality = "Not good"
        else:
            color = RED
            quality = "Bad"
        ssd.fill(color)
        wri = CWriter(ssd, arial35, BLACK, color)  # Report on fast mode. Or use verbose=False
        wri.set_clip(True, True, False)
        lbltim = Label(wri, 0, 0, 10)
        lbltim.value('PM2.5:\n {:02d}\nPM10:\n {:02d}\n{}'.format(pm2_5, pm10, quality))
        refresh(ssd, False)
