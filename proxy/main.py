import socket
import connectionHandler

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 30625))

s.listen() # was 5
print("socket is listening")

while True:
    connection, _ = s.accept()

    handler = connectionHandler.ConnectionHandler(
        connection,
    )

    handler.start()

