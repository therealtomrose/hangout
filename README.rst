hangout
=======

A persistant hangout for our remote office.


Requirements
============


python
------

Make sure you are running python 2.7: http://www.python.org/download


Clone Testive git repo
======================


- Make a directory where you will store hangout (suggestions below)::

    mkdir ~/projects
    mkdir ~/projects/hangout
    cd ~/projects
    git clone https://github.com/therealtomrose/hangout.git hangout


Setup Virtual Env
=================


Create virtual environment
--------------------------

Do this where the project will live e.g. 'testive'
- install virtualenv::

    sudo easy_install pip
    sudo pip install virtualenv

- install a new virtual environment in the directory where the project will live::

    cd ~/projects
    virtualenv --no-site-packages hangout
    sudo pip install -U versiontools

- configure the local python path::

    echo 'export PYTHONPATH=$PYTHONPATH:~/projects/hangout' >> ~/projects/hangout/bin/activate
    echo 'export PATH=~/projects/hangout:$PATH' >> ~/projects/hangout/bin/activate


Install requirements
--------------------

- Run the pip installer with a requirements file. (Look in ~/projects/testive/conf for a requirements file that matches your hardware)::

    cd ~/projects/hangout
    source bin/activate
    sudo pip install -r requirements.txt


Configure Settings
==================

- Make a copy of the settings template file and enter your local settings.
- To get the URI of a persistant google hangout, create a virtual event far in the future in google plus, then get the associated hangout address.

    cd ~/projects/hangout
    cp settings_local.template settings_local.py


Running
=======


Load Virtual Environment
------------------------

::

    cd ~/projects/testive
    source bin/activate


Run Hangout
-----------

::

    python hangout.py
