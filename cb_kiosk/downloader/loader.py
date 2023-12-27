from downloader.GoogleDrive import GoogleDrive

downloader_list = [
	GoogleDrive
]

def load(resource: str, log = None):
	for loader in downloader_list:
		obj = None
		try:
			obj = loader(resource, log=log)
		except ValueError as e:
			print(e)

	if obj is None:
		raise ValueError(f"Could not find a loader for [{resource}] in {str(downloader_list)}")

	return obj
