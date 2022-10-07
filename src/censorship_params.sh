#!/usr/bin/env bash

ROOT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
PARSER_BIN="${ROOT_DIR}/censor_parser.py"
WGET_BIN=$(which wget)

BLACKHOLE="127.0.0.1" #Replace with the chosen IP address
OUTPUT_FORMAT="bind"  # Replace to "bind" or to "unbound"

TMP_DL_DIR="${ROOT_DIR}/tmp"

# Unbound params
if [ "$OUTPUT_FORMAT" = "bind" ]
then
  CONF_DIR="/etc/bind/zones"
  /usr/bin/systemctl reload bind9
else
  # shellcheck disable=SC2034
  CONF_DIR="/usr/local/etc/unbound"
fi
