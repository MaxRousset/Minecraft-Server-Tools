#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""MST (Minecraft Server Tools)"""

import mstools
import cmd
from subprocess import run
from shutil import which
from time import sleep
from xdg.BaseDirectory import xdg_config_home

CONF_DIR = xdg_config_home+"/mst"
CONF_FILE = xdg_config_home+"/mst/config"
DEPENDANCES=["wget","java","screen","git"]
WARNING = '\033[31m'
HEADER = '\033[95m'
OKGREEN = '\033[92m'
INFO = '\033[93m'
ENDC = '\033[0m'

# Verifie que les dependance sont bien installler
for prog in DEPENDANCES:
	reponse = str(which(prog) is not None)
	if reponse:
		pass
	else:
		print (WARNING+"Veuillez installer %s pour continuer" %prog+ENDC)
		exit(0)

# Verifie qu'une config existe sinon en creer une
try:
	infos = mstools.get_conf()
	SERVER_LOCATION= infos[0]
	SERVER_VERSION  = infos[1]
	MAXIMUM_RAM = infos[2]
except IOError:
	infos = mstools.first_setup_wizard()
	SERVER_LOCATION= infos[0]
	SERVER_VERSION  = infos[1]
	MAXIMUM_RAM = infos[2]

class CLISimple (cmd.Cmd) :
	run("clear")

	intro = HEADER+'Minecraft Server Tools (help pour de l\'aide)'+ENDC
	doc_header = INFO+'Aide sur les commandes (help <cmd>) :'+ENDC
	undoc_header = INFO+'Commandes non documentées'+ENDC
	prompt = OKGREEN+'MST > '+ENDC

	def do_start(self, line):
		"""Démarrer le serveur minecraft"""
		
		run("clear")
		is_runing = mstools.detect_screen()
		if not is_runing:
			print (INFO+"Pour retourner au menu, utilisez la combinaison de touches ctrl+a+d\nAppuyez sur n'importe quelle touche pour continuer\n"+ENDC)
			nimp = input()

			mstools.start(SERVER_LOCATION, SERVER_VERSION, MAXIMUM_RAM)
			run(["screen", "-x"])
		else:
			print(WARNING+"Serveur deja en route !\nVeuillez l eteindre ou le redemarrer"+ENDC)
			nimp = input()

	def do_status (self, line) :
		"""Infos sur l'etat actuel"""
		is_runing = mstools.detect_screen()
		if is_runing:
			print (INFO+"Serveur : "+OKGREEN+"UP"+ENDC)
		else:
			print (INFO+"Serveur : "+WARNING+"DOWN"+ENDC)

		print (INFO+"Version : "+ENDC+SERVER_VERSION)
		print (INFO+"Ram: "+ENDC+MAXIMUM_RAM)
		print (INFO+"Location : "+ENDC+SERVER_LOCATION)

		check = mstools.check_cron("MST autorestart")
		if check:
			print(INFO+"Autorestart: "+OKGREEN+"ON")
		else:
			print(INFO+"Autorestart: "+WARNING+"OFF")

		check = mstools.check_cron("MST autoreboot")
		if check:
			print(INFO+"Autoreboot: "+OKGREEN+"ON")
		else:
			print(INFO+"Autoreboot: "+WARNING+"OFF")

	def do_access (self, line) :
		"""Accéder à la console du serveur minecraft"""

		print (INFO+"Pour retourner au menu, utilisez la combinaison de touches ctrl+a+d\nAppuyez sur n'importe quelle touche pour continuer\n"+ENDC)
		nimp = input()
		run(["screen", "-x"])

	def do_restart (self, line) :
		"""Redémarre le serveur minecraft"""

		print (WARNING+"ATTENTION REDEMARRAGE DU SERVEUR !"+ENDC)
		print (INFO+"Appuyez sur n'importe quelle touche pour continuer\n"+ENDC)
		nimp = input()
		run(["screen", "-S", "minecraft_server", "-p", "0", "-X", "stuff", "broadcast reboot du serveur ! on se retrouve dans 30 secondes^M"])
		sleep(5)

		mstools.stop()

		mstools.start(SERVER_LOCATION, SERVER_VERSION, MAXIMUM_RAM)
		run(["screen", "-x"])
		
	def do_logs(self, line):
		"""Accéder au log les plus récents"""

		run(["cat", "logs/latest.log"],cwd=SERVER_LOCATION)
		print (INFO+"\nAppuyez sur n'importe quelle touche pour retourner au menu"+ENDC)
		nimp = input()

	def do_change(self, line):
		"""Changer les parametres du serveur (dossier, version, ...)"""

		run(["rm", "-r", CONF_DIR])
		mstools.first_setup_wizard()
		
		"""Redemarage necessaire pour apliquer les changements"""
		print (INFO+"\nRedemarage pour apliquer les changements"+ENDC)
		print (INFO+"\nAppuyez sur n'importe quelle touche pour quitter"+ENDC)
		nimp = input()
		exit(0)

	def do_autorestart_on(self, line):
		"""Active l'autorestart en cas de crash"""
		mstools.enable_autorestart()

	def do_autorestart_off(self, line):
		"""Desactive l'autorestart en cas de crash"""
		mstools.disable_autorestart()

	def do_autoreboot_on(self, line):
		"""Active l'autoreboot quotidien"""
		mstools.enable_autoreboot()

	def do_autoreboot_off(self, line):
		"""DEsactive l'autoreboot quotidien"""
		mstools.disable_autoreboot()
	
	def do_update(self, line):
		"""Mise à jour de spigot"""
		
		# Build la derniere version de spigot
		mstools.build_spigot(SERVER_VERSION)
		
		# Applique la mise à jour si le serveur est eteint
		is_runing = mstools.detect_screen()
		build_location = "/tmp/buildspigot/spigot-"+SERVER_VERSION+".jar"

		if not is_runing:
			run(["cp",build_location ,SERVER_LOCATION])
			print("Serveur mis à jour")
		# Sinon si le serveur tourne demande quoi faire
		else:
			print (WARNING+"Le serveur est en route, que faire ?"+ENDC)
			print (INFO+"(1) Redémarrer le serveur et appliquer la mise à jour"+ENDC)
			print (INFO+"(2) Conserver la version mise à jour pour plus tard"+ENDC)
			nimp = input()
			if nimp == "1":
				# Redemarre et aplique la mise a jour
				mstools.stop()
				run(["cp",build_location ,SERVER_LOCATION])
				mstools.start(SERVER_LOCATION, SERVER_VERSION, MAXIMUM_RAM)
				run(["screen", "-x"])
			elif nimp == "2":
				# Stock la nouvelle version
				newer_location = SERVER_LOCATION+"/spigot-"+SERVER_VERSION+".jar.newer"
				run(["cp",build_location ,newer_location])
			else:
				print("Erreur ! 1 ou 2 abruti !")

	def do_stop (self, line) :
		"""Stop le serveur minecraft"""

		mstools.stop()

	def do_quit (self, line) :
		"""Quitte l'interface"""

		print ('See you soon !')
		exit(0)

if __name__ == '__main__' :
	cli = CLISimple()
	cli.cmdloop()
