#!/bin/sh

set -ex

THIS_SCRIPT_DIR="$(realpath "$(dirname "$0" )" )"

KIOSK_DIR="$(realpath "${THIS_SCRIPT_DIR}/../../cb_kiosk" )"

# Note the version file must be edited to point to a ppt file
VERSION_FILE="https://docs.google.com/document/d/11hGse_OyqGQiy3qAaDMSHnrFX0_YyG2o/edit?usp=drive_link&ouid=104564737776631583414&rtpof=true&sd=true"
VENV="${VENV:-}"

if [ ! -z "${VENV}" ];then
	. "${VENV}/bin/activate"
fi

# Echo print env
set

env

python3 "${KIOSK_DIR}/main.py" "${VERSION_FILE}"
