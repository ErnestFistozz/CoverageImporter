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
            BUILD_URL = f"https://coveralls.io/github/{self.org}/{self.repo}.json?page=1{page}&branch={self.branch}"
            res = requests.get(BUILD_URL)
            if res.status_code != 200:
                 raise ValueError, KeyError, requests.RequestException
            else:
                 pass
        except (ValueError, KeyError, requests.RequestException):
                print('Error fetching coveralls builds')

    def fetch_source_file_info(self, b: Build, page: int) -> None:
        pass
    
    def fecth(url: str) -> any:
        pass



    def get_coverage_array( commit: str,   sf: SourceFile) -> None:
        pass