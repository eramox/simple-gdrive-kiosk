#!/bin/bash

set -e

# Test script for the server

SERVER="http://127.0.0.1:5000"
TMP_FILE="out.json"

# Start server
export FLASK_APP="$(realpath ../server.py)"
# Run via flask to avoid flask start another process
flask run &

PID_SERVER="$!"
echo "Server started: ${PID_SERVER}"

function server_cleanup() {
	echo "Stopping server on PID ${PID_SERVER}"
	kill -9 "${PID_SERVER}"
}

function script_cleanup() {
	cp "images/slideshow.yaml.empty" "images/slideshow.yaml"
	server_cleanup
}

trap script_cleanup EXIT

sleep 2

function check_content() {
	local field="$1"
	local expected="$2"
	local file="$3"

	local content
	content="$(jq ".${field}" "${file}" )"

	if [ "${content}" == "${expected}" ];then
		echo "OK"
	else
		echo "FAIL: got ${content} when expecting ${expected}"
		exit 1
	fi
}

function check_ep() {
	local ep="$1"
	local field="$2"
	local expected="$3"
	local arg="$4"

	curl --silent --show-error  --output "${TMP_FILE}" "${SERVER}${ep}${arg}"

	check_content "${field}" "\"${expected}\"" "${TMP_FILE}"
	ret="$?"

	if [ "${ret}" == 0 ];then
		echo "OK"
	else
		echo "FAIL: ${ep} had failures"
		exit 1
	fi
}

# Test server

# Empty slideshow
cp "images/slideshow.yaml.empty" "images/slideshow.yaml"

# slideshow1

cp "images/slideshow1.yaml" "images/slideshow.yaml"
touch "images/refresh"
IMAGES=("slide1.jpeg" "slide2.jpeg")

# These are dependent
check_ep "/get_image" "name" "${IMAGES[0]}"
check_ep "/get_image" "name" "${IMAGES[1]}"

# These are independant
check_ep "/get_duration" "duration" "5"  "/${IMAGES[0]}"
check_ep "/get_duration" "duration" "10" "/${IMAGES[1]}"


# slideshow2

cp "images/slideshow2.yaml" "images/slideshow.yaml"
touch "images/refresh"
IMAGES=("slide3.jpeg" "slide4.jpeg")

# These are dependent
check_ep "/get_image" "name" "${IMAGES[0]}"
check_ep "/get_image" "name" "${IMAGES[1]}"

# These are independant
check_ep "/get_duration" "duration" "3"  "/${IMAGES[0]}"
check_ep "/get_duration" "duration" "7" "/${IMAGES[1]}"

rm "${TMP_FILE}"

echo "SUCCESS"
