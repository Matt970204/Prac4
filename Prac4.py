#!/usr/bin/python
import spidev
import time
import os
import sys
import RPi.GPIO as GPIO

# Open SPI bus
spi = spidev.SpiDev() # create spi object
spi.open(0,0)
spi.max_speed_hz = 1000000

# RPI has one bus (#0) and two devices (#0 & #1)
GPIO.setmode(GPIO.BCM)
switch_1 = 23
switch_2 = 22
switch_3 = 27
switch_4 = 17
# switch 1 & switch 2: input – pull-up
GPIO.setup(switch_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(switch_4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

count = 0

def callback1(channel):
    global timer
    timer = 0
    print ("\n" * 100)

def callback2(channel2):
     global y
     global arr
     arr.clear()
     global count
     count = count + 1
     if (count%2 == 0):
         y = True
     else:
         y = False
     
def callback3(channel3):
     global delay
     if (delay >= 2):
         delay = 0.5
     else:
         delay = delay * 2 

def callback4(channel4):
    global arr
    print('_______________________________________________')
    print('Time        Timer          Pot    Temp   Light')

    for i in range(0,5):
        print(arr[i])
        print('_____________________________________________')

GPIO.add_event_detect(switch_1,GPIO.FALLING,callback=callback1,bouncetime=200)
GPIO.add_event_detect(switch_2,GPIO.FALLING,callback=callback2,bouncetime=200)
GPIO.add_event_detect(switch_3,GPIO.FALLING,callback=callback3,bouncetime=200)
GPIO.add_event_detect(switch_4,GPIO.FALLING,callback=callback4,bouncetime=200)

# function to read ADC data from a channel
def GetData(channel): # channel must be an integer 0-7
 adc = spi.xfer2([1,(8+channel)<<4,0]) # sending 3 bytes
 data = ((adc[1]&3) << 8) + adc[2]
 return data

# function to convert data to voltage level (ALSO function for pot)
# places: number of decimal places needed
def ConvertVolts(data,places):
 volts = (data * 3.3) / float(1023)
 volts = round(volts,places)
 return volts

#function to convert voltage to temperature
def Temperature (voltage):
    temp = voltage
    temp = int ((temp - 0.5)/0.01 )
    return temp

#function to convert voltage to %
def Percent (voltage):
    per = (int (voltage/3.1*100))
    return per

# Define sensor channels
channel1 = 0
channel2 = 1
channel3 = 2
# Define delay between readings
delay = .5

timer = 0.5
arr = []

y = True 
try:
    while 1:
        if(y == True):

            sensor_data1 = GetData (channel1)
            pot = ConvertVolts(sensor_data1,2)
            sensor_data2 = GetData (channel2)
            sensor_volt2 = ConvertVolts(sensor_data2,2)
            sensor_data3 = GetData (channel3)
            sensor_volt3 = ConvertVolts(sensor_data3,2)
            temp = Temperature (sensor_volt3)
            light = Percent(sensor_volt2)
            
            element = (str(time.strftime("%H:%M:%S   ")) + '00:00:' + str(timer)+ "     " + str(pot)+ 'V    ' + str(temp) + 'C     ' + str(light) +'%')
            arr.append(element) 
           
           # print (time.strftime("%H:%M:%S  "),'00:00:' + str(timer),'   ',str(pot)+ 'V   ' , str(temp) + 'C   ', str(light) +'%')
        

        # Wait before repeating loop
        time.sleep(delay)
        timer = timer + delay

except KeyboardInterrupt:
    spi.close()
