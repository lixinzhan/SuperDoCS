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
PKGTIME=$(date +"%Y-%m-%d %H:%M:%S")

mkdir -p ../${SITE}
cd ../${SITE}
cp -rf ../sxtweb/* .
cp ../LICENSE ../README.md ../CHANGES.txt .
sed "s/^DEBUG\ =.*/DEBUG\ =\ False/" ../sxtweb/sxtweb/local.py > ./sxtweb/local.py

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
echo "" >> PLATFORM
echo "Package Generation Time: $(PKGTIME)" >> PLATFORM

cd ..
tar zcvf ${PACKAGE}_${VERSION}_${OS_NAME}_${OS_VER}_${HW_PLATFORM}.tar.gz ${SITE}

