


GOOGLE_DRIVE_CONTENT_FILE=https://docs.google.com/document/d/11hGse_OyqGQiy3qAaDMSHnrFX0_YyG2o/edit?usp=drive_link&ouid=104564737776631583414&rtpof=true&sd=true

default: start_test

${OUT_DIR}/venv/done: ${PROJ_ROOT}/conf/requirements.txt
	python3 -m venv ${OUT_DIR}/venv
	. ${OUT_DIR}/venv/bin/activate
	pip install -r ${PROJ_ROOT}/conf/requirements.txt
	touch ${OUT_DIR}/venv/done

setup_env: ${OUT_DIR}/venv/done

.PHONY: start_test
start_test: setup_env
	cp "${PROJ_ROOT}/conf/script_split_pdf_page.sh" "${OUT_DIR}/pdfsplit.sh"
	chmod +x "${OUT_DIR}/pdfsplit.sh"
	cd ${OUT_DIR}
	python3 ${KIOSK_SERVICE} ${GOOGLE_DRIVE_CONTENT_FILE}
