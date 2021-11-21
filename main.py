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
        pm1_0 = (buff[2] << 8) + buff[3]
        pm2_5 = (buff[4] << 8) + buff[5]
        pm10 = (buff[6] << 8) + buff[7]

        CWriter.set_textpos(ssd, 0, 0)
        wri = CWriter(ssd, arial35, WHITE, BLACK)  # Report on fast mode. Or use verbose=False
        wri.set_clip(True, True, False)
        lbltim = Label(wri, 0, 0, 35)
        lbltim.value('PM1.0: {:02d}\nPM2.5: {:02d}\nPM10: {:02d}'.format(pm1_0, pm2_5, pm10))
        refresh(ssd)
