#!/usr/bin/env bash

. "$(dirname "${0}")/censorship_params.sh"

LIST_URL="https://www1.adm.gov.it/files_siti_inibiti_tabacchi/elenco_siti_inibiti.txt"
LIST_FILE="${TMP_DL_DIR}/blacklist_admt.txt"
LIST_OUT="${CONF_DIR}/db.blacklist_admt.conf"
LIST_TYPE="admt"
BLACKHOLE="217.175.53.228"

WGET_CERTS=""
WGET_OPTS="${WGET_CERTS} --no-check-certificate"

if [ ! -d "${TMP_DL_DIR}" ]
then
   echo "Missing temp download dir ${TMP_DL_DIR}"
   mkdir "${TMP_DL_DIR}"
fi

PARSER_OPTS="-i ${LIST_FILE} -o ${LIST_OUT} -f ${OUTPUT_FORMAT} -d ${LIST_TYPE} -b ${BLACKHOLE}"

##############################################################################
# be verbose when stdout is a tty
if [ ! -t 0 ]; then
  WGET_OPTS="$WGET_OPTS -q"
fi

## downloading ###############################################################
${WGET_BIN} ${WGET_OPTS} ${LIST_URL} -O ${LIST_FILE}

## parsing ###################################################################
${PARSER_BIN} ${PARSER_OPTS}

## delete tmp junk ###########################################################
rm "${LIST_FILE}"