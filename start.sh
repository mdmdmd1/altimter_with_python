#!/bin/bash

sleep 10

rm /home/pi/Desktop/Scripts/gps_log
rm /home/pi/Desktop/Scripts/last_run_log

while :
do
	if [ -c /dev/ttyUSB0 ]
	then
	echo 'GPS device found'
	/home/pi/Desktop/Scripts/gps.sh >> /home/pi/Desktop/Scripts/gps_log &
	sleep 5 
	python3 /home/pi/Desktop/Scripts/temp2.py >> /home/pi/Desktop/Scripts/last_run_log &
	break
	else
	echo 'GPS device not connected'
	sleep 5
	fi
done
