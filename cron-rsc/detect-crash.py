#!/usr/bin/python3

""" Monitoring serveur minecraft """

import requests, time, datetime
from subprocess import run
from xdg.BaseDirectory import xdg_config_home
import mstools

now = datetime.datetime.now()

"""Intervalle en minutes entre deux check"""
INTERVALL = 1
SERVER_ADRESS = '127.0.0.1'
SERVER_PORT = 25565

"""logs file location"""
LOGS_FILE = xdg_config_home+"/mst/logs"

"""Conf file location"""
CONF_FILE = xdg_config_home+"/mst/config"

"""Get conf"""
conf = open(CONF_FILE, 'r')
infos = mstools.get_conf()
SERVER_LOCATION = infos[0]
SERVER_VERSION  = infos[1]
MAXIMUM_RAM = infos[2]


try:
	conf = open(LOGS_FILE, 'w')

except IOError:
	run(["touch", LOGS_FILE])


is_runing = mstools.detect_screen()

if is_runing:
	current_date = now.strftime("%Y-%m-%d %H:%M")
	conf.write("server up "+current_date+"\n")

else:
	#if down try restart
	mstools.start(SERVER_LOCATION, SERVER_VERSION, MAXIMUM_RAM)

	current_date = now.strftime("%Y-%m-%d %H:%M")
	conf.write("server restarted "+current_date+"\n")