# arduino Handler
# 8/13/2020
# Michael Fuell, Aaron Laster


import threading
import time
import serial
import glob

class ardHandler:

#---------------------------------------------------------------
    def __init__(self):
        self.open()

#---------------------------------------------------------------         
    def open(self):
        _port = glob.glob("/dev/ttyUSB*")
        #self.data
        try:
            self.arduino = serial.Serial(_port[0], 9600)
        except:  #Not Sucessful
            print("Port Error_2 'A'")
        else:    #sucessful
            print("Port Opened 'A'")
            time.sleep(2)
            self.runThread = True
            self.ardThread = threading.Thread(target=self.ping)
            self.ardThread.start()

#---------------------------------------------------------------
    def close(self):
        print("Closing Port 'A'")
        self.runThread = False
        self.arduino.close()
        #self.ardThread.join()

#---------------------------------------------------------------
    def calibrate(self):
        #
        self.arduino.write("C".encode()) # begin calibration
        #calibration here
        self.arduino.write("Z".encode()) #   end calibration
        print("Calibration Done 'A'")

#---------------------------------------------------------------
    def ping(self):
        while(self.runThread):
            self.arduino.write('P'.encode())  #send poll
            time.sleep(1)                     #wait for reply
            print(self.arduino.in_waiting)    #print how many chars in waiting
            while(self.arduino.in_waiting>0): #get chars from buffer
                self.data = self.arduino.read()
                #depending on data, change display in GUI
                print(str(self.data) + " 'A'")              #print chars
        print("Thread Ended 'A'")

#---------------------------------------------------------------

    def getStatus(self):
        if(self.data == 0):
            return "Processing"
        elif(self.data == 1):
            return "Reading"
        elif(self.data == 2):
            return "Done"
        elif(self.data == 3):
            return "Moving"
        elif(self.data == 4):
            return "Calibrating"
        else:
            return "Error"
#---------------------------------------------------------------
    def upload(self):
        _lambda = 0.5 #self.doubleSpinBox_DOA_d.value()
        _frequency = 900000000.0 #self.doubleSpinBox_center_freq.value() *10**6
        if((_frequency >=900000000.0) and (_frequency <=1200000000.0)):
            _spacing = _lambda * (300000000.0/_frequency)
            _turns = _spacing/(0.0000130258)
            _turns_str = str(int(_turns))
            #_spacing_str = str('%.3f'%(_spacing))
            _spacing_str = str(int( (_spacing*1000000.0)))
            print("_lambda: "+str(_lambda)+", _freq: " +str(_frequency) + ", _spacing: "+ str(_spacing)+ ", turns: '"+ _turns_str +"' , strSpacing: '" + _spacing_str + "' 'A'")
            self.arduino.write("S".encode())
            self.arduino.write(_spacing_str.encode())
            self.arduino.write("E".encode())
        else:
            print("_lambda: "+str(_lambda)+", _freq: " +str(_frequency)+" 'The frequency is not within paramaters' 'A'")

#---------------------------------------------------------------

#END
