#!/bin/bash
if [ "$#" -ne 1 ]; then
    echo "Usage ./gen_keys.sh <sensorid>"
    exit 1
fi

echo "$1"

cd $(dirname $0)
cd broker
mkdir -p keys
cd keys
openssl genrsa -out "$1_priv.pem" 2048
openssl rsa -in "$1_priv.pem" -outform PEM -pubout -out "$1_pub.pem"
