import logging
import os
import sys

from kiosk_service import KioskService

logging.basicConfig()

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

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

    KioskService(version_share_link).loop()
