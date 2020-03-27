# SuperDoCS
Superficial/Orthovoltage Dose Calculation System

SuperDoCS is a Dose Calculation and Calibration System for Superficial/Orthovoltage X-ray machines. 
It is developed based on Django platform (currently 1.11).

Before setting up the development virtual environment, packages
linux-source, python3-dev, python3, git are required.

The development of this application is based on Ubuntu. For other distros or Windows or Mac OS X,
make your changes correspondingly.

Following steps below to set up a development environment in Ubuntu 18.04:

1. sudo apt install gcc g++ gfortran python-dev

2. python3 -m venv .env-SuperDoCS

3. source .env-SuperDoCS/bin/active

4. git clone https://github.com/lixinzhan/SuperDoCS.git

   git config --global user.name "Your Name"
   
   git config --global user.email you@email
   
5. cd SuperDoCS

6. pip3 install -r requirement.txt

7. vi sxtweb/sxtweb/local.py # make sure DEBUG=True and add your servers IP address to ALLOWED_HOSTS

8. python3 manage.py runserver 0:8000

Now you can use http://your-ip:8000 for web site access.


**This is now also the development branch.**

*Current Status:*

* DB Schema changed.

* Based on Python3 and Django 1.11.

* Version 2.0 will be based on python 3.6 + django 1.11 (on Ubuntu 18.04)
  Version 3.0 will be based on python 3.8 + django 2.2 (on Ubuntu 20.04)

* Supports both script setup and docker installation for web services.

More installation procedure can be found in the description for releases and the docker hub.

(Note: Django 1.11 works with Python 2.7, 3.4-3.7, Django 2.2 works with Python 3.5-3.8)
