# SuperDoCS
Superficial/Orthovoltage Dose Calculation System

SuperDoCS is a Dose Calculation and Calibration System for Superficial/Orthovoltage X-ray machines. 
It is based on the Django platform (2.x on Django-1.11, 3.x on Django 3.2 and 4.x on Django 4.2).

Before setting up the development virtual environment, packages
linux-source, python3-dev, python3 and git are required.

SuperDoCS is being developed based on Ubuntu. Setup steps below are hence Ubuntu based, for both development and production:

<h3>Setup Steps for Development System</h3>

1. Ubuntu base installation (any flavors, including WSL). Make sure it has a Python version that Django supports. See Compatibility Matrix for more information.

2. `sudo apt install gcc g++ gfortran python3-dev python3-pip python3-venv python3-wheel libjpeg-dev`

   _Note: the development tools above are required for building python wheels_

3. Download SuperDoCS

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

5. `vi sxtweb/sxtweb/local.py` # make sure DEBUG=True and add your servers IP address to ALLOWED_HOSTS

6. `python3 manage.py runserver 0:8000`

Now you can use http://your-ip:8000 for web site access.


<h3>Setup Steps for Production System</h3>

1. Ubuntu based installation (Ubuntu LTS recommented). Make sure that SuperDoCS -- Django -- Python -- Ubuntu versions are matching. See Compatibility Matrix for more information.

2. `sudo apt install git vim`

3. Download SuperDoCS
   ```
   git clone https://github.com/lixinzhan/SuperDoCS.git
   git config --global user.name "Your Name"
   git config --global user.email you@email
   git config --global core.editor "vim"
   ```

4. Make necessary changes in `local.py`
   ```
   cd SuperDoCS
   vi sxtweb/sxtweb/local.py
   ```

7. Setup services

   ```
   ./setup.sh -a 2>&1 | tee /tmp/sxt_install.log
   ```

8. Access the webpage and commission the system.



<h3>Migrate Existing DB</h3>

```
# copy the existing DB to the sxtweb/sxt.db
python3 manage.py makemigrations
python3 manage.py migrate
```



<h3>TODO:</h3>

- update jQuery scripts from Ver 4.x.
- simplify the system setup procedure.
- add unit tests.


----------------------------------------------------

<h3>Appendix: Compatibility Matrix</h3>

   | SuperDoCS | Django | Django EOL  | Python       | Ubuntu              | RHEL    | Comment |
   | ----------| ---    | ---         | ---          | ---                 | ---     | ---     |
   | 2.x       | 1.11   | 20200401    | 2.7, 3.4-3.7 | 18.04               | 7, 8    | gunicorn 20.x |
   | 3.x       | 3.2    | 20240401    | 3.6-3.10     | 20.04, 22.04        | 7, 8, 9 | gunicorn 22.x |
   | 4.x       | 4.2    | 20260401    | 3.8-3.12     | 20.04, 22.04, 24.04 | 8, 9    | |
   | 5.x       | 5.2    | 20280401    | ---          | 22.04, 24.04, 26.04 | 8, 9    | |
  
   _Notes:_
   
1. Default Python Versions in Linux Distributions

   - Ubuntu 18.04: 2.7, 3.6
   - Ubuntu 20.04: 3.8
   - Ubuntu 22.04: 3.10
   - Ubuntu 24.04: 3.12
   - Ubuntu 26.04: 3.14(?)
   - RHEL 7.7+: 2.7, 3.6
   - RHEL 8: 3.6 (available 2.7, 3.8, 3.9, 3.11, 3.12)
   - RHEL 9: 3.9 (available 3.11, 3.12)

2. [Python version support information](https://devguide.python.org/versions/)_
