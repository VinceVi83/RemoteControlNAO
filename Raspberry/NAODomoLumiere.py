# coding=utf-8
__author__ = 'Vincent'

import socket
import time
import sys

"""
:warning: Attention se programme ne marche uniquement sur le NAO V1 et V2
"""
class GeneratedClass(object):

    # Classe a virer c'est pour la génération de documentation

    pass


class MyClass(GeneratedClass):
    """
    * Code dans la box PythonScript sur Chorégraphe
    """
    def __init__(self):
        GeneratedClass.__init__(self)
        self.ip = "192.168.1.153"
        self.port = 8888
        self.connexion_RPI = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion_RPI.connect((self.ip, self.port))
        print("Connexion établie avec le serveur")


    def onInput_obcurite(self):
        """
        * Envoie un message à la Raspberry que ce n'est éclairé et envoie un message à la boite suivante
        """
        #self.fin(p) #activate the output of the box
        msg = "Il fait sombre ici, je vais allumer la lumiere"
        print(msg)
        token = "1"
        self.connexion_RPI.send(token.encode())
        self.connexion_RPI.close()
        self.fin(msg)
        pass

    def onInput_eclaire(self):
        """
        * Envoie un message à la Raspberry que c'est éclairé et envoie un message à la boite suivante
        """
        msg = "La piece est bien eclairee ici, inutile d'allumer la lumiere"
        print(msg)
        token = "0"
        self.connexion_RPI.send(token.encode())
        self.connexion_RPI.close()
        self.fin(msg)
        pass