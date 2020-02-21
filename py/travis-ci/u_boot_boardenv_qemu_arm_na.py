import os
import travis_tftp

env__net_uses_pci = True
env__net_dhcp_server = True
env__net_tftp_readable_file = travis_tftp.file2env('u-boot.bin', 0x40400000)
env__efi_loader_helloworld_file = travis_tftp.file2env('lib/efi_loader/helloworld.efi', 0x40400000)
env__efi_loader_grub_file = travis_tftp.file2env('grub_arm.efi', 0x40400000)
env__efi_fit_tftp_file = {
    'addr' : 0x40400000,
    "dn" : os.environ['UBOOT_TRAVIS_BUILD_DIR'],
}
