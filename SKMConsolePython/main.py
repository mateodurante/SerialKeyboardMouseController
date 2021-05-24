#!/usr/bin/python3

## Ya funciona, falta mejorar la implementacion del keypress y keyrelease con todos los HID posibles

import serial
import time
import ctypes

BaudRate = 500000 #

# Uses ctypes.c_ubyte == uint8_t
FrameStart = 0xAB

MouseMove = 0xAA
MouseScroll = 0xAB
MousePress = 0xAC
MouseRelease = 0xAD
MouseResolution = 0xAE

KeyboardPress = 0xBB
KeyboardRelease = 0xBC

Unknown = 0xFF

ReleaseAllKeys =  0x00

MouseButtonLeft =  0x01
MouseButtonRight =  0x02
MouseButtonMiddle =  0x04


MinFrameLength = 5 # // 0xAB <Length> <Type> <Value> <Checksum>
MaxDataLength = 6 # // Coordinate type, 4-byte coordinates + <Type> + <Checksum>
MaxFrameLength = MaxDataLength + 2 #

arduino = serial.Serial(port='COM7', baudrate=500000, timeout=.1)

def calculate_checksum(data):
    if data == 0:
        return 0
    checksum = data[0]
    for d in data[1:]:
        checksum ^= d
    return checksum

def send(data):
    checksum = calculate_checksum(data)
    message = list(map(ctypes.c_ubyte, [FrameStart, len(data)+1] + data + [checksum]))
    bytes_sent = bytes([b.value for b in message])

    print("SENDING: ", bytes_sent)
    reply_ok = False
    
    while not reply_ok:
        for b in message:
            arduino.write(b)
        recv = arduino.readline()
        print("RECIVED: ", recv)
        if recv == bytes_sent:
            reply_ok = True
        else:
            print(f"BAD REPLY: Retrying {bytes_sent}")


# TODO: Mejorar el keypress BB y el keyrelease BC separado de los HID, o sea una funcion que sea release o press y el codigo de tecla. Lo mismo con el mouse
press_s = [0xBB, 0x16]
release_s = [0xBC, 0x16]
press_d = [0xBB, 0x07]
release_d = [0xBC, 0x07]

mouse_press_right = [0xAC, MouseButtonRight]
mouse_release_right = [0xAD, MouseButtonRight]

mouse_scroll_up = [0xAB, 0x01]
mouse_scroll_down = [0xAB, -0x02]

# TODO: Ver si realmente vale la pena configurar una resolucion pequeña, ya que la posicion es absoluta respecto de la resolucion real.
# 0xAB 0x06 0xAA <4-byte resolution> <Checksum>
mouse_resolution = [0xAE] + list((2000).to_bytes(2,'little')) + list((2000).to_bytes(2,'little'))

# 0xAB 0x06 0xAA <4-byte coordinate> <Checksum>
mouse_move = [0xAA] + list((1100).to_bytes(2,'little')) + list((500).to_bytes(2,'little'))



# EJEMPLOS: 

# time.sleep(1)

# send(mouse_resolution)
# send(mouse_move)
# send(mouse_scroll_up)
# send(mouse_scroll_down)
# send(mouse_press_right)
# send(mouse_release_right)

# send(press_s)
# send(release_s)





