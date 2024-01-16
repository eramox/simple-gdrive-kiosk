#!/bin/sh

set -ex

THIS_SCRIPT_DIR="$(realpath "$(dirname "$0" )" )"

ROOT_DIR="$(realpath "${THIS_SCRIPT_DIR}/../../" )"
KIOSK_DIR="$(realpath "${ROOT_DIR}/cb_kiosk" )"

# Note the version file must be edited to point to a ppt file
VERSION_FILE="https://docs.google.com/document/d/11hGse_OyqGQiy3qAaDMSHnrFX0_YyG2o/edit?usp=drive_link&ouid=104564737776631583414&rtpof=true&sd=true"

echo "Running from dir ${PWD}"

# Set the path to the venv if it is not defined
if [ ! -n "${VENV}" ];then
	VENV=venv
fi

# Create the venv if it does not exists
if [ ! -d "${VENV}" ];then
	python3 -m venv "${VENV}"
fi

# Start the venv
. "${VENV}/bin/activate"

# Update the venv
pip install -r "${ROOT_DIR}/conf/requirements.txt"

# Echo print env
set

env

# Start the main script
python3 "${KIOSK_DIR}/main.py" "${VERSION_FILE}"
