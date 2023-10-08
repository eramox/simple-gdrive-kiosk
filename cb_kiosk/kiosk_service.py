import glob
import logging
import os
import subprocess
import tempfile
import time
from typing import List
import shutil
import http.server
import threading

from docx import Document

from drive_file_downloader import DriveFileDownloader, DriveError
from SlideshowWriter import SlideshowWriter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def informed_delay(seconds: int, reason: str, logger: logging.Logger = logger) -> None:
	logger.info(f"Delay {seconds} seconds: {reason}")
	time.sleep(seconds)

class KioskService:
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
		self.version_drive: DriveFileDownloader = DriveFileDownloader(share_link_published_version, logger=self.log)
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
		self.has_drive_access = True

		self.link_presentation = None

		self.httpd = self.create_server()

	def check_for_update(self) -> bool:
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

	def download_presentation(self) -> None:
		# Download the new document
		presentation_drive = DriveFileDownloader(self.link_presentation, logger=self.log)
		presentation_drive.download(self.presentation_file)

	# async def loop(self):
	def loop(self):
		self.log.info(f"Starting main loop")

		while True:
			if not self.has_drive_access:
				informed_delay(self.delay_drive_m * 60, "Waiting for drive access to be resolved", logger=self.log)

			try:
				# if self.check_for_update():
					# self.download_presentation()

				if True:
					self.log.info(f"Post processing the file {self.presentation_file}")

					images = self.convert_presentation()

					self.prepare_slideshow(images)

					self.show_slideshow()
			except DriveError as e:
				self.has_drive_access = False
				self.log.error(f"Lost access to google drive: {e}")

			# await asyncio.sleep(delay)
			informed_delay(self.delay_loop_s, "Wait until next occurence of the loop", logger=self.log)

	def get_lines_from_docx(self, doc: str) -> [str]:
		self.log.debug(f"Processing docx file {doc}")

		all_text = []

		document = Document(doc)

		for i, p in enumerate(document.paragraphs):
			text = p.text
			self.log.debug(f"{i}: {text}")
			all_text.append(text)

		return all_text

	def filter_lines(self, lines: [str]) -> str:
		text = None

		# Return the first line not blank
		for l in lines:
			if l != '':
				text = l
				break

		return text

	def convert_presentation_to_pdf(self, presentation: str) -> str:
		conv_pdf_dir = os.path.join(self.CONVERT_OUTDIR, "conv_pdf")
		shutil.rmtree(conv_pdf_dir, ignore_errors=True)
		os.mkdir(conv_pdf_dir)
		basename = os.path.basename(presentation)
		file_wo_ext = basename[:-4]
		ext = "pdf"

		cmd = [
			"soffice",
			"--headless",
			"--convert-to",
			ext,
			"--outdir",
			conv_pdf_dir,
			presentation,
		]

		self.execute_command(cmd)

		outfile = f"{conv_pdf_dir}/{file_wo_ext}.{ext}"

		if not os.path.isfile(outfile):
			raise FileNotFoundError(f"Conversion of {presentation} to pdf {outfile} failed")
		else:
			self.log.debug(f"Generated {outfile}")

		return outfile

	def split_pdf_by_page(self, pdf) -> [str]:
		split_pdf_dir = os.path.join(self.CONVERT_OUTDIR, "split_pdf")
		shutil.rmtree(split_pdf_dir, ignore_errors=True)
		os.mkdir(split_pdf_dir)
		basename = os.path.basename(pdf)
		file_wo_ext = basename[:-4]

		cmd = [
			"./pdfsplit.sh",
			f"{pdf}",
			"1",
			f"{split_pdf_dir}/",
		]

		self.execute_command(cmd)

		outfiles = list(glob.glob(f"{split_pdf_dir}/{file_wo_ext}_*.pdf"))
		nb_outfiles = len(list(glob.glob(f"{split_pdf_dir}/{file_wo_ext}_*.pdf")))

		if nb_outfiles == 0:
			raise FileNotFoundError(f"Split of {pdf} into pages failed")
		else:
			outfiles = [ f"{split_pdf_dir}/{file_wo_ext}_{i}.pdf" for i, _ in enumerate(outfiles) ]
			self.log.debug(f"Generated {outfiles}")

		return outfiles

	def convert_pdf_to_jpeg(self, pdfs: [str]) -> [str]:
		conv_jpeg_dir = os.path.join(self.CONVERT_OUTDIR, "conv_jpeg")
		shutil.rmtree(conv_jpeg_dir, ignore_errors=True)
		os.mkdir(conv_jpeg_dir)

		images = []

		for pdf in pdfs:
			basename = os.path.basename(pdf)
			file_wo_ext = basename[:-4]
			ext = "jpeg"

			cmd = [
				"soffice",
				"--headless",
				"--convert-to",
				ext,
				"--outdir",
				conv_jpeg_dir,
				pdf,
			]

			self.execute_command(cmd)

			outfile = f"{conv_jpeg_dir}/{file_wo_ext}.{ext}" 

			if not os.path.isfile(outfile):
				raise FileNotFoundError(f"Conversion of {presentation} to jpeg {outfile} failed")
			else:
				images.append(outfile)
				self.log.debug(f"Generated {outfile}")

		return images

	def convert_presentation(self) -> [str]:
		self.log.info(f"Converting {self.presentation_file}")

		shutil.rmtree(self.CONVERT_OUTDIR, ignore_errors=True)
		os.mkdir(self.CONVERT_OUTDIR)

		pdf = self.convert_presentation_to_pdf(self.presentation_file)
		self.log.debug(f"{pdf=}")

		pdfs = self.split_pdf_by_page(pdf)
		self.log.debug(f"{pdfs=}")

		images = self.convert_pdf_to_jpeg(pdfs)

		self.log.debug(f"{images=}")

		self.log.info(f"Conversion done")

		return images

	def execute_command(self, cmd: List[str], env = None):
		self.log.info(f"Executing {cmd}")
		result: subprocess.CompletedProcess = subprocess.run(cmd, capture_output=True, env=env)

		if result.returncode != 0:
			log = f"\n{result.stdout=}\n{result.stderr=}"
			agreg = " ".join(w for w in cmd)
			raise ValueError(f"Command [{agreg}], failed: {log}")
		else:
			self.log.debug(f"{result.stdout=}")

		self.log.info(f"Command succeeded")


	def prepare_slideshow(self, images):
		web_dir = self.WEBSERVER_DIR

		# Copy the files to the dir
		for f in images:
			shutil.copy(f, web_dir)

		# Write the script for the server
		timings = [ self.DEFAULT_TIMEOUT ] * len(images)

		index_file = os.path.join(web_dir, "index.html")
		SlideshowWriter(images, timings).write(index_file)

	def show_slideshow(self):
		cmd = [
			"firefox",
			"--kiosk",
			"-private-window",
			f"localhost:{self.WEBSERVER_PORT}/index.html"
		]

		self.execute_command(cmd)

	def create_server(self):
		web_dir = self.WEBSERVER_DIR

		os.makedirs(web_dir, exist_ok=True)

		class Handler(http.server.SimpleHTTPRequestHandler):
		    def __init__(self, *args, **kwargs):
		        super().__init__(*args, directory=web_dir, **kwargs)

		_ , addr = http.server._get_best_family(None, self.WEBSERVER_PORT)
		serv = http.server.HTTPServer(addr, Handler)

		self.log.info(f"Created the server {serv}")

		return serv

	def __start_server(self):
		self.httpd.serve_forever()

	def start_server(self):
		self.log.debug(f"Starting server {self.httpd}")
		# thread.start_new_thread(self.__start_server(), () )
		self.server_thread = threading.Thread(target=self.__start_server)
		self.server_thread.start()
		self.log.info(f"Server {self.httpd} started")

	def stop_server(self):
		self.log.debug(f"Stopping server {self.httpd}")
		self.httpd.shutdown()
		self.server_thread._stop()
		self.log.info(f"Server {self.httpd} stopped")

