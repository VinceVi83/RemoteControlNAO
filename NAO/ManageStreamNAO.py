# coding=utf-8
__author__ = 'Vincent, Aloys'


# Python Image Library
from PIL import Image
import vision_definitions
import pickle

from threading import Thread
import os
import time

# os.chdir("/opt/lampp/htdocs/naoprt/")
data_image = []
def add_dataImage(image):
    data_image.append(image)


def memorise():
    """
    * Permet d'enregistrer un jeu de donnée, des images binaires dans un objet utilisable. Pour travailler sans NAO.

    :param camproxy: Objet permettant d'utiliser les fonctions du NAOqi sur la vidéo
    :type camproxy: ALVideoDevice
    """
    with open('/home/vinsento/Desktop/naoPRT/image_prt', 'wb') as fichier:
        mon_pickler = pickle.Pickler(fichier)
        mon_pickler.dump(data_image)
    print("Enregistrer")
    print()
    memory_last()
    return 0


def memory_last():
    """
    * Récupère un jeu de donnée.L'intention était de l'utiliser afin de travailler sur le stream video en hors ligne.
    * Pour faire des tests pour réaliser le stream en utilisant des données déja générer.
    """
    with open('/home/vinsento/Desktop/naoPRT/image_prt', 'rb') as fichier:
        mon_depickler = pickle.Unpickler(fichier)
        data = mon_depickler.load()
    cpt = 0
    for t in data:
        imageWidth = t[0]
        imageHeight = t[1]
        array = t[6]
        # Create a PIL Image from our pixel array.
        im = Image.fromstring("RGB", (imageWidth, imageHeight), array)
        im.save("test" + str(cpt) + ".png", "PNG")
        cpt += 1
    print("Loaded")


class GetImage():
    """
    * Recupère une image du NAO à l'aide de la fonction "getImageRemote" disponible dans le NAOqi
    """
    def __init__(self, camProxy):
        self.camProxy = camProxy
        self.resolution = vision_definitions.kQVGA
        self.colorSpace = 11  # RGB
        self.alterne = True
        self.numero = "0"

    def getImage(self):
        videoClient = self.camProxy.subscribe("python_client", self.resolution, self.colorSpace, 5)
        t0 = time.time()
        # Get a camera image.
        # image[6] contains the image data passed as an array of ASCII chars.
        naoImage = self.camProxy.getImageRemote(videoClient)
        t1 = time.time()
        print("acquisition delay " + str(t1 - t0))
        self.camProxy.unsubscribe(videoClient)
        # Now we work with the image returned and save it as a PNG  using ImageDraw
        # package.

        # Get the image size and pixel array.
        imageWidth = naoImage[0]
        imageHeight = naoImage[1]
        array = naoImage[6]

        # Create a PIL Image from our pixel array.
        im = Image.fromstring("RGB", (imageWidth, imageHeight), array)

        im.save("image" + str(len(data_image)) + ".png", "PNG")
        #save data
        # add_dataImage(naoImage)
        time.sleep(0.5)


        # try:
        #     if (connected.get_bool()):
        #         print(type(naoImage[6]))
        #         listclient[0].sendMessage(array)
        #         time.sleep(10)
        # except:
        #     connected.setvalue(0)

class ManageStreamNAO(Thread):
    """
    * Gere la diffusion video du NAO

    :param camproxy: Objet permettant d'utiliser les fonctions du NAOqi sur la vidéo
    :type camproxy: ALVideoDevice
    """

    def __init__(self, camproxy):
        Thread.__init__(self)
        self.flag = False
        self.init = True
        self.image = GetImage(camproxy)

    def run(self):
        """
        * Recupère une image une par une et
        :return:
        """
        print("start thread image    zz")
        self.flag = True

        while self.flag:
            self.image.getImage()
             # envoyer l'image au client

            # Enregistre un jeu de donnée
            # if len(data_image) == 100:
            #     memorise()
            # else:
            #     time.sleep(0.1)
            #     print("attend ack")



    def stop(self):
        self.flag = False
