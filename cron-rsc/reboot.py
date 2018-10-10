#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Auto reboot"""

from subprocess import run
from time import sleep
from xdg.BaseDirectory import xdg_config_home
from cronlibs import get_conf, stop, start

# Get conf
CONF_FILE = xdg_config_home+"/mst/config"

infos = get_conf()
SERVER_LOCATION = infos[0]
SERVER_VERSION  = infos[1]
MAXIMUM_RAM = infos[2]

# Broadcast
run(["screen", "-S", "minecraft_server", "-p", "0", "-X", "stuff", "broadcast ATENTION ! reboot auto du serveur ! on se retrouve dans 30 secondes^M"])
sleep(10)

# Stop
stop()

# Start
start(SERVER_LOCATION, SERVER_VERSION, MAXIMUM_RAM)
