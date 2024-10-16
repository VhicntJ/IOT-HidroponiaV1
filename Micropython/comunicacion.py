# comunicacion.py

import time
from machine import Pin, UART

# Configuración de UART
uart = UART(1, baudrate=115200, tx=17, rx=16)  # TX=GPIO17, RX=GPIO16
uart.init(baudrate=115200, bits=8, parity=None, stop=1)

class Medicion:
    def __init__(self, tds=None, distancia=None, temperatura=None, ph=None, humedad=None, ec=None):
        self.tds = tds
        self.distancia = distancia
        self.temperatura = temperatura
        self.ph = ph
        self.humedad = humedad
        self.ec = ec

def send_command(command, timeout=2):
    """
    Envía un comando al Arduino y espera una respuesta.

    :param command: Caracter que representa el comando a enviar.
    :param timeout: Tiempo máximo de espera para la respuesta (en segundos).
    :return: Respuesta recibida como string o None si no se recibe respuesta.
    """
    try:
        uart.write(command.encode())  # Envía el comando
        start_time = time.time()
        while (uart.any() == 0) and (time.time() - start_time < timeout):
            time.sleep(0.1)  # Espera por datos
        if uart.any():
            response = uart.readline().decode().strip()
            return response
        else:
            return None
    except Exception as e:
        print("Error en send_command:", e)
        return None

def obtener_tds():
    response = send_command('1')
    if response and response != "Error":
        try:
            return float(response)
        except:
            print("Error al parsear TDS")
            return None
    return None

def obtener_distancia():
    response = send_command('2')
    if response and response != "Error":
        try:
            return float(response)
        except:
            print("Error al parsear Distancia")
            return None
    return None

def obtener_temperatura():
    response = send_command('3')
    if response and response != "Error":
        try:
            return float(response)
        except:
            print("Error al parsear Temperatura")
            return None
    return None

def obtener_ph():
    response = send_command('4')
    if response and response != "Error":
        try:
            return float(response)
        except:
            print("Error al parsear pH")
            return None
    return None

def obtener_humedad():
    response = send_command('7')  # Nuevo comando para Humedad
    if response and response != "Error":
        try:
            return float(response)
        except:
            print("Error al parsear Humedad")
            return None
    return None

def controlar_bomba(estado):
    """
    Controla la bomba enviando comandos '5' para encender y '6' para apagar.

    :param estado: Booleano, True para encender, False para apagar.
    :return: Respuesta del Arduino o None.
    """
    try:
        if estado:
            comando = '5'
        else:
            comando = '6'
        response = send_command(comando)
        return response
    except Exception as e:
        print("Error en controlar_bomba:", e)
        return None
