import logging
import os
import subprocess
import tempfile
import time
from typing import List

from odf import opendocument

from drive_file_downloader import DriveFileDownloader

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class KioskService:
	VERSION_FILE = "tmp_file.doc"
	PRESENTATION_FILE = "presentation.ppt"
	CONVERT_TYPE = "pdf"
	DISPLAY_FILE = "presentation.pdf"

	def __init__(self, share_link_published_version: str, delay_seconds: int = 10):
		""" Link to the file containing the share link of the presentation to use """
		self.log = logger

		# Variables related to the links
		self.link: str = share_link_published_version
		self.version_drive: DriveFileDownloader = DriveFileDownloader(share_link_published_version)
		self.last_link: str = ""
		
		self.delay_seconds: int = delay_seconds

		# Create a temporary directory to store files downloaded
		# self.tdir = tempfile.TemporaryDirectory().name
		self.tdir = os.getcwd()

		self.version_file: str = os.path.join(self.tdir, self.VERSION_FILE)
		self.presentation_file: str = os.path.join(self.tdir, self.PRESENTATION_FILE)
		self.display_file: str = os.path.join(self.tdir, self.DISPLAY_FILE)

		self.log.info(f"Created the kiosk service in {self.tdir} with a delay of {self.delay_seconds} using file {self.link}")

		self.display_task = None

	# async def loop(self):
	def loop(self):
		self.log.info(f"Starting main loop")

		while True:
			self.log.info(f"Checking if version file {self.link} changed")

			# Download file containing the link of the published presentation
			self.version_drive.download(self.version_file)

			# Get the link of the presentation
			link_presentation = self.get_version_from_libreoffice_doc(self.version_file)
			self.log.debug(f"Got presentation link {link_presentation}")

			if link_presentation != self.last_link:
				self.log.info(f"Found a new version: {link_presentation}")

				# Download the new document
				presentation_drive = DriveFileDownloader(link_presentation)
				presentation_drive.download(self.presentation_file)

				self.convert_presentation(self.CONVERT_TYPE)

				self.run_presentation()
				# if self.last_link is not None:
				# 	self.display_task.cancel()

				# self.display_task = asyncio.create_task(run_presentation)

			# await asyncio.sleep(delay)
			time.sleep(self.delay_seconds)

	def get_version_from_libreoffice_doc(self, doc: str) -> str:
		self.log.debug(f"Processing libreoffice file {doc}")
		document = opendocument.load(doc)
		return str(document.body)

	def convert_presentation(self, convert_type: str):
		self.log.debug(f"Converting {self.presentation_file} to {self.display_file}")

		command = [
			"soffice",
			"--headless",
			"--convert-to",
			convert_type,
			self.presentation_file,
		]
		execute_command(command)

	# async def run_presentation(self):
	def run_presentation(self):
		""" Run with impressive """
		self.log.debug(f"Running the presentation {self.display_file}")

		# command = [
		# 	".",
		# 	os.path.join(self.venv, "bin/activate"),
		# 	"&&"
		# 	"impressive",
		# 	"--auto", "15",
		# 	"--fullscreen",
		# 	"--page",
		# 	"--progress",
		# 	"--wrap",
		# 	"--nocursor",
		# 	"--nologo",
		# 	"--noclicks",
		# 	"--nooverview",
		# 	'--clock',
		# 	self.display_file,
		# ]
		# execute_command(command)


def execute_command(cmd: List[str]):
	result: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True)
	if result.returncode != 0:
		log = f"{result.stdout=}{result.stderr=}"
		raise ValueError(f"Command {cmd} failed: {log}")
