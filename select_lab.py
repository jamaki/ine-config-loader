#!/usr/bin/python
# Version 1.0
# Author Nick Shaw - www.geekynick.co.uk
# Script to select an initial config from the INE configs and apply it to the necessary routers.

from os import listdir
import json, time, pexpect, sys

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

def PrintDict(thedict):
    for i in thedict:
        print "%s : %s" % (i,thedict[i])

def configdevice(ip,port,config):
    child = pexpect.spawn('telnet %s %s' % (ip, port))
    print "Connecting to  %s:%s" % (ip, port)
    child.timeout = 10 
    child.logfile = sys.stdout
    #child.sendline('')
    child.sendcontrol('m')
    m = child.expect(['>','#'])
    if m==0:
        child.sendline('en')
    elif m==1:
        print "Enabled on %s:%s" % (ip, port)
    child.sendline('config replace flash:blank-cfg.cfg force')
    time.sleep(5)
    child.sendline('conf t')
    with open(config) as f:
        for line in f:
            line.rstrip('\0')
            child.sendline(line)


#List directories
path = '/home/nick/ine_configs'
directorylist = listdir(path)
directorylist.sort()
directorydict = ListToDict(directorylist)
PrintDict(directorydict)
choice = input('Make a choice: ')
path += '/%s' %(directorydict[choice])

#List subfolder
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
    configfile = path+'/'+i+'.txt'
    print 'Applying %s to %s' %(configfile, i)
    configdevice(devices[i]['ip'], devices[i]['port'], configfile)

