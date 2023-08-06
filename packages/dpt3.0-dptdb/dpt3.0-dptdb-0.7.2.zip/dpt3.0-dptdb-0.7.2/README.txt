==========================================
DPT database API wrappers built using SWIG
==========================================

.. contents::


Description
===========

This package provides Python applications with the database API used by DPT.

DPT is a multi-user database system for Microsoft Windows.

The Python application can be as simple as a single-threaded process embedding the DPT API.

The package is available only as a source distribution.  It is built with the `MinGW`_ toolchain and `SWIG`_, either on Microsoft Windows or on `Wine`_ on an operating system able to run `Wine`_.

This version of the package is known to work with MinGW-6.3.0 but not with MinGW-5.3.0, MinGW-4.9.3, or MinGW-4.8.1.  Use dpt3.0-dptdb-0.6.5, or later 0.6.n versions, with earlier versions of MinGW if necessary.

Setup will download the DPT API `source`_ and `documentation`_ zip files if an internet connection is available.

There is no separate documentation for Python.


Installation Instructions
=========================

Microsoft Windows
-----------------

   Build dependencies

      * `Python`_ 2.7 or later 
      * `setuptools`_
      * `SWIG`_ 4.0.1 or later
      * `MinGW Installation Manager`_

      Download and install the MinGW Installation Manager.

      Follow the `MinGW`_ instructions to install MSYS and at least the MinGW base and gcc-g++ compiler suite.

      Download and install SWIG and Python.

      Download and install setuptools in Python if not already present.

   Use 'regedit' to put the directories containing the MinGW runtime in the path: usually C:\MinGW\bin and C:\MinGW\lib\gcc\mingw32\6.3.0 where the 6.3.0 is an example of a compiler version. 

   Install the package by typing

       python setup.py install

   at the command prompt of an MSYS shell with setup.py in the current directory.

   Runtime dependencies

   * Python 2.7 or later provided the version (2.7 for example) is the same as the Python used to build dptdb.
   * The MinGW runtime used to build dptdb.

Wine
----

    These installs were done on FreeBSD.  I do not know what happens elsewhere.

    The package can be installed for Pythons 2.7, 3.3, 3.4, and 3.5, which are installed under Wine.

    The package cannot be installed for Pythons 3.7, and 3.8, which are installed under Wine.

    For Python 3.6 it may matter whether the FreeBSD is i386 or amd64:

        The package can be installed for Python 3.6 on FreeBSD 11.3 i386 with the emulators/wine port (on a 64-bit box).

        The package cannot be installed for Python 3.6 on FreeBSD 12.1 amd64 with the emulators/i386-wine port.

   Build dependencies

      * `Wine`_ 
      * `Python`_ 2.7 or later (both host system and Microsoft Windows versions) 
      * `setuptools`_
      * `SWIG`_ 4.0.1 or later
      * `MinGW Installation Manager`_
      * 'GNU make'_ (called gmake on BSD systems, usually make otherwise)

      Download and install Wine.

      Download and install the MinGW Installation Manager under Wine.

      Follow the `MinGW`_ instructions to install at least the MinGW base and gcc-g++ compiler suite.

      Download and install Python if not already present. (Your distribution almost certainly provides Python.)

      Download and install GNU make if not already present. (Your distribution almost certainly provides GNU make.)

      Download and install Microsoft Windows versions of SWIG and Python under Wine.

      Download and install setuptools in Python if not already present.

      Download and install setuptools in the Python installed under Wine if not already present.

   At Python 3.4 and later it is not possible to use the Windows installers to install Python under Wine.  Several problem forums suggest copying a 'user-only' install under Microsoft Windows to Wine as a workaround.

   Install the package by typing

       python setup.py install

   at the command prompt of a shell with setup.py in the current directory.

   'python' should be the same version as the one under Wine where dptdb is being installed.  If this is not possible the command must be something like:

       python3.8 setup.py install PATH_TO_PYTHON=C:/Python27 PYTHON_VERSION=27

    The PATH_TO_PYTHON can be omitted if the Python on Wine is at it's default location for a 'user-only' install.  C:/Users/[user]/AppData is accepted as the default location if C:/Users/[user]/AppData/Local/Programs does not exist.

   Runtime dependencies

   * Python 2.7 or later provided the version (2.7 for example) is the same as the Python used to build dptdb.
   * The MinGW runtime used to build dptdb.


A directory named like dpt3.0_dptdb-0.5-py2.7.egg is put in site-packages by the install command.  The name means version 0.5 of dptdb for Python 2.7 wrapping version 3.0 of the DPT API.  This directory contains the dptdb and EGG-INFO directories.

The DPT documentation zip file is in the dptdb directory.


Sample code
===========

The dptdb/test directory contains a simple application which populates a database, using some contrived data, and does some simple data retrievals.

This can be run on Microsoft Windows by typing

   python pydpt-test.py

at the command prompt of a shell with pydpt-test.py in the current directory.

The equivalent command to run the sample application under Wine is

   wine python pydpt-test.py

at the command prompt of a shell with pydpt-test.py in the current directory.

You may need to use '<path to python>/python pydpt-test.py' if several versions of Python are installed.


The sample application offers seven options which create databases with different numbers of records.  Each record has 6 fields and all fields are indexed.

   One option, called normal, adds 246,625 records to a database in a 16 Mb file in about 3.33 minutes with transaction backout enabled.

   The shortest option adds 246,625 records to a database in a 16 Mb file in about 0.6 minutes with transaction backout disabled.

   The longest option adds 7,892,000 records to a database in a 526 Mb file in about 18.75 minutes with transaction backout disabled.

The figures are for a 2Gb 667MHz memory, 1.8GHz CPU, solid state drive, Microsoft Windows XP installation.


Restrictions
============

When used under Wine, very large single-step loads will fail through running out of memory because the test to decide when to complete a chunk of the load and start a new one never says 'do so'.  One workaround is to do multi-step loads, potentially a lot slower as explained in `relnotes_V2RX.html`_ from DPT_V3R0_DOCS.ZIP, which was the only way to do this before version 2 release 14 of the DPT API.  Another is to split the load into small enough chunks somehow before invoking the single-step process for each chunk.

The "Try to force 'multi-chunk' on 32Gb memory" option does enough index updating, see slowest option under `Sample code`_ for detail, to cause this failure under Wine on a 2Gb memory machine.

This is known to happen on FreeBSD.  It is possible it does not happen on other Operating Systems able to run Wine.


Notes
=====

This package is built from `DPT_V3R0_DBMS.ZIP`_, a recent DPT API source code distribution, by default.

You will need the `DPT API documentation`_ to use this package.  This is included as `DBAPI.html`_ in DPT_V3R0_DOCS.ZIP.

The DPT documentation zip file is in a directory named like C:/Python27/Lib/site-packages/dpt3.0_dptdb-0.5-py2.7.egg/dptdb, using the example at the end of `Installation Instructions`_.

The dptapi.py and _dptapi.pyd modules are built using `SWIG`_ and `MinGW`_ for a particular version of Python.  In particular a _dptapi.pyd built for Python 2.7 will work only on Python 2.7 and so on. 

The `DPT API distribution`_ contains independent scripts and instructions to build dptdb mentioning much earlier versions of the build dependencies.

This package will work only on a Python built for the Microsoft Windows platform.


.. _DPT API documentation: http://solentware.co.uk/files/DPT_V3R0_DOCS.ZIP
.. _documentation: http://solentware.co.uk/files/DPT_V3R0_DOCS.ZIP
.. _DBAPI.html: http://solentware.co.uk/files/DPT_V3R0_DOCS.ZIP
.. _relnotes_V2RX.html: http://solentware.co.uk/files/DPT_V3R0_DOCS.ZIP
.. _DPT_V3R0_DBMS.ZIP: http://solentware.co.uk/files/DPT_V3R0_DBMS.ZIP
.. _DPT API distribution: http://solentware.co.uk/files/DPT_V3R0_DBMS.ZIP
.. _source: http://solentware.co.uk/files/DPT_V3R0_DBMS.ZIP
.. _Python: https://python.org
.. _setuptools:  https://pypi.python.org/pypi/setuptools
.. _SWIG: http://swig.org
.. _MinGW: http://mingw.org
.. _Wine: https://winehq.org
.. _MinGW Installation Manager: http://sourceforge.net/projects/mingw/files/Installer/mingw-get-setup.exe/download
.. _GNU make: https://www.gnu.org/software/make/
