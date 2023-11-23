import time

import requests
from src.basecoverage import BaseCoverage
import json
import urllib3
from src.helpers import Helpers

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CoverallsCoverage(BaseCoverage):
    def __init__(self, organisation: str, repository: str) -> None:
        super().__init__(organisation, repository)

    def total_builds_pages(self) -> int:
        print("TotalBuilds")
        url = f'https://coveralls.io/github/{self.organisation}/{self.repository}.json?page=1&per_page=10'
        wait_time = 600
        try:
            res = requests.get(url, verify=False)
            if res.status_code != 200:
                if res.status_code in [403, 429]:
                    time.sleep(wait_time)
                    res = requests.get(url, verify=False)
                else:
                    raise Exception
            return res.json()['pages']
        except Exception as e:
            Helpers.coverage_logger('coverallsTotalBuildsError', str(e))
            return 0

    def collect_builds_data(self) -> list:
        print("BuildData")
        data = []
        builds_pages = self.total_builds_pages()
        wait_time = 600
        if builds_pages != 0:
            for page in range(1, builds_pages + 1):
                url = f'https://coveralls.io/github/{self.organisation}/{self.repository}.json?page={page}&per_page=10'
                try:
                    res = requests.get(url, verify=False)
                    if res.status_code != 200:
                        if res.status_code in [403, 429]:
                            time.sleep(wait_time)
                            res = requests.get(url, verify=False)
                        else:
                            raise Exception
                    data.extend(
                        {
                            'created_at': build['created_at'],
                            'commit_sha': build['commit_sha'],
                            'covered_percent': round(build['covered_percent'], 3),
                            'branch': build['branch'],
                            'repository_name': build['repo_name']
                        }
                        for build in res.json()['builds']
                    )

                except Exception as e:
                    Helpers.coverage_logger('coverallsTotalDataError', str(e))
                    continue
                time.sleep(5)
        return data

    @staticmethod
    def fetch_source_files(commit_hash: str) -> list:
        print("sourceFiles")
        source_files = []
        file_url = f"https://coveralls.io/builds/{commit_hash}/source_files.json"
        wait_time = 600
        try:
            res = requests.get(file_url, verify=False)
            if res.status_code != 200:
                if res.status_code in [403, 429]:
                    time.sleep(wait_time)
                    res = requests.get(file_url, verify=False)
                else:
                    raise Exception
            total_pages = res.json()['total_pages']
            if total_pages > 1:
                for page in range(1, total_pages + 1):
                    page_url = f'{file_url}?&page={page}'
                    result = requests.get(page_url, verify=False)
                    try:
                        if result.status_code != 200:
                            if result.status_code in [403, 429]:
                                time.sleep(wait_time)
                                result = requests.get(page_url, verify=False)
                            else:
                                raise Exception
                        source_files.extend(file['name'] for file in json.loads(result['source_files']))
                    except Exception:
                        continue
                    time.sleep(5)
            else:
                source_files.extend(source_file['name'] for source_file in json.loads(res.json()['source_files']))
            return source_files
        except Exception as e:
            Helpers.coverage_logger('coverallSourceFilesListError', str(e))
            return []

    @staticmethod
    def source_coverage_array(commit: str, filename: str) -> list:
        url = f'https://coveralls.io/builds/{commit}/source.json?filename={filename}'
        wait_time = 600
        try:
            response = requests.get(url, verify=False)
            if response.status_code != 200:
                if response.status_code in [403, 429]:
                    time.sleep(wait_time)
                    response = requests.get(url, verify=False)
            return response.json()
        except Exception as e:
            Helpers.coverage_logger('coverallsFileCoverageArrayError', str(e))
            return []


if __name__ == '__main__':
    print(__name__)
