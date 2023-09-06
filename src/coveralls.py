import requests
from .basecoverage import BaseCoverage
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CoverallsCoverage(BaseCoverage):
    def __init__(self, organisation: str, repository: str, branch: str = 'master' ) -> None:
        super().__init__(organisation, repository, branch)

    def total_builds_pages(self) -> int:
        url = f'https://coveralls.io/github/{self.organisation}/{self.repository}.json?page=1&branch={self.branch}&per_page=10'
        try:
            res = requests.get(url, verify=False)
            res.raise_for_status()
            if res.status_code != 200:
                raise Exception
            return res.json()['pages']
        except Exception:
            return 0

    def collect_builds_data(self) -> list[dict]:
        data = []
        builds_pages = self.total_builds_pages()
        if builds_pages != 0:
            for page in range(1, builds_pages + 1):
                url = f'https://coveralls.io/github/{self.organisation}/{self.repository}.json?page={page}&branch={self.branch}&per_page=10'
                try:
                    res = requests.get(url, verify=False)
                    res.raise_for_status() 
                    if res.status_code != 200:
                        raise Exception
                    data.extend(   
                        {
                        'created_at': build['created_at'],
                        'commit_sha': build['commit_sha'],
                        'coverage_change': round(build['coverage_change'], 3),
                        'covered_percent': round(build['covered_percent'], 3),
                        'branch': build['branch']
                    } 
                        for build in res.json()['builds']
                    )
                except Exception:
                    continue
        return data
    
    def fetch_source_files(self, commit_hash: str) -> list[str]:
        source_files = []
        file_url = f"https://coveralls.io/builds/{commit_hash}/source_files.json"
        try:
            res = requests.get(file_url, verify=False)
            res.raise_for_status()
            if res.status_code != 200:
                raise Exception
            total_pages = res.json()['total_pages']
            if total_pages > 1:
                for page in range(1, total_pages + 1):
                    page_url = f'{file_url}?&page={page}'
                    result = requests.get(page_url, verify=False)
                    result.raise_for_status()
                    try:
                        if result.status_code != 200:
                            raise Exception
                        source_files.extend( file['name'] for file in json.loads(result['source_files']) )
                    except Exception:
                        continue
            else:
                source_files.extend( source_file['name'] for source_file in json.loads(res.json()['source_files']) )
            return source_files
        except Exception:
            return []
    
    def source_coverage_array(self, commit: str, filename: str) -> list:
        url = f'https://coveralls.io/builds/{commit}/source.json?filename={filename}'
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            if response.status_code != 200:
                raise Exception
            return response.json()
        except Exception:
            return []
                    
if __name__ == '__main__':
    print(__name__)