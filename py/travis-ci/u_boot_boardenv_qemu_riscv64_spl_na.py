import os
import travis_tftp

env__net_dhcp_server = True
env__net_tftp_readable_file = travis_tftp.file2env('u-boot')
env__efi_loader_helloworld_file = travis_tftp.file2env('lib/efi_loader/helloworld.efi')
env__efi_loader_grub_file = travis_tftp.file2env('grub_riscv64.efi')
env__efi_fit_tftp_file = {
    "dn" : os.environ['UBOOT_TRAVIS_BUILD_DIR'],
}
