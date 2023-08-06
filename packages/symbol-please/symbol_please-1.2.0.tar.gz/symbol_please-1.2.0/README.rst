=============
Symbol Please
=============


.. image:: https://img.shields.io/pypi/v/symbol-please.svg
        :target: https://pypi.python.org/pypi/symbol-please


Symbol Please is a visual log parsing helper for Project 1999 with a built-in spell timer overlay.

.. image:: /uploads/e81cb7fbf04c916e055534cbd5142ca8/image.png
   :alt: Screenshot of spell timer window


How to Install
--------------

Symbol Please can be installed using pip from a terminal:

.. code-block:: bash

    $ sudo pip install symbol_please

NOTE: If you're installing inside of a virtualenv, the environment must have access to the system site packages to use GTK.

.. code-block:: bash

    $ mkvirtualenv --system-site-packages symbol_please

Getting Started
---------------

You'll need to enable logging for Symbol Please to work. This can be done in-game with the command `/log on`, but I recommend enabling logging permanently by changing `Log=FALSE` to `Log=TRUE` in eqclient.ini.

Once installed, Symbol Please should be available in your system application menu. Symbol Please can also be launched from the terminal by running the following command:

.. code-block:: bash

    $ symbol_please

When you first launch Symbol Please, you'll need to make a new profile for the character you plan to play with. The only configuration necessary is the path to the logfile, and your character's level, which is used for variable duration spells.

Once your profile is created, you can select it and press start. This will open the overlay window. As you cast spells, duration bars will show up here. Drag it over you EQ window, and press Lock. While this window is locked, mouse clicks will pass through to the game until you press unlock.

Dependencies
------------

* GTK+3

Features
--------

* Built-in buff timers

Changelog
---------

1.2.0 (November 20, 2019)
~~~~~~~~~~~~~~~~~~~~~~~~~
- Illusions fade when zoning

1.1.1 (November 11, 2019)
~~~~~~~~~~~~~~~~~~~~~~~~~
- Also detect level changes when losing a level
- Install desktop files to launch from application menu

1.1.0 (November 10, 2019)
~~~~~~~~~~~~~~~~~~~~~~~~~
- Detect new level messages, and auto-update config
- Consistent window size between lock/unlocked

1.0.0 (June 13, 2019)
~~~~~~~~~~~~~~~~~~~~~
- Initial release.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
