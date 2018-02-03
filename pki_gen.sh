#!/bin/bash
# Generate RSA private key
openssl genrsa -aes256 -out private.pem 4096

# Generate public key with the previous generated private key
openssl rsa -in private.pem -outform PEM -pubout -out public.pem