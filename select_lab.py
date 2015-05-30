#!/usr/bin/python
# Version 1.0
# Author Nick Shaw - www.geekynick.co.uk
# Script to select an initial config from the INE configs and apply it to the necessary routers.

from os import listdir
import json, time, pexpect, sys

#Set the path where this script is - CHANGE THIS ON A NEW BOX!
path = '/home/nick/ine-config-loader/ine.ccie.rsv5.workbook.initial.configs'

#Turn list into dictionary
def ListToDict(thelist):
    index = 0
    thedict = {}
    for i in thelist:
        #ignore dotfiles and self
        if (i[0] != '.') and (i != 'select_lab.py'):
            thedict[index] = i
        index += 1
    return thedict

#Print out the list of choices
def PrintDict(thedict):
    for i in thedict:
        print "%s : %s" % (i,thedict[i])

#Apply the configuration to the device
def configdevice(ip,port,config):
    child = pexpect.spawn('telnet %s %s' % (ip, port)) #Start the telnet
    print "Connecting to  %s:%s" % (ip, port) #Print something for debugging
    child.timeout = 10 #Set a timeout value
    child.logfile = sys.stdout #Log to screen
    child.sendcontrol('m') #Send a carriage return. Sending '' wasn't successful on a router which had been idle for a while.
    m = child.expect(['>','#']) #Figure out whether it needs enabling
    if m==0:
        child.sendline('en')
    elif m==1:
        print "Enabled on %s:%s" % (ip, port)
    child.sendline('config replace flash:blank-cfg.cfg force') #Clear the config back to basics
    time.sleep(5) #Let the router do it's config replace in peace!
    child.sendline('conf t')
    with open(config) as f: #Load the config file
        for line in f: #Read it line by line
            line.rstrip('\0') #Lose any null characters
            child.sendline(line) #Send the config


#List directories
directorylist = listdir(path)
directorylist.sort()
directorydict = ListToDict(directorylist)
PrintDict(directorydict)
choice = input('Make a choice: ')
path += '/%s' %(directorydict[choice])

#List subfolders
directorylist = listdir(path)
directorylist.sort()
directorydict = ListToDict(directorylist)
PrintDict(directorydict)
choice = input('Make a choice: ')
path += '/%s' %(directorydict[choice])

#Get devices to be configured
directorylist = listdir(path)
devicestoconfig=[]
for i in directorylist:
    devicestoconfig.append(i[0:i.index('.')])

#Get device definitions from json file
with open('devices.json') as data_file:
    devices = json.load(data_file)

#print devices['R1']['ip']
for i in devicestoconfig:
    configfile = path+'/'+i+'.txt' #Append the directory with the router name and .txt
    print 'Applying %s to %s' %(configfile, i)
    configdevice(devices[i]['ip'], devices[i]['port'], configfile)

