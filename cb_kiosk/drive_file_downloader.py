import re
import sys
import requests
import logging

import requests_debugger

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class DriveFileDownloader:
    URL = "https://docs.google.com/uc?export=download"
    CHUNK_SIZE = 32768

    def __init__(self, uid: str):
        """
        id: Unique identifier of the google document
        destination: Where to save the file downlaod
        """
        self.log = logger
        self.uid = self.get_unique_if(uid)

    def get_unique_if(self, uid: str) -> str:
        self.log.debug(f"Resolving UID for {uid}")

        if uid.startswith("http"):
            # The string is of the form https://docs.google.com/presentation/d/<UID>/edit?usp=sh<garbage>
            # We capture the ID which is between the /d/ marker and the /edit marker
            result = re.search('.*d/(.*)/edit', uid)

            if result is None:
                result = re.search('.*d/(.*)/view', uid)
                
            if result is not None:
                uid = result.group(1)
                self.log.debug(f"Resolved to {uid}")
            else:
                raise ValueError(f"Cannot find the UID from {uid}")

        return uid


    def get_confirm_token(self, response):
        self.log.debug(f"Cookies: {response.cookies.items()}")
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(self, response, destination):
        with open(destination, "wb") as f:
            for chunk in response.iter_content(self.CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    def download(self, destination: str):
        self.log.debug(f"Downloading {self.uid} to {destination}")
        session = requests.Session()

        params = {
            'id' : self.uid,
            'confirm': 1
        }
        response = session.get(self.URL, params = params, stream = True)
        token = self.get_confirm_token(response)

        if token:
            params = {
                'id' : self.uid,
                'confirm' : token
            }
            response = session.get(URL, params = params, stream = True)
        else:
            self.log.error(f" req url: {response.request.url}")
            self.log.error(f" req body: {response.request.body}")
            self.log.error(f" req headers: {response.request.headers}")

            self.log.error(f" rsp headers: {response.headers}")
            self.log.error(f" rsp json: {response.json}")
            self.log.error(f" rsp cookie: {response.cookies}")

            raise ValueError(f'Could not get token from response: {response.status_code}')

        self.save_response_content(response, destination)

if __name__ == "__main__":
    print(f"argv: {sys.argv}")
    file_id = sys.argv[1]
    destination = sys.argv[2]

    DriveFileDownloader(file_id, destination).download()
