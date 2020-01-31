from sense_hat import SenseHat
import time
import io
import subprocess
import os
import requests

#def menu_ui():


def get_pressure_from_location():
	f = open("gps_log", "r")
	log_line = f.read()
	#initializing variables
	latitude = None
	longitude = None
	while 1:
            log_line = log_line.split(":")
            print(log_line[1])
            if(log_line[0] == "NOFIX"):
                log_line = f.read()
            continue
            if(log_line[0] == "LOC"):
  		log_line = log_line[1].split(",")
            	latitude = float(log_line[0])
            	longitude = float(log_line[1])
            	break
    	##Calling API to know the weather
    	print("out of loop: lat %s and long %s" %(latitude,longitude))
    	response = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&appid=9de243494c0b295cca9337e1e96b00e2")
    	return response.json()

sense = SenseHat()
print(get_pressure_from_location())
while 1:
	temp = sense.get_temperature_from_humidity()
	print("[%s]Temperature_from_humidity: %s C" % (time.ctime(), temp))
	temp2 = sense.get_temperature_from_pressure()
	print("[%s]Temperature_from_pressure: %s C" % (time.ctime(), temp2))
	#cpu temp
	bashCommand = "/opt/vc/bin/vcgencmd measure_temp"
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output = str(process.communicate())
	output = output.split("=")
	output = output[1].split("\\")
	cpu_temp = output[0].split("'")
	print("[%s]Temperature_from_cpu: %s C" %(time.ctime(),cpu_temp[0]))

	pressure = sense.get_pressure()
	print("[%s]Pressure: %s Millibars" % (time.ctime(),pressure))
	print()
	time.sleep(2)
