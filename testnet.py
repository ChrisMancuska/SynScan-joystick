
#test network
def do_connect(wifi):
      if not wlan.isconnected():
        print('connecting to network...'+wifi)
        wlan.connect(wifi)
        while not wlan.isconnected():
            pass
      print('network config:', wlan.ifconfig())
      
      
      
def findserver():
  #need to find the listener on the subnet on tcp11882
  #lets try an brave split 
  iptuple = wlan.ifconfig()[0].split('.')
  #build the first three octets
  ipstart = iptuple[0]+'.'+iptuple[1]+'.'+iptuple[2]
  #now loop for the last one and test for a connection.
  i = 2
  while i < 10:
    ipaddress = ipstart+'.'+str(i)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Trying "+ipaddress)
    try:
      s.connect((ipaddress, 11882))
      print('socket is open')
      s.close()
      return ipaddress    
    except:
      print("IP "+ipaddress+" not listening")
    i += 1
def findwifi():
  #search for synscan wifi and pass it as parameter to connect to for do_connect.
  # maybe if there are multiple, show and allow choice in future
  nets = wlan.scan()
  for net in nets:
    print((net[0]).decode('UTF-8'))
    testwifi = (net[0]).decode('UTF-8')
    if testwifi[0:7] == 'SynScan':
        wifi = testwifi
        print('Network found!'+wifi)

        return wifi
    else:
        print("Found Wifi "+testwifi+" continuing scan")
  
  #no suitable wifi so return
  return ''
  

import sys
import binascii
import time
from machine import Pin, ADC
import network
import socket
#stop and start wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(False)
time.sleep(0.5)
wlan.active(True)
    

wifi = ''
while (wifi == ''):
  wifi = findwifi()

do_connect(wifi)
ipaddress=''
while ipaddress=='':
  ipaddress = findserver()
print("IP address "+ipaddress)



