# coding=utf-8
__author__ = 'Vincent'

from threading import Thread
import time


class DeplacementNAO(Thread):
    """
    * Gère le deplacement du NAO

    :param motion: Objet permettant d'utiliser les fonctions de déplacement du NAO
    :type motion: ALProxy()
    :param pilotage: Savoir le pilotage est actif ou non
    :type pilotage: Ctes_bool
    :var cmd: Ce tableau servira à piloter le NAO, chaque case correspond à un axe de déplacement
    """
    def __init__(self, motion, pilotage):
        Thread.__init__(self)
        self.cmd = [0, 0, 0]
        self.flag = False
        self.init = True
        self.pilotage = pilotage
        self.motion = motion


    def setX(self, value):
        """
        * Déplacement sur l'axe X

        :param value: < 0 recule, = 0 arrêt et > 0 avance
        """
        self.cmd[1] = value
        self.init = False


    def setY(self, value):
        """
        * Déplacement sur l'axe y

        :param value: < 0 marche à gauche, > 0 marche à droite et = 0 arrêt
        """
        self.cmd[0] = value
        self.init = False

    def setTheta(self, value):
        """
        * Déplacement sur l'axe Theta

        :param value: < 0 pivote à gauche, > 0 pivote à droite et 0 arrêt
        """
        self.cmd[2] = value
        self.init = False

    def run(self):
        """
        * Code exécutant le pilotage du NAO en fonction de la variable cmd

        """
        self.flag = True

        while self.flag:
            if self.init:
                time.sleep(0.5)
            else:
                if not (self.cmd == [0, 0, 0]):
                    if not (self.pilotage.get_bool()):
                        self.stop()
                        return

                    # # ****************************************************************************************
                    # self.motion.post.moveTo(self.cmd)
                    # # ****************************************************************************************
                    print(self.cmd)
                    # if (self != self.manage[0]):
                    # print(self)
                    #     print('Le thread a plante')
                    #     self.stop()

                else:
                    print('killed --> je faisais rien')
                    time.sleep(0.5)
                    self.stop()

    def stop(self):
        self.flag = False
        self.pilotage.setvalue(0)