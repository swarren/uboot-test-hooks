# Copyright (c) 2015, NVIDIA CORPORATION. All rights reserved.
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

env__mount_points = (
    "/mnt/ubtest-mnt-p2371-2180-na",
)

env__usb_dev_ports = (
    {
        "tgt_usb_ctlr": "0",
        "host_ums_dev_node": "/dev/disk/by-path/pci-0000:00:14.0-usb-0:13:1.0-scsi-0:0:0:0",
        "host_usb_dev_node": "/dev/usbdev-p2371-2180",
        "host_usb_port_path": "3-13",
    },
)

env__block_devs = (
    # eMMC; always present
    {
        "type": "mmc",
        "id": "0",
        "writable_fs_partition": 1,
        "writable_fs_subdir": "tmp/",
    },
    # SD card; present since I plugged one in
    {
        "type": "mmc",
        "id": "1"
    },
)

env__dfu_configs = (
    # eMMC, partition 1
    {
        "alt_info": "/dfu_test.bin ext4 0 1;/dfu_dummy.bin ext4 0 1",
        "cmd_params": "mmc 0",
    },
    # RAM
    {
        "alt_info": "alt0 ram 80000000 01000000;alt1 ram 81000000 01000000",
        "cmd_params": "ram na",
    },
)

env__net_uses_pci = True

env__net_dhcp_server = True

env__net_tftp_readable_file = {
    "fn": "ubtest-readable.bin",
    "size": 5058624,
    "crc32": "c2244b26",
}
