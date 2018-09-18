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
s1 = 23
s2 = 22
s3 = 27
s4 = 17

#Setup GPIO for the switches
GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(s2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(s3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(s4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#Button 1: CLears the timer
def button1(ch1):
    global timer
    timer = 0
    print ("\n" * 50)

#Buttton 2: Increases the delay between readings
def button2(ch2):
    global delay
    if (delay >= 2):
        delay = 0.5
    else:
        delay = delay * 2    

#Button 3 : Gets readings
def button3(ch3):
    global y
    y = not y      

#Button 4 : displays values
def button4(ch4):
    global arr
    print('_______________________________________________')
    print('Time        Timer          Pot    Temp   Light')

    for i in range(5,0,-1):
        if i<len(arr):

            print(arr[len(arr)-i])   
            print('_____________________________________________')

#interrrupt
GPIO.add_event_detect(s1,GPIO.FALLING,button=button1,bouncetime=500)
GPIO.add_event_detect(s2,GPIO.FALLING,button=button2,bouncetime=500)
GPIO.add_event_detect(s3,GPIO.FALLING,button=button3,bouncetime=500)
GPIO.add_event_detect(s4,GPIO.FALLING,button=button4,bouncetime=500)

# function to read ADC data from a ch
def ADC_Data(ch): # ch must be an integer 0-7
    adc = spi.xfer2([1,(8+ch)<<4,0]) # sending 3 bytes
    data = ((adc[1]&3) << 8) + adc[2]
    return data

# function to convert data to voltage level (ALSO function for pot)
# places: number of decimal places needed
def ConvertVolts(data):
    volts = (data * 3.3) / float(1023)
    return volts

#function to convert voltage to temperature
def Temperature(voltage):
    temp = voltage
    temp = ((temp - 0.5)/0.01)
    return temp

#function to convert voltage to %
def Percent (voltage):
    per = (int (voltage/3.1*100))
    return per

# Define sensor chs
ch1 = 0
ch2 = 1
ch3 = 2

# Define delay between readings
delay = .5

#Default values
timer = 0
second = 0
minute = 0
hour = 0
arr = []

#Function to run
y = True 
try:
    while 1:
        if(y == True):
            sensor_data1 = ADC_Data (ch1)
            pot = round(ConvertVolts(sensor_data1),2)
            sensor_data2 = ADC_Data (ch2)
            sensor_volt2 = round(ConvertVolts(sensor_data2),2)
            sensor_data3 = ADC_Data (ch3)
            sensor_volt3 = ConvertVolts(sensor_data3)
            temp = round(Temperature(sensor_volt3),2)
            light = Percent(sensor_volt2)
            element = (str(time.strftime("%H:%M:%S   ")) + str(hour).zfill(2) +':' +str(minute).zfill(2) +':' + str(int(timer*10)).zfill(2) + "     " + str(pot)+ 'V    ' + str(temp) + 'C     ' + str(light) +'%')
            arr.append(element)
    
        # Wait before repeating loop
        time.sleep(delay)
        timer = timer + delay
       
        if timer >= 6:
            timer = timer - 6
            minute = minute + 1
        if minute >= 60:
            minute = minute - 60
            hour = hour + 1

#Interrupt to allow exit of code
except KeyboardInterrupt:
    spi.close()
