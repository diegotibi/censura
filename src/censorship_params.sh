#!/usr/bin/env sh

ROOT_DIR="/root/censorship"
#ROOT_DIR=$(pwd)
PARSER_BIN="${ROOT_DIR}/censor_parser.py"
WGET_BIN=$(which wget)

BLACKHOLE="127.0.0.1" #Replace with the chosen IP address
OUTPUT_FORMAT="bind"  # Replace to "bind" or to "unbound"

TMP_DL_DIR="${ROOT_DIR}/tmp"

# Unbound params
CONF_DIR="/etc/bind/zones"
#CONF_DIR="${ROOT_DIR}/tmp"
