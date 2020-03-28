#!/bin/bash -x
#

OS_NAME=`lsb_release -a 2>&1 | grep "Distributor ID" | awk -F: '{print $2}' | tr -d '\t'`
OS_VER=`lsb_release -a 2>&1 | grep "Release" | awk '{print $2}'`
HW_PLATFORM=`uname -i`
GCC_VER=`gcc -v 2>&1 | tail -1 | awk '{print $3}'`
GLIBC_VER=`ldd --version | head -1 | awk -F\) '{print $2}' | awk '{print $1}'`
PYTHON_VER=`python3 -V 2>&1 | awk '{print $2}'`
DJANGO_VER=`python3 -c 'import django; print(django.get_version())'`

PACKAGE="SuperDoCS"
VERSION=`grep VERSION sxtweb/version.py | awk -F\' '{print $2}'`
SITE=${PACKAGE}_${VERSION}
PRJ=${PACKAGE}

mkdir -p ../${SITE}
cd ../${SITE}
cp -rf ../sxtweb/* .
cp ../LICENSE ../README.md ../CHANGES.txt .
sed "s/^DEBUG\ =.*/DEBUG\ =\ False/" ../sxtweb/sxtweb/local.py > ./sxtweb/local.py

##########################################################################################
# docker related.
sed -i "s:^ENV prj .*:ENV prj ${PACKAGE}:g" Dockerfile
sed -i "s:^ENV ver .*:ENV ver ${VERSION}:g" Dockerfile
sed -i "s:^ENV prjroot .*:ENV prjroot /var/www/${PRJ}:g" Dockerfile

sed -i "s|sxt_vol:/var.*|sxt_vol:/var/www/${PRJ}/sxtweb|g" docker-compose.yml
sed -i "s|static_vol:/var.*|static_vol:/var/www/${PRJ}/static|g" docker-compose.yml
sed -i "s|media_vol:/var.*|media_vol:/var/www/${PRJ}/media|g" docker-compose.yml
sed -i "s|usercodes_vol:/var.*|usercodes_vol:/var/www/${PRJ}/xcalc/UserCodes|g" docker-compose.yml
sed -i "s|nginxconf_vol:/var.*|nginxconf_vol:/var/www/${PRJ}/config/nginx_conf.d|g" docker-compose.yml
sed -i "s|nginxconf_vol:/etc.*|nginxconf_vol:/etc/nginx/conf.d|g" docker-compose.yml
# docker related done.
##########################################################################################

python3 manage.py collectstatic --noinput

find . -name CVS -exec rm -rf {} \;
find . -name "*.pyc" -exec rm -rf {} \;
find . -name "*.so" -exec rm -rf {} \;
find . -name "*.o" -exec rm -rf {} \;
find . -name "*.c" -exec rm -rf {} \;
find . -name "__pycache__" -type d -delete
rm -rf etc scripts setup.py ssl_key_install.sh ssl_keygen.sh cleanup.sh

echo "PACKAGE GENERATING ENVIROMNENT " > PLATFORM
echo "" >> PLATFORM
echo "Operating System: ${OS_NAME} ${OS_VER}" >> PLATFORM
echo "HW Platform:      ${HW_PLATFORM}" >> PLATFORM
echo "GCC Version:      ${GCC_VER}" >> PLATFORM
echo "Glibc Version:    ${GLIBC_VER}" >> PLATFORM
echo "Python Version:   ${PYTHON_VER}" >> PLATFORM
echo "Django Version:   ${DJANGO_VER}" >> PLATFORM

cd ..
tar zcvf ${PACKAGE}_${VERSION}_${OS_NAME}_${OS_VER}_${HW_PLATFORM}.tar.gz ${SITE}

