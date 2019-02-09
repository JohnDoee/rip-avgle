Rip Avgle
===========

Small script to download videos from avgle.

Requirements
------------

- Linux, BSD, OSX - Something not windows
- Docker (and access to run commands with it)
- ffmpeg
- Python 3.5, 3.6
- Shell / SSH / Putty

Install
-------

::

    git clone https://github.com/JohnDoee/rip-avgle.git
    cd rip-avgle
    python3 -m venv .env
    .env/bin/pip install requests

Usage
-----

::

    .env/bin/python rip-avgle.py "http://url/video/2/" "http://url/video/1/"

License
-------

MIT, see LICENSE
