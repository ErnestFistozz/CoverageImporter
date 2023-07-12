import requests, json
from json import JSONEncoder
BASE_URL = "https://coveralls.io/github/ErnestFistozz/codecov-coveralls.json?page=1&branch=main"

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace

res = requests.get(BASE_URL).json()

class Build:
    def __init__(self, repo_name, branch, url, badge_url, date, commit_msg, author_name,
                email, commit_id, coverage_delta, overall_coverage, covered_lines,
                missed_lines, relevant_lines, covered_branches, missed_branches, relevant_branches) -> None:
        self.repo_name = repo_name
        self.branch = branch
        self.url = url
        self.badge_url = badge_url
        self.created_at = date
        self.commit_message = commit_msg
        self.committer_name = author_name
        self.committer_email = email
        self.commit_sha = commit_id
        self.coverage_change = coverage_delta
        self.covered_percent = overall_coverage
        self.covered_lines = covered_lines
        self.missed_lines = missed_lines
        self.relevant_lines = relevant_lines
        self.covered_branches = covered_branches
        self.missed_branches = missed_branches
        self.relevant_branches = relevant_branches

    @staticmethod
    def from_json(cls, JSONdata):
        return Build( JSONdata['repo_name'], JSONdata['branch'], JSONdata['url'], JSONdata['badge_url'], JSONdata['created_at'],
            JSONdata['commit_message'], JSONdata['committer_name'], JSONdata['committer_email'], JSONdata['commit_sha'], JSONdata['coverage_change'],
            JSONdata['covered_percent'], JSONdata['covered_lines'], JSONdata['missed_lines'],
            JSONdata['relevant_lines'], JSONdata['covered_branches'], JSONdata['missed_branches'], JSONdata['relevant_branches'])


class BuildList:
    def __init__(self, page: int, pages: int, total: int, builds: list[Build]) -> None:
        self.page = page
        self.pages = pages 
        self.total = total
        self.builds = builds


def from_json(cls, JSONdata):
    return BuildList(
             JSONdata['page'], JSONdata['pages'], JSONdata['total'],
            json.loads( json.loads(JSONdata['builds']), object_hook=lambda d: Namespace(**d)) 
         )
    

build = json.loads(res, object_hook=from_json)
print(build)
