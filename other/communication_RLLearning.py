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

#   PC Communications
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Create server
server_address = ('192.168.1.177', 8000)
print('Server ip {} port {}'.format(*server_address))
sock.bind(server_address)
sock.listen(1)
data_recv = [0,0]
ard_rcv = [0,0,0]
data_ard_rcv=""
send_ok=[1]

def posture_msg (i):
    switcher = {
            1: 'kbalance',
            2: 'kheadL',
            3: 'kheadR',
            4: 'kstr',
            5: 'ksleep',
            6: 'ksleep' #kbuttUp
            }
    return switcher.get(i,"Invalid posture")

def skill_msg (i):
    switcher = {
            0: 'ksleep',
            1: 'kcr',
            2: 'kbk',
            3: 'kbalanceUp',
            4: 'ksit',
            5: 'kbalanceDown',
            6: 'kcr',
            7: 'khi2',
            8: 'khunt',
            9: 'kcr',
            10: 'kdropped',
            11: 'kstr',
            12: 'kbuttUp',
            13: 'klay',
            14: 'kheadlay',
            15: '2',
            16: '3',
            17: 'kbuttUp',
            18: 'krest'
            }
    return switcher.get(i,"Invalid skill")

while(1):
    ## receive
    ##data = sock.recv(2)
    ## Karo
    ## data = data.decode()
    ## karo
    
    c,a=sock.accept()
    read = c.makefile('r')
    write = c.makefile('w')
    
    with c, read, write:
        while True:
            data = read.readline()
            if not data: break
            cmd = data.strip()
            
            data_recv = list(cmd)
            #karo
            data_recv = list(map(int, data_recv))
            #karo
            #print("Recibido: ", data)
            print("Recibido PC: ", data_recv)
            
            
            if data_recv[0] == 4:
                #leer sensor tactil
                for j in range(0,len(touch_array)):
                    touch_array[j]=0
                for i in range(1, 9):
                    if cap[i].value:
                        #print("Pin {} touched!".format(i))
                        touch_array[i-1]=cap[i].raw_value
                #print(touch_array)
                #         enviar a arduino solicitud de sensores y recepcion
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
                    
                    
                    
                    
                    
                    
                    #data_ard_rcv = ard.readline().decode("utf-8")       
                    #print("test:"+data_ard_rcv)
                    #ard_rcv[i]= int((data_ard_rcv.split())[0])
                    #i = i + 1
                #print(ard_rcv)
                # enviar lectura de sensores a PC
                #send_array = ard_rcv + touch_array
                #sock.sendall(struct.pack("iiiiiiiiiii", *send_array))
                #print(type(send_array))
                
                write.write( str(send_array_updated)+ '\n')
                write.flush()
                print("Enviando PC: ", send_array_updated)
                time.sleep(5)
                
            if data_recv[0] == 1:
                ard_msg=posture_msg(data_recv[1])
                print("Solicitado cambio de postura: ", ard_msg)
                ard.write((str(ard_msg)+'\n').encode())
                time.sleep(2)
            if data_recv[0] == 2:
                ard_msg=skill_msg (data_recv[1])
                print("Solicitado cambio de estado: ", ard_msg)
                ard.write((str(ard_msg)+'\n').encode())
                time.sleep(4)
        # finally:
        #     print('closing socket')
        #      sock.close()
