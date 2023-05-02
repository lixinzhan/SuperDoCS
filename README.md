# SuperDoCS
Superficial/Orthovoltage Dose Calculation System

SuperDoCS is a Dose Calculation and Calibration System for Superficial/Orthovoltage X-ray machines. 
It is based on the Django platform (2.x on Django-1.11 and 3.x on Django 3.2).

Before setting up the development virtual environment, packages
linux-source, python3-dev, python3 and git are required.

SuperDoCS is being developed mainly on Ubuntu. Steps below briefly shows how to set up a development environment on Ubuntu 20.04:

0. Ubuntu base installation (any flavors, including WSL)

1. `sudo apt install gcc g++ gfortran python3-dev python3-pip python3-venv python3-wheel libjpeg-dev`

2. `python3 -m venv .env-SuperDoCS`

3. `source .env-SuperDoCS/bin/active`

4. `git clone https://github.com/lixinzhan/SuperDoCS.git`

   `git config --global user.name "Your Name"`
   
   `git config --global user.email you@email`
   
5. `cd SuperDoCS`

6. `pip3 install -r requirement.txt`

7. `vi sxtweb/sxtweb/local.py` # make sure DEBUG=True and add your servers IP address to ALLOWED_HOSTS

8. `python3 manage.py runserver 0:8000`

Now you can use http://your-ip:8000 for web site access.


**To Migrate existing DB**

```
# copy the existing DB to the sxtweb/sxt.db
python3 management.py makemigrations
python3 management.py migrate
```


**This is the development branch.**

More installation procedure can be found in the description for releases. Contact me if you are interested in an installation based on a docker image.

(Note: Django 1.11 works with Python 2.7, 3.4-3.7, Django 3.2 (together with numpy and scipy) works with Python 3.8-3.11)
