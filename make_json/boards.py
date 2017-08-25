import re
import os
from utils import *
from paths import *

def list_board_files():
    ret = []
    for entry in os.listdir(ARCPATH):
        if entry[0] != '.':
            try:
                split_board_filename(entry)
                ret.append(os.path.join(ARCPATH, entry))
            except:
                pass
    return ret

def get_tools_deps(board_type):
    if board_type == "AVR":
        return """
                    { "packager": "arduino", "name": "avr-gcc", "version": "4.9.2-atmel3.5.3-arduino2" },
                    { "packager": "arduino", "name": "avrdude", "version": "6.3.0-arduino8" }"""
    else:
        return """
                    { "packager": "PLDuino", "version": "0.4.6", "name": "esptool-plduino" },
                    { "packager": "esp8266", "version": "1.20.0-26-gb404fb9-2", "name": "xtensa-lx106-elf-gcc" },
                    { "packager": "arduino", "name": "avrdude", "version": "6.3.0-arduino8" }"""

def split_board_filename(filename):
    name = os.path.basename(filename)
    m = re.compile("PLDuino([a-zA-z0-9_]+)-([0-9\\.]*)\\.[a-zA-Z]+.*").match(name)
    if m == None:
        raise "INVALID FILE NAME: " + filename
    else:
        return (
            m.group(1),
            name,
            filename,
            m.group(2),
            get_tools_deps(m.group(1))
        )

def make_board_entry(filename):#board_type, filename, version, toolsdep):
    board_type, name, fullpath, version, toolsdep = split_board_filename(filename)
    def template(board_type):
        if board_type == "AVR":
            return """
            {
                "name": "PLDuino/Mega2560",
                "category": "Contributed",
                "url": "$URL$",
                "archiveFileName": "$ARCFILE$",
                "checksum": "$CHECKSUM$",
                "size": "$SIZE$",
                "version": "$VERSION$",
                "architecture": "avr",
                "boards": [{ "name": "PLDuino/Mega2560" }],
                "toolsDependencies": [$TOOLSDEP$
                ]
            }"""
        elif board_type == "ESP":
            return """
            {
                "name": "PLDuino/ESP-02",
                "category": "Contributed",
                "url": "$URL$",
                "archiveFileName": "$ARCFILE$",
                "checksum": "$CHECKSUM$",
                "size": "$SIZE$",
                "version": "$VERSION$",
                "architecture": "esp8266",
                "boards": [{ "name": "PLDuino/ESP-02" }],
                "toolsDependencies": [$TOOLSDEP$
                ]
            }"""
    return (
        template(board_type)
            .replace("$URL$", BASE_URL + "/" + name)
            .replace("$CHECKSUM$", calc_hash(fullpath))
            .replace("$VERSION$", version)
            .replace("$ARCFILE$", name)
            .replace("$SIZE$", str(filesz(fullpath)))
            .replace("$TOOLSDEP$", toolsdep)
    )

def make_boards():
    files = list_board_files()
    res = ""
    for file in files:
        res += make_board_entry(file) + ","
    res = res[:(len(res)-1)] # removing last comma
    return res
