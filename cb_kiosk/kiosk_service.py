import time
import logging
import docx2txt

from drive_file_downloader import DriveFileDownloader

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class KioskService:
	VERSION_FILE = "tmp_file.doc"
	PRESENTATION_FILE = "presentation.ppt"

	def __init__(self, share_link_published_version: str, delay: int = 10):
		""" Link to the file containing the share link of the presentation to use """
		self.log = logger
		
		self.link = share_link_published_version
		self.version_drive = DriveFileDownloader(share_link_published_version)
		self.last_link = None

		self.display_task = None
		
		self.delay = delay

	# async def loop(self):
	def loop(self):
		self.log.info(f"Startign main loop")

		while True:
			self.log.info(f"Checking if version file {self.link} changed")

			# Download file containing the link of the published presentation
			self.version_drive.download(self.VERSION_FILE)

			# Get the link of the presentation
			link_presentation = self.get_version_from_doc(self.VERSION_FILE)
			self.log.debug(f"Got presentation link {link_presentation}")

			if link_presentation != self.last_link:
				self.log.info(f"Found a new version: {link_presentation}")
				# if self.last_link is not None:
				# 	self.display_task.cancel()

				# self.display_task = asyncio.create_task(run_presentation)

			# await asyncio.sleep(delay)
			time.sleep(delay)

	def get_version_from_doc(self, doc: str) -> str:
		my_text = docx2txt.process(doc)
		return my_text

	# async def run_presentation(self):
	def run_presentation(self):
		""" Run with impressive """
		self.log.debug(f"Running the presentation")

		# # Download the presentation
		# presentation = DriveFileDownloader(share_link_published_version)

		# presentation.download(self.PRESENTATION_FILE)

		# # Run the presentation
		# self.run_presentation(self.PRESENTATION_FILE)
