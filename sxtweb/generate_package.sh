#!/bin/bash
#

OS_NAME=`lsb_release -a 2>&1 | grep "Distributor ID" | awk -F: '{print $2}' | tr -d '\t'`
OS_VER=`lsb_release -a 2>&1 | grep "Release" | awk '{print $2}'`
HW_PLATFORM=`uname -i`
GCC_VER=`gcc -v 2>&1 | tail -1 | awk '{print $3}'`
GLIBC_VER=`ldd --version | head -1 | awk -F\) '{print $2}' | awk '{print $1}'`
PYTHON_VER=`python3 -V 2>&1 | awk '{print $2}'`
#CYTHON_VER=`cython3 -V 2>&1 | awk '{print $3}'`
DJANGO_VER=`python3 -c 'import django; print(django.get_version())'`

PACKAGE="SuperDoCS"
VERSION=`grep VERSION sxtweb/version.py | awk -F\' '{print $2}'`
SITE=${PACKAGE}_${VERSION}
PRJ=${PACKAGE}

mkdir -p ${SITE}
mkdir -p ${SITE}/sxtweb
mkdir -p ${SITE}/protocols/TG61/Data
mkdir -p ${SITE}/xcalc/templatetags
mkdir -p ${SITE}/common
mkdir -p ${SITE}/xcalib
mkdir -p ${SITE}/resources

#echo "Enter the INSTITUTION_CODE this build is for: "
#read institut
#sed "s/^INSTITUTION_CODE\ =.*/INSTITUTION_CODE\ =\ \'${institut}\'/" xcalc/models.py > xcalc/models_2build.py

# prepare binary and static files
python3 setup.py build_ext --inplace 
python3 manage.py collectstatic

cp -rf media static templates ${SITE}
cp -rf manage.py ${SITE}
cp -rf www-configure.sh ${SITE}
cp -rf ../LICENSE ${SITE}

##########################################################################################
#
# docker related.
#
sed -i "s:^ENV prj .*:ENV prj ${PACKAGE}:g" Dockerfile
sed -i "s:^ENV ver .*:ENV ver ${VERSION}:g" Dockerfile
sed -i "s:^ENV prjroot .*:ENV prjroot /var/www/${PRJ}:g" Dockerfile
cp -rf Dockerfile ${SITE}

sed -i "s|sxt_vol:/var.*|sxt_vol:/var/www/${PRJ}/sxtweb|g" docker-compose.yml
sed -i "s|static_vol:/var.*|static_vol:/var/www/${PRJ}/static|g" docker-compose.yml
sed -i "s|media_vol:/var.*|media_vol:/var/www/${PRJ}/media|g" docker-compose.yml
sed -i "s|usercodes_vol:/var.*|usercodes_vol:/var/www/${PRJ}/xcalc/UserCodes|g" docker-compose.yml
sed -i "s|nginxconf_vol:/var.*|nginxconf_vol:/var/www/${PRJ}/config/nginx_conf.d|g" docker-compose.yml
sed -i "s|nginxconf_vol:/etc.*|nginxconf_vol:/etc/nginx/conf.d|g" docker-compose.yml
cp -rf docker-compose.yml ${SITE}
#
# docker related done.
#
##########################################################################################

cp -rf config ${SITE}
cp -rf xcalc/UserCodes ${SITE}/xcalc/
cp -rf xcalc/static ${SITE}/xcalc/
cp -rf xcalc/templatetags ${SITE}/xcalc/
cp -rf protocols/TG61/Data ${SITE}/protocols/TG61/

cp sxtweb/__init__.py ${SITE}/sxtweb/
cp sxtweb/settings.py ${SITE}/sxtweb/
sed "s/^DEBUG\ =.*/DEBUG\ =\ False/" sxtweb/local.py > ${SITE}/sxtweb/local.py
cp sxtweb/urls.py ${SITE}/sxtweb/
cp sxtweb/wsgi.py ${SITE}/sxtweb/
cp sxtweb/sxt.db ${SITE}/sxtweb/
cp sxtweb/*.so ${SITE}/sxtweb/

cp common/__init__.py ${SITE}/common/
cp common/*.so ${SITE}/common/

cp xcalc/__init__.py ${SITE}/xcalc/
cp xcalc/*.so ${SITE}/xcalc/

cp xcalib/__init__.py ${SITE}/xcalib/
cp xcalib/*.so ${SITE}/xcalib/

cp resources/__init__.py ${SITE}/resources/
cp resources/*.so ${SITE}/resources/

cp protocols/TG61/*.so ${SITE}/protocols/TG61/
cp protocols/TG61/__init__.py ${SITE}/protocols/TG61/
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

