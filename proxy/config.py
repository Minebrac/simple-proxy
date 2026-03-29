import tomllib
import re

CONF = None

try:
    CONF = tomllib.load(
        open("config.toml", "rb")
    )
except tomllib.TOMLDecodeError as error:
    print("Failed to decode config !")
    print(error.msg)
    exit(1)
except FileNotFoundError as error:
    print("Failed to open file !")
    print(error)
    exit(1)