yapyutils
=========

**THIS IS A NIGHTLY PRE_BUILD FOR THE TEST OF THE BUILD CHAIN.**

The 'yapyutils' - Yet Another Python Utils - package provides miscellaneous *Python* utilities for the adaptation 
of platform independent APIs of the low-level part of the software stack.
These are e.g. used for extensions of the *setuptools* and *distutils*, thus reduce
the package dependency and avoid circular dependencies whenever possible by using standard packages and classes only. 
The more complex and complete data packages are provided for higher application layer 
functionality.

The current release contains:

* *yapyutils.modules*

  A utility to locate and load modules by a given name and/or file system path name,
  based on the *sys.path* variable.

* *yapyutils.files*

  Search and location of files, e.g. modules and configuration files.

* *yapyutils.help*

  Simple help for command line interfaces. 

* *yapyutils.config*

  Configuration file support, in particular for the initial setup of software packages.


**Online documentation**:

* https://yapyutils.sourceforge.io/


**Runtime-Repository**:

* PyPI: https://pypi.org/project/yapyutils/

  Install: *pip install yapyutils*, see also section 'Install' of the online documentation.


**Downloads**:

* sourceforge.net: https://sourceforge.net/projects/yapyutils/files/

* bitbucket.org: https://bitbucket.org/acue/yapyutils

* github.com: https://github.com/ArnoCan/yapyutils/

* pypi.org: https://pypi.org/project/yapyutils/


Project Data
------------

* PROJECT: 'yapyutils'

* MISSION: Canonical numeric platform IDs for the core Python environment.

* VERSION: 00.01

* RELEASE: 00.01.001

* STATUS: beta

* AUTHOR: Arno-Can Uestuensoez

* COPYRIGHT: Copyright (C) 2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez

* LICENSE: Artistic-License-2.0 + Forced-Fairplay-Constraints

Runtime Environment
-------------------
For a comprehensive list refer to the documentation.

**Python Syntax Support**

*  Python2.7, and Python3

**Python Implementation Support**

*  CPython, IPython, IronPython, Jython, and PyPy

**OS on Server, Workstation, Laptops, Virtual Machines, and Containers**

* Linux: AlpineLinux, ArchLinux, CentOS, Debian, Fedora, Gentoo, OpenSUSE, Raspbian, RHEL, Slackware, SLES, Ubuntu, ...  

* BSD: DragonFlyBSD, FreeBSD, NetBSD, OpenBSD, GhostBSD, TrueOS, NomadBSD

* OS-X: Snow Leopard

* Windows: Win10, Win8.1, Win7, WinXP, Win2019, Win2016, Win2012, Win2008, Win2000

* WSL-1.0: Alpine, Debian, KaliLinux, openSUSE, SLES, Ubuntu

* Cygwin

* UNIX: Solaris10, Solaris11

* Minix: Minix3

* ReactOS

**Network and Security**

* Network Devices: OpenWRT

* Security: KaliLinux, pfSense, BlackArch, ParrotOS, Pentoo

**OS on Embedded Devices**

* RaspberryPI: ArchLinux, CentOS, OpenBSD, OpenWRT, Raspbian

* ASUS-TinkerBoard: Armbian

* By special modules e.g. for Adafruit Trinket M0: CircuitPython, MicroPython

Current Release
---------------

Major Changes:

* Initial version.

ToDo:

* AIX

* MicroPython, CircuitPython

* test Windows10IoT-Core

