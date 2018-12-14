#!/bin/bash
#

# Get the current directory and project.
CWD=$(pwd)
PRJ=$(basename $CWD)
ENV=$(pwd)/.env
PORT=8000
HOSTNAME=$(ip route get 1 | awk '{print $7;exit}' | head -1)
UID=$(id -u)
GID=$(id -g)

echo CWD:  $CWD
echo PRJ:  $PRJ
echo ENV:  $ENV
echo PORT: $PORT
echo HOST: $HOSTNAME
echo UID:  $UID
echo GID:  $GID

# add universe.
sudo add-apt-repository universe


# check if packages python3-dev and nginx are installed.
if [[ $(dpkg -l python3-dev | grep '^ii') = *python3-dev* ]]; then
    echo "python3-dev was previously installed!"
else
    echo sudo apt install -y python3-dev
fi

if [[ $(dpkg -l nginx | grep '^ii') == *python3-venv* ]]; then
    echo "python3-venv was previously installed!"
else
    sudo apt install -y python3-venv
fi

if [[ $(dpkg -l nginx | grep '^ii') == *nginx* ]]; then
    echo "nginx was previously installed!"
else
    sudo apt install -y nginx
fi


# seup virtual environment
sudo chown -R $UID:$GID .
python3 -m venv .env
source .env/bin/activate
pip install -r config/requirements.txt
deactivate
echo "Setting up virtual environment done!"

# stop services gunicorn and nginx
sudo systemctl stop gunicorn.socket
sudo systemctl stop nginx
echo "Services gunicorn and nginx stopped!"

#
# setup services for gunicorn and nginx.
#

# gunicorn service
sed -i "s:^WorkingDirectory=.*:WorkingDirectory=$CWD:g" config/gunicorn.service
sed -i "s:^ExecStart=.*:ExecStart=$ENV/bin/gunicorn \\\:g" config/gunicorn.service
sed -i "s:access-logfile.*:access-logfile $CWD/log/access.log \\\:g" config/gunicorn.service
sed -i "s:error-logfile.*:error-logfile $CWD/log/error.log \\\:g" config/gunicorn.service
sudo rm -f /etc/systemd/system/gunicorn.socket
sudo rm -f /etc/systemd/system/gunicorn.service
sudo ln -s $CWD/config/gunicorn.socket  /etc/systemd/system/
sudo ln -s $CWD/config/gunicorn.service /etc/systemd/system/

sed -i "s:listen.*:listen $PORT;:g" config/superdocs_nginx.conf
sed -i "s:server_name.*:server_name $HOSTNAME 127.0.0.1;:g" config/superdocs_nginx.conf
sed -i "s:alias.*media;:alias $CWD/media/;:g" config/superdocs_nginx.conf
sed -i "s:alias.*static;:alias $CWD/static/;:g" config/superdocs_nginx.conf
sudo rm -f /etc/nginx/sites-enabled/default
sudo rm -f /etc/nginx/sites-enabled/superdocs_nginx.conf
sudo rm -f /etc/nginx/sites-available/superdocs_nginx.conf
sudo ln -s $CWD/config/superdocs_nginx.conf /etc/nginx/sites-enabled/
sudo ln -s $CWD/config/superdocs_nginx.conf /etc/nginx/sites-available/

sudo chown -R www-data:www-data $CWD

sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn.socket
echo "Services gunicorn started!"

sudo systemctl start nginx
sudo systemctl enable nginx
echo "Services nginx started!"

echo
echo "Web server for SuperDoCS done! Please check by visiting http://$HOSTNAME:8000/ :)"
echo

