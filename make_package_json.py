import json
import re
import os
import hashlib

ARCPATH = "./dist"
BASE_URL = "https://raw.githubusercontent.com/ddrd/tmp-plduino-arduino/master/dist"
OUT_JSON = os.path.join(ARCPATH, "package_PLDuino_index.json")


def calc_hash(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return "MD5:" + hash_md5.hexdigest()
def filesz(filepath):
    return os.stat(filepath).st_size


def make_boards():
    def split_board_filename(filename):
        name = os.path.basename(filename)
        m = re.compile("PLDuino([a-zA-z0-9_]+)-([0-9\\.]*)\\.[a-zA-Z]+.*").match(name)
        if m == None:
            raise RuntimeError("INVALID FILE NAME: " + filename)
        else:
            return (
                m.group(1),
                name,
                filename,
                m.group(2)
            )
    def list_board_files():
        ret = []
        for entry in os.listdir(ARCPATH):
            if entry[0] != '.':
                try:
                    split_board_filename(entry)
                    ret.append(os.path.join(ARCPATH, entry))
                except RuntimeError as e:
                    pass
        return ret
    def make_board_entry(filename):
        def get_tools_deps(board_type):
            if board_type == "AVR":
                return """
                    { "packager": "arduino", "name": "avr-gcc", "version": "4.9.2-atmel3.5.3-arduino2" },
                    { "packager": "arduino", "name": "avrdude", "version": "6.3.0-arduino8" }
                """
            else:
                return """
                    { "packager": "PLDuino", "version": "0.4.6", "name": "esptool-plduino" },
                    { "packager": "esp8266", "version": "1.20.0-26-gb404fb9-2", "name": "xtensa-lx106-elf-gcc" },
                    { "packager": "arduino", "name": "avrdude", "version": "6.3.0-arduino8" }
                """
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
                        "toolsDependencies": [
                            $TOOLSDEP$
                        ]
                    }
                """
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
                        "toolsDependencies": [
                            $TOOLSDEP$
                        ]
                    }
                """
        board_type, name, fullpath, version = split_board_filename(filename)
        return (
            template(board_type)
                .replace("$URL$", BASE_URL + "/" + name)
                .replace("$CHECKSUM$", calc_hash(fullpath))
                .replace("$VERSION$", version)
                .replace("$ARCFILE$", name)
                .replace("$SIZE$", str(filesz(fullpath)))
                .replace("$TOOLSDEP$", get_tools_deps(board_type))
        )
    files = list_board_files()
    res = ""
    for file in files:
        res += make_board_entry(file) + ","
    res = res[:(len(res)-1)] # removing last comma
    return res


def make_esptools():
    def get_os_by_platform(platform):
        return {
            "win32": "i686-mingw32",
            "osx": "x86_64-apple-darwin",
            "linux64": "x86_64-pc-linux-gnu",
            "linux32": "i686-pc-linux-gnu",
        }[platform]
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
    def make_esptool_entry(files):
        def make_esptool_platform_entry(filename):
            fullpath, name, version, platform = split_esptool_filename(filename)
            return ("""
                {
                    "url": "$URL$",
                    "checksum": "$CHECKSUM$",
                    "size": "$SIZE$",
                    "host": "$HOST$",
                    "archiveFileName": "$ARCFILE$"
                }
                """.replace("$URL$", BASE_URL + "/" + name)
                   .replace("$CHECKSUM$", calc_hash(filename))
                   .replace("$SIZE$", str(filesz(filename)))
                   .replace("$HOST$", get_os_by_platform(platform))
                   .replace("$ARCFILE$", name)
            )
        fp, n, version, p = split_esptool_filename(files[0])
        tool_files = ""
        for f in files:
            tool_files += make_esptool_platform_entry(f) + ","
        tool_files = tool_files[:(len(tool_files)-1)]
        return ("""
            {
                "version": "$VERSION$", 
                "name": "esptool-plduino", 
                "systems": [
                    $TOOLFILES$
                ]
            }
            """.replace("$VERSION$", version)
               .replace("$TOOLFILES$", tool_files)
        )
    files = list_esptools_files()
    res = ""
    for file in files:
        res += make_esptool_entry(files[file]) + ","
    return res[:(len(res)-1)]


def make_json():
    return ("""
        {
            "packages": [{
                "maintainer": "Digital Loggers Inc", 
                "websiteURL": "https://github.com/digitalloggers/", 
                "name": "PLDuino",
                "platforms": [
                    $PLATFORMS$
                ],
                "tools": [
                    $TOOLS$
                ]
            }]
        }
        """.replace("$PLATFORMS$", make_boards())
           .replace("$TOOLS$", make_esptools()))

open(OUT_JSON, "w").write(json.dumps(json.loads(make_json()), indent=2, sort_keys=True))
print "done"
