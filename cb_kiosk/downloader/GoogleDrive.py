import re
import sys
import requests
import json

# from requests_toolbelt.utils import dump
# import requests_debugger
# from requests_toolbelt.cookies.forgetful import ForgetfulCookieJar

from downloader.Downloader import Downloader, DownloadError


'''
In case get does nto seolve, disable ipv6:
sudo sysctl net.ipv6.conf.all.disable_ipv6=1
'''

def pretty_print_POST(req) -> str:
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    return '{}\n{}\r\n{}\r\n\r\n{}\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
        '------------END------------',
    )

class DriveError(DownloadError):
    pass

class GoogleDrive(Downloader):
    DRIVE_PATH = "https://docs.google.com/"
    URL = "https://drive.google.com/uc"
    CHUNK_SIZE = 32768

    def __init__(self, http_share_link: str, log = None):
        """
        id: Unique identifier of the google document
        destination: Where to save the file downlaod
        """
        super().__init__(http_share_link, log=log)

        if not http_share_link.startswith(self.DRIVE_PATH):
            raise ValueError(f"The link {http_share_link} is not a google drive link")

        self.export_type : str = "pptx"
        self.uid : str
        self.share_link : str
        self.uid, self.share_link = self.get_link_data(self.res)

    def get_link_data(self, link):
        # We replace the /view or /edit with /export
        m1 = re.search(r'(.*d/(.*))/.*', link)

        export_link = ""

        if m1 is not None:
            uid = m1.group(2)
            exp_link = m1.group(1)
        else:
            raise ValueError(f"Could not get the data from link {link}")

        exp_link += f"/export/{self.export_type}"

        self.log.debug(f"{uid=}")
        self.log.debug(f"{exp_link=}")

        return uid, exp_link

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
        self.log.debug(f'Saving to {destination}')
        with open(destination, "wb") as f:
            for chunk in response.iter_content(self.CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    def download(self, destination: str):
        self.log.debug(f"Downloading {self.uid} to {destination}")
        session = requests.Session()
        # session.cookies = ForgetfulCookieJar()

        params = {
            'export' : 'download',
            'id' : self.uid,
        }

        req = requests.Request('GET', self.URL, params = params)
        prepped = req.prepare()

        # self.log.debug(pretty_print_POST(prepped))

        try:
            response = session.get(self.URL, params = params)
        except requests.exceptions.HTTPError as e:
            raise DriveError(e)

#        self.log.debug(f"{response.headers=}")
#        self.log.debug(f"{response.json=}")
#        self.log.debug(f"{response.cookies=}")
        # self.log.debug(f"Content-Disposition {response.headers['Content-Disposition']}")
        # self.log.debug(f"Content-Type {response.headers['Content-Type']=}")

        # self.log.debug(f"content size = {len(response.content)}")
        self.log.debug(f"{response.status_code=} {type(response.status_code)=}")


        if response.status_code == 200:
            # We save the value
            self.save_response_content(response, destination)
            return
        elif response.status_code == 500:
 #           self.log.debug(dump.dump_all(response).decode('utf-8'))

            response2 = session.get(response.headers['location'])

            self.log.debug(f"{response2.headers=}")
            self.log.debug(f"{response2.json=}")
            self.log.debug(f"{response2.cookies=}")
            self.log.debug(f"{response.status_code=} {type(response.status_code)=}")

            # if not response.ok:
            #     raise ValueError(f"Failed to download document {response.status_code}: {response.reason}")

            self.save_response_content(response2, destination)

            return
        else:
            response.raise_for_status()

        # Download the document
        headers = {
            'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding' : 'gzip, deflate, br'
        }


if __name__ == "__main__":
    print(f"argv: {sys.argv}")
    file_id = sys.argv[1]
    destination = sys.argv[2]

    DriveFileDownloader(file_id, destination).download()
