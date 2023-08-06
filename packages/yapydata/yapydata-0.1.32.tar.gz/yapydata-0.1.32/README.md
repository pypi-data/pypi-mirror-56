YapyData
=========

**THIS IS A NIGHTLY PRE_BUILD FOR THE TEST OF THE BUILD CHAIN.**

The *YapyData* - Yet Another Python Data - package provides miscellaneous data processing *Python* utilities
for the adaptation of abstract APIs at the low-level part of the software stack.
The features comprise the management and processing of structured data types including the definition,
persistence, and the processing. The processing supports hereby the arbitrary mixed syntaxes for the
sources and targets, thus it is a "fingertip" to mixup e.g. *YAML*, *XML*, and *JSON* with *INI* in
any combination and at any data tree position - or basically with whatever.

The initial supported data definition languages are:

* *JSON*
* *Python* - used as dynamic DDL based on pickling for persistence
* *XML*
* *YAML*

In addition the syntaxes defined by the widespread configuration files:

* *INI* - multiple variants: *INI*, *INIX*, *CFG*, *CONF*
* *.properties* - the *Java* configuration syntax in *INI* style

The design targets of the low-level package *YapyData* are in particular:

* core processing of heterogeneous data definition syntaxes - DDLs
* abstract processing of heterogeneous input data structures against canonical reference data
* a mix of APIs for flexibility and use-case driven high performance 

This in particular supports the modularization, and the automation of the processing of
large scale heterogeneous data sets with canonical reference data.

The package *YapyData* is member of the *DataFusion* family by providing the basic 
syntaxes and features required for the low-level components of modern software stacks.
This is applicable including for installation utilities, thus is kept independent
from higher stack-layers when ever possible.
Ultimately, when required features are even provided redundant in favor of independence,
and appropriate API mix of flexibility with high-performance use-cases.

The higher application level offers semantic features such as full validation and standard compliant
processing options for example RFC-6901 [RFC6901]_ and RFC6902 [RFC6902]_, relative JSON paths,
and also for XML the processing of XPATH XSD, and XSLT.
See also *multiconf*, *jsondata*, *xmldata*, and *yamldata*.

Once again, the absolute and overall priority is the avoidance of circular dependencies by providing
an abstract core layer for a broad range of syntaxes.
The package  prioritizes modularity and granularity, eventually at the cost of
minor performance reduction e.g by using standard packages only.
For specific use-cases of large data alternates with better performance are included,
while the generic cases offer flexibility.

Last but not least the whole set of standard *Python* and *platforms* implementations is supported - and tested of course:

* *CPython*
* *IPython*
* *IronPython*
* *Jython*
* *PyPy*

soon:

* *Cython*
* *Stackless*


**Online documentation**:

* https://yapydata.sourceforge.io/


**Runtime-Repository**:

* PyPI: https://pypi.org/project/yapydata/

  Install: *pip install yapydata*, see also section 'Install' of the online documentation.


**Downloads**:

* sourceforge.net: https://sourceforge.net/projects/yapydata/files/

* bitbucket.org: https://bitbucket.org/acue/yapydata

* github.com: https://github.com/ArnoCan/yapydata/

* pypi.org: https://pypi.org/project/yapydata/


Project Data
------------

* PROJECT: 'YapyData'

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

* started with basic API - but those in production quality as required for other projects.

ToDo:

* add additional APIs

* add .Properties - yapydata.datatree.datatreesprop

* AIX

* MicroPython, CircuitPython

* test Windows10IoT-Core

