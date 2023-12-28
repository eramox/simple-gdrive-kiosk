#!/bin/sh

set -ex

THIS_SCRIPT_DIR="$(realpath "$(dirname "$0" )" )"

KIOSK_DIR="$(realpath "${THIS_SCRIPT_DIR}/../../cb_kiosk" )"

# Note the version file must be edited to point to a ppt file
VERSION_FILE="${THIS_SCRIPT_DIR}/version.docx"
PPT_FILE="${THIS_SCRIPT_DIR}/abc.ppt"
VENV="${VENV:-}"

if [ ! -z "${VENV}" ];then
	. "${VENV}/bin/activate"
fi

python3 -c "from docx import Document;d = Document(\"${VERSION_FILE}\");d.paragraphs[0].text = \"${PPT_FILE}\";d.save(\"${VERSION_FILE}\")"

python3 "${KIOSK_DIR}/main.py" "${VERSION_FILE}"
