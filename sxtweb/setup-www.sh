#!/bin/bash
#

# Get the current directory and project.
CWD = $(pwd)
PRJ = $(basename $CWD)
ENV = $(pwd)+'/.env/'

# add universe.
add-apt-repository universe

# check if package is installed.
if [ -z `dpkg -l python3-dev | grep '^ii'` ]
then
    apt install python3-dev
else
    echo "python3-dev was previously installed!"
fi

if [ -z `dpkg -l nginx | grep '^ii'` ]
then
    apt install nginx
else
    echo "nginx was previously installed!"
fi

# seup virtual environment
python3 -m venv .env
source .env/bin/active
pip install -r requirement.txt

# setup services

# gunicorn
cat config/gunicorn.service | sed "s|^WorkingDirectory=.*|WorkingDirectory=$CWD/g" | sed "s/^ExecStart=.*/ExecStart=\'$ENV\' \\/" 

sed ???? ??? config/gunicorn.service
cp gunicorn.service > /etc/systemd/system/
cp gunicorn.socket > /etc/systemd/system/

sed ??? ??? config/superdocs.site
cp superdocs.site > /etc/nginx/site-enabled/

systemctl daemon-reload
systemctl stop gunicorn
systemctl stop nginx
systemctl start gunicorn
systemctl start nginx

