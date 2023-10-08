import logging
import logging.handlers
import os
import sys
import signal

from kiosk_service import KioskService

# Configuration of logging
# https://stackoverflow.com/questions/41814988/share-python-logger-across-multiple-files
format = '%(asctime)s - %(module)s - %(levelname)s - %(message)s'
logging.basicConfig(filename=f"kiosk.log")

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(format)

fileHandler = logging.FileHandler("kiosk.log")
fileHandler.setFormatter(formatter)
log.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
log.addHandler(consoleHandler)

if __name__ == "__main__":
    nb_args = len(sys.argv)

    if nb_args > 1:
        version_share_link = sys.argv[1]
        log.info(f"Using the version file {version_share_link}")
    else:
        log.error(f"Missing link on version file")
        exit(1)

    # if nb_args > 2:
    #     new_root_dir = sys.argv[2]
    #     log.info(f"Chnaging root to new directory: {new_root_dir}")
    #     os.chdir(new_root_dir)

    service = KioskService(version_share_link, logger=log)

    def signal_term_handler(signal, frame):
        print('got SIGTERM')
        service.stop_server()
 
    signal.signal(signal.SIGTERM, signal_term_handler)

    ret = 0
    try:
        service.start_server()
        log.debug(f"Running main loop")
        service.loop()
        a = 1
        while True:
            a = a + 1
    except KeyboardInterrupt:
        log.error("ctrl+c pressed")
        ret = 1
    finally:
        service.stop_server()

    log.warning(f"out of the main loop")
    sys.exit(ret)
