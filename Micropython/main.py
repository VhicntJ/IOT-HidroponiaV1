# main.py

#==========================================Librerías=======================================#
import time
from machine import RTC, reset
import startup
import ufirebase as firebase
from comunicacion import (
    obtener_tds,
    obtener_distancia,
    obtener_temperatura,
    obtener_ph,
    obtener_humedad,
    controlar_bomba
)

#=====================================Conexión Internet=====================================#
SSID = "Xhcss"          # Reemplaza con tu SSID
PASSWORD = "13111964"   # Reemplaza con tu contraseña

if not startup.wlan_connect(SSID, PASSWORD):
    print("No se pudo conectar a la red Wi-Fi. Reiniciando...")
    reset()

URL = "https://iot-hidroponia-2f639-default-rtdb.firebaseio.com/"


#================================Transmisión de datos tiempo real===============================#
def mensaje():
    # Obtener la clave 'i' actual
    try:
        i = firebase.get(URL + "i")
        i = int(i) + 1
    except Exception as e:
        print("Error al obtener 'i' desde Firebase:", e)
        i = 1  # Si no existe, iniciar en 1

    # Obtener datos de los sensores
    tds = obtener_tds()
    distancia = obtener_distancia()
    temperatura = obtener_temperatura()
    ph = obtener_ph()
    humedad = obtener_humedad()
    ec = tds  # Asumiendo que EC está mapeado a TDS

    # Validar datos antes de enviarlos
    if None in [tds, distancia, temperatura, ph, humedad]:
        print("Algunos datos no están disponibles, omitiendo envío.")
        return

    # Datos a enviar
    datos = {
        'Sensor/Sensor1/{}/Humedad'.format(i): humedad,
        'Sensor/Sensor1/{}/Temp_dht'.format(i): temperatura,
        'Sensor/Sensor1/{}/Distancia'.format(i): distancia,
        'Sensor/Sensor1/{}/PH'.format(i): ph,
        'Sensor/Sensor1/{}/EC'.format(i): ec
    }

    # Actualizar 'i' y enviar datos
    try:
        firebase.patch(URL, {'i': str(i)})
        firebase.patch(URL, datos)
        print("Datos enviados en la entrada {}".format(i))
    except Exception as e:
        print("Error al enviar datos a Firebase:", e)

def main_loop():
    while True:
        try:

            # Obtener humedad nuevamente para controlar la bomba
            humedad = obtener_humedad()
            if humedad is not None:
                if humedad < 50:
                    controlar_bomba(True)  # Encender bomba
                    print("Bomba encendida debido a baja humedad.")
                elif humedad > 70:
                    controlar_bomba(False)  # Apagar bomba
                    print("Bomba apagada debido a alta humedad.")
            else:
                print("No se pudo obtener la humedad para controlar la bomba.")

            time.sleep(60)  # Espera de 60 segundos antes de la siguiente lectura
        except Exception as e:
            print("Error en main_loop:", e)
            # Intentar reconectar Wi-Fi
            if not startup.wlan_connect(SSID, PASSWORD):
                print("No se pudo reconectar a Wi-Fi. Reiniciando...")
                reset()
            time.sleep(10)  # Espera antes de reintentar

def main():
    main_loop()

if __name__ == "__main__":
    main()

