#!/bin/bash

set -ex

# Ce script va automatiquement configurer la PI pour utilisation
# Par default le script va s'envoyer a la pi via ssh puis
# proceder a l'installation

# configuration
PI_USERNAME="pi"
PI_IP_ADDR="192.168.1.43"
PI_SSH_PORT="22"

EXCHANGE_PORT="26000"

USERNAME="eramox" # username on the computer
USER_IP_ADDR="88.170.53.149" # Public address
USER_SSH_PORT="22222" # Port of the SSH server

# Code

CUR_FILE="$(realpath "$0")"
CUR_FILENAME="$(basename "$0")"

SAMPLE_PPT="https://www.dickinson.edu/download/downloads/id/1076/sample_powerpoint_slides.pptx"

function verify_display () {
	local tmp_prez="cur.ppt"

	rm -f "${tmp_prez}"
	wget -O "${tmp_prez}" "${SAMPLE_PPT}"

	# Use the PI screen
	export DISPLAY=:0.0

	# Run the presentation
	soffice --show "${tmp_prez}"
}

function configure_reverse_ssh () {

	cat > "/etc/systemd/system/autossh.service" << EOF
[Unit]
Description=Keep a tunnel open on port 22
After=network.target
 
[Service]
# User=<PI_USERNAME>
User=${PI_USERNAME}
# ExecStart=/usr/bin/autossh -o ServerAliveInterval=60 -NR ${EXCHANGE_PORT}:localhost:${PI_SSH_PORT} -p ${USER_SSH_PORT} ${USERNAME}@${USER_IP_ADDR}
ExecStart=/usr/bin/autossh -o ServerAliveInterval=60 -NR 26000:localhost:22 -p 22222 eramox@88.170.53.149
Restart=on-failure
 
[Install]
WantedBy=multi-user.target
EOF

	sudo systemctl --now enable autossh.service

	sudo systemctl daemon-reload

	sudo systemctl restart "autossh"
}

function configure_ssh_key () {
	# Generate keys
	# https://stackoverflow.com/questions/43235179/how-to-execute-ssh-keygen-without-prompt
	ssh-keygen -t rsa -N '' -f "${HOME}/.ssh/id_rsa" <<< y

	ssh-copy-id -p "${USER_SSH_PORT}" "${USERNAME}@${USER_IP_ADDR}"
}

function verify_revert_ssh ()
{
	ls -al "${HOME}/.ssh/id_rsa"
	ls -al "/etc/systemd/system/autossh.service"

	sudo systemctl status "autossh"
}

_PACKAGES=(
	"byobu"
	"openjdk-8-jre-headless"
	"libreoffice-java-common"
	"libreoffice-impress"
	"autossh"
)
declare -a _PACKAGES

function verify_packages () {
	local package

	for package in "${_PACKAGES[@]}"; do
		dpkg -s "${package}"
	done
}

function install_packages () {
	sudo apt update
	sudo apt install -y "${_PACKAGES[*]}"
}

function local_install () {
	configure_ssh_key
	configure_reverse_ssh
	install_packages
}

function remote_install () {

	local remote_file="/home/${PI_USERNAME}/${CUR_FILENAME}"

	# Copy the file
	scp "${CUR_FILE}" "${}@@{}:${remote_file}"

	# Run the install
    ssh -p "${PI_SSH_PORT}" "${PI_USERNAME}@${PI_IP_ADDR}" \
    	"bash ${remote_file} local_install && bash ${remote_file} local_verify"
}

function local_verify () {
	verify_revert_ssh
	verify_packages
	verify_display
}

function remote_verify () {

	local remote_file="/home/${PI_USERNAME}/${CUR_FILENAME}"

	# Copy the file
	scp "${CUR_FILE}" "${PI_USERNAME}@${PI_IP_ADDR}:${remote_file}"

	# Run the install
    ssh -p "${EXCHANGE_PORT}" "${PI_USERNAME}@localhost" "bash ${remote_file} local_verify"
}

function main () {
	local mode="$1"

	if [ "${mode}" == "local_install" ];then
		local_install
	elif [ "${mode}" == "local_verify" ];then
		local_verify
	elif [ "${mode}" == "install" ];then
		remote_install
	elif [ "${mode}" == "verify" ];then
		remote_verify
	else
		echo "No command to execute"
		return 1
	fi
}

main "$@"
