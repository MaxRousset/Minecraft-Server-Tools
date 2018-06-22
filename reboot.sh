#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Auto reboot"""
# Pour un reboot auto tout les jours a 6 heures du matin :
# 00 6 * * * /home/spigot/.bin/reboot.sh
# a placer dans crontab

from subprocess import run
from time import sleep
from xdg.BaseDirectory import xdg_config_home
import mstools



CONF_FILE = xdg_config_home+"/mst/config"


conf = open(CONF_FILE, 'r')
infos = mstools.get_conf()
SERVER_LOCATION = infos[0]
SERVER_VERSION  = infos[1]
MAXIMUM_RAM = infos[2]



# location = "/home/spigot/server"

# Broadcast
run(["screen", "-S", "minecraft_server", "-p", "0", "-X", "stuff", "broadcast ATENTION ! reboot auto du serveur ! on se retrouve dans 30 secondes^M"])
sleep(10)


#stop
mstools.stop()

#start
mstools.start(SERVER_LOCATION, SERVER_VERSION, MAXIMUM_RAM)