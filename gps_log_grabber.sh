#!/bin/bash

file='/dev/ttyUSB0'

while read line; do
if [ -z '\$line' ]; then
	echo 'Device empty - Check connection'
else
	#Parsing Message ID
	msg_id=$(echo $line | cut -d ',' -f1)
	#echo 'msg_id:'$msg_id
	# getting altitude
	if [[ $msg_id == "\$GPGGA" ]]; then
		#Veryfing if fix = 1
		fix=$(echo $line | cut -d ',' -f7)
		if [[ $fix == 1 ]]; then
			#Altitude message
			altitude=$(echo $line | cut -d ',' -f10)
			altitude_measure=$(echo $line | cut -d ',' -f11)
			echo "ALTI:${altitude} ${altitude_measure}"
		else
			echo 'NOFIX'
		fi
	fi
 	#Latitude & Longitude
	if [[ $msg_id == "\$GPGLL" ]]; then
               	#Validate if good data
               	data_valid=$(echo $line | cut -d ',' -f7)
		if [[ $data_valid == "A" ]]; then
               		#Location message
               		latitude=$(echo $line | cut -d ',' -f2,3)
               		longitude=$(echo $line | cut -d ',' -f4,5)
               		out="LOC:${latitude},${longitude}"
			echo $out
		fi
	fi
fi

done < $file
