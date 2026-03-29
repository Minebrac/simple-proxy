import select
import threading
import socket
import io
import utils
from config import CONF


class ConnectionHandler(threading.Thread):

    def __init__(self, sock: socket.socket):

        super().__init__(daemon=True)
        self.incoming_sock = sock

        full_buffer = b''
        state = 0

        packet_buffer = bytearray(self.incoming_sock.recv(1024))

        while True:
            packet_size, off = utils.read_varint(packet_buffer)
            while len(packet_buffer) < packet_size + off:
                packet_buffer += bytearray(self.incoming_sock.recv(1024))

            if state == 0:
                # handshaking
                handshake_packet = packet_buffer[:packet_size+off]
                next_packet = packet_buffer[packet_size+off:]

                full_buffer += handshake_packet
                # we may receive only the handshake packet
                if next_packet == b'':
                    packet_buffer = bytearray(self.incoming_sock.recv(1024))
                else:
                    packet_buffer = next_packet

                state = 1
            else:
                full_buffer += packet_buffer
                # decoding the packet
                packet = io.BytesIO(packet_buffer)
                packet_size = utils.read_varint_stream(packet)
                packet_id = utils.read_varint_stream(packet)

                player_name = packet.read(utils.read_varint_stream(packet)).decode("utf-8")

                address = utils.find_host(player_name)
                port = CONF["general"]["backend-port"]

                print(f"{self.name} : We are going to connect {player_name} to {address}:{port}, which is {socket.gethostbyname(address)}")

                self.outgoing_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.outgoing_sock.connect((
                    socket.gethostbyname(address),
                    port
                ))
                self.outgoing_sock.sendall(full_buffer)
                break



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