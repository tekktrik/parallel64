Installation Instructions
=========================

Downloading parallel64
----------------------

You can install ``parallel4`` from PyPI using ``pip``:

.. code-block:: shell

    pip install parallel64

You can also install ``parallel64`` using either ``git`` or by downloading the source
code from `Github <https://github.com/tekktrik/parallel64>`_.

Using ``git``:

.. code-block:: shell

    git clone https://github.com/tekktrik/parallel64.git

Using Github:

    - Click the green button that says "Code"
    - In the "HTTPS" option, select ``Download ZIP``
    - Extract the contents of the ZIP file

Then make sure you are in the folder containing the source code
(either the git repository or the extracted folder), and install the package:

.. code-block:: shell

    pip install .

Determining the port address
----------------------------

You can see your parallel ports hardware addresses using the Device Manager.
Open the Device Manager (you can type "Device Manager in the start menu"),
and locate your parallel port in the "Ports (COM & LPT)".  Right click your
port and select "Properties", then select the "Resources" tab.

You may see 0ne or more hardware resources assigned for your port, depending
on it's capabilities, for the SPP and/or ECP base addresses.  These numeric
values are what you will use when instancing the ports in Python!
