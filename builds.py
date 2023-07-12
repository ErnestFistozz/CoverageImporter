from source_file import SourceFileList

BASE_URL = "https://coveralls.io/github/ErnestFistozz/codecov-coveralls.json?page=1&branch=main"

class Build:
    repo_name: str
    branch: str
    url: str
    badge_url: str
    created_at: str
    commit_message: str
    committer_name: str
    committer_email: str
    commit_sha: str
    coverage_change: float
    covered_percent: float
    covered_lines: int
    missed_lines: int
    relevant_lines: int
    covered_branches: int
    missed_branches: int
    relevant_branches: int
    source_file_list: SourceFileList

    # def __str__(self) -> str:
    #     return f"Build [url={self.url}, date={self.created_at}, repo_name={self.repo_name}, coverage_change={self.coverage_change}, coverage_percent={self.covered_percent}, commit_sha={self.commit_sha}]"
    
    # def __repr__(self) -> str:
    #     return f"Build [url={self.url}, date={self.created_at}, repo_name={self.repo_name}, coverage_change={self.coverage_change}, coverage_percent={self.covered_percent}, commit_sha={self.commit_sha}]";
    
    # def is_code_file(self, s: str , file_extensions: list[str]) -> bool:
    #     if s in file_extensions:
    #         return True
    #     return False

    # def append_sfl(self, sfl: SourceFileList) -> None: 
    #     if self.source_file_list: 
    #         self.source_file_list = sfl
    #     else:
    #         self.source_file_list.parsed_files.append(sfl.parsed_files)

class BuildList:
    page: int
    pages: int
    total: int
    builds: list[Build]

    # def non_empty_builds(self) -> list[Build]:
    #     ret = []
    #     for build in self.builds:
    #         if isinstance(build, Build):
    #             if build.source_file_list and build.source_file_list.parsed_files:
    #                 ret.append(build)
    #     return ret
    
    # def __str__(self) -> str:
    #     return f"BuildList [page={self.page}, pages={self.pages}, total={self.total}, builds={self.builds}]"
    
    # def __repr__(self) -> str:
    #     return f"BuildList [page={self.page}, pages={self.pages}, total={self.total}, builds={self.builds}]"

    # def summarize(self) -> str:
    #     nBuilds = 0
    #     nSourceFiles = 0
    #     for b in self.builds: 
    #         if b.source_file_list and b.source_file_list.parsed_files:
    #             nSourceFiles += len(b.source_file_list.parsed_files)
    #             nBuilds += 1
    #     return nBuilds + " builds fetched, " + nSourceFiles + " total source files coverage files fetched"
