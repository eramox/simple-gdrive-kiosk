
OUTD=$(OUTDIR)/kiosk

all: test

$(OUTD)/venv:
	mkdir -p $(OUTD)
	python3 -m venv $@
	. $@/bin/activate && pip3 install -r $(ROOT)/kiosk_requirements.txt

test: venv start

start: venv
	. $(OUTD)/venv/bin/activate && cd $(OUTD) && python3 $(ROOT)/kiosk.py

clean:
	rm -Rf $(OUTD)/venv
