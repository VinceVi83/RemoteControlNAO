# coding=utf-8
__author__ = 'Vincent'


from Client import Client

IP_Local = "192.168.1.137"
robotIP = IP_Local
PORT = 9559


class ManageCLient:
    """
    * Gere l'ajout et la suppression des clients
    """

    def __init__(self):
        self.liste = {}

    def addClient(self, name, communication):
        """
        * Ajoute un client à gérer

        :param name: nom ou identifiant du client, ce n'est pas encore utilisé. C'est dans le cadre du multi-client
        :param communication: Permet d'avoir accès à la communication vers le client, à partir des classes et fonction de niveau inférieur
        """
        if name not in self.liste.keys():
            # Pour éviter qu'il y a deux fois le même client
            self.liste[name] = Client(robotIP, PORT, communication)

    def popClient(self, name):
        """
        * Supprime un client
        :param name:
        :return:
        """
        self.liste[name].dead()
        self.liste.pop(name)

    def useFunctionCli(self, name):
        """
        * Permet d'utiliser les fonctions du client
        """
        return self.liste[name]