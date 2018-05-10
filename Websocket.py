# coding=utf-8
__author__ = 'Vincent, others'

import base64
import struct
import socket
import hashlib
from select import select
import logging


"""
Code récupére sur internet permettant de faire tourner un serveur Websocket en Python
J'ai laissé les liens originaux. J'ai légèrement modifié des parties.
"""
# Constants
MAGICGUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
TEXT = 0x01
BINARY = 0x02

# Simple WebSocket server implementation. Handshakes with the client then echos back everything
# that is received. Has no dependencies (doesn't require Twisted etc) and works with the RFC6455
# version of WebSockets. Tested with FireFox 16, though should work with the latest versions of
# IE, Chrome etc.
#
# rich20b@gmail.com
# Adapted from https://gist.github.com/512987 with various functions stolen from other sites, see
# below for full details.


class WebSocket(object):
    """
    * Used for the communication between client and server
    """
    handshake = (
        "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
        "Upgrade: WebSocket\r\n"
        "Connection: Upgrade\r\n"
        "Sec-WebSocket-Accept: %(acceptstring)s\r\n"
        "Server: TestTest\r\n"
        "Access-Control-Allow-Origin: http://192.168.1.147\r\n"
        "Access-Control-Allow-Credentials: true\r\n"
        "\r\n"
    )

    # Constructor
    def __init__(self, client, server):
        self.client = client
        self.server = server
        self.handshaken = False
        self.header = ""
        self.data = ""

    # Serve this client
    def feed(self, data):

        # If we haven't handshaken yet
        if not self.handshaken:
            logging.debug("No handshake yet")
            self.header += data
            if self.header.find('\r\n\r\n') != -1:
                parts = self.header.split('\r\n\r\n', 1)
                self.header = parts[0]
                if self.dohandshake(self.header, parts[1]):
                    logging.info("Handshake successful")
                    self.handshaken = True

        # We have handshaken
        else:
            logging.debug("Handshake is complete")

            # Decode the data that we received according to section 5 of RFC6455
            recv = decodeCharArray(data)

            # Send our reply
            self.sendMessage(''.join(recv).strip())

    # Stolen from http://www.cs.rpi.edu/~goldsd/docs/spring2012-csci4220/websocket-py.txt
    def sendMessage(self, s):
        """
        * Encode and send a WebSocket message
        """
        # Empty message to start with
        message = ""
        # always send an entire message as one frame (fin)
        b1 = 0x80
        # in Python 2, strs are bytes and unicodes are strings
        if type(s) == unicode:
            b1 |= TEXT
            payload = s.encode("UTF8")
        elif type(s) == str:
            b1 |= TEXT
            payload = s

        # Append 'FIN' flag to the message
        message += chr(b1)
        # never mask frames from the server to the client
        b2 = 0
        # How long is our payload?
        length = len(payload)
        if length < 126:
            b2 |= length
            message += chr(b2)

        elif length < (2 ** 16) - 1:
            b2 |= 126
            message += chr(b2)
            l = struct.pack(">H", length)
            message += l

        else:
            l = struct.pack(">Q", length)
            b2 |= 127
            message += chr(b2)
            message += l

        # Append payload to message
        message += payload

        # Send to the client
        self.client.send(str(message))

    # Handshake with this client
    def dohandshake(self, header, key=None):
        logging.debug("Begin handshake: %s" % header)
        # Get the handshake template
        handshake = self.handshake
        # Step through each header
        for line in header.split('\r\n')[1:]:
            name, value = line.split(': ', 1)
            # If this is the key
            if name.lower() == "sec-websocket-key":
                # Append the standard GUID and get digest
                combined = value + MAGICGUID
                response = base64.b64encode(hashlib.sha1(combined).digest())

                # Replace the placeholder in the handshake response
                handshake = handshake % {'acceptstring': response}

        logging.debug("Sending handshake %s" % handshake)
        self.client.send(handshake)
        return True

    def onmessage(self, data):
        # logging.info("Got message: %s" % data)
        self.send(data)

    def send(self, data):
        logging.info("Sent message: %s" % data)
        self.client.send("\x00%s\xff" % data)

    def close(self):
        self.client.close()


# WebSocket server implementation
class WebSocketServer(object):
    """
    * Server Websocket
    :param manageCli: Pour gérer les clients pour le pilotage et autres
    :param cls: Permettra de pouvoir communiquer avec les clients
    """
    def __init__(self, bind, port, cls, manageCli):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((bind, port))
        self.bind = bind
        self.port = port
        self.cls = cls
        self.connections = {}
        self.listeners = [self.socket]
        self.manageCli = manageCli


    def listen(self, backlog=5):
        """
        * Manage the entries of clients and the reception of requests
        """

        self.socket.listen(backlog)
        logging.info("Listening on %s" % self.port)

        # Keep serving requests
        self.running = True
        while self.running:

            # Find clients that need servicing
            rList, wList, xList = select(self.listeners, [], self.listeners, 1)
            for ready in rList:
                if ready == self.socket:
                    logging.debug("New client connection")
                    client, address = self.socket.accept()
                    fileno = client.fileno()
                    self.listeners.append(fileno)
                    self.connections[fileno] = self.cls(client, self)
                    self.manageCli.addClient("user", self.connections[fileno])

                else:
                    logging.debug("Client ready for reading %s" % ready)
                    client = self.connections[ready].client
                    data = client.recv(4096)
                    fileno = client.fileno()
                    if data:
                        self.connections[fileno].feed(data)
                        print('data incomming')
                        cmd = decodeCharArray(data)
                        print(cmd)

                        # Interprete les commandes de l'utilisateur1
                        self.manageCli.useFunctionCli("user").interpret(cmd)

                    else:
                        logging.debug("Closing client %s" % ready)
                        self.connections[fileno].close()
                        del self.connections[fileno]
                        self.listeners.remove(ready)

            # Step though and delete broken connections
            for failed in xList:
                if failed == self.socket:
                    logging.error("Socket broke")
                    for fileno, conn in self.connections:
                        conn.close()
                    self.running = False


# Stolen from http://stackoverflow.com/questions/8125507/how-can-i-send-and-receive-websocket-messages-on-the-server-side
def decodeCharArray(stringStreamIn):
    """
    * Fonction pour décoder un message car la communication du client vers le serveur en chiffrer
    :param stringStreamIn: data à décoder
    :return: data décodé
    """
    # Turn string values into opererable numeric byte values
    byteArray = [ord(character) for character in stringStreamIn]
    datalength = byteArray[1] & 127
    indexFirstMask = 2
    msg = ''

    if datalength == 126:
        indexFirstMask = 4
    elif datalength == 127:
        indexFirstMask = 10

    # Extract masks
    masks = [m for m in byteArray[indexFirstMask: indexFirstMask + 4]]
    indexFirstDataByte = indexFirstMask + 4

    # List of decoded characters
    decodedChars = []
    i = indexFirstDataByte
    j = 0

    # Loop through each byte that was received
    while i < len(byteArray):
        # Unmask this byte and add to string decoded
        # ~ decodedChars.append( chr(byteArray[i] ^ masks[j % 4]) )
        msg += chr(byteArray[i] ^ masks[j % 4])
        i += 1
        j += 1
    # ~ print msg
    # Return the decoded string
    return msg
