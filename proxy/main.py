import socket
import connectionHandler

import config
import traceback

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', config.CONF["general"]["proxy-port"]))

s.listen()
print("socket is listening")

while True:
    connection, _ = s.accept()

    try:
        handler = connectionHandler.ConnectionHandler(
            connection,
        )

        handler.start()
    except Exception:
        traceback.print_exc()

