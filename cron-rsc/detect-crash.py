#!/usr/bin/python3

""" Monitoring serveur minecraft """

import requests, time, datetime
from subprocess import run
from xdg.BaseDirectory import xdg_config_home
from cronlibs import get_conf, detect_screen, start

now = datetime.datetime.now()

"""logs file location"""
LOGS_FILE = xdg_config_home+"/mst/logs"

"""Conf file location"""
CONF_FILE = xdg_config_home+"/mst/config"

"""Get conf"""
infos = get_conf()
SERVER_LOCATION = infos[0]
SERVER_VERSION  = infos[1]
MAXIMUM_RAM = infos[2]

try:
	conf = open(LOGS_FILE, 'w')

except IOError:
	run(["touch", LOGS_FILE])

is_runing = detect_screen()

if is_runing:
	current_date = now.strftime("%Y-%m-%d %H:%M")
	conf.write("server up "+current_date+"\n")

else:
	#if down try restart
	start(SERVER_LOCATION, SERVER_VERSION, MAXIMUM_RAM)
	#write to logs
	current_date = now.strftime("%Y-%m-%d %H:%M")
	conf.write("server restarted "+current_date+"\n")