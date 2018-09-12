import spidev
import time
import os
 
# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def Read(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  adc_value = ((adc[1]&3) << 8) + adc[2]
  return adc_value
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ADC_to_Volts(value):
  volts = round((value * 3.3) / float(1024),2)
  return volts
 
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def volts_to_degrees(t):
  Tc = 0.01
  V_0c = 0.5
      
  temp = round((t-V_0c)/Tc, 2)
  return temp
 
# Define frequency between readings
#**********************************
def frequency(d):
  if d==0.5:
    d = 1
  elif d == 1:
    d=2
  else:
    d = 0.5
    
  return d    

      
frequency = 1
 
while True:

  # Read the light sensor data
  pot_value = Read(2)
  pot_volts = ADC_to_Volts(pot_value) 
 
  # Read the light sensor data
  light_value = Read(1)
  light_percent = round((light_value*100)/float(1007),2)
 
  # Read the temperature sensor data
  temp_value = Read(0)
  temp_volts = ADC_to_Volts(temp_value)
  temp       = volts_to_degrees(temp_volts)
 
  # Print out results
  #*************************************
 
  # Wait before repeating loop
  time.sleep(frequency)
  # Print out results
  print "--------------------------------------------"
  print("Light: {} ({}%)".format(light_value,light_percent))
  print("Temp : {} ({}V) {} deg C".format(temp_value,temp_volts,temp))  