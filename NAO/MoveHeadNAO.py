# coding=utf-8
__author__ = 'Vincent'

from threading import Thread
import time


class MoveHeadNAO(Thread):
    """
    * Gere le pilotage de la tête du NAO

    :param motion: Objet permettant de contrôler la tête du NAO
    :type motion: ALMotion
    """
    def __init__(self, motion):
        Thread.__init__(self)
        # Initialisation
        self.cmd = 1
        self.flag = False
        self.init = True
        self.angleHead = 0
        self.angleHeady = 0
        self.sleep = 0.2
        self.lasty = 0

        # Valeur Max et Min de HeadPitch et de HeadYaw en radian
        self.XMAX = 117 / 360.0 * 3 * 3.44
        self.XMIN = (( - 117) / 360.0) * 3.0 * 3.44
        self.YMAX = 18 / 360.0 * 2 * 3.44
        self.YMIN = -25 / 360.0 * 2 * 3.44

        # Determination des pas a chaque incrementation
        self.mvx = (self.XMAX - self.YMIN) / 20.0
        self.mvy = (self.YMAX - self.YMIN) / 5.0
        self.names = "Head"
        self.initial = True
        self.targetAngles = 1.0
        self.maxSpeedFraction = 0.2  # Using 20% of maximum joint speed
        self.motion = motion

    def setX(self, value):
        """
        * A method who add or reduce the coordinate of the NAO at HeadYaw depend of the value.
        """
        print(value)
        self.cmd = int(value)
        if value == '0' or value == '2':
            self.x = True
            self.initial = False
            print('Je control la tete')
        else:
            self.x = False


    def setY(self, value):
        """
        * A method who add or reduce the coordinate of the NAO at HeadPitch depend of the value.
        """

        if value == 1 and ((self.angleHeady + self.mvy) < self.YMAX):
            self.angleHeady += self.mvy
            print("bas")

        if value == 0 and ((self.angleHeady + self.mvy) > self.YMIN):
            self.angleHeady -= self.mvy
            print("haut")


    def manageX(self):
        """
        * A method who manage the coordinate of the movement of the NAO at HeadYaw.
        * At first control increment the coordinate of head when it is controlled.
        * When the head is not controlled, the head return to initial position.
        """
        if self.x:
            # Le client controle la tête

            # Tourne la tête à gauche
            if self.cmd == 0 and ((self.angleHead + self.mvx * 1.0 ) < self.XMAX):
                self.angleHead += self.mvx * 1.0

            # Tourne la tête à droite
            if self.cmd == 2 and ((self.angleHead + self.mvx * -1.0 ) > self.XMIN):
                self.angleHead += self.mvx * -1.0

            self.initial = False
            print("down")
            return

        # La tête du NAO est dans sa position initiale
        if 0.5 > self.angleHead > -0.5:
            # self.motion.setAngles("HeadYaw", 0, 0.8)
            self.initial = True
            return

        # La ẗête retourne à sa position initiale
        if self.angleHead > 0:
            toto = self.angleHead + self.mvx * -1.0
            self.angleHead = toto
            return

        # La ẗête retourne à sa position initiale
        if self.angleHead < 0:
            toto = self.angleHead + self.mvx * 1.0
            self.angleHead = toto
            return

    def run(self):
        """
        * Run the thread to control the head depending of self.angleHeady
        """
        self.flag = True

        while self.flag:

            if self.initial:
                # Tete non contrôlé sur l'axe X
                if self.lasty != self.angleHeady:
                    # self.motion.setAngles("HeadPitch", self.angleHeady, 0.2)
                    print("vertical")
                    time.sleep(self.sleep)

                else:
                    # print('sleep')
                    time.sleep(self.sleep)
            else:
                # Tete contrôlé sur les axes X et Y
                self.manageX()
                print(self.angleHead)
                # motion.setAngles("Head",[self.angleHead, self.angleHeady], 0.2)
                time.sleep(self.sleep)
                print(self.cmd)

    def stop(self):
        self.flag = False
