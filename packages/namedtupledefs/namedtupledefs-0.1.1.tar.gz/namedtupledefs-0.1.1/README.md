namedtupledefs
==============

**THIS IS A NIGHTLY PRE_BUILD FOR THE TEST OF THE BUILD CHAIN.**

The package 'namedtupledefs' provides a patched version of the *collections.namedtuple* 
with field defaults for *namedtuple* and type-accurate *_merge*. This is a drop-in compatible
patch with multiple enhancements.

Standard *collections.namedtuple* compatible: 

	import namedtupledefs
	
	Point0 = namedtupledefs.namedtuple('Point', ('x', 'y', 'z'))
	Point1 = namedtupledefs.namedtuple('Point', ('x y z'))
	
	point0 = Point0(11, 22, 33) 
	point1 = Point1(11, 22, 33)


The same with defaults:
	
	from namedtupledefs import namedtuple
	
	Point0defs = namedtupledefs.namedtuple('Point', ('x', 'y', 'z'), fielddefaults=(22, 33))
	Point1defs = namedtupledefs.namedtuple('Point', ('x y z'), fielddefaults=(22, 33))
	
	point0defs = Point0defs(11, 22) 
	point1defs = Point1defs(11) 
	
With the identical results:
		
	point0defs == point0 
	point1defs == point1 
	
of the printout:
	
	>>> point0
	Point(x=11, y=22, z=33)
	
	>>> point0defs
	Pointdefs(x=11, y=22, z=33)

Added the method *_merge* to the created class with accurate handling of
*_fields* and *_fielddefaults*:

	msg_header._merge('NewClassName', msg_body, msg_data)



See doc-string and online documents for more examples.
For the standard library *collections.namedtuple* see Python documentation.

**Online documentation**:

* https://namedtupledefs.sourceforge.io/


**Runtime-Repository**:

* PyPI: https://pypi.org/project/namedtupledefs/

  Install: *pip install namedtupledefs*, see also section 'Install' of the online documentation.


**Downloads**:

* sourceforge.net: https://sourceforge.net/projects/namedtupledefs/files/

* bitbucket.org: https://bitbucket.org/acue/namedtupledefs

* github.com: https://github.com/ArnoCan/namedtupledefs/

* pypi.org: https://pypi.org/project/namedtupledefs/


Project Data
------------

* PROJECT: 'namedtupledefs'

* MISSION: The extension of the standard *collections.namedtuple* by default values, merging, and accurate pickling.

* VERSION: 00.01

* RELEASE: 00.01.001

* STATUS: alpha

* AUTHOR: Arno-Can Uestuensoez

* COPYRIGHT=Copyright (c) 2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez. 
	
* LICENSE=Artistic-License-2.0 + Forced-Fairplay-Constraints - see following clauses

Patches and this Documentation:

* COPYRIGHT=Copyright (c) 2019 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez. All rights reserved.
	
* LICENSE=Artistic-License-2.0 + Forced-Fairplay-Constraints
	      
  With exception for the public integration into the standard library *collections* 
  by the PSF. Than for the integrated public code-patches: 
    PSF LICENSE AGREEMENT FOR PYTHON.  

Original code copied from Standard Python Library see "namedtupledefs.namedtuple_original":

* COPYRIGHT ORIGINAL=Copyright (c) 2001-2018 Python Software Foundation. All rights reserved.

* LICENSE ORIGINAL=PSF LICENSE AGREEMENT FOR PYTHON


Runtime Environment
-------------------
For a comprehensive list refer to the documentation.

**Python Syntax Support**

* Python3
* For the Python2.7 refer to the package namedtupledefs2.
  
  This package requires the *exec* statement/function, due to it's size it is
  separated into two variants instead of using shared code.  

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

Current Release
---------------

Major Changes:

* Initial release.


ToDo:

* MicroPython, CircuitPython

Known Issues:

* not yet

