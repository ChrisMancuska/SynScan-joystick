
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('VM2544132', 'w4dfChqQxfxt')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    

do_connect()

#Now we can do something...
import socket
import sys
import binascii
import time



commandleft =         '\x50\x02\x10\x25\x07\x00\x00\x00'
commandtwiststop =     '\x50\x02\x10\x25\x00\x00\x00\x00'
commandright =     '\x50\x02\x10\x24\x07\x00\x00\x00'

commandup =         '\x50\x02\x11\x25\x07\x00\x00\x00'
commandupstop =     '\x50\x02\x11\x25\x00\x00\x00\x00'
commanddown =         '\x50\x02\x11\x24\x07\x00\x00\x00'

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('192.168.0.15', 11882)
sock.connect(server_address)
sock.send('e'.encode()) 
data = ''
data = (sock.recv(1024))
sock.send('e'.encode()) 
data = ''
data = (sock.recv(1024))
sock.send('e'.encode()) 
data = ''
data = (sock.recv(1024))
sock.send('e'.encode()) 
data = ''
data = (sock.recv(1024))
print ("twist")
print (data)
sock.send(commandleft.encode())
gc.collect() 

data = ''
data = (sock.recv(1024))
print (data)
time.sleep(1)
print("stop")
#sock.send(commandtwiststop.encode())
data = ''
#data = (sock.recv(1024))
print (data)

print("twistback")
sock.send(commandright.encode())
data = ''
data = (sock.recv(1024))
print (data)
time.sleep(1)
print("Stop")
sock.send(commandtwiststop.encode())
data = ''
data = (sock.recv(1024))
print (data)

print ("up")
sock.send(commandup.encode())
data = ''
data = (sock.recv(1024))
print (data)
time.sleep(1)

print ("stop")
sock.send(commandupstop.encode())
data = ''
data = (sock.recv(1024))
print (data)

print ("down")
sock.send(commanddown.encode())
data = ''
data = (sock.recv(1024))
print (data)
time.sleep(1)


print("stop")
sock.send(commandupstop.encode())
data = ''
data = (sock.recv(1024))
print (data)

print("position")
sock.send('e'.encode()) 
data = ''
data = (sock.recv(1024))
print (data)

