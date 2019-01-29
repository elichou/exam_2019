# coding: utf-8

import socket
import signal
import sys
import os
import numpy as np
import pygame
from pygame.locals import *
import time
import PIL.Image as Image

def close_all(signal, frame):
	socket_servo.close()
	socket_camera.close()
	socket_image.close()
	print("\nSIG : {} : Interruption programme...".format(signal))
	sys.exit(0)

def check_adresse_ip(adresse):
	tab = adresse.split('.')
	for el in tab:
		if not (0 <= int(el) <= 255):
			return False
	return True


if len(sys.argv) < 2:
	print("Merci de rentrer l'adresse IP de la raspberry en argument")
	sys.exit()

if sys.argv[1]:
	adresse = sys.argv[1]
	if not check_adresse_ip(adresse):
		print("Adresse IP non valide")
		sys.exit()
	
try:
	socket_image.close()
	socket_servo.close()
	socket_camera.close()
except:
	pass	

#Paramètre IP et port	
hote = sys.argv[1]
port_servo  = 15554
port_camera = 15555
port_image  = 15556


#Gestion des signaux
signal.signal(signal.SIGINT, close_all)  #Ctrl + C
signal.signal(signal.SIGTSTP, close_all) #Ctrl + Z
signal.signal(signal.SIGTERM, close_all) #kill python


if __name__=='__main__':

	#Initialisation pygame window
	pygame.init()
	pygame.font.init()
	font = pygame.font.Font(None, 20)

	clock  = pygame.time.Clock()
	screen = pygame.display.set_mode((640,480))

	cmd_servo = 90 #init au milieu (de 0 à 180)
	isEnabled = 0

   	#Creation du socket et connection au port 
	socket_servo  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_camera = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket_image  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	#Connection aux différents sockets 
	socket_servo.connect((hote, port_servo))
	socket_camera.connect((hote, port_camera))
	socket_image.connect((hote, port_image))

	while True:
		time.sleep(1)
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				print("Fermeture des sockets")
				socket_image.close()
				socket_servo.close()
				socket_camera.close()
				sys.exit(0)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					cmd_servo += 5
					cmd_servo = min(180,cmd_servo)
				if event.key == pygame.K_LEFT:
					cmd_servo -= 5
					cmd_servo = max(0,cmd_servo)
				if event.key == pygame.K_s:
					isEnabled = 1

		#creation de l'information sous la forme d'un dictionnaire
		str_cmd_servo = str(cmd_servo)  #commande angle entre 0 et 180
		str_isEnabled = str(isEnabled)  #permet de demander une image ou non

		#print(cmd_servo)
		#print(str_cmd_servo)

		socket_servo.send(  (str_cmd_servo).encode() )
		socket_camera.send( (str_isEnabled).encode() )

		#Reception Image
		if isEnabled:
			time.sleep(1)
			isEnabled = 0
			data = socket_image.recv(921600)
					
			image = Image.frombytes("RGB", (640, 480), data)
			image.save('out.jpg')

			img_jpg = pygame.image.load("out.jpg")

			screen.blit(img_jpg, (0,0))
			screen.blit(font.render("Angle = {:d}".format(cmd_servo),-1, (255,255,255)), (70,200))
			pygame.display.update()
			
		
