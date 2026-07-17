import socket
import connectionHandler

import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', config.CONF["general"]["proxy-port"]))

s.listen()
logger.info("socket is listening")

while True:
    connection, _ = s.accept()

    try:
        handler = connectionHandler.ConnectionHandler(
            connection,
        )

        handler.start()
    except Exception as e:
        logger.exception("Error in ConnectionHandler !")

