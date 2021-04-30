import board
import busio
import digitalio
from adafruit_cap1188.spi import CAP1188_SPI
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs  = digitalio.DigitalInOut(board.D5)
cap = CAP1188_SPI(spi,cs)

touch_array=[0,0,0,0,0,0,0,0]


while True:
    for j in range(0,len(touch_array)):
        touch_array[j]=0
    for i in range(1,9):
        if cap[i].value:
            #print("Pin {} touched ".format(i))
            touch_array[i-1]=cap[i].raw_value
    print(touch_array)