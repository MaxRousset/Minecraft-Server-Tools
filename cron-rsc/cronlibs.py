#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""MST (Minecraft Server Tools)"""

from subprocess import run, check_output
from time import sleep
from xdg.BaseDirectory import xdg_config_home

CONF_FILE = xdg_config_home+"/mst/config"
WARNING = '\033[31m'
ENDC = '\033[0m'
INFO = '\033[93m'

def get_conf():
	infos = []
	conf = open(CONF_FILE, 'r')
	for line in conf:
		info = line.strip()
		infos.append(info)
	conf.close()
	return infos

def detect_screen():
	try:
		check_output(['screen', '-ls', 'minecraft_server'])
		return True
	except:
		return False

def start(location, version, ram_max):
	cmd = "cd "+location+" && screen -dmS minecraft_server java -Xms1G -Xmx"+ram_max+" -jar spigot-"+version+".jar"
	run([cmd],shell=True ,cwd=location)

def stop():
	print (WARNING+"ATTENTION ARRET DU SERVEUR !"+ENDC)
	run(["screen", "-S", "minecraft_server", "-p", "0", "-X", "stuff", "stop^M"])

	is_runing = detect_screen()

	while is_runing:
		print (WARNING+"\nArrêt complet du serveur ...\nVeuillez patienter ..."+ENDC)
		sleep(1)
		is_runing = detect_screen()
