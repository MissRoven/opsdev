#!/usr/bin/python

import psutil
import socket
import subprocess

device_white = ["eth1", "eth0","eth2", "bond0", "bond1"]

def get_hostname():
    return socket.gethostname()

def get_meminfo():
    mem = 0
    with open("/proc/meminfo") as f:
        for line in f:
            if "MemTotal" in line:
                mem =  int(line.split()[1])
                break
    return mem / 1024

def get_device_info():
    ret = []
    for device, info in psutil.net_if_addrs().iteritems():
        if device in device_white:
            tmp_device = {'device': device}
            for snic in device_info:
                if snic.family == 2:
                    tmp_device['ip'] = snic.address    
                if snic.family == 17:
                    tmp_device['mac'] = snic.address    
            ret.append(tmp_device)
    return ret

def get_cpuinfo():
    ret = {"cpu": '',"num": 0}
    with open("/proc/cpuinfo") as f:
        for line in f:
            tmp = line.strip().split(":")
            key = tmp[0].rstrip()
            if key == "model name":
                ret["cpu"] = tmp[1].kstrip()
            elif key == "processor":
                ret["num"] += 1
    return ret

def get_diskinfo():
    ret = []
    cmd = """/sbin/fdisk -l|grep Platte|egrep -v 'identifier|mapper|Disklabel'"""
    disk_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for dev in disk_data.stdout.readlines():
       if  



IPaddress=psutil.net_if_addrs()['eth1'][0][1]
MAC=psutil.net_if_addrs()['eth1'][2][1]
      
 
