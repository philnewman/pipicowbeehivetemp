import dht
import gc
import network
import ntptime
import secrets
import socket
import time
import urequests
from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import Pin, RTC

sheetsURL = secrets.secrets['sheetsURL']
ssid = secrets.secrets['ssid']
password = secrets.secrets['password']

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
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(connection)
    return connection
    
def sendToSpreadsheet(wifi):
    for attempts in range(5):
        try:
            print(sheetsURL+wifi)
            res = urequests.get(url=sheetsURL+wifi)
            print("Request sent!")
            res.close()
            gc.collect()
            
        except:
            print("Error! Retrying...")
            continue

        else:
            break
        
    if (attempts >= 4):
        print("Unrecoverable error!")
    
    atttempts = 0
    
def getFormattedCurrTime(adjustTimeZone):
    plusZeroTime = time.time()
    now = time.localtime(plusZeroTime + (adjustTimeZone * 3600))
    timeStr = "{:02}-{:02}-{}%20{:02}:{:02}".format(now[2],now[1],now[0],now[3],now[4])
    return timeStr

ip = connect()
#connection = open_socket(ip)
#serve(connection)

rtc = RTC()
ntptime.settime()

prev = 0
timeStr = ''

minutes = 1
timeZone = -7

print("Time is set: ", getFormattedCurrTime(timeZone))

while True:
    curr = time.ticks_ms()
    if(curr - prev >=  minutes * 60 * 1000):
        prev = curr
        timeStr = getFormattedCurrTime(timeZone)
        temp = pico_temp_sensor.temp
        print("{} - Temp: {}\xBAC".format(timeStr, temp))
        sendToSpreadsheet("?datetime={}&temperature={}".format(timeStr, temp)) 
    else:
        time.sleep(minutes * 60)
