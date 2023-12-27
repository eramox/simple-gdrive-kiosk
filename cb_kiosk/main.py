import logging
import logging.handlers
import os
import sys

from kiosk_service import KioskService

logging.basicConfig(filename=f"kiosk.log")

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

def configure_logger():

	# Configuration of logging
	# https://stackoverflow.com/questions/41814988/share-python-logger-across-multiple-files
	format = '%(asctime)s - %(module)s - %(levelname)s - %(message)s'

	formatter = logging.Formatter(format)

	# Log to file
	fileHandler = logging.FileHandler("kiosk.log")
	fileHandler.setFormatter(formatter)
	log.addHandler(fileHandler)

	# Log to shell
	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(formatter)
	log.addHandler(consoleHandler)

def process_args() -> str:
	'''
	The only input we expect is one parameter which is the link to the file storing
	the file to display
	'''

	nb_args = len(sys.argv)

	if nb_args > 1:
		version_share_link = sys.argv[1]
		log.info(f"Using the version file {version_share_link}")

		return version_share_link
	else:
		raise ValueError(f"Missing link on version file")

if __name__ == "__main__":
	configure_logger()

	version_share_link = process_args()

	service = KioskService(version_share_link, logger=log)

	try:
		service.start_server()

		log.debug(f"Running main loop")
		service.loop()
	except KeyboardInterrupt:
		log.error("ctrl+c pressed")
	finally:
		service.stop_server()

	log.warning(f"out of the main loop")
