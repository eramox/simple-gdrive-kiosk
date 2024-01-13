#!/bin/sh

set -ex

THIS_SCRIPT_DIR="$(realpath "$(dirname "$0" )" )"

ROOT_DIR="$(realpath "${THIS_SCRIPT_DIR}/../../" )"
KIOSK_DIR="$(realpath "${ROOT_DIR}/cb_kiosk" )"

# Note the version file must be edited to point to a ppt file
VERSION_FILE="https://docs.google.com/document/d/11hGse_OyqGQiy3qAaDMSHnrFX0_YyG2o/edit?usp=drive_link&ouid=104564737776631583414&rtpof=true&sd=true"
VENV="${VENV:-}"

if [ -n "${VENV}" ];then
	. "${VENV}/bin/activate"
else
	rm -Rf venv
	python3 -m venv venv
	. ./venv/bin/activate
	pip install -r "${ROOT_DIR}/conf/requirements.txt"
fi

# Echo print env
set

env

python3 "${KIOSK_DIR}/main.py" "${VERSION_FILE}"
