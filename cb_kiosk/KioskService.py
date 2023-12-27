import logging
import os
import tempfile
import shutil

from docx import Document

from downloader.Downloader import Downloader, DownloadError
from downloader.loader import load as load_downloader
from SlideshowWriter import SlideshowWriter
from util import execute_command, background_command, informed_delay
from converter.Converter import Converter, Data
from converter.PPTtoPDF import PPTtoPDF
from converter.PDFtoPDFS import PDFtoPDFS
from converter.PDFtoJPEG import PDFtoJPEG
from DisplayServer import DisplayServer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class KioskService:
	'''
	Based on a version file containing the presentation to be displayed,
	the service will make the presentation displayed, checking regularly for updates
	'''
	VERSION_FILE = "tmp_file.docx"
	PRESENTATION_FILE = "tmp_presentation.ppt"
	CONVERT_OUTDIR = "convert"
	WEBSERVER_DIR = "webserver"
	DISPLAY_FILE = "presentation.pdf"
	WEBSERVER_PORT = 8000
	DEFAULT_TIMEOUT = 2000

	def __init__(self, share_link_published_version: str, delay_loop_s: int = 10, logger=logger):
		""" Link to the file containing the share link of the presentation to use """
		self.log = logger

		# Variables related to the links
		self.link: str = share_link_published_version
		self.version_drive: Downloader = load_downloader(share_link_published_version, log = self.log)
		self.last_link: str = ""

		self.delay_loop_s: int = delay_loop_s
		self.delay_drive_m: int = 30

		# Create a temporary directory to store files downloaded
		# self.tdir = tempfile.TemporaryDirectory().name
		self.tdir = os.getcwd()

		self.version_file: str = os.path.join(self.tdir, self.VERSION_FILE)
		self.presentation_file: str = os.path.join(self.tdir, self.PRESENTATION_FILE)
		self.display_file: str = os.path.join(self.tdir, self.DISPLAY_FILE)

		self.log.info(f"Created the kiosk service in {self.tdir} with a delay of {self.delay_loop_s} using file {self.link}")

		self.display_task = None

		self.link_presentation = None

		self.httpd = None

		self.wd = os.getcwd()

		self.slideshow_pid = None

	# def __del__(self):
	# 	self.stop()

	def init(self):
		self.log.info(f"Init the service")

		httpd = DisplayServer(self.WEBSERVER_DIR, self.WEBSERVER_PORT, log=self.log)
		httpd.start_server()
		self.httpd = httpd

	def stop(self):
		pass
	# 	self.log.info(f"Stopping the service")

	# 	if self.httpd is not None:
	# 		self.httpd.stop_server()

	def check_for_update(self) -> bool:
		'''
		Check for updates by checking if the content of the version file changed
		'''
		self.log.info(f"Checking if version file {self.link} changed")

		# Download file containing the link of the published presentation
		self.version_drive.download(self.version_file)

		# Get the link of the presentation
		link_presentation = self.filter_lines(self.get_lines_from_docx(self.version_file))
		self.log.debug(f"Got presentation link {link_presentation}")

		if link_presentation != self.link_presentation:
			self.log.info(f"Found a new version: {link_presentation}")
			self.link_presentation = link_presentation
			return True

		return False

	def has_update(self) -> bool:
		return self.check_for_update()

	def download_presentation(self) -> None:
		'''
		Download the presentation
		'''
		# Download the new document
		presentation_drive: Downloader = load_downloader(self.link_presentation, log = self.log)
		presentation_drive.download(self.presentation_file)

	# async def loop(self):
	def loop(self):
		'''
		Main loop doing:
			- Download the presentation
			- convert the presentation to images
			- Prepare the slides to be discplayed
			- Display the slides
		'''
		self.log.info(f"Starting main loop")

		version_file_not_accessible = False

		while True:
			if version_file_not_accessible
				informed_delay(self.delay_drive_m * 60, "Waiting for drive access to be resolved", logger=self.log)

			try:
				if self.has_update():
					self.download_presentation()
					version_file_not_accessible = False

					self.log.info(f"Post processing the file {self.presentation_file}")

					images = self.convert_presentation()

					self.prepare_slideshow(images)

					self.stop_slideshow()
					self.show_slideshow()
			except DownloadError as e:
				version_file_not_accessible = True
				self.log.error(f"Lost access to google drive: {e}")

			# await asyncio.sleep(delay)
			informed_delay(self.delay_loop_s, "Wait until next occurence of the loop", logger=self.log)

	def get_lines_from_docx(self, doc: str) -> [str]:
		'''
		Read from a docx document
		'''
		self.log.debug(f"Processing docx file {doc}")

		all_text = []

		document = Document(doc)

		for i, p in enumerate(document.paragraphs):
			text = p.text
			self.log.debug(f"{i}: {text}")
			all_text.append(text)

		return all_text

	def filter_lines(self, lines: [str]) -> str:
		'''
		Return the first line which is not blank
		'''
		text = None

		# Return the first line not blank
		for l in lines:
			if l != '':
				text = l
				break

		return text

	def convert_presentation(self) -> [str]:
		'''
		Convert the presentation to images
		'''
		self.log.info(f"Converting {self.presentation_file}")

		class presentation_converter(Converter):
			def convert_one(self, data: Data) -> [Data]:

				ppt_to_pdf = PPTtoPDF(self.wd, log=self.log)
				pdf = ppt_to_pdf.convert([data])
				self.log.debug(f"{pdf=}")

				pdf_to_pdfs = PDFtoPDFS(self.wd, log=self.log)
				pdfs = pdf_to_pdfs.convert(pdf)
				self.log.debug(f"{pdfs=}")

				pdf_to_jpegs = PDFtoJPEG(self.wd, log=self.log)
				images = pdf_to_jpegs.convert(pdfs)

				return images

		convert_dir = os.path.join(self.wd, self.CONVERT_OUTDIR)

		pres_converter = presentation_converter(convert_dir, log=self.log)
		data_images = pres_converter.convert([Data(self.presentation_file)])

		images = [ str(elm) for elm in data_images]

		self.log.debug(f"{images=}")

		self.log.info(f"Conversion done")

		return images


	def prepare_slideshow(self, images):
		'''
		Write a webpage to display the slides
		'''
		web_dir = self.WEBSERVER_DIR

		# Copy the files to the dir
		for f in images:
			shutil.copy(f, web_dir)

		# Write the script for the server
		timings = [ self.DEFAULT_TIMEOUT ] * len(images)

		index_file = os.path.join(web_dir, "index.html")
		SlideshowWriter(images, timings).write(index_file)

	def show_slideshow(self):
		'''
		Display the slides
		'''
		cmd = [
			"firefox",
			"--kiosk",
			"-private-window",
			f"localhost:{self.WEBSERVER_PORT}/index.html",
		]

		self.slideshow_pid = background_command(cmd, log=self.log)
		self.log.debug(f"{self.slideshow_pid=}")

	def stop_slideshow(self):
		if self.slideshow_pid is None:
			return

		'''
		Stop the disply of slides
		'''
		# cmd = [
		# 	"ps", "-ux", 
		# 	"|", "grep", "firefox",
		# 	"|", "grep", "kiosk",
		# 	"|", "awk", "'{print $2}'",
		# 	"|", "xargs", "kill", "-9"
		# ]
		cmd = [
			"kill", "-9", str(self.slideshow_pid)
		]

		execute_command(cmd, log=self.log)
