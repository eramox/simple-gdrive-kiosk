import logging
import os
import sys

from kiosk_service import KioskService

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# async def main(version_share_link):
def main(version_share_link: str, python_env_path: str):
    # return await KioskService(version_share_link).loop()
    return KioskService(version_share_link, python_env_path).loop()


if __name__ == "__main__":
    link = sys.argv[1]

    if len(sys.argv) >= 3 and sys.argv[2] is not None:
        python_env_path = sys.argv[2]
    else:
        python_env_path = os.path.join(os.path.dirname(__file__), "venv")

    logger.info(f"Using the version file {link}")

    # asyncio.run(main(link))
    main(link, python_env_path)
