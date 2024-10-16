# comunicacion.py

import time
from machine import Pin, UART

led = Pin(2, Pin.OUT)

uart = UART(0, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

class Medicion:
    def __init__(self, tds=None, distancia=None, temperatura=None, humedad=None, temp_dht=None):
        self.tds = tds
        self.distancia = distancia
        self.temperatura = temperatura
        self.humedad = humedad
        self.temp_dht = temp_dht

def Uaart(val):
    byte = b''
    while True:
        byte = val
        uart.write(byte)
        time.sleep(1)
        if uart.any() > 0:
            strigByte = uart.readline()
            time.sleep(1)
            return strigByte

def obtener_humedad():
    return Uaart(b'5').decode('utf-8').strip()

def obtener_temp_dht():
    return Uaart(b'6').decode('utf-8').strip()

