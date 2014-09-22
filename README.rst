hangout
=======

A script for maintaining persistant google hangouts. (We use this for connecting a remote office.)


Requirements
============


python
------

Make sure you are running python 2.7: http://www.python.org/download


unhangout
---------

Create an unhangout conference room at http://unhangout.media.mit.edu/h/

git
---

Make sure you have git http://git-scm.com/


Clone git repo
==============


- Make a directory where you will store hangout (suggestions below)::

    mkdir ~/projects
    mkdir ~/projects/hangout
    cd ~/projects
    git clone https://github.com/therealtomrose/hangout.git hangout


Setup Virtual Env
=================


Create virtual environment
--------------------------

Do this where the project will live e.g. 'hangout'
- install virtualenv::

    sudo easy_install pip
    sudo pip install virtualenv

- install a new virtual environment in the directory where the project will live::

    cd ~/projects
    virtualenv --no-site-packages hangout/venv
    sudo pip install -U versiontools

- configure the local python path::

    echo 'export PYTHONPATH=$PYTHONPATH:~/projects/hangout' >> ~/projects/hangout/vevn/bin/activate
    echo 'export PATH=~/projects/hangout:$PATH' >> ~/projects/hangout/venv/bin/activate


Install requirements
--------------------

- Run the pip installer with a requirements file.::

    cd ~/projects/hangout
    source bin/activate
    sudo pip install -r requirements.txt


Configure Settings
==================

- Make a copy of the settings template file and enter your local settings.::

    cd ~/projects/hangout
    cp settings_local.template settings_local.py


Running
=======


Load Virtual Environment
------------------------

::

    cd ~/projects/hangout
    source bin/activate


Run Hangout
-----------

::

    python hangout.py
