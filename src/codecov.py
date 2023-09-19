import requests
from .basecoverage import BaseCoverage


class CodeCovCoverage(BaseCoverage):

    def __init__(self, organisation: str, repository: str) -> None:
        super().__init__(organisation, repository)

    def total_builds_pages(self) -> int:
        try:
            url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos/{self.repository}/commits'
            res = requests.get(url, verify=False)
            res.raise_for_status()
            return res.json()['total_pages']
        except Exception:
            return 0

    def collect_build_data(self) -> list:
        data = []
        builds_pages = self.total_builds_pages()
        if builds_pages != 0:
            for page in range(1, builds_pages + 1):
                try:
                    url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos/{self.repository}/commits?page={page}'
                    res = requests.get(url, verify=False)
                    res.raise_for_status()
                    data.extend(
                        {
                            'created_at': build['timestamp'],
                            'commit_sha': build['commitid'],
                            'covered_percent': round(build['totals']['coverage'], 3),
                            'branch': build['branch'],
                            'parent_commit_sha': build['parent']
                        }
                        for build in res.json()['results']
                    )
                except Exception:
                    continue
        return data

    def fetch_source_file_names(self, commit_report) -> list[str]:
        if commit_report:
            try:
                full_file_names = [file['name'].lower() for file in commit_report['files']]
                return full_file_names
            except Exception:  # Most likely exception is KeyError -> But all exceptions will be handled the same way
                return []
        return []

    def file_line_coverage_array(self, commit_report, filename: str) -> list:
        if commit_report:
            try:
                data = [tuple(line_coverage) for file in commit_report['files'] if
                        file['name'].lower() == filename.lower() for line_coverage in file['line_coverage']]
                return data
            except Exception:
                return []
        return []

    def computed_overall_coverage(self, commit_report) -> float:
        if commit_report:
            try:
                source_files = commit_report['files']
                executable_lines = covered_lines = 0
                for file in source_files:
                    for file_line_coverage in file['line_coverage']:
                        if file_line_coverage[1] == 0:
                            covered_lines += 1
                    executable_lines += len(file['line_coverage'])
                return round((covered_lines / executable_lines) * 100, 3)
            except Exception:
                return 0
        return 0

    # Method to fetch the commit report once --> introduced to remove multiple api calls to same endpoint
    def commit_report(self, commitId: str):
        try:
            url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos/{self.repository}/report?sha={commitId}'
            res = requests.get(url, verify=False)
            res.raise_for_status()
            if res.status_code != 200:
                raise Exception
            return res.json()
        except Exception:
            return {}  # returns an empty dictionary

    # method to fetch the patch returned from REST API
    def api_patch_coverage(self, commit_report) -> float:
        if commit_report:
            try:
                if not isinstance(commit_report['totals']['diff'], type(None)):
                    if isinstance(commit_report['totals']['diff'], list):
                        if not isinstance(commit_report['totals']['diff'][5], type(None)):
                            return float(commit_report['totals']['diff'][5])
            except Exception:
                return 0
        return 0


if __name__ == '__main__':
    print(__name__)
