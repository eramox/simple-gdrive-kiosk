
OUTD=$(OUTDIR)/kiosk

.PHONY: clean

all: test

$(OUTD)/venv:
	mkdir -p $(OUTD)
	python3 -m venv $@
	. $@/bin/activate && pip3 install -r $(ROOT)/code/server_requirements.txt

test: $(OUTD)/venv
	. $</bin/activate && ROOT=$(ROOT) OUTDIR=$(OUTDIR) bash test.sh

start: $(OUTD)/venv
	. $</bin/activate && cd $(OUTD) && python3 $(ROOT)/code/server.py

clean:
	rm -Rf venv
