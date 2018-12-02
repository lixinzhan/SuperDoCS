#!/bin/sh
#

mkdir -p OpenSSL

# Generate a private key
openssl genrsa -des3 -out OpenSSL/server.key 4096

# Gernerate a CSR (Certificate Signing Request)
openssl req -new -key OpenSSL/server.key -out OpenSSL/server.csr

# Remove passphrase from key to make sure server auto reboot
cp OpenSSL/server.key OpenSSL/server.key.orig
openssl rsa -in OpenSSL/server.key.orig -out OpenSSL/server.key

# Generate a Self-Signed Certificate for 1 year
openssl x509 -req -days 365 -in OpenSSL/server.csr -signkey OpenSSL/server.key -out OpenSSL/server.crt

