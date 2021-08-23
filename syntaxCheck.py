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
def findwifi():
time.sleep(5)

oldtime = time.ticks_ms()
button = Pin(23, Pin.IN, Pin.PULL_UP) # enable internal pull-up resistor


PECGoTo = '' #Target coordinates if a GoTo is performed. Overwritten by a new GoTo or by performing PEC
      print ('y '+str(yMap)+' '+str(oldyMap)+' '+str(yValue))
      if oldxMap == 4 and oldyMap == 4:
        tracking = get_tracking_mode()
  
      if xMap == 3: 
      data = (sock.recv(1024))
      print (data) 
      print ('y '+str(yMap)+' '+str(oldyMap)+' '+str(yValue))
      #send command to move based on new xmap, read and print response and set oldxmap to xmap
    #Get current tracking mode if we are currently stationary
      #if oldxMap == 4 and oldyMap == 4:
        #tracking = get_tracking_mode()
      if yMap == 7: 
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
    