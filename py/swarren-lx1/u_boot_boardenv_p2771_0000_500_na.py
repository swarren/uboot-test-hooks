# Copyright (c) 2015-2018, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

env__net_uses_pci = False

env__net_dhcp_server = True

env__net_tftp_readable_file = {
    "fn": "ubtest-readable.bin",
    "size": 5058624,
    "crc32": "c2244b26",
}

env__mmc_rd_configs = (
    {
        "fixture_id": "emmc-boot0",
        "is_emmc": True,
        "devid": 0,
        "partid": 1,
        "sector": 0x10,
        "count": 1,
    },
    {
        "fixture_id": "emmc-boot1",
        "is_emmc": True,
        "devid": 0,
        "partid": 2,
        "sector": 0x10,
        "count": 1,
    },
    {
        "fixture_id": "emmc-data",
        "is_emmc": True,
        "devid": 0,
        "partid": 0,
        "sector": 0x10,
        "count": 0x1000,
    },
    {
        "fixture_id": "sd-mbr",
        "is_emmc": False,
        "devid": 1,
        "partid": None,
        "sector": 0,
        "count": 1,
        "crc32": "8f6ecf0d",
    },
    {
        "fixture_id": "sd-large",
        "is_emmc": False,
        "devid": 1,
        "partid": None,
        "sector": 0x10,
        "count": 0x1000,
    },
)
