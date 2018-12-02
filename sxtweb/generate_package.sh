#!/bin/bash
#

OS_NAME=`lsb_release -a 2>&1 | grep "Distributor ID" | awk -F: '{print $2}' | tr -d '\t'`
OS_VER=`lsb_release -a 2>&1 | grep "Release" | awk '{print $2}'`
HW_PLATFORM=`uname -i`
GCC_VER=`gcc -v 2>&1 | tail -1 | awk '{print $3}'`
GLIBC_VER=`ldd --version | head -1 | awk -F\) '{print $2}' | awk '{print $1}'`
PYTHON_VER=`python -V 2>&1 | awk '{print $2}'`
#CYTHON_VER=`cython -V 2>&1 | awk '{print $3}'`
DJANGO_VER=`python -c 'import django; print django.get_version()'`

PACKAGE="SuperDoCS"
VERSION=`grep VERSION sxtweb/version.py | awk -F\' '{print $2}'`
SITE=${PACKAGE}_${VERSION}

mkdir -p ${SITE}
mkdir -p ${SITE}/sxtweb
mkdir -p ${SITE}/protocols/AAPM_TG61/Data
mkdir -p ${SITE}/tegmine/templatetags

#echo "Enter the INSTITUTION_CODE this build is for: "
#read institut
#sed "s/^INSTITUTION_CODE\ =.*/INSTITUTION_CODE\ =\ \'${institut}\'/" tegmine/models.py > tegmine/models_2build.py

# prepare binary and static files
python setup.py build_ext --inplace 
python manage.py collectstatic

cp -rf etc media static templates ${SITE}
cp -rf manage.py ${SITE}
cp -rf tegmine/UserCodes ${SITE}/tegmine/
cp -rf tegmine/static ${SITE}/tegmine/
cp -rf tegmine/templatetags ${SITE}/tegmine/
cp -rf protocols/AAPM_TG61/Data ${SITE}/protocols/AAPM_TG61/

cp sxtweb/__init__.py ${SITE}/sxtweb/
#cp sxtweb/settings.py ${SITE}/sxtweb/
sed "s/^DEBUG\ =.*/DEBUG\ =\ False/" sxtweb/settings.py > ${SITE}/sxtweb/settings.py
cp sxtweb/urls.py ${SITE}/sxtweb/
cp sxtweb/wsgi.py ${SITE}/sxtweb/
cp sxtweb/sxt.db ${SITE}/sxtweb/
mv sxtweb/*.so ${SITE}/sxtweb/

cp tegmine/__init__.py ${SITE}/tegmine/
mv tegmine/*.so ${SITE}/tegmine/

mv protocols/AAPM_TG61/*.so ${SITE}/protocols/AAPM_TG61/
cp protocols/AAPM_TG61/__init__.py ${SITE}/protocols/AAPM_TG61/
cp protocols/__init__.py ${SITE}/protocols/

cp ssl_keygen.sh ssl_key_install.sh ${SITE}


find ${SITE} -name CVS -exec rm -rf {} \;
find ${SITE} -name "*.pyc" -exec rm -rf {} \;

echo "PACKAGE BUILT ENVIROMNENT " > ${SITE}/PLATFORM
echo "" >> ${SITE}/PLATFORM
echo "Operating System: ${OS_NAME} ${OS_VER}" >> ${SITE}/PLATFORM
echo "HW Platform:      ${HW_PLATFORM}" >> ${SITE}/PLATFORM
echo "GCC Version:      ${GCC_VER}" >> ${SITE}/PLATFORM
echo "Glibc Version:    ${GLIBC_VER}" >> ${SITE}/PLATFORM
echo "Python Version:   ${PYTHON_VER}" >> ${SITE}/PLATFORM
#echo "Cython Version:   ${CYTHON_VER}" >> ${SITE}/PLATFORM
#echo "Django Version:   ${DJANGO_VER}" >> ${SITE}/PLATFORM

tar zcvf ${PACKAGE}_${VERSION}_${OS_NAME}_${OS_VER}_${HW_PLATFORM}.tar.gz ${SITE}

