# test_firebase_full.py

import time
import ufirebase as firebase
from startup import wlan_connect

# Configuración de la red Wi-Fi
SSID = "Xhcss"
PASSWORD = "13111964"

# URL de tu Realtime Database
URL = "https://iot-hidroponia-2f639-default-rtdb.firebaseio.com/"




def enviar_datos_prueba():
    # Obtener la clave 'i' actual
    try:
        i = firebase.get(URL + "i")
        i = int(i) + 1
    except:
        i = 1  # Si no existe, iniciar en 1

    # Datos de prueba
    datos = {
        
        'Sensor/Sensor1/{}/Humedad'.format(i): 60,        # Valor de Humedad de prueba (%)
        'Sensor/Sensor1/{}/Temp_dht'.format(i): 25,       # Valor de Temperatura del DHT11 de prueba (°C)
        'Sensor/Sensor1/{}/Distancia'.format(i): 45,      # Valor de Distancia de prueba (cm)
        'Sensor/Sensor1/{}/PH'.format(i): 7.0,            # Valor de pH de prueba
        'Sensor/Sensor1/{}/EC'.format(i): 1.5            # Valor de EC de prueba (dS/m)
    }

    # Actualizar 'i'
    firebase.patch(URL, {'i': str(i)})

    # Enviar datos de prueba
    firebase.patch(URL, datos)
    print("Datos de prueba enviados en la entrada {}".format(i))

def main():
    # Conectar a Wi-Fi
    wlan_connect(SSID, PASSWORD)
    print("Conectado a Wi-Fi")

    # Enviar datos de prueba
    enviar_datos_prueba()

if __name__ == "__main__":
    main()

