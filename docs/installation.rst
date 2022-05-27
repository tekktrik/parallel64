Installation Instructions
=========================

Due to having to run the contained DLL (explained later), this package
is no longer available on PyPI.  You must instead download the source
code to install this library.

Downloading parallel64
----------------------

You can install ``parallel64`` using either ``git`` or by downloading the source
code from `Github <https://github.com/tekktrik/parallel64>`_.

Using ``git``:

.. code-block:: shell

    git clone https://github.com/tekktrik/parallel64.git

Using Github:

    - Click the green button that says "Code"
    - In the "HTTPS" option, select ``Download ZIP``
    - Extract the contents of the ZIP file

Installing parallel64
---------------------

You can use ``pip`` to install the package!  Make sure you are in the folder
containing the source code (either the git repository or the extracted folder),
and install the package:

.. code-block:: shell

    pip install .

Setting up the DLL
------------------

On most modern versions of Windows, the DLL must be used once with Adminstrator
priveleges in order to function properly.  You can do so by running
``InpOutBinaries_1501/Win32/InstallDriver.exe`` in the source code folder.  This
will prompt you to use administrator priveleges.

.. note::

    You only need to do this step once!  After that, you're good to go!

Determining the port address
----------------------------

You can see your parallel ports hardware addresses using the Device Manager.
Open the Device Manager (you can type "Device Manager in the start menu"),
and locate your parallel port in the "Ports (COM & LPT)".  Right click your
port and select "Properties", then select the "Resources" tab.

You may see 0ne or more hardware resources assigned for your port, depending
on it's capabilities, for the SPP and/or ECP base addresses.  These numeric
values are what you will use when instancing the ports in Python!
