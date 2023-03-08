import logging
import asyncio
import sys

from kiosk_service import KioskService

logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# async def main(version_share_link):
def main(version_share_link):
	# return await KioskService(version_share_link).loop()
	return KioskService(version_share_link).loop()

if __name__ == "__main__":
	link = sys.argv[1]

	logger.info(f"Using the version file {link}")

	# asyncio.run(main(link))
	main(link)