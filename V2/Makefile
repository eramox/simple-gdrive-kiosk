
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.PHONY: all start test clean

all:

start:
	# Expect OUTDIR to be set
	ROOT=$(ROOT_DIR) make -C start
	rm -Rf $(OUTDIR)

test:
	ROOT=$(ROOT_DIR) OUTDIR=$(PWD)/tmp make -C test
	make clean

clean:
	rm -Rf $(PWD)/tmp
