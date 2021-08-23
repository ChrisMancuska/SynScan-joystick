
import sys
import binascii
import time
from machine import Pin, ADC
import network
import socket

adc1 = ADC(Pin(32)) #set pin 32 as ADC
adc2 = ADC(Pin(35)) #set pin 33 as ADC
#adc3 = ADC(Pin(33)) #set pin 33 as ADC
button = Pin(23, Pin.IN, Pin.PULL_UP) # enable internal pull-up resistor
adc1.atten(ADC.ATTN_11DB)  #set sampling to allow 0-3.3v and 12bits
adc2.atten(ADC.ATTN_11DB)  #set sampling to allow 0-3.3v and 12bits
#adc3.atten(ADC.ATTN_11DB)  #set sampling to allow 0-3.3v and 12bits
oldxMap = 4
oldyMap = 4  
#oldzMap = 4
oldtime = time.ticks_ms()
#oldzMap = 4
while 1:
    
    xValue = adc1.read() +530 # read value, 0-4095
    yValue = adc2.read() +500 # read value, 0-4095
    #zValue = adc3.read() 
    xMap = int((xValue/4095) * 6)+1 #want integer value between 1 and 7
    yMap = int((yValue/4095) * 6)+1 #want integer value between 1 and 7
    #zMap = int((zValue/4095) * 6)+1 #want integer value between 1 and 7
    if (oldxMap != xMap):
      print ('x '+str(xMap)+'y '+str(yMap)+' button '+str(but.value()))
      oldxMap = xMap
      
    
    
    if (oldyMap != yMap):
      print ('x '+str(xMap)+'y '+str(yMap)+' button '+str(button.value()))
      oldyMap = yMap  
    time.sleep(1)
    print(str(but.value()))
    if button.value() == 0:
      print("button pressed")
      time.sleep(1)
      
    
