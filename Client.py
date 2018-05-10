# coding=utf-8

__author__ = 'Vincent'


from NAO.PositionNAO import PositionNAO
from NAO.MoveHeadNAO import MoveHeadNAO
from NAO.ManageBehaviorNAO import ManageBehaviorNAO
from NAO.DeplacementNAO import DeplacementNAO
# from NAO.ManageStreamNAO import ManageStreamNAO


value_dpl = 0.2
value_theta = 0.4
dpl = ''

class Ctes_bool():
    """
    * Permettant de créer des booléens qui seront utilisés et modifié par d'autres classes en donnant la référence du bool.
    * Les fonctions devront utliser une fonction pour modifier la valeur du booléen ou savoir sa valeur.
    * Pour une histoire de variables gloabales qui n'existe pas sur python ou l'utiliser est risqué par une méthode classique.
    """

    def __init__(self):
        self.boolean = False

    def setvalue(self, test):
        if test == 1:
            self.boolean = True
        if test == 0:
            self.boolean = False

    def get_bool(self):
        return self.boolean


class Client:
    """
    * Cette classe contient toutes les fonctions nécéssaires au client pour piloter un NAO.
    * Les parties avec des Etoiles commenté c'est pour délimiter ce qu'il faut commenter. Si on travail avec ou sans le NAO.
    * Le Constructeur

    :param ip: L'IP du NAO que le client pilotera
    :type ip: str
    :param port: L'PORT d'écoute du NAO par défaut 9559
    :type port: str
    :param communication: Permet d'avoir accès à la communication vers le client, à partir des classes et fonction de niveau inférieur
    """
    def __init__(self, ip, port, communication):

        self.pilotage = Ctes_bool()
        self.init = Ctes_bool()
        self.connected = Ctes_bool()
        self.ack = Ctes_bool()
        self.communication = communication
        # Sans NAO******************************************************************************************************
        self.tts = ""
        self.posture = ""
        self.motion = ""
        self.abm = ""
        self.dpl = ""
        # **************************************************************************************************************

        # Avec NAO******************************************************************************************************
        # self.tts = ALProxy("ALTextToSpeech", ip, port)
        # self.tts.setLanguage("French")
        # self.posture = ALProxy("ALRobotPosture", ip, port)
        # self.motion = ALProxy("ALMotion", ip, port)
        # self.abm = ALProxy("ALBehaviorManager", ip, port)
        # self.stream = ALProxy("ALVideoDevice", IP, PORT)
        # # ManageStream invoked
        # gestion_image = ManageStreamNAO(self.stream)
        # gestion_image.start()
        # **************************************************************************************************************

        self.behavior = ManageBehaviorNAO(self.abm)
        self.positionNAO = PositionNAO(self.motion, self.posture)
        self.headNAO = MoveHeadNAO(self.motion)
        self.headNAO.start()
        self.dpl = ""


    def interpret(self, commande):
        """
        * Fonction d'interpretation des commandes reçu du client.
        * Nous utilisons un code pour savoir dans quel catégorie se situe la commande et la traiter

        :param commande: commande reçu du client, l'entête du string a un code déterminant quel est le type de commande
        """

        cmd = commande[0]
        print(commande.isdigit())

        # if not (commande.isdigit()):
        #     self.positionNAO.arretUrgent()

        print("Reception d'une commande")
        print(commande)

        if cmd == '1':
            # Deplacement
            self.depl(commande)

        # if cmd == '8':
        #     # Utilisation de la fonction Vocale (tts)
        #     self.parler(commande[1:])

        # if cmd == '4':
        #     # Changer la position du NAO
        #     self.pos(commande)

        if cmd == '9':
            # Deplacement de la tête d NAO sur l'axe X
            self.teteX(commande)

        if cmd == '6':
            # Deplacement de la tête d NAO sur l'axe Y
            self.teteY(commande)

        # if cmd == '7':
        #     # Demande de lancement d'un comportement
        #     self.comp(commande)
        # if cmd == '0':
        #     self.positionNAO.arret()


    def depl(self, commande):
        """
        * Permet d'affecter le type de la commande de l'utilisateur.
        * Si l'utilisateur veut se déplacer sur l'axe X, Y ou Theta

        :param commande: l'axe demandée par l'utilisateur se trouve en 2ème position
        :type commande: str
        """

        cmd = commande[1]
        if not self.pilotage.boolean:
            # Lance la gestion du Deplacement si elle n'est pas lancé dû à un plantage de ce dernier, ou un arrêt prévu
            try:
                self.dpl.stop()
            except:
                print("No reference")

            self.dpl = DeplacementNAO(self.motion, self.pilotage)
            self.dpl.start()
            self.pilotage.setvalue(1)

        if cmd == '0':
            # Déplacement sur X
            self.deplx(commande)

        if cmd == '1':
            # Déplacement sur Y
            self.deply(commande)

        if cmd == '2':
            # Déplacement sur Theta
            self.deplo(commande)


    def deplo(self, commande):  # se diriger vers l'axe teta
        """
        * Permet de pivoter NAO sur lui-même.
        * Il y a une modification sur la valeur de la rotation. Elle varie en fonction si le NAO pivote seulement ou marche en pivotant.
        * Le NAO pivote plus quand il se déplace sur l'axe X ou Y.

        :param commande: 0 le NAO tourne à gauche et 2 à droite
        :type commande: str
        """
        cmd = commande[2]
        value = value_theta

        if self.dpl.cmd[0:2] != [0, 0]:
            # Si le NAO se déplace en tournant sur lui-même, la valeur est doublé
            value = value_theta * 2

        if cmd == '0':
            self.dpl.setTheta(value)

        if cmd == '1':
            self.dpl.setTheta(0)

        if cmd == '2':
            self.dpl.setTheta(-value)

    def deply(self, commande):
        """
        * Permet de déplacer NAO sur l'axeY

        :param commande: à 0 le NAO recule, à 2 le NAO avance
        :type commande: string
        """

        cmd = commande[2]

        if cmd == '0':
            self.dpl.setY(-value_dpl)

        if cmd == '1':
            self.dpl.setY(0)

        if cmd == '2':
            self.dpl.setY(value_dpl)


    def deplx(self, commande):  # se deplacer suivant l'axe x
        """
        * Permet de déplacer NAO sur  l'axeX

        :param commande: à 0 le NAO tourne à gauche, à 2 le NAO tourne à droite
        :type commande: str
        """

        cmd = commande[2]

        if cmd == '0':
            self.dpl.setX(-value_dpl)

        if cmd == '1':
            self.dpl.setX(0)

        if cmd == '2':
            self.dpl.setX(value_dpl)


    def parler(self, commande):
        """
        * Utilise la fonction TTS du NAO

        :param commande: Message que le NAO devra dire
        """
        print(commande)
        self.tts.say(commande)


    def pos(self, commande):
        """
        * Change la position du NAO

        :param commande: la position demandée par l'utilisateur se trouve en 2ème position
        """
        cmd = commande[1]
        if cmd == '0':
            self.positionNAO.coucher()

        if cmd == '9':
            self.positionNAO.assis()

        if cmd == '1':
            self.positionNAO.accroupi()

        if cmd == '2':
            self.positionNAO.debout()


    def teteX(self, commande):
        """
        * Permet de piloter la tête du NAO sur l'axe X

        :param commande: l'axe demandée par l'utilisateur se trouve en 2ème position
        """
        cmd = commande[1]
        if cmd == '0':
            self.headNAO.setY(0)

        if cmd == '1':
            self.headNAO.setY(1)


    def teteY(self, commande):
        """
        * Permet de piloter la tête du NAO sur l'axe Y

        :param commande: l'axe demandée par l'utilisateur se trouve en 2ème position
        """

        cmd = commande[1]

        if cmd == '0':
            print("Tourne la tete à droite")
            self.headNAO.setX(cmd)
        if cmd == '1':
            print("Fin pilotage tête")
            self.headNAO.setX(cmd)
        if cmd == '2':
            print("Tourne la tete à gauche")
            self.headNAO.setX(cmd)


    def comp(self, commande):
        """
        * Fait appel au lanceur de comportement

        :param commande: l'axe demandée par l'utilisateur se trouve en 2ème position
        """

        self.behavior.lauchBehavior(commande[1:])


    def dead(self):
        """
        * Lorsque le client est déconnecté d'une façon d'un autre on détruit les processus qui lui appartient
        """
        try:
            self.headNAO.stop()
        except:
            print("No reference")

        try :
            self.dpl.stop()
        except:
            print("No reference")