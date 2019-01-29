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




On branche le servo moteur sur le port **GPIO4**.

Sur le servo moteur, on envoie une commande en angle entre 0 et 180 degres.

Adresse ip fixe de la raspberry : _172.20.21.164_

Adresse ip fixe de l'ordinateur :
_172.20.11.72_