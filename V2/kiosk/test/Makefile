
all: test

venv:
	python3 -m venv venv
	. ./venv/bin/activate && pip3 install google-api-python-client oauth2client PyYAML pillow python-pptx

test: venv start

start: venv
	. ./venv/bin/activate && python3 ../kiosk.py

clean:
	rm -Rf venv
