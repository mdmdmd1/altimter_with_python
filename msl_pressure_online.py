#!/usr/bin/python
import math
import sys

if __name__ == '__main__':
	# get altitude , pressure reading and msl pressure ?
   if args.altitude is None:
      args.altitude = 112.2  # Value from my GPS for my house
   if args.pressure is None:
      print "Pressure value required"
      sys.exit(40)
   if args.msl is None:
      args.msl = 1013.25
   args.pressure = float(args.pressure)
   args.altitude = float(args.altitude)
   args.msl = float(args.msl)
   print "inputs:"
   print "Alt:", args.altitude, "Pressure:", args.pressure, "MSL:", args.msl
   print "Sealevel:",args.pressure/pow(1-(args.altitude/44330.0),5.255)
   print "Alt:",(44330.0*(1-pow(args.pressure/args.msl,1/5.255)))
