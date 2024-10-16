# main.py

#==========================================Librerias=======================================#
import time
from machine import RTC
import ntptime
import startup
import ufirebase as firebase
from comunicacion import (
    obtener_tds,
    obtener_distancia,
    obtener_temperatura,
    obtener_ph,
    controlar_bomba
)

#=====================================Conexion internet=====================================#
SSID = "Xhcss"
PASSWORD = "13111964"
startup.wlan_connect(SSID, PASSWORD)
URL = "https://iot-hidroponia-2f639-default-rtdb.firebaseio.com/"

#=======================================Tiempo Fecha=========================================#
rtc = RTC()

def sincronizar_hora():
    try:
        ntptime.settime()
    except:
        print("Error al sincronizar NTP")
    date = rtc.datetime()
    return date

def hora():
    date = sincronizar_hora()
    # Ajuste de zona horaria si es necesario (ejemplo: UTC-7)
    hora_local = date[4] - 7
    if hora_local < 0:
        hora_local += 24
    return "{:02d}:{:02d}".format(hora_local, date[5])

def fecha():
    date = sincronizar_hora()
    return "{:04d}-{:02d}-{:02d}".format(date[0], date[1], date[2])

#================================Transmicion de datos tiempo real===============================#
def mensaje():
    # Obtener la clave 'i' actual
    try:
        i = firebase.get(URL + "i")
        i = int(i) + 1
    except:
        i = 1  # Si no existe, iniciar en 1

    # Obtener datos de los sensores
    tds = obtener_tds()
    distancia = obtener_distancia()
    temperatura = obtener_temperatura()
    ph = obtener_ph()
    # Asumimos que Humedad y Temp_dht también se obtienen del Arduino
    # Si el Arduino no los está enviando, necesitarás ajustar esto
    # Por ahora, supongamos que 'temperatura' es Temp_dht y 'humedad' se obtiene también
    # Si tienes más comandos para Humedad y Temp_dht, agrégalos aquí

    # Para este ejemplo, asumiremos que 'temperatura' es Temp_dht y que la humedad no se está obteniendo
    # Si el Arduino está enviando Humedad, agrega una función similar para obtenerla
    # Aquí, por simplicidad, asignamos valores estáticos
    humedad = 60  # Reemplaza con la función adecuada si está disponible
    temp_dht = temperatura  # Reemplaza con la función adecuada si está disponible
    ec = tds  # Asumiendo que EC está mapeado a TDS

    # Validar datos antes de enviarlos
    if None in [tds, distancia, temperatura, ph]:
        print("Algunos datos no están disponibles, omitiendo envío.")
        return

    # Datos a enviar
    datos = {
        'Sensor/Sensor1/{}/Fecha'.format(i): fecha(),
        'Sensor/Sensor1/{}/Hora'.format(i): hora(),
        'Sensor/Sensor1/{}/Humedad'.format(i): humedad,
        'Sensor/Sensor1/{}/Temp_dht'.format(i): temp_dht,
        'Sensor/Sensor1/{}/Distancia'.format(i): distancia,
        'Sensor/Sensor1/{}/PH'.format(i): ph,
        'Sensor/Sensor1/{}/EC'.format(i): ec
    }

    # Actualizar 'i' y enviar datos
    firebase.patch(URL, {'i': str(i)})
    firebase.patch(URL, datos)
    print("Datos enviados en la entrada {}".format(i))

def main_loop():
    while True:
        try:
            mensaje()
            # Control de la bomba si es necesario
            # Por ejemplo, encender o apagar la bomba basado en ciertos criterios
            # controlar_bomba(True)  # Encender
            # controlar_bomba(False)  # Apagar
            time.sleep(60)  # Espera de 60 segundos antes de la siguiente lectura
        except Exception as e:
            print("Error en main_loop:", e)
            # Opcional: apagar la bomba en caso de error
            # controlar_bomba(False)
            # Intentar reconectar Wi-Fi
            startup.wlan_connect(SSID, PASSWORD)
            time.sleep(10)  # Espera antes de reintentar

def main():
    main_loop()

if __name__ == "__main__":
    main()
