# startup.py
import network
import time

def wlan_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        print("Activando interfaz Wi-Fi...")
        wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red:', ssid)
        wlan.connect(ssid, password)
        timeout = 20  # Tiempo máximo de espera en segundos
        start_time = time.time()
        while not wlan.isconnected():
            if time.time() - start_time > timeout:
                print("Tiempo de espera agotado. No se pudo conectar a la red.")
                return False
            print('.', end='')
            time.sleep(1)
    print('\nConexión establecida:', wlan.ifconfig())
    return True
