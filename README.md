This repository contains working example support ("hook") scripts for U-Boot's
built-in test framework. That framework is located in the `test/py/` directory
in the U-Boot source tree.

You may use these examples as a reference when creating your own hook scripts,
or even derive your own scripts directly from the files in this repository.

# Flashing Philosophy

U-Boot may be installed onto a target device either by:

- Writing the U-Boot binary to flash, so that it runs at every cold boot or
  reset. In this case, flashing is a one-time operation.

- Downloading U-Boot into RAM whenever it needs to RAM. In this case, the
  download needs to happen every time the target board is reset, since the
  desired binary is not permanently stored on the system.

The example scripts in this repository take the second approach. This approach
avoids modifying the device's flash memory for each U-Boot binary to be tested,
which should increase longevity of the device. This does mean that the
implementation of the `test/py/` hook scripts is slightly inconsistent with
their naming; `u-boot-test-flash` does nothing whereas `u-boot-test-reset`
downloads U-Boot into RAM rather than only performing a simple system reset.

# USB Port Paths

When multiple USB devices of the same type are attached to the same system, some
mechanism for differentiating between them is required, in order for software to
choose which device to communicate with. In some cases, the only available
mechanism is based on the physical USB port to which the device is attached. For
this mechanism to work, there must be a stable way to uniquely name each
physical USB port. The naming convention is known as the USB port path.

Each USB bus in the system is assigned a unique number by the Linux kernel.
These numbers are typically stable across reboots since they are assigned based
on device creation or probing order, which is usually driven by stable
BIOS-driven data structures. Changes to system hardware can cause these numbers
to change though. Equally, it's a good idea to validate the bus numbers after
reboot. The USB bus number forms the first part of the USB port path.

Each USB controller or hub contains a number of physical USB ports (sockets).
Each of these has a unique fixed number, per the USB specification. These port
numbers form the balance of the USB port path.

Linux uses the format `${bus}-${port}.${port}.${port}...` to represent the USB
port path.

For example:

    +--------------+
    | PC           |
    | +----------+ |
    | | USB ctlr | |
    | | Bus 4    | |       +----------+
    | |   Port 1 |---------| USB hub  |
    | +----------+ |       |   Port 1 |     +-----------------+
    +--------------+       |   Port 2------ | USB device      |
                           |   Port 3 |     | Port path 4-1.2 |
                           +----------+     | Bus/device 4/15 |
                                            +-----------------+

Note that USB device numbers are not stable; they change each time a device
appears on the bus, such as when it is power cycled or reset.

To determine the USB port path of your device, first manually identify a device
node related to your USB device. For example, you might run `lsusb` with the
device both unplugged and plugged in, find the device's bus and device number,
and then use device file `/dev/bus/usb/${busnum}/${devnum}`. Alternatively, you
may find some type-specific device node such as `/dev/ttyUSB2` or `/dev/sdc` by
experimentation using tools such as `picocom` or `mount` and `ls`.

Once a device node has been identified, use udevadm to query all known
information about the device, then find an entry with `SUBSYSTEMS=="usb"` and a
`KERNELS` value in the format of a USB port path:

    $ udevadm info -a /dev/ttyUSB2
    ...
    looking at device '/devices/pci0000:00/0000:00:14.0/usb3/3-6/3-6:1.2/ttyUSB2/tty/ttyUSB2':
        KERNEL=="ttyUSB2"
        SUBSYSTEM=="tty"
        DRIVER==""

    looking at parent device '/devices/pci0000:00/0000:00:14.0/usb3/3-6/3-6:1.2/ttyUSB2':
        KERNELS=="ttyUSB2"
        SUBSYSTEMS=="usb-serial"
        DRIVERS=="ftdi_sio"
    ...
    looking at parent device '/devices/pci0000:00/0000:00:14.0/usb3/3-6/3-6:1.2':
        KERNELS=="3-6:1.2"
        SUBSYSTEMS=="usb"
        DRIVERS=="ftdi_sio"
    ...
    looking at parent device '/devices/pci0000:00/0000:00:14.0/usb3/3-6':
        KERNELS=="3-6"
        SUBSYSTEMS=="usb"
        DRIVERS=="usb"
    ...
    looking at parent device '/devices/pci0000:00/0000:00:14.0/usb3':
        KERNELS=="usb3"
        SUBSYSTEMS=="usb"
        DRIVERS=="usb"

Here, the USB port path is "`3-6`".

or:

    $ udevadm info -a /dev/bus/usb/003/086
    ....
    looking at device '/devices/pci0000:00/0000:00:14.0/usb3/3-10/3-10.4':
        KERNEL=="3-10.4"
        SUBSYSTEM=="usb"
        DRIVER=="usb"

Here, the USB port path is "`3-10.4`".

# udev Rules

See the `udev/` directory in this repository.

Testing should be performed as a non-root user. This requires that the relevant
device nodes have non-default permissions. udev rules may be used to achieve
this.

To save hardware, it is possible to attach multiple Tegra devices to a single
host machine. This requires that each program that interacts with the device be
able to communicate with a specific Tegra device.

Some applications allow the USB port path be passed to them as a parameter. This
requires no configuration via udev.

Some applications use device-specific properties to identify devices, such as
the serial number encoded into a USB device descriptor. This requires no
configuration via udev.

Other applications allow a USB device filename to be passed in. udev rules may
be used to create well-known device filenames based on a device's USB port
path.

The example udev rules demonstrate both of these types of rules.

# Scripts and Binaries

See the `bin/` directory in this repository.

Scripts exist to power on, power off, flash, and reset Tegra boards, and access
their serial console. The U-Boot test framework expects these scripts to exist
in `$PATH`, and executes them at appropriate times.

Note that the test framework itself does not use the power on/off scripts.
However, they may be used by a companion continuous integration framework that
triggers the U-Boot test framework. For example,
https://github.com/swarren/u-boot-ci-scripts.

U-Boot's test framework identifies each board by type (e.g. p2371-2180; the
engineering name for Jetson TX1) and identity (an arbitrary user-assigned string
used to differentiate multiple instances of the same board type within a user's
testing setup). Each script is passed these two parameters to inform it which
board to operate upon.

Different test setups will use different techniques to control target hardware.
For example, reset and forced recovery signals may be manipulated through
NVIDIA's proprietary PM342 debug board, or some form of relay or electronic
switch board hard-wired to the board's physical buttons.

The scripts are written to be highly generic, and allow sharing of code between
boards. To this end, the top-level implementation of each script does little
more than include a board-specific configuration file, and then include another
file specific to implementation the desired action.

Board configuration files are located in
`bin/${hostname}/conf.${board_type}_${board_identity}`. These files are
segregated by hostname so that the repository can be used directly across
multiple different test machines, without the need for host-specific branches or
post-checkout configuration.

The board configuration file defines which mechanism is used for each possible
action, and any parameters associated with it. For example, downloading U-Boot
into RAM may used either the `tegra-uboot-flasher` tool for boards containing
T124 or earlier, or L4T's `exec-uboot.sh` for boards containing T210 or newer.
These scripts. In each case, the directory name where the tool is installed must
be defined.

Each action is implemented in a script fragment directly in the `bin/` directory,
with filename `${action_type}.${implementation_name}`.

If using these scripts directly for testing Tegra devices, it is likely that
you will not need to create new `download.*` implementations, but will need to
create new `poweroff.*`, `poweron.*`, and `recovery.*` implementations.

Observe that some external tools (`download.*` especially) invoked by these
scripts must be replicated once per board instance, or their actions somehow
serialized, since they copy files into their own directories when executing, and
hence parallel execution would cause incorrect operation.

## Dependencies

The example scripts depend on various external tools, the installation location
of which must be specified in the board configuration files:

- `tegra-uboot-flasher`; see
  https://github.com/NVIDIA/tegra-uboot-flasher-scripts.
- L4T's flashing tools. This must be a regular L4T host-side installation,
  possibly stripped down to contain just:
  - The top-level directory (which contains `flash.sh` and `*.conf`).
  - The `bootloader/` directory.
  - The `kernel/` directory.
- `imx_usb`; see
  https://github.com/boundarydevices/imx_usb_loader.
- As-yet-unpublished scripts to control various USB relay boards.

U-Boot's test framework also requires a `dfu-util` that supports the -p
command-line option. Many distros don't provide this, so a manually compiled
binary is included.

# Python Modules

See the `py/` directory in this repository.

A Python module exists for each board and defines numerous parameters used by
the U-Boot test framework. The framework expects to simply import these modules
directly, and hence they must be locatable within `$PYTHONPATH`.

These modules are again located in a separate directory for each host, so that
the repository may be shared across hosts.

For complete details re: the required content of these Python modules, please
see `test/py/README.md` in the U-boot source tree, and also the comments in some
individual test files in `test/py/tests/test_*.py`.
