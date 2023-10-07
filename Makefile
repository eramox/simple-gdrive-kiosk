
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
PROJ_ROOT := $(dir $(mkfile_path))

KIOSK_SERVICE=${PROJ_ROOT}/cb_kiosk/main.py

default: run

build:
	echo "Building"

setup:
	echo "Setuping"

test: setup
	echo "Testing"
	PROJ_ROOT=${PROJ_ROOT} KIOSK_SERVICE=${KIOSK_SERVICE} make -C test

run: setup
	echo "Running"
