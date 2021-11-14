import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev
from urllib.request import urlopen
import sms

APIkey = #your write api key
baseURL = "https://api.thingspeak.com/update?api_key=#your write api key=0"

APIkey = #your write api key
baseURL = "https://api.thingspeak.com/update?api_key=#your write api key&field2=0"

GPIO.setmode(GPIO.BCM)
 
pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]
 
radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(0, 17)
 
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)
 
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
 
radio.openReadingPipe(1, pipes[1])
radio.printDetails()
radio.startListening()

count=0

while(1):
    # ackPL = [1]
    while not radio.available(0):
        time.sleep(1 / 100)
    receivedMessage = []
    radio.read(receivedMessage, radio.getDynamicPayloadSize())
    print("Received: {}".format(receivedMessage))
 
    print("Translating the receivedMessage into unicode characters")
    string = ""
    for n in receivedMessage:
        # Decode into standard unicode set
        if (n >= 48 and n <= 57):
            string += chr(n)
        if (n == 46):
            string += '.'
    print("Current Temperature: {}".format(string))
    temp = float(string)
    print(type(temp))

    #print(temp)
    if(temp>24):
        count+=1
    elif(temp<24):
        count=0
        
    if(count>120):
        sms.send()
        count=0
        
    try:
        #conn = urlopen((baseURL + '&field0={}').format(float(string)))
        conn = urlopen((baseURL + '&field1=%f') % (temp))
        print(conn.read())
        conn1 = urlopen((baseURL + '&field2=%f') % (temp))
        print(conn1.read())
        #Closing the connection
        conn.close()
        conn1.close()
    except Exception as e:
        print('Error')
        print(e)
        '''temp=float(string)
    elif(string.find('V')>0):
        string=string.split('V')[0]
        volt=float(string)
        print(volt)'''
