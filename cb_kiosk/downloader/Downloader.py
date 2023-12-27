
import logging

logger = logging.getLogger(__name__)

class Downloader:

	def __init__(self, resource: str, log = logger):
		self.log : Logger = log
		self.res = resource

	def download(self, destination: str):
		'''
		Download a resource to the destination 
		'''
		pass

	def support_resource(resource: str) -> bool:
		pass

class DownloadError(Exception):
	pass
