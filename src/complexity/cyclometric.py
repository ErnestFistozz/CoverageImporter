from pydriller import Repository
from src.basecoverage import BaseCoverage
import lizard

class CylometricComplexity(BaseCoverage):
    def __init__(self, organisation: str, repository: str, branch: str = 'master', language: str = 'java') ->None:
        super().__init__(organisation, repository, branch)
        self.language = language
        self.github_url = f'https://github.com/{self.organisation}/{self.repository}.git'
    
    def cyclometric_mapper(self, commit_hash: str):
        for commit in Repository(self.github_url, single = commit_hash).traverse_commits():
            for m in commit.modified_files:
                return
