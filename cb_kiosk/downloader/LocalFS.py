import os
import shutil

from downloader.Downloader import Downloader

class LocalFS(Downloader):

	def __init__(self, fs_path: str, log = None):
		super().__init__(fs_path, log=log)

		if not os.path.isfile(fs_path):
			raise ValueError(f"{fs_path} is not a file in the local fs")

	def download(self, destination: str):
		shutil.copyfile(self.res, destination)
