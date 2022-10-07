#!/usr/bin/env bash

. "$(dirname "${0}")/censorship_params.sh"

#"${ROOT_DIR}"/update_cncpo.sh
"${ROOT_DIR}"/update_aams.sh
"${ROOT_DIR}"/update_admt.sh
"${ROOT_DIR}"/update_manual.sh

if [ "$OUTPUT_FORMAT" = "bind" ]
then
  /usr/bin/systemctl reload bind9
else
  /usr/local/etc/rc.d/unbound reload
fi