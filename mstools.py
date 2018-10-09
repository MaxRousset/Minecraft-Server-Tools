#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""MST (Minecraft Server Tools)"""

from subprocess import run, check_output
from time import sleep
from xdg.BaseDirectory import xdg_config_home
from crontab import CronTab
import os

CONF_DIR = xdg_config_home+"/mst"
CONF_FILE = xdg_config_home+"/mst/config"
WARNING = '\033[31m'
ENDC = '\033[0m'
INFO = '\033[93m'

def build_spigot(server_version):
	run(["rm", "-fr", "/tmp/buildspigot"])
	run(["mkdir", "/tmp/buildspigot"])
	run(["wget", "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"],cwd="/tmp/buildspigot")
	run(["java", "-jar", "BuildTools.jar", "--rev", server_version],cwd="/tmp/buildspigot")

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

def enable_autoreboot():
	reboot_script = os.path.abspath(os.path.join(__file__, os.pardir))+"/cron-rsc/reboot.py"
	check = check_cron("MST autoreboot")
	
	if check:
		print("Autoreboot deja en route")
	else:
		print(INFO+"Entrez l' heure du redemarage auto (exemple: 13)\n"+ENDC)
		reboot_hour = input()
		cron_time = "0 "+reboot_hour+" * * *"

		# use current user for cron
		cron = CronTab(user=True)
		# create task
		job = cron.new(command=reboot_script, comment="MST autoreboot")
		# set time
		job.setall(cron_time)
		# write to file
		cron.write()

def disable_autoreboot():
	# use current user for cron
	cron = CronTab(user=True)
	# remove task
	cron.remove_all(comment="MST autoreboot")
	# write to file
	cron.write()

def enable_autorestart():
	monitor_script = os.path.abspath(os.path.join(__file__, os.pardir))+"/cron-rsc/detect-crash.py"
	check = check_cron("MST autorestart")
	
	if check:
		print("Autorestart deja en route")
	else:
		# use current user for cron
		cron = CronTab(user=True)
		# create task
		job = cron.new(command=monitor_script, comment="MST autorestart")
		# set time
		job.minute.every(1)
		# write to file
		cron.write()

def disable_autorestart():
	# use current user for cron
	cron = CronTab(user=True)
	# remove task
	cron.remove_all(comment="MST autorestart")
	# write to file
	cron.write()

def check_cron(job):
	#check for a specific cron task from comment
	cron = CronTab(user=True)
	test = cron.find_comment(job)

	for item1 in test:
		test = 0
	if not test:
		return True
	else:
		return False
