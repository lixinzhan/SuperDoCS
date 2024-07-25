# SuperDoCS
Superficial/Orthovoltage Dose Calculation System

SuperDoCS is a Dose Calculation and Calibration System for Superficial/Orthovoltage X-ray machines. 
It is based on the Django platform (2.x on Django-1.11, 3.x on Django 3.2 and 4.x on Django 4.2).

Before setting up the development virtual environment, packages
linux-source, python3-dev, python3 and git are required.

SuperDoCS is being developed mainly on Ubuntu. Steps below briefly shows how to set up a development environment on Ubuntu:

0. Ubuntu base installation (any flavors, including WSL). Make sure it has a Python version that Django supports. See Compatibility Matrix for more information.

2. `sudo apt install gcc g++ gfortran python3-dev python3-pip python3-venv python3-wheel libjpeg-dev`

   _Note: the development tools above are required for building python wheels_

2. Download SuperDoCS

   ```
   git clone https://github.com/lixinzhan/SuperDoCS.git
   git config --global user.name "Your Name"
   git config --global user.email you@email
   git config --global core.editor "vim"
   ```

4. Setup Virtual Environment
  
   ```
   cd SuperDoCS
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip3 install -r requirement.txt
   ```

9. `vi sxtweb/sxtweb/local.py` # make sure DEBUG=True and add your servers IP address to ALLOWED_HOSTS

10. `python3 manage.py runserver 0:8000`

Now you can use http://your-ip:8000 for web site access.


**To Migrate existing DB**

```
# copy the existing DB to the sxtweb/sxt.db
python3 manage.py makemigrations
python3 manage.py migrate
```


**This is the development branch.**

More installation procedure can be found in the description for releases. Contact me if you are interested in an installation based on a docker image.

TODO:

- update jQuery scripts from Ver 4.x.

----------------------------------------------------

<h3>Appendix: Compatibility Matrix</h3>

   | SuperDoCS | Django | Django EOL  | Python       | Ubuntu              | Comment |
   | ----------| ---    | ---         | ---          | ---                 | ---     |
   | 2.x       | 1.11   | 20200401    | 2.7, 3.4-3.7 | 18.04               | gunicorn 20.x |
   | 3.x       | 3.2    | 20240401    | 3.6-3.10     | 20.04, 22.04        | gunicorn 22.x |
   | 4.x       | 4.2    | 20260401    | 3.8-3.12     | 20.04, 22.04, 24.04 | |
   | 5.x       | 5.2    | 20280401    | ---          | 22.04, 24.04, 26.04 | |
  
   _Note: Default Python versions in Ubuntu_

   - Ubuntu 18.04: 2.7, 3.6
   - Ubuntu 20.04: 3.8
   - Ubuntu 22.04: 3.10
   - Ubuntu 24.04: 3.12
