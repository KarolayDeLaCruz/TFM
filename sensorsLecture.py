import socket
import sys
import time
import struct
import board
import busio
import serial
import syslog
import io

#   ARDUINO communications
#The following line is for serial over GPIO
ard = serial.Serial(
    port='/dev/ttyS0',
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
sio = io.TextIOWrapper(io.BufferedRWPair(ard, ard))

#   TACTIL SPI setup
from digitalio import DigitalInOut, Direction
from adafruit_cap1188.spi import CAP1188_SPI
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = DigitalInOut(board.D5)
cap = CAP1188_SPI(spi, cs)
touch_array=[0,0,0,0,0,0,0,0]


data_recv = [0,0]
ard_rcv = [0,0,0]
data_ard_rcv=""
send_ok=[1]


while(1):
                #leer sensor tactil
                for j in range(0,len(touch_array)):
                    touch_array[j]=0
                for i in range(1, 9):
                    if cap[i].value:
                        touch_array[i-1]=cap[i].raw_value
                
                #enviar a arduino solicitud de sensores y recepcion
                ard_msg='1'
                ard.write((str(ard_msg)+'\n').encode('utf-8'))
                # leer arduino
                ard_msg='1'
                ard.write((str(ard_msg)+'\n').encode('utf-8'))

                # leer arduino
                i=0
                # ard.reset_input_buffer()
                while i < 3:
                    try:
                        data_ard_rcv = ard.readline()
                    except:
                        print("No se pudo leer arduino")
                        data_ard_rcv = ""
                    if data_ard_rcv:
                        data_ard_rcv =data_ard_rcv .decode("utf-8")       
                        ard_rcv[i]= int((data_ard_rcv.split())[0])
                    i = i + 1
                
                # enviar lectura de sensores a PC
                send_array = ard_rcv + touch_array
                send_array_updated=send_array
                send_array_updated[1]=send_array[6]
                send_array_updated[2]=send_array[7]
                send_array_updated[6]=0
                send_array_updated[7]=0
                send_array_updated[8]=0
                #sock.sendall(struct.pack("iiiiiiiiiii", *send_array))
                print(send_array_updated)
                
                
                time.sleep(2)
