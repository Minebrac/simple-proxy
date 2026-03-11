from io import BytesIO
import re

import config


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

def find_host(req: str):
    s = str(config.CONF["route"]["backend"])

    match = config.REG.match(req)

    if not match: return s

    for i, gr in enumerate(match.groups()):
        s = s.replace(f"${i+1}", gr)
    return s