__author__ = 'vincent'

# -*- coding: utf-8 -*-


import sys
import time
import logging
from threading import Thread
import signal

from Websocket import WebSocket, WebSocketServer
from ManageClient import ManageCLient

IP_Serveur = "192.168.1.92"

# Entry point
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    # Launch the client manager to pilot NAO
    manageCli = ManageCLient()
    # Start the serveroc
    server = WebSocketServer(IP_Serveur, 8080, WebSocket, manageCli)
    # server = WebSocketServer(IP_Local, 8080, WebSocket)
    server_thread = Thread(target=server.listen, args=[5])
    server_thread.start()



# Add SIGINT handler for killing the threads
def signal_handler(signal, frame):
    logging.info("Caught Ctrl+C, shutting down...")
    server.running = False
    sys.exit()


signal.signal(signal.SIGINT, signal_handler)

while True:
    time.sleep(10)
    print("hello")
