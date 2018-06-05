#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""MST (Minecraft Server Tools)"""

from subprocess import run, check_output
from time import sleep
from xdg.BaseDirectory import xdg_config_home

CONF_DIR = xdg_config_home+"/mst"
CONF_FILE = xdg_config_home+"/mst/config"
WARNING = '\033[31m'
ENDC = '\033[0m'
INFO = '\033[93m'

def first_setup_wizard():
	infos = []

	run(["mkdir", CONF_DIR])
	run(["touch", CONF_FILE])
	conf = open(CONF_FILE, 'w')

	location = input(INFO+"Entrez l'emplacement du serveur (exemple: /home/spigot/server)\n"+ENDC)
	infos.append(location)
	conf.write(location+"\n")

	version = input(INFO+"Entrez la version du serveur (exemple: 1.12.2)\n"+ENDC)
	infos.append(version)
	conf.write(version+"\n")

	ram_max = input(INFO+"Entrez la quantiter de ram maximum en giga (exemple: 6G)\n"+ENDC)
	infos.append(ram_max)
	conf.write(ram_max+"\n")
	
	conf.close()
	return infos

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

	cmd = "cd "+location+" && screen -S minecraft_server java -Xms1G -Xmx"+ram_max+" -jar spigot-"+version+".jar"
	run([cmd],shell=True ,cwd=location)

def stop():
	print (WARNING+"ATTENTION ARRET DU SERVEUR !"+ENDC)
	run(["screen", "-S", "minecraft_server", "-p", "0", "-X", "stuff", "stop^M"])

	is_runing = detect_screen()

	while is_runing:
		print (WARNING+"\nArrêt complet du serveur ...\nVeuillez patienter ..."+ENDC)
		sleep(1)
		is_runing = detect_screen()