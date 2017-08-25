import hashlib
import os

def calc_hash(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return "MD5:" + hash_md5.hexdigest()

def filesz(filepath):
    return os.stat(filepath).st_size

def get_os_by_platform(platform):
    return {
        "win32": "i686-mingw32",
        "osx": "x86_64-apple-darwin",
        "linux64": "x86_64-pc-linux-gnu",
        "linux32": "i686-pc-linux-gnu",
    }[platform]

