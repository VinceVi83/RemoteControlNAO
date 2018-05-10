# coding=utf-8
__author__ = 'Vincent'

# !/usr/bin/env python2
#
#  raspberryLumiere.py
#
#  Copyright 2015 Vincent NGUYEN <vincent@nguyen.lt>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import socket
import select

"""
:warning: Attention se programme ne marche uniquement que sur la Rasberry Pi B. Faite attention si vous utilisé une autre Raspberry Pi
"""
try:

    import RPi.GPIO as GPIO



    class GestionGPIO:
        """
        * Gere les PINs sur la Raspberry
        """
        def __init__(self):
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(7, GPIO.OUT)

        def controlGPIO(self, value):
            """
            * Contrôle la PIN 7 physique de la raspberry
            """
            if value == True:
                GPIO.output(7, True)

            if value == False:
                GPIO.output(7, False)
except:
    print("Enlever ce try et exception c'est juste pour la génération automatique de ce script")

def interprete(cmd):
    """
    * Interprète l'information envoyé par le NAO

    :param cmd: Etat lumineux de la pièce, 1 sombre, 2 éclairé
    :return:
    """
    print(cmd)
    if cmd == '1':
        print('sombre')
        led.controlGPIO(True)

    if cmd == '0':
        print('eclaire')
        led.controlGPIO(False)


hote = ''
port = 8888

def socketServeur():
    """
    * Fonction démarrant le serveur et écoute sur son IP au port 8888
    """
    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((hote, port))
    connexion_principale.listen(5)
    print("Le serveur écoute à présent sur le port {}".format(port))

    serveur_lance = True
    clients_connectes = []
    while serveur_lance:
        # On va vérifier que de nouveaux clients ne demandent pas à se connecter
        # Pour cela, on écoute la connexion_principale en lecture
        # On attend maximum 50ms
        connexions_demandees, wlist, xlist = select.select([connexion_principale],
                                                           [], [], 0.05)

        for connexion in connexions_demandees:
            connexion_avec_client, infos_connexion = connexion.accept()
            # On ajoute le socket connecté à la liste des clients
            clients_connectes.append(connexion_avec_client)

        # Maintenant, on écoute la liste des clients connectés
        # Les clients renvoyés par select sont ceux devant être lus (recv)
        # On attend là encore 50ms maximum
        # On enferme l'appel à select.select dans un bloc try
        # En effet, si la liste de clients connectés est vide, une exception
        # Peut être levée
        clients_a_lire = []
        try:
            clients_a_lire, wlist, xlist = select.select(clients_connectes,
                                                         [], [], 0.05)
        except select.error:
            pass
        else:
            # On parcourt la liste des clients à lire
            for client in clients_a_lire:
                # Client est de type socket
                msg_recu = client.recv(1024).decode()
                if msg_recu != '':
                    # Peut planter si le message contient des caractères spéciaux
                    msg_recu = msg_recu.decode()
                    print(msg_recu)
                    interprete(msg_recu)
                if msg_recu == "fin":
                    serveur_lance = False

    print("Fermeture des connexions")
    for client in clients_connectes:
        client.close()

    connexion_principale.close()

# Point d'entré
if __name__ == "__main__":
    led = GestionGPIO()
    serveur = socketServeur()