#!/bin/sh

set -ex

# The file uninstall.sh is a symbolink link on install.sh
# to have both function in the same file

SCRIPT_NAME="$(basename "$0" )"

THIS_SCRIPT_DIR="$(realpath "$(dirname "$0" )" )"

SERVICE_NAME="kiosk"
SERVICE_FILE="${SERVICE_NAME}.service"

INSTALL_DIR="${HOME}/.config/systemd/user"

if [ "$SCRIPT_NAME" == "install.sh" ];then

echo "Install the service"

echo "Copy service file"
mkdir -p "${INSTALL_DIR}"
cp "${THIS_SCRIPT_DIR}/${SERVICE_FILE}" "${INSTALL_DIR}/${SERVICE_FILE}"

echo "Enable the service"
systemctl --user enable "${SERVICE_NAME}"

echo "Start the service"
systemctl --user start ${SERVICE_NAME}

echo "Status of the service"
# Pipe to cat to avoid paged output
systemctl --user status "${SERVICE_NAME}" | cat

echo "log of service: journalctl --user -u ${SERVICE_NAME} -b [-f]"

elif [ "$SCRIPT_NAME" == "uninstall.sh" ]; then

	echo "Uninstalling the service"

	echo "Stop the service"
	systemctl --user stop "${SERVICE_NAME}"

	echo "Disable the service"
	systemctl --user disable "${SERVICE_NAME}"

	echo "Delete service file"
	rm -f "${INSTALL_DIR}/${SERVICE_FILE}"

else
	echo "Do not know what to do"
	exit 4
fi

echo "SUCCESS"
