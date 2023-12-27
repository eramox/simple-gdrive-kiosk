from downloader.GoogleDrive import GoogleDrive
from downloader.LocalFS import LocalFS

downloader_list = [
	GoogleDrive,
	LocalFS
]

def load(resource: str, log = None):
	for loader in downloader_list:
		obj = None
		try:
			obj = loader(resource, log=log)
		except ValueError as e:
			print(e)

		log.debug(f"using the downlaoder {loader}")

	if obj is None:
		raise ValueError(f"Could not find a loader for [{resource}] in {str(downloader_list)}")

	return obj
