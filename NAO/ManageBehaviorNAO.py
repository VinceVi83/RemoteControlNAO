# coding=utf-8
__author__ = 'Vincent, Aloys'


class ManageBehaviorNAO:
    """
    * Gere le lancement du comportement
    """
    def __init__(self, abm):
        self.abm = abm
        # name-id/behavior_1


    @staticmethod
    def getBehaviorName(name):
        """
        * A partir du nom, le programme recherche dans un fichier text contenant tout les chemins des comportements.
        * Si ce comportement existe, il revoit le chemin.

        :param name: nom du compotement
        :return: le chemin du comportement dans le NAO
        :rtype: str
        """
        my_file = open("ComportementUtilisateur/Noctali.txt",
                        "r")  # il faudra rendre automatique en mettant l'utilisateur de maniere automatique
        lignes = my_file.readlines()
        my_file.close()
        for ligne in lignes:
            print(ligne)
            if name in ligne:
                return ligne
        return ""

    def lauchBehavior(self, name):
        """
        * Lance un comportement donné en pararmètre s'il existe.
        * L'adresse d'un comportement est sous la forme de : comportement-identifiant/behavior_1
        * Pour connaitre l'adresse du comportement, il faut regarder sur chorégraphe.

        :param name: nom du comportement
        """
        behaviorPath = self.getBehaviorName(name)
        print(behaviorPath)
        if name in behaviorPath:
            self.abm.runBehavior(behaviorPath)
            # self.abm.runBehavior('domo-919be2/behavior_1')

        else:
            print("Le comportement n'existe pas")