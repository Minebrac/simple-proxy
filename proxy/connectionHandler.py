import select
import threading
import socket
import io
import utils
from config import CONF

class ConnectionHandler(threading.Thread):

    def __init__(self, sock):

        super().__init__(daemon=True)
        self.incoming_sock = sock

        data = bytearray(sock.recv(20480))
        packet_size, off = utils.read_varint(data)

        packet = io.BytesIO(data[off:packet_size + 1])
        packet_id = utils.read_varint_stream(packet)
        if packet_id != 0:
            raise RuntimeError("unable to decode")

        proto = utils.read_varint_stream(packet)
        address = utils.find_host(
            packet.read(utils.read_varint_stream(packet)).decode('utf-8')
        )
        port = CONF["route"]["backend-port"]

        print(f"{self.name} : connecting {address}:{port}")

        self.outgoing_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.outgoing_sock.connect((
            socket.gethostbyname(address),
            port
        ))
        self.outgoing_sock.sendall(data)


    def run(self):
        # this code is a part of PyProxy by rsc-dev
        # https://github.com/rsc-dev/pyproxy

        try:
            print(f"{self.name} : Running")

            sockets = [self.incoming_sock, self.outgoing_sock]
            while True:
                s_read, _, _ = select.select(sockets, [], [])

                for s in s_read:
                    data = s.recv(10240)

                    if s == self.incoming_sock:
                        self.outgoing_sock.sendall(data)
                    elif s == self.outgoing_sock:
                        self.incoming_sock.sendall(data)

        except BrokenPipeError:
            self.incoming_sock.close()
            self.outgoing_sock.close()
            print(f"{self.name} : End of connection")