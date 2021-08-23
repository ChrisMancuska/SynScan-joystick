#Bunch of predetermined commands to use for  clarity


def get_tracking_mode():
  print ("Get tracking mode")
  #find out the current tracking mode so we can store before issuing a slew and 
  #then return to it once slew is complete.
  #We just issue the command here...
  sock.send('t')
  data = sock.recv(1024)
  #b'\x00#': no trackibn
  #b'\x01#': alt az
  
  #expecting 'tn#' whenre n=0-4
  #want to save it as 'Tn' so we can just restore tracking mode by sending it without changes
  print("Tracking mode returned as "+'T'+data[1:1])
  return 'T'+data[1:1]
  
def set_tracking_mode(mode):
  print("Set tracking mode to "+mode)
  sock.send(mode)
  data = sock.recv(1024)
  print (str(data))
  if data == b'#':
    print("success")
    return 'OK'
  print ("fail")
  return 'FAIL - Tracking not restored'
  #expecting an '#' as OK

def get_goto_target():
  print ("Get goto target")
  #See if we are currently doing a goto and if we have finished store target so we can do PEC and unlock slewing etc
  #This may as well be blocking because otherwise we are complicating things....
  #Do initial enquiry and lock up if we are goto, finally returning a position.
  #If we are NOT doing a GoTo, return instantly 'NoGoTo', don't get a position.
  
  #b'0#' no goto
  #b'1#' goto
  sock.send('L')
  data = sock.recv(1024)
  if data == b'0#':
    print ("No go to currently active")
    return 'NoGoTo'
  while (data==b'1#'):
    sock.send('L')
    #this will break the loop when the goto ends
    data = sock.recv(1024)
    #Can use a blocking sleep delay step
    print ("waiting for goto to complete")
    time.sleep(0.5)
    
  #Now goto is complete, return current position
  sock.send('e')
  data = sock.recv(1024).decode()
  #Get string like this b'34AB0500,12CE0500#'
  #Want to remove # and return...after decoding as ascii
  print ("goto is complete, sending position "+data[0:-1])
  return data[0:-1]

def set_goto_target(gototarget):
  print ("PEC target "+gototarget)
  #We are refining the coordinates of the telescope
  sock.send('s'+gototarget)
  data = sock.recv(1024)
  if data == '#':
    print ("PEC OK")
    return 'OK'
  print ("PEC fail")
  return 'FAIL - PEC align failed'
  #expecting an '#' as OK
def findwifi():  #search for synscan wifi and pass it as parameter to connect to for do_connect.  # maybe if there are multiple, show and allow choice in future  nets = wlan.scan()  for net in nets:    print((net[0]).decode('UTF-8'))    testwifi = (net[0]).decode('UTF-8')    if testwifi[0:7] == 'SynScan':        wifi = testwifi        print('Network found!'+wifi)        return wifi    else:        print("Found Wifi "+testwifi+" continuing scan")    #no suitable wifi so return  return ''  def do_connect(wifi):      if not wlan.isconnected():        print('connecting to network...'+wifi)        wlan.connect(wifi)        while not wlan.isconnected():            pass      print('network config:', wlan.ifconfig())                  def findserver():  #need to find the listener on the subnet on tcp11882  #lets try an brave split   iptuple = wlan.ifconfig()[0].split('.')  #build the first three octets  ipstart = iptuple[0]+'.'+iptuple[1]+'.'+iptuple[2]  #now loop for the last one and test for a connection.  i = 2  while i < 10:    ipaddress = ipstart+'.'+str(i)    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    print("Trying "+ipaddress)    try:      s.connect(('ipaddress', 11882))      print('socket is open')      s.close()      return ipaddress        except:      print("IP "+ipaddress+" not listening")    i += 1import sysimport binasciiimport timefrom machine import Pin, ADCimport networkimport socket#stop and start wifiwlan = network.WLAN(network.STA_IF)wlan.active(False)time.sleep(0.5)wlan.active(True)    wifi = ''while (wifi == ''):  wifi = findwifi()time.sleep(5)do_connect(wifi)
time.sleep(5)server_address = ('192.168.4.4',11882)#while (server_address ==''):#  server_address = findserver()    #movement command as binary stringsleft =        '\x50\x02\x10\x25\x07\x00\x00\x00'leftslow =    '\x50\x02\x10\x25\x04\x00\x00\x00'leftvslow =   '\x50\x02\x10\x25\x02\x00\x00\x00'right =       '\x50\x02\x10\x24\x07\x00\x00\x00'rightslow =   '\x50\x02\x10\x24\x04\x00\x00\x00'rightvslow =  '\x50\x02\x10\x24\x02\x00\x00\x00'stoptwist =   '\x50\x02\x10\x25\x00\x00\x00\x00'up =          '\x50\x02\x11\x25\x07\x00\x00\x00'upslow =      '\x50\x02\x11\x25\x04\x00\x00\x00'upvslow =     '\x50\x02\x11\x25\x02\x00\x00\x00'down =        '\x50\x02\x11\x24\x07\x00\x00\x00'downslow =    '\x50\x02\x11\x24\x04\x00\x00\x00'downvslow =   '\x50\x02\x11\x24\x02\x00\x00\x00'stopinc =     '\x50\x02\x11\x24\x00\x00\x00\x00'

oldtime = time.ticks_ms()adc1 = ADC(Pin(32)) #set pin 32 as ADCadc2 = ADC(Pin(35)) #set pin 35 as ADC
button = Pin(23, Pin.IN, Pin.PULL_UP) # enable internal pull-up resistoradc1.atten(ADC.ATTN_11DB)  #set sampling to allow 0-3.3v and 12bitsadc2.atten(ADC.ATTN_11DB)  #set sampling to allow 0-3.3v and 12bits
oldyMap=4 #set joystick to be in centre of yoldxMap=4 #set joystick to be in centre of x

PECGoTo = '' #Target coordinates if a GoTo is performed. Overwritten by a new GoTo or by performing PECtracking = 'T0' #Init# Create a TCP/IP socketsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# Bind the socket to the portwhile 1:   sock.connect(server_address)  #start loop  while 1:    time.sleep(0.1)    xValue = adc1.read() +530 # read value, 0-4095    yValue = adc2.read() +500 # read value, 0-4095    xMap = int((xValue/4095) * 6)+1 #want integer value between 1 and 7    yMap = int((yValue/4095) * 6)+1 #want integer value between 1 and 7      #compare to see if joystick has moved    #x axis    if xMap != oldxMap:      print ('x '+str(xMap)+' '+str(oldxMap)+' '+str(xValue))
      print ('y '+str(yMap)+' '+str(oldyMap)+' '+str(yValue))    #send command to move based on new xmap, read and print response and set oldxmap to xmap 
      if oldxMap == 4 and oldyMap == 4:
        tracking = get_tracking_mode()      if xMap == 7:         sock.send(right.encode())      if xMap == 6:        sock.send(rightslow.encode())      if xMap == 5:         sock.send(rightvslow.encode())           if xMap == 4:         sock.send(stoptwist.encode())
  
      if xMap == 3:         sock.send(leftvslow.encode())      if xMap == 2:         sock.send(leftslow.encode())      if xMap == 1:         sock.send(left.encode())      oldxMap = xMap
      data = (sock.recv(1024))
      print (data)     #y axis    if yMap != oldyMap :      print ('x '+str(xMap)+' '+str(oldxMap)+' '+str(xValue))
      print ('y '+str(yMap)+' '+str(oldyMap)+' '+str(yValue))
      #send command to move based on new xmap, read and print response and set oldxmap to xmap
    #Get current tracking mode if we are currently stationary
      #if oldxMap == 4 and oldyMap == 4:
        #tracking = get_tracking_mode()
      if yMap == 7:         sock.send(down.encode())      if yMap == 6:        sock.send(downslow.encode())      if yMap == 5:         sock.send(downvslow.encode())            if yMap == 4:         sock.send(stopinc.encode())      if yMap == 3:         sock.send(upvslow.encode())      if yMap == 2:         sock.send(upslow.encode())      if yMap == 1:         sock.send(up.encode())      oldyMap = yMap      data = (sock.recv(1024))
      print (data) 
   
 
  #Now - every half second, see if we are doing a goto, and if so, 
  #lock the joystick until it completes, and then get ready to sync
  #Also start tracking if the scope is stationary and stick centred
    newtime = time.ticks_ms()
    if time.ticks_diff(newtime, oldtime) > 500:
      #reset timer
      oldtime = time.ticks_ms()
      #We are not moving, so restore tracking
      if yMap == 4 and xMap == 4:
        #print(set_tracking_mode(tracking))
        #tracking = get_tracking_mode().decode()
        print("tracking is "+tracking)
    #Are we doing a Goto? This is blocking if there is a Goto
    #We want to overwrite PECGoTo if it is not 'NoGoTo'. Pressing the button to PEC will also clear
    #PECGoTo
      GoTo = get_goto_target()
      if GoTo != 'NoGoTo':
        PECGoTo = GoTo
    
    #Now we need to look at the status of the button and trigger PEC is it is pressed.
    #To avoid dealing with bounce we will make the setting delay a second to let the user
    #let go of the button.
    
    if button.value() == 0:
      print ("Button pressed!")
      #We have a pressed button! pass the PECGoTo value if it is valid
      if PECGoTo != '':
        print(set_goto_target(PECGoTo))
        PECGoTo = ''
        time.sleep(1)
    #except:#  #cannot connect or have been disconnected#  print("Error occurred - stopping")#  while 1:#    time.sleep(10)