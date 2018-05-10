# coding=utf-8
__author__ = 'Vincent'

from threading import Thread
import time

class RecuperationInfoNAO(Thread):
    '''
    * This class is a template, the objectif of this Class is to use a thread to get information from NAO with a regular interval. The interpreration and action will be defined here as method.
    '''
    def __init__(self , ALMemory):
        '''
        :param ALMemory: Objet permettant d'avoir accès aux informations contenues dans le NAO.
        :type ALMemory: ALMemory
        :var listKeys: Une liste de clé afin de récupérer les informations du NAO. Ces clés sont données dans la documentation du NAOqi.
        :type listKeys: list
        :var data: Un dictionnaire enregistrant les informations du NAO, on accèdes aux informations à partir de la Clé.
        :type data: dict
        :var sleep: Intervalle de temps entre la récupération des informations.
        :type sleep: int
        '''

        Thread.__init__(self)
        self.listKeys = []
        self.flag = False
        self.data = {}
        self.acces = ALMemory
        self.sleep = 1


    def getData(self, key):
        """
        * Récupére une donnée en fonction de la clé

        :param key: Information à récupérer
        :return:
        """
        data = self.acces.get(key)
        return data


    def addKey(self, key):
        """
        * Ajoute une clé dans la liste d'information à récupérer et dans le dictionnaire
        :param key: Information à surveiller
        :return:
        """
        self.listKeys.append(key)
        self.data[key] = []


    def run(self):
        """
        * Récupère les informations du NAO en continu
        """
        self.flag = True

        while self.flag:
            for key in self.listKeys:
                # Itération des cles pour récupérer les informations
                data = self.getData(key)
                self.data[key].append(data)

            # Pause de self.sleep secpndes
            time.sleep(self.sleep)


    def stop(self):
        self.flag = False