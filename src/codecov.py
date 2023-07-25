import requests
from .basecoverage import BaseCoverage

class CodeCovCoverage(BaseCoverage):

	def __init__(self, organisation: str, repository: str, branch: str = 'master') -> None:
		super().__init__(organisation, repository, branch)
	    
	def total_builds_pages(self) -> int:
		try:
			url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos/{self.repository}/commits?branch={self.branch}'
			res  = requests.get(url, verify=False)
			res.raise_for_status()
			return res.json()['total_pages']
		except (requests.RequestException, KeyError):
			return 0

	def collect_build_data(self) -> list:
		data = []
		builds_pages = self.total_builds_pages()
		if builds_pages != 0:
			for page in range(1, builds_pages + 1):
				try:
					url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos/{self.repository}/commits?branch={self.branch}&page={page}'
					res = requests.get(url, verify=False)
					res.raise_for_status()
					data.extend(   
						{
							'created_at': build['timestamp'],
							'commit_sha': build['commitid'],
							'covered_percent': build['totals']['coverage'],
							'branch': build['branch']
						} 
						for build in res.json()['results']
					)
				except Exception:
					continue
		return data
	
	def fetch_source_file_names(self, commit: str) -> list[str]:
		try:
			url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos/{self.repository}/report?sha={commit}&branch={self.branch}'
			res = requests.get(url, verify=False)
			res.raise_for_status()
			full_file_names = [ file['name'] for file in res.json()['files']]
			return full_file_names
		except (requests.RequestException, KeyError):
			return None
		
	def file_line_coverage_array(self, commit: str, filename: str) -> list:
		try:
			url = f'https://codecov.io/api/v2/gh/{self.organisation}/repos/{self.repository}/report?sha={commit}&branch={self.branch}'
			res = requests.get(url, verify=False)
			res.raise_for_status()
			data = [tuple(line_coverage) for file in res.json()['files'] if file['name'] == filename for line_coverage in file['line_coverage']]
			return data
		except (requests.RequestException, KeyError):
			return None

if __name__ == '__main__':
	print(__name__)