from multiprocessing import Pool
from multiprocessing import cpu_count
import time
import math
from sense_hat import SenseHat
import psutil
import subprocess
import os

# sense hat API
sense = SenseHat()
sense.get_pressure()

# data lists
cpu_temperature = []
sh_pressure = []
sh_temperature_p = []
sh_temperature_h = []
timestamp = []

print("Insert run time:")
runtime = int(input())

#timer
start_time = time.time()
now = start_time

def recursive_stress():
    for i in range(0,100):
        i*i
    return

def get_cpu_temp():
    global cpu_temperature
    #cpu temp
    bashCommand = "/opt/vc/bin/vcgencmd measure_temp"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = str(process.communicate())
    output = output.split("=")
    output = output[1].split("\\")
    cpu_temp = output[0].split("'")
    cpu_temp = cpu_temp[0]
    print("CPUTEMP:%s" %(cpu_temp))
    #print(int(cpu_temp))
    cpu_temp.replace("'","")
    cpu_temperature.append(round(float(cpu_temp),1))
    return

def get_sensehat_data():
    # round numbers if need
    temperature_p = round(sense.get_temperature_from_pressure(),1)
    pressure = round(sense.get_pressure(),2)
    temperature_h = round(sense.get_temperature_from_humidity(),1)
    #put values on list
    global sh_temperature_p
    global sh_pressure
    global sh_temperature_h
    sh_temperature_p.append(temperature_p-11)
    sh_temperature_h.append(temperature_h-7.6) 
    sh_pressure.append(pressure-6.72)
    return


processes = cpu_count()
pool = Pool(processes)

print('stress')
while now < start_time + runtime:
    pool.imap(recursive_stress, range(processes))
    timestamp.append(now-start_time)
    # get data   
    get_sensehat_data()
    get_cpu_temp()
    now = time.time()   
pool.close()

#generate graph
# print values
print('end')
print(sh_temperature_p)
print(sh_temperature_h)
print(sh_pressure)
print(cpu_temperature)
load = os.getloadavg()
print(load)
print(len(sh_temperature_p))

# generate graph
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')
fig, ax = plt.subplots(2,1)
plt.tight_layout()
outside_temp = input('Enter real temperature:')
outside_pressure = input('Enter real pressure:')

# TEMPERATURE (pressure vs humidity vs CPU)
ax[0].plot(timestamp, sh_temperature_p,'-r' ,label = "Sensor Pressure")
ax[0].plot(timestamp, sh_temperature_h,'-g', label ="Sensor Humidity")
ax[0].plot(timestamp, cpu_temperature,'-b', label= "Sensor CPU")
ax[0].axhline(y=int(outside_temp), xmin=0.0, xmax=2000, color='m', label='Room Temperature')
ax[0].grid(True)
ax[0].legend(loc=0)
ax[0].set_ylim(ymin=10)
ax[0].set_ylim(ymax=55)
ax[0].set_xlim(xmin=0)
ax[0].set_xlim(xmax=runtime)
ax[0].set_title("Temperature Variation Upon CPU Stress test")
ax[0].set_ylabel('Temperature (C)')


# PRESSURE ( temp + barometric + CPU)
ax[1].set_xlabel('Time Elapsed (Seconds)')
ax[1].plot(timestamp, cpu_temperature,'-b', label = "CPU Temp")
ax1 = ax[1].twinx()
ax1.plot(timestamp, sh_pressure,'-r',label = "Pressure")
ax1.axhline(y=float(outside_pressure), xmin=0.0, xmax=2000, color='m', label='Real Pressure')
ax[1].set_ylim(ymin=10)
ax[1].set_ylim(ymax=55)
ax[1].set_xlim(xmin=0)
ax[1].set_xlim(xmax=runtime)
#ax1.set_ylim(ymin= 950)
#ax1.set_ylim(ymax=1020)
ax[1].set_title("Pressure Variation Upon CPU Stress test")
ax[1].set_ylabel('Temperature (ºC)')
ax1.set_ylabel('Pressure (mmHg)')


ax[1].legend(loc=2)
ax1.legend(loc=1)
now = time.time()
graphname = 'graph_no_variation' + str(now) + '.png'
plt.savefig(graphname ,bbox_inches='tight')
