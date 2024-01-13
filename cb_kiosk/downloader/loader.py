from downloader.GoogleDrive import GoogleDrive
from downloader.LocalFS import LocalFS

downloader_list = [
	GoogleDrive,
	LocalFS
]

def load(resource: str, log = None):
	obj = None
	for loader in downloader_list:
		try:
			obj = loader(resource, log=log)
			log.debug(f"using the downlaoder {loader}")
			return obj
		except ValueError as e:
			print(e)

	raise ValueError(f"Could not find a loader for [{resource}] in {str(downloader_list)}")
