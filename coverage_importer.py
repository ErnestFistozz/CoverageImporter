from builds import Build, BuildList
from source_file import SourceFile, SourceFileList
import requests, json

class CoverageImporter:

    def __init__(self, organisation: str, repository: str, branch: str = 'master') -> None:
        self.org = organisation
        self.repo = repository
        self.branch = branch

    def fetch_builds(self, page: int) -> BuildList:
        try:
            url = f"https://coveralls.io/github/{self.org}/{self.repo}.json?page=1{page}&branch={self.branch}"
            res = requests.get(url)
            if res.status_code != 200:
                 raise ValueError, KeyError, requests.RequestException
            else:
                 pass
        except (ValueError, KeyError, requests.RequestException):
                print('Error fetching coveralls builds')

    def fetch_source_file_info(self, b: Build, page: int) -> None:
        try:
             url = f"https://coveralls.io/builds/{b.commit_sha}/source_files.json"
             res = requests.get(url)
             if res.status_code != 200:
                  raise ValueError, KeyError, requests.RequestException
             else:
                  pass
        except (ValueError, KeyError, requests.RequestException):
             pass
    
    def fecth(url: str) -> any:
        pass

    def get_coverage_array( commit: str,   sf: SourceFile) -> None:
        try:
             url = f"https://coveralls.io/builds/{commit}/source.json?filename={sf.name}"
             res = requests.get(url)
             if res.status_code != 200:
                  raise ValueError, KeyError, requests.RequestException
             else:
                  pass
        except (ValueError, KeyError, requests.RequestException):
             pass