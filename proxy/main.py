import socket
import connectionHandler

import config

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', config.CONF["general"]["port"]))

s.listen()
print("socket is listening")

while True:
    connection, _ = s.accept()

    handler = connectionHandler.ConnectionHandler(
        connection,
    )

    handler.start()

