import sys
import time
def wlan_connect(ssid, password):
    import network
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active() or not wlan.isconnected():
        print("Conectando a la red WiFi...")
        wlan.active(True)
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(1)
    print("\nConectado a la red WiFi:", wlan.ifconfig())
