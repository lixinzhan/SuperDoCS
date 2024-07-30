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
CWD=$(pwd)
PRJ=$(basename $CWD)
ENV=$(pwd)/.venv

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
echo "CWD:     $CWD"
echo "PRJ:     $PRJ"
echo "ENV:     $ENV"
echo "HOST:    $HOSTNAME"
echo "IP:      $IP"
echo "USRID:   $USRID"
echo "GRPID:   $GRPID"
echo "USRNAME: $USRNAME"

echo
echo "Setup Infor for Web Service"
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
        sudo apt install -y $1 && echo "Package $1 installed!" || echo "Error in installing $1 !!"
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
sudo apt update
sudo apt upgrade -y


if $SETENV; then
    # install base packages
    install-package g++
    install-package gfortran
    install-package libjpeg-dev
    install-package python3-dev
    install-package python3-venv
    install-package python3-wheel

    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    deactivate
    echo "Setting up virtual environment done!"
    echo
fi

#
# Setup web service for grouping calculation
#

if $SETWEB; then
    echo "In setup web"
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

