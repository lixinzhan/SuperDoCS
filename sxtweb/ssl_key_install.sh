#!/bin/sh
#

SUPERDOCS_SITE='superdocs.ca'

# install the private key and certificate to /etc/ssl/
sudo cp OpenSSL/server.crt /etc/ssl/certs/${SUPERDOCS_SITE}.crt
sudo cp OpenSSL/server.key /etc/ssl/private/${SUPERDOCS_SITE}.key
sudo chown root:root /etc/ssl/certs/${SUPERDOCS_SITE}.crt
sudo chown root:ssl-cert /etc/ssl/private/${SUPERDOCS_SITE}.key
sudo chmod 644 /etc/ssl/certs/${SUPERDOCS_SITE}.crt
sudo chmod 640 /etc/ssl/private/${SUPERDOCS_SITE}.key
# sudo rm -rf OpenSSL
