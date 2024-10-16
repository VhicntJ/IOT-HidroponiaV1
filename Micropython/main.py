# main.py

#==========================================Librerias=======================================#
import time
from machine import RTC
# synchronize RTC with ntp
import ntptime
import startup
import ufirebase as firebase
from comunicacion import Uaart, obtener_humedad, obtener_temp_dht

#=====================================Conexion internet=====================================#
startup.wlan_connect("Xhcss", "13111964")
URL = "https://iot-hidroponia-2f639-default-rtdb.firebaseio.com/"

#=======================================Tiempo Fecha=========================================#
rtc = RTC()
#fecha(0:year, 1:month, 2:day, 4:hour, 5:minute, 6:second)
def hora():
    ntptime.settime()
    date = rtc.datetime()
    if ((int(date[4]) - 7) <= 0):
        return (str(int(date[4])+17) + ":" +str(date[5]))
    else:
        return (str(int(date[4])-7) + ":" +str(date[5]))

def fecha():
    ntptime.settime()
    date = rtc.datetime()
    return "{}-{}-{}".format(date[0], date[1], date[2])

#=========================================Sensores=============================================#
def TDS():
    return Uaart(b'1').decode('utf-8').strip()

def DISTANCIA():
    return Uaart(b'2').decode('utf-8').strip()

def TEMPERATURA():
    return Uaart(b'3').decode('utf-8').strip()

def PH():
    return Uaart(b'4').decode('utf-8').strip()

def HUMEDAD():
    return obtener_humedad()

def TEMP_DHT():
    return obtener_temp_dht()

#=========================================Actuadores=============================================#
def Bomba_2():
    estado = firebase.get(URL + "bomba")
    try:
        estado = int(estado)
    except:
        estado = 0  # Valor por defecto si falla la conversión
    uart.write(str(estado).encode())
    time.sleep(1)
    return estado

#================================Transmicion de datos tiempo real===============================#
i = firebase.get(URL + "i")
try:
    i = int(i)
except:
    i = 0  # Valor por defecto si falla la conversión

def mensaje():
    global i
    i += 1

    # Obtener datos
    try:
        fecha_val = fecha()
        hora_val = hora()
        humedad_val = int(HUMEDAD())
        temp_dht_val = float(TEMP_DHT())
        distancia_val = float(DISTANCIA())
        ph_val = float(PH())
        ec_val = float(TDS())
    except Exception as e:
        print("Error al obtener datos:", e)
        return

    # Validar datos
    if not (0 <= humedad_val <= 100):
        print("Humedad fuera de rango:", humedad_val)
        humedad_val = None

    # Agrega más validaciones según tus necesidades

    # Datos a enviar
    datos = {
        'Sensor/Sensor1/{}/Fecha'.format(i): fecha_val,
        'Sensor/Sensor1/{}/Hora'.format(i): hora_val,
        'Sensor/Sensor1/{}/Humedad'.format(i): humedad_val,
        'Sensor/Sensor1/{}/Temp_dht'.format(i): temp_dht_val,
        'Sensor/Sensor1/{}/Distancia'.format(i): distancia_val,
        'Sensor/Sensor1/{}/PH'.format(i): ph_val,
        'Sensor/Sensor1/{}/EC'.format(i): ec_val
    }

    # Actualizar 'i' y enviar datos
    firebase.patch(URL, {'i': str(i)})
    firebase.patch(URL, datos)
    print("Datos enviados en la entrada {}".format(i))
    time.sleep(56)

def main_loop():
    while True:
        try:
            mensaje()
            Bomba_2()
            time.sleep(1)
        except Exception as e:
            print("Error:", e)
            uart.write(b'5')  # Apagar bomba
            startup.wlan_connect("Xhcss", "13111964")

def main():
    main_loop()

if __name__ == "__main__":
    main()

