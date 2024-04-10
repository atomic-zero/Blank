#!/bin/bash

# Install Node.js and npm
apt upgrade && apt update
apt install openssl-tool
apt-get update
apt-get install -y nodejs npm

# Install bash-obfuscate npm package
npm install -g bash-obfuscate
pip install requests uuid rich

