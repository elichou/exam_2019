Linux Embarqué : Mini Projet
=========

## Flashage de la Raspberry

On récupére le docker :

$ docker pull pblottiere/embsys-rpi3-buildroot-video

$ docker run -it pblottiere/embsys-rpi3-buildroot-video /bin/bash

$ docker# cd /root

$ docker# tar zxvf 
buildroot-precompiled-2017.
08.tar.gz

On copie l'image a flasher sur la carte sd depuis le docker. 

$ docker cp <container_id>:/root/buildroot-precompiled-2017.08/output/images/sdcard.img .
 
Puis on Flash la carte SD a l'aide de la commande _dd_

$ sudo dd if=sdcard.img of=/dev/sdX

sdX étant le port sur lequel la carte SD est branché. On peut le récuperer a l'aide de dmesg

Dans le docker commencer par faire un autogen, puis un configure et enfin cross compilé

Pour ce faire, il existe la méthode brute qui consiste a modifier les gcc par le gcc d'arm dans le Makefile.

## Servo Moteur 

On a choisit de brancher le servo moteur sur le port **GPIO4**.

Sur le servo moteur, on envoie une commande en angle entre 0 et 180 degres.

## Modification de l'adresse Ip de la Raspb pour la rendre statique

Afin de modifier l'adresse ip de la Raspberry 
il faut effectuer les commandes suivantes :

sudo nano /etc/network/interfaces

Il faut ensuite remplacer la ligne 

iface eth0 inet dhcp  

par 

iface eth0 inet static
 
 
address 172.20.21.164
 
netmask 255.255.0.0
 (Evan je suis pas sur de ouf pour cette partie la)

Adresse ip fixe de la raspberry : _172.20.21.164_

## Il faut ensuite faire correspondre 
Adresse ip fixe de l'ordinateur :

Pour l'orinateur il faut effectuer la commade 

ifconfig XXXXXXX 172.20.11.72

Pour moi XXXXXX c'est enp4s0f1, c'est le nom de l'ethernet du pc.

_172.20.11.72_

../../buildroot-precompiled-2017.08/output/host/usr/bin/arm-linux-gcc