import requests
from src.basecoverage import BaseCoverage
from src.helpers import Helpers
import time

class CodeCovCoverage(BaseCoverage):

    def __init__(self, organisation: str, repository: str) -> None:
        super().__init__(organisation, repository)

    def total_builds_pages(self) -> int:
        wait_time = 600
        try:
            url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos/{self.repository}/commits'
            res = requests.get(url, verify=False)
            if res.status_code != 200:
                if res.status_code in [403, 429]:
                    time.sleep(wait_time)
                    res = requests.get(url, verify=False)
                else:
                    raise Exception
            return res.json()['total_pages']
        except Exception as e:
            Helpers.coverage_logger('codecovTotalBuildsError', str(e))
            return 0

    def collect_build_data(self) -> list:
        data = []
        builds_pages = self.total_builds_pages()
        wait_time = 600
        if builds_pages != 0:
            for page in range(1, builds_pages + 1):
                try:
                    url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos/{self.repository}/commits?page={page}'
                    res = requests.get(url, verify=False)
                    if res.status_code != 200:
                        if res.status_code in [403, 429]:
                            time.sleep(wait_time)
                            res = requests.get(url, verify=False)
                        else:
                            raise Exception
                    data.extend(
                        {
                            'created_at': build['timestamp'],
                            'commit_sha': build['commitid'],
                            'covered_percent': round(build['totals']['coverage'], 3),
                            'branch': build['branch']
                        }
                        for build in res.json()['results']
                    )
                except Exception as e:
                    Helpers.coverage_logger('codecovBuildsDataError', str(e))
                    continue
                time.sleep(5)
        return data

    @staticmethod
    def fetch_source_file_names(commit_details: dict) -> list:
        if commit_details:
            try:
                files = commit_details['files']
                full_file_names = [file['name'].lower() for file in files]
                return full_file_names
            except Exception as e:  # Most likely exception is KeyError -> But all exceptions will be handled
                # the same way
                Helpers.coverage_logger('codecovSourceFilesError', str(e))
                return []
        return []

    @staticmethod
    def file_line_coverage_array(commit_details: dict, filename: str) -> list:
        if commit_details:
            try:
                data = [tuple(line_coverage) for file in commit_details['files'] if
                        file['name'].lower() == filename.lower() for line_coverage in file['line_coverage']]
                return data
            except Exception as e:
                Helpers.coverage_logger('codecovFileCoverageArray', str(e))
                return []
        return []

    @staticmethod
    def computed_overall_coverage(commit_details: dict) -> float:
        if commit_details:
            try:
                source_files = commit_details['files']
                executable_lines = covered_lines = 0
                for file in source_files:
                    for file_line_coverage in file['line_coverage']:
                        if file_line_coverage[1] == 0:
                            covered_lines += 1
                    executable_lines += len(file['line_coverage'])
                return round((covered_lines / executable_lines) * 100, 3)
            except Exception as e:
                Helpers.coverage_logger('codecovComputedOverallCoverageError', str(e))
                return 0
        return 0

    # Method to fetch the commit report once --> introduced to remove multiple api calls to same endpoint
    def commit_report(self, commitId: str):
        wait_time = 600
        try:
            url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos/{self.repository}/report?sha={commitId}'
            res = requests.get(url, verify=False)
            if res.status_code != 200:
                if res.status_code in [403, 429]:
                    time.sleep(wait_time)
                    res = requests.get(url, verify=False)
                else:
                    raise Exception
            return res.json()
        except Exception as e:
            Helpers.coverage_logger('codecovCommitReportError', str(e))
            return {}  # returns an empty dictionary

    # method to fetch the patch returned from REST API
    @staticmethod
    def api_patch_coverage(commit_details: dict) -> float:
        if commit_details:
            try:
                if not isinstance(commit_details['totals']['diff'], type(None)):
                    if isinstance(commit_details['totals']['diff'], list):
                        if not isinstance(commit_details['totals']['diff'][5], type(None)):
                            return float(commit_details['totals']['diff'][5])
            except (KeyError, TypeError) as e:
                Helpers.coverage_logger('codecovAPIPatchError', str(e))
                return 0
        return 0


if __name__ == '__main__':
    print(__name__)
