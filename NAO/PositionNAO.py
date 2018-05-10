# coding=utf-8
__author__ = 'Vincent, Aloys'

class PositionNAO:
    """
    * Permet de mettre NAO dans une position existante dans le NAOqi

    :param motion: Objet permettant de controler l'asservissement des moteurs ici
    :type motion: ALMotion
    :param posture: Objet permettant de piloter le NAO pour qu'il se mettent dans une posture
    :type posture: ALPosture
    """
    def __init__(self, motion, posture):
        """"""
        self.posture = posture
        self.motion = motion


    def debout(self):
        """ """
        self.motion.wakeUp()
        self.posture.goToPosture("StandInit", 0.8)
        print("Debout")


    def arretUrgent(self):
        """ """
        self.posture.goToPosture("Crouch", 0.8)
        # try:
        #     dpl.stop()
        # except:
        #     print('dpl ne tourne pas')
        self.motion.rest()
        print("arret d'urgence")


    def arret(self):
        """ """
        print("arret du nao")
        self.arretUrgent()


    def accroupi(self):
        """ """
        self.motion.wakeUp()
        self.posture.goToPosture("Crouch", 0.8)
        self.motion.rest()


    def assis(self):
        """ """
        self.motion.wakeUp()
        self.posture.goToPosture("Sit", 0.8)
        self.motion.rest()


    def coucher(self):
        """ """
        self.motion.wakeUp()
        self.posture.goToPosture("LyingBelly", 0.8)
        self.motion.rest()
