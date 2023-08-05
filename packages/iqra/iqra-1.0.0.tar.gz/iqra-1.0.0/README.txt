:Date: 2019-11-18
:Version: 1.0.0
:Authors:
    * Mohammad Alghafli <thebsom@gmail.com>

Iqra, a library management program.
This is the core iqra library. It also acts as a commandline interface to interact with iqra database with basic commands.
If you are looking for a GUI library management program, look for giqra which provides a user interface to interact with iqra database.

------------
Installation
------------

On windows install using pip by running the
command::
    
    pip install iqra

Or on linux::
    
    pip3 install iqra

All dependancies will be installed automatically by pip. The stickers plugin needs pycairo so you need to install it if you want to use this plugin.

-----
Usage
-----

Running the commandline interface::

    python3 -m iqra

Use -h option to know all the possible options::

    python3 -m iqra -h

You can use iqra as a library and import it in your project::

    import iqra

