import os
import binascii

def file2env(file_name):
    file_full = os.environ['UBOOT_TRAVIS_BUILD_DIR'] + "/" + file_name

    if not os.path.isfile(file_full):
        return None

    return {
        "fn": file_name,
        "size": os.path.getsize(file_full),
        "crc32": hex(binascii.crc32(open(file_full, 'rb').read()) & 0xffffffff)[2:],
    }
