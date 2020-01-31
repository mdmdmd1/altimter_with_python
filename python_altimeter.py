from sense_hat import SenseHat
import time
import threading 
import requests
import time
import io
import subprocess
import os


sense = SenseHat()
sense.clear()

altitude = 0
latitude = 0
longitude = 0
menu = 1
sea_level_pressure = 0
pressure = 0
temperature = sense.get_temperature_from_pressure()
api_data = None
cpu_temp = 0

def start_fix_nofix():
    sense.clear()
    for blink in range (10):
        for x in range(8):
           sense.set_pixel(x,3,255,0,0)
           sense.set_pixel(3,x,255,0,0)
           sense.set_pixel(4,x,255,0,0)
           sense.set_pixel(x,4,255,0,0)
        time.sleep(.2)
        sense.clear()
        time.sleep(.1)
    return

def start_fix_fixfound():
    for blink in range (10):
        for x in range(8):
            sense.set_pixel(x,3,0,255,0)
            sense.set_pixel(3,x,0,255,0)
            sense.set_pixel(4,x,0,255,0)
            sense.set_pixel(x,4,0,255,0)
        time.sleep(.1)
        time.sleep(.1)
    return

def get_gps_first_data():
    while True:
        with open('gps_log') as fp:
            for line in fp:
                #nofix
                if(line[0] == "N"):
                    print("N")
                    continue
                #altitude
                if(line[0] == "A"):
                    continue
                #location
                if(line[0] == "L"):
                    line = line.split(":")
                    line = line[1].split(",")
                    time.sleep(2)
                    display_end.start()
                    latitude = float(line[0])/100
                    longitude = float(line[2])/100
                    if(line[1] != "N"):
                        latitude = latitude * -1
                    if(line[3] != 'E'):
                        longitude = longitude * -1
                    print("FIRST GPS DATA:" + str(latitude) + str(longitude))
                    return
        start_fix_nofix()
        time.sleep(8)        

def get_gps_latest_data():
    with open('gps_log') as fp:
        for line in reversed(list(fp)):
            #nofix
            line = line.rstrip()
            if(line[0] == "N"):
                print("N")
                continue
             #altitude
            if(line[0] == "A"):
                continue
            #location
            if(line[0] == "L"):
                line = line.split(":")
                line = line[1].split(",")
                time.sleep(2)                
                global latitude
                global longitude
                latitude = float(line[0])/100
                longitude = float(line[2])/100
                if(line[1] != "N"):
                    latitude = latitude * -1
                if(line[3] != 'E'):
                    longitude = longitude * -1
                print("LATEST GPS:" + str(latitude) + str(longitude))
                return


def start_fix():
    display_start.start()
    time.sleep(2)
    get_gps_first_data()
    print("GPS First data loaded")
    return

## Initiliazing altimeter
# starting thread for display without delay.
display_start = threading.Thread(target=start_fix_nofix)
display_end = threading.Thread(target=start_fix_fixfound)

start_fix()
time.sleep(5)
sense.clear()

## Main Menu
def show_menu():
    if menu == 1:
        #altitude pressao
        sense.show_letter("P" ,text_colour=[0,0,255], back_colour=[0,0,0])
    elif menu == 2:
        #altitude verdadeira
        sense.show_letter("V", text_colour=[0,255,0], back_colour=[0,0,0])
    elif menu == 3:
        #temperatura
        sense.show_letter("T", text_colour=[250,128,114], back_colour=[0,0,0])
    elif menu == 4:
        #weather and calibrating info
        sense.show_letter("M", text_colour=[255,255,0], back_colour=[0,0,0])
    elif menu ==5: 
        sense.show_letter("C", text_colour=[128,0,128], back_colour=[0,0,0])

def show_menu_name():
    global menu

    #sense.show_message(str(menu))
    if menu == 1:
        #altitude pressao
        sense.show_message("Altitude Pressao", text_colour=[0,0,255], back_colour=[0,0,0], scroll_speed=.1)
        show_menu()
    elif menu == 2: 
        #altitude verdadeira
        sense.show_message("Altitude Verdadeira" ,text_colour=[0,255,0], back_colour=[0,0,0], scroll_speed=.1)
        show_menu()
    elif menu == 3:
        #temperatura
        sense.show_message("Temperatura atual", text_colour=[250,128,114], back_colour=[0,0,0], scroll_speed=.1)
        show_menu()
    elif menu == 4:
        #weather and calibrating info
        sense.show_message("Meteorologia", text_colour=[255,255,0], back_colour=[0,0,0], scroll_speed=.1)
        show_menu()
    elif menu == 5:
        #cpu temp
        sense.show_message("Temperatura CPU", text_colour=[128,0,128], back_colour=[0,0,0], scroll_speed=.1)
        show_menu()

def internet():
    import urllib
    from urllib import request
    try:
        urllib.request.urlopen('http://google.com', timeout=5)
        return True
    except:
        return False


def show_data():
    if menu == 0:
        return 0
    elif menu == 1:
        # continuous datastream from pressure altitude
        get_senser_hat_latest_data()
        pressure_altitude_algorithm()
        sense.show_message(str(altitude) + ' M', text_colour=[0,0,255], back_colour=[0,0,0], scroll_speed=.1)
        print(altitude)
        show_menu()
    elif menu == 2:
        if not internet():
            return
        full_sensor_refresh()
        pressure_altitude_algorithm()
        sense.show_message(str(altitude) + ' M', text_colour=[0,255,0], back_colour=[0,0,0], scroll_speed=.10)
        print(altitude)
        show_menu()
        # continous datastream from real altitude
    elif menu == 3:
        get_senser_hat_latest_data()
        temperature1 = str(round(temperature,1))
        sense.show_message(str(temperature1) + " C", text_colour=[250,128,114], back_colour=[0,0,0], scroll_speed=.10)
        show_menu()
    elif menu == 4:
        if not internet():
            return
        # datastream from weather API
        get_gps_latest_data()
        get_api_latest_data()
        sense.show_message(api_data['name'] + ', ', text_colour=[255,255,0], back_colour=[0,0,0], scroll_speed=.1)
        sense.show_message(str(api_data['weather'][0]['main']), text_colour=[255,255,0], back_colour=[0,0,0], scroll_speed=.1)
        show_menu()
    elif menu == 5:
        get_cpu_temp_latest_data()
        sense.show_message(str(cpu_temp) + ' C', text_colour=[128,0,128], back_colour=[0,0,0], scroll_speed=.10)
        show_menu()
    return 

def full_sensor_refresh():
    get_gps_latest_data()
    get_api_latest_data()
    get_senser_hat_latest_data()
    return

def get_cpu_temp_latest_data():
    global cpu_temp
    #cpu temp
    bashCommand = "/opt/vc/bin/vcgencmd measure_temp"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = str(process.communicate())
    output = output.split("=")
    output = output[1].split("\\")
    cpu_temp = output[0].split("'")
    cpu_temp = cpu_temp[0]
    print("CPU:%s" %(cpu_temp))


def get_api_latest_data():
    global api_data
    api_data = requests.get("http://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&appid=9de243494c0b295cca9337e1e96b00e2")
    api_data = api_data.json()
    print(api_data)
    return 

def get_senser_hat_latest_data():
    global temperature
    global pressure
    global sea_level_pressure
    global api_data
    temperature = sense.get_temperature_from_pressure()
    
    ## pressure calculation
    ## needs pressure test and ffixing
    pressure1 = sense.get_pressure()
    pressure = sense.get_pressure() - 6.72
    ## sea level pressure
    ## Se altitude pressão, valor default 1023,24 ## verificar
    if menu == 1:
        sea_level_pressure = 1023.2
        temperature = 15
        print(sea_level_pressure)
    elif menu == 2:
        get_api_latest_data()
        sea_level_pressure = float(api_data['main']['pressure'])
        print("MSL" + str(sea_level_pressure))
    return 
    
def pressure_altitude_algorithm():
    if temperature == None:
        return
    elif pressure == 0:
        return
    elif sea_level_pressure == None:
        return
    print("algorith values: temperature:" + str(temperature) + " MSL:" + str(sea_level_pressure) + " Pressure" + str(pressure))
    #hypsometric formula
    global altitude 
    altitude = ((pow((sea_level_pressure / pressure), 1/5.257999999999) - 1.0) * (temperature -11 + 273.15)) / 0.0065;
    altitude = str(round(altitude, 1))
    return

## Loop for menu and controls
show_menu()
## 1- Setting controls
while True:
    for event in sense.stick.get_events():
        if event.action == 'pressed' and event.direction == 'up':
            if menu > 1:
                menu-=1
            show_menu()    
        if event.action == 'pressed' and event.direction == 'down':
            if menu < 5:
                menu+=1
            show_menu()
        if event.action == 'pressed' and event.direction == 'right':
            print("Select DataStream")           
            ## start threading, so menu still works.
            show_data()
        if event.action == 'pressed' and event.direction == 'left':
            print("Back From DataStream")
            show_menu()
        if event.action == 'pressed' and event.direction == 'middle':
            print("Menu Name Selected")
            show_menu_name()

