from io import BytesIO
import redis

from config import CONF

r = redis.Redis(host=CONF["redis"]["host"], port=CONF["redis"]["port"], db=0, decode_responses=True)


def read_varint(data: bytearray):
    val = 0
    counter = 0
    position = 0

    SEGMENT_BITS = 0x7F
    CONTINUE_BIT = 0x80

    while True:
        byte = data[counter]
        counter+=1

        val |= (byte & SEGMENT_BITS) << position

        if (byte & CONTINUE_BIT) == 0: break

        position += 7

        if position >= 32:
            raise ValueError("VarInt too big")

    return val, counter


def read_varint_stream(data: BytesIO):
    val = 0
    position = 0

    SEGMENT_BITS = 0x7F
    CONTINUE_BIT = 0x80

    while True:
        d = data.read(1)

        val |= (d[0] & SEGMENT_BITS) << position

        if (d[0] & CONTINUE_BIT) == 0: break

        position += 7

        if position >= 32:
            raise ValueError("VarInt too big")

    return val

def find_host(player_name: str):
    return r.get(player_name)

if __name__ == "__main__":
    print(find_host("test"))