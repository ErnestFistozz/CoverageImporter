import requests
import urllib3
urllib3.disable_warnings()
from pydriller import Repository

def computed_overall_coverage(commit: str) -> float:
  try:
    url = f'https://codecov.io/api/v2/gh/ErnestFistozz/repos/codecov-coveralls/report?sha={commit}&branch=main'
    res = requests.get(url, verify=False)
    res.raise_for_status()
    source_files = res.json()['files']
    executable_lines = executed_lines  = 0 
    for file in source_files:
      for file_line_coverage in file['line_coverage']:
        if file_line_coverage[1] == 0:
          executed_lines += 1
      executable_lines += len(file['line_coverage'])
    return (executed_lines / executable_lines)*100
  except (requests.RequestException, KeyError):
    return 0.0

def patch_coverage(commitId: str):
  url = f'https://github.com/ErnestFistozz/codecov-coveralls.git'
  executable_lines , executed_lines = 0, 0
  for commit in Repository(url, single = commitId).traverse_commits():
    for m in commit.modified_files:
      if m.filename.endswith('.py'):
        url = f'https://codecov.io/api/v2/gh/ErnestFistozz/repos/codecov-coveralls/report?sha={commitId}&branch=main'
        res = requests.get(url, verify=False)
        modified_lines  = [ line_number[0] for line_number in m.diff_parsed['added'] ]
        line_coverage_array = [line_coverage for file in res.json()['files'] if file['name'] == m.filename for line_coverage in file['line_coverage']]
        if line_coverage_array:
          for line in modified_lines:
            for line_cover in line_coverage_array:
              if line == line_cover[0]:
                if line_cover[1] == 0: # line_cover[1] != 1:
                  executed_lines += 1
                if line_cover[1] == 0 or line_cover[1] == 1 or line_cover[1] == 2:
                  executable_lines += 1
  return (executed_lines / executable_lines )*100
if __name__ == '__main__':
  commit_coverage = patch_coverage('129854f34036e5e01e75a0c8c06d72aa6d8c57f6')
  print('Patch Coverage = ', commit_coverage)
  # system_coverage = computed_overall_coverage('738ecc8ff5626b4797eff801fd61103b4487f06e')
  # print('Overall Coverage = ', system_coverage)