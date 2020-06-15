Haxo - What's inside my docker image
====================================

.. toctree::
   :hidden:
   :maxdepth: 1

  license
  reference


List deb, rpm, pip and npm packages installed in a docker image.


Installation
------------

To install haxo project, run this command in your terminal:

.. code-block:: console
  $ pip install haxo

Usage
-----

Haxo has a cli and it looks like:

.. code-block:: console
   $ Usage: haxo [OPTIONS] COMMAND [ARGS]...

  Haxo - look inside a docker image.

  This tool can be used to get information on system packages installed in a
  container image using package managers such as apt, dnf, rpm, pip and npm.

  Options:
    --version  Show the version and exit.
    --help     Show this message and exit.

  Commands:
    apt           apt package info.
    apt-licenses  apt packages and licenses info.
    pip           pip package info.
    rpm           rpm package info.

