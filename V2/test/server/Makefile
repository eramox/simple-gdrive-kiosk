
all: test

venv:
	python3 -m venv venv
	. ./venv/bin/activate && pip3 install flask pyyaml flask-cors

test: venv
	. ./venv/bin/activate && bash test.sh

start: venv
	. ./venv/bin/activate && python3 ../server.py

clean:
	rm -Rf venv
