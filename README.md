I recently proposed a Python-based test infra-structure for U-Boot:

https://www.mail-archive.com/u-boot@lists.denx.de/msg194624.html

[PATCH V2 1/7] test/py: Implement pytest infrastructure

That system requires a number of "hook" scripts to exist to integrate the test
system with the specific hardware setup of the host it's running on. This
repository contains a complete example implementation of those scripts.
