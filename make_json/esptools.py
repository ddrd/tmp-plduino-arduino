from utils import *
from paths import *
import re

def split_esptool_filename(file):
    m = re.compile("esptool-plduino-([0-9\\.]*)-([a-zA-z0-9]+)\\..*").match(os.path.basename(file))
    if m == None:
        raise "INVALID FILE NAME: " + file
    else:
        return file, os.path.basename(file), m.group(1), m.group(2)

def list_esptools_files():
    def arrange_esptools_list(toolfiles):
        tools = {}
        for filename in toolfiles:
            fullpath, name, version, platform = split_esptool_filename(os.path.basename(filename))
            if version not in tools:
                tools[version] = []
            tools[version].append(filename)
        return tools
    ret = []
    for entry in os.listdir(ARCPATH):
        if entry[0] != '.':
            try:
                split_esptool_filename(entry)
                ret.append(os.path.join(ARCPATH, entry))
            except Exception as e:
                pass
    return arrange_esptools_list(ret)

def make_esptool_platform_entry(filename):
    fullpath, name, version, platform = split_esptool_filename(filename)
    return ("""
                    {
                        "url": "$URL$",
                        "checksum": "$CHECKSUM$",
                        "size": "$SIZE$",
                        "host": "$HOST$",
                        "archiveFileName": "$ARCFILE$"
                    }"""
            .replace("$URL$", BASE_URL + "/" + name)
            .replace("$CHECKSUM$", calc_hash(filename))
            .replace("$SIZE$", str(filesz(filename)))
            .replace("$HOST$", get_os_by_platform(platform))
            .replace("$ARCFILE$", name))

def make_esptool_entry(files):
    fp, n, version, p = split_esptool_filename(files[0])
    tools = ""
    for f in files:
        tools += make_esptool_platform_entry(f) + ","
    tools = tools[:(len(tools)-1)]
    return (
        """{
                "version": "$VERSION$", 
                "name": "esptool-plduino", 
                "systems": ["""
            .replace("$VERSION$", version)
        + tools
        + "\n"
        + "                ]\n"
        + "            }")

def make_esptools():
    files = list_esptools_files()
    res = ""
    for file in files:
        res += make_esptool_entry(files[file]) + ","
    return res[:(len(res)-1)]
