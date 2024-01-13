import re
import sys
import requests
import json
import pathlib

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

    def save_response_content(self, response, destination):
        self.log.debug(f'Saving to {destination}')
        with open(destination, "wb") as f:
            for chunk in response.iter_content(self.CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)



    def download(self, destination: str):
        self.log.debug(f"Downloading {self.uid} to {destination}")

        extension = pathlib.Path(destination).suffix

        params = {
            'export' : 'download',
            'id' : self.uid,
        }

        def callback_response(response):
            self.save_response_content(response, destination)

        with requests.Session() as session:
            req = requests.Request('GET', self.URL, params = params)
            process_req(session, req, callback_response, self.log)

    def download_presentation(self, destination: str):
        self.log.debug(f"Downloading presentation {self.uid} to {destination}")

        url = "https://docs.google.com/feeds/download/presentations/Export"

        extension = pathlib.Path(destination).suffix[1:]

        params = {
            'id' : self.uid,
            'format' : extension,
        }

        def callback_response(response):
            self.save_response_content(response, destination)

        with requests.Session() as session:
            req = requests.Request('GET', url, params = params)
            process_req(session, req, callback_response, self.log)

def process_req(session, req, callback_response, log):
    prepped = req.prepare()

    log.debug(pretty_print_POST(prepped))

    try:
        response = session.send(prepped)
    except requests.exceptions.HTTPError as e:
        raise DriveError(e)

#        self.log.debug(f"{response.headers=}")
#        self.log.debug(f"{response.json=}")
#        self.log.debug(f"{response.cookies=}")
    # self.log.debug(f"Content-Disposition {response.headers['Content-Disposition']}")
    # self.log.debug(f"Content-Type {response.headers['Content-Type']=}")

    # self.log.debug(f"content size = {len(response.content)}")
    log.debug(f"{response.status_code=} {type(response.status_code)=}")


    if response.status_code == 200:
        # We save the value
        callback_response(response)
        return
    elif response.status_code == 500:
#           self.log.debug(dump.dump_all(response).decode('utf-8'))

        response2 = session.get(response.headers['location'])

        log.debug(f"{response2.headers=}")
        log.debug(f"{response2.json=}")
        log.debug(f"{response2.cookies=}")
        log.debug(f"{response.status_code=} {type(response.status_code)=}")

        return
    else:
        response.raise_for_status()

if __name__ == "__main__":
    print(f"argv: {sys.argv}")
    file_id = sys.argv[1]
    destination = sys.argv[2]

    DriveFileDownloader(file_id, destination).download()
