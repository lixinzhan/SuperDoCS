#!/bin/bash
#

#
# handling command line switches.
#

usage() 
{ 
    echo "Usage: $0 [-a] [-e] [-w] [-s] [-h]" 1>&2 
    echo "    -a    setup all: environment, web service, and security"
    echo "    -e    setup development environment"
    echo "    -w    setup web service"
    echo "    -s    setup security: firewall and system hardening"
    echo "    -h    display this help"
    echo
    exit 0 
}

SETALL=false
SETSEC=false
SETWEB=false
SETENV=false
OPTSTRING="aewsh"
while getopts ${OPTSTRING} opt; do
    case ${opt} in
        a)
	    SETALL=true
	    SETWEB=true
	    SETENV=true
	    SETSEC=true
	    ;;
        e)
	    SETENV=true
	    ;;
        w)
        SETENV=true
	    SETWEB=true
	    ;;
        s)
	    SETSEC=true
	    ;;
        h)
	    usage
	    exit 0
            ;;
        ?)
            echo "Invalid option: -${OPTARG}."
	    echo
	    usage
            exit 1
            ;;
    esac
done

if [ $# = 0 ]; then
    usage
fi
 
# Get the current directory and project info.
PRJDIR=$(pwd)
PRJ=$(basename $PRJDIR)
ENV=$PRJDIR/.venv

# info for web service setup
WWWPORT=8000 		# `grep WWWPORT settings.py | awk -F= '{print$2}' | xargs`
WWWGRP="www-data" 	#`grep WWWGRP settings.py | awk -F= '{print$2}' | xargs`

# system info
IP=$(ip route get 1 | awk '{print $7;exit}' | head -1)
FQDN=$(hostname -f)
HOSTNAME=$(hostname -s)
USRID=$(id -u)
GRPID=$(id -g)
USRNAME=$(whoami)

echo "System Environment" 
echo "PRJDIR:  $PRJDIR"
echo "PRJ:     $PRJ"
echo "ENV:     $ENV"
echo "HOST:    $HOSTNAME"
echo "IP:      $IP"
echo "USRID:   $USRID"
echo "GRPID:   $GRPID"
echo "USRNAME: $USRNAME"

echo
echo "Setup Info for Web Service"
echo "WWWPORT: $WWWPORT"
echo "WWWGRP:  $WWWGRP"


#
# check OS family. (command/type/hash)
#

if command -v dpkg > /dev/null 2>&1; then
    OSFAMILY="DEBIAN"
elif command -v zypper > /dev/null 2>&1; then
    OSFAMILY="SUSE"
elif command -v pacman > /dev/null 2>&1; then
    OSFAMILY="ARCH"
elif command -v rpm > /dev/null 2>&1; then
    OSFAMILY="REDHAT"
else
    OSFAMILY="UNKNOWN"
fi

if [ $OSFAMILY == "DEBIAN" ]; then
    echo OS: $(cat /etc/os-release | grep PRETTY_NAME | awk -F \" '{print $2}')
    echo
else
    echo "OS family $OSFAMILY not supported yet!"
    exit 1
fi

# function to check if a packgage installed. If not, install it.
install-package() 
{
    if [[ $(dpkg -l $1 | grep '^ii' | awk '{print $2}') = $1 ]]; then
        echo "$1 exists!"
    else
	echo "Install package $1 ..."
        sudo apt-get install -y $1 && echo "Package $1 installed!" || echo "Error in installing $1 !!"
    fi
    echo
}

# function for service stop if active
stop-service()
{
    systemctl is-active --quiet $1 \
        && sudo systemctl stop $1 \
        && echo "Service $1 stopped!"
}
# function to start a system service
start-service()
{
    systemctl is-active --quiet $1 && sudo systemctl stop $1 
    sudo systemctl start $1 \
        && echo "Service $1 start successfully!" \
        || echo "Service $1 start failed!"
}


# add universe and update the sytem to the latest.
sudo add-apt-repository -y universe
sudo systemctl daemon-reload
sudo apt-get update
sudo apt-get upgrade -y


if $SETENV; then
    # install base packages
    install-package g++
    install-package gfortran
    install-package libjpeg-dev
    install-package python3-dev
    install-package python3-venv
    install-package python3-wheel

    python3 -m venv $ENV
    source $ENV/bin/activate
    pip install --upgrade pip
    pip install -r $PRJDIR/config/requirements.txt
    deactivate
    echo "Setting up virtual environment done!"
    echo
fi

#
# Setup web service for grouping calculation
#

if $SETWEB; then
    echo
    echo "In Web Setup"
    echo

    install-package nginx

    source $ENV/bin/activate

    # No debug mode
    sed -i "s/^DEBUG\ =.*/DEBUG\ =\ False/" sxtweb/local.py

    # collect static files
    python3 manage.py collectstatic --noinput

    # stop web services
    stop-service gunicorn.socket
    stop-service gunicorn.service
    stop-service nginx.service

    #
    # Setup services for gunicorn and nginx
    #

    # gunicorn service
    echo "Configure gunicorn service ..."
    SYSDIR=/etc/systemd/system
    sudo cp -rf $PRJDIR/config/gunicorn.service $SYSDIR
    sudo cp -rf $PRJDIR/config/gunicorn.socket  $SYSDIR
    sudo sed -i "s:^User=.*:User=$USRNAME:g" $SYSDIR/gunicorn.service
    sudo sed -i "s:^WorkingDirectory=.*:WorkingDirectory=$PRJDIR:g" $SYSDIR/gunicorn.service
    sudo sed -i "s:^ExecStart=.*:ExecStart=$ENV/bin/gunicorn \\\:g" $SYSDIR/gunicorn.service
    sudo sed -i "s:access-logfile.*:access-logfile $PRJDIR/log/access.log \\\:g" $SYSDIR/gunicorn.service
    sudo sed -i "s:error-logfile.*:error-logfile $PRJDIR/log/error.log \\\:g" $SYSDIR/gunicorn.service

    # nginx service
    echo "Configure nginx service ..."
    NGAVL=/etc/nginx/sites-available
    NGENB=/etc/nginx/sites-enabled
    echo "NGAVL: $NGAVL"
    echo "NGENB: $NGENB"
    sudo cp -rf $PRJDIR/config/superdocs_nginx.conf $NGAVL/
    sudo rm -rf $NGENB/superdocs_nginx.conf > /dev/null 2>&1
    sudo ln -s $NGAVL/superdocs_nginx.conf $NGENB/
    sudo sed -i "s:listen.*:listen $WWWPORT;:g" $NGAVL/superdocs_nginx.conf
    sudo sed -i "s:server_name.*:server_name $IP 127.0.0.1;:g" $NGAVL/superdocs_nginx.conf
    sudo sed -i "s:alias.*media/;:alias $PRJDIR/media/;:g" $NGAVL/superdocs_nginx.conf
    sudo sed -i "s:alias.*static/;:alias $PRJDIR/static/;:g" $NGAVL/superdocs_nginx.conf
    sudo rm -f $NGENB/default

    sudo chown -R $USRNAME:$WWWGRP $PRJDIR

    sudo systemctl daemon-reload
    sudo systemctl enable gunicorn.service
    sudo systemctl enable nginx

    start-service gunicorn.socket
    start-service gunicorn.service
    start-service nginx.service

    echo
    echo "Web server for SuperDoCS done! Please check by visiting http://$IP:$WWWPORT/ :)"
    echo

fi  # web


#
# setup firewall and system hardening.
#

if $SETSEC; then

    echo
    echo "Firewall setup and system hardening goes here!"
    echo

    install-package ufw
    sudo ufw enable
    sudo ufw allow $WWWPORT
    sudo ufw reload
    echo
    sudo ufw status verbose

fi  # sec

