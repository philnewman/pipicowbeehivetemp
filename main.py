import dht
import gc
import network
import ntptime
import secrets
import time
import urequests
from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import Pin, RTC

# Startup Variables
ssid = secrets.secrets['ssid']
password = secrets.secrets['password']
sheetsURL = secrets.secrets['sheetsURL']
timeZone = secrets.secrets['timeZone']

def connect():
    #Connect to WLAN
    print("Connecting to network...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')

def disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
    wlan.active(False)
    wlan.deinit()
    print('Disconnected from network')

def sendToSpreadsheet(wifi):
    try:
        res = urequests.get(url=sheetsURL+wifi)
        res.close()
        gc.collect()
    except Exception as e:
        print("An error has occured.",e) 
    
def getFormattedCurrTime(adjustTimeZone):
    plusZeroTime = time.time()
    now = time.localtime(plusZeroTime + (adjustTimeZone * 3600))
    dateStr = "{:02}-{:02}-{}".format(now[0],now[1],now[2])
    timeStr = "{:02}:{:02}:{:02}".format(now[3],now[4],now[5])
    return dateStr, timeStr

def celsius_to_fahrenheit(temp_celcius):
    temp_fahrenheit = round(temp_celcius * (9/5) + 32,2)
    return temp_fahrenheit

def send_message():
    try:
        dateStr, timeStr = getFormattedCurrTime(timeZone)
        tempC = round(pico_temp_sensor.temp,2)
        tempF = celsius_to_fahrenheit(tempC)
        sendToSpreadsheet("?datetime={}&time={}&tempF={}&tempC={}".format(dateStr, timeStr, tempF, tempC)) 
    except Exception as e:
        print("Error:", e)

for i in range(20):
    pico_led.on()
    connect()
    ntptime.settime()
    rtc = RTC()
    send_message()
    disconnect()
    pico_led.off()
    time.sleep(900)
