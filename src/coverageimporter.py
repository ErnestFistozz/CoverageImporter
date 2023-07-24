from .codecov import CodeCovCoverage
from .coveralls import CoverallsCoverage
from pydriller import Repository
from .helpers import Helpers

class CoverageImporter:

    def coveralls_data(self, coveralls: CoverallsCoverage, helpers: Helpers, lang_ext: str):
        git_url = f'https://github.com/{coveralls.org()}/{coveralls.repo()}.git'
        builds = coveralls.collect_builds_data()

        for build in builds:
            try:
                for commit in Repository(git_url, single = build['commit_sha']).traverse_commits():
                    coveralls_commit_files = coveralls.fetch_source_files(commit.hash)
                    executable_lines, executed_lines = 0 , 0
                    for m in commit.modified_files:
                        if m.filename.endswith(lang_ext) and helpers.index_finder(m.filename, coveralls_commit_files) != -1:
                            coveral_file_path = helpers.index_finder(m.filename, coveralls_commit_files)
                            coverage_array = coveralls.source_coverage_array( commit.hash,
                                            coveralls_commit_files[coveral_file_path])
                            modified_lines  = [ line_number[0] for line_number in m.diff_parsed['added'] ]
                            executable_lines += len([1 for line_number in modified_lines  if isinstance(coverage_array[line_number - 1], int)])
                            executed_lines += len([1 for line_number in modified_lines  if isinstance(coverage_array[line_number - 1], int) and coverage_array[line_number - 1] > 0])
                            #print("Commit hash: ", commit.hash, "File Changed:", m.filename)
                try:
                    #print("Executed Lines: ", executed_lines, "Executable Lines: ", executable_lines)
                    build['patch_coverage'] = round((executed_lines/executable_lines)*100, 3)
                    build['repository_name'] = f'{coveralls.org()}/{coveralls.repo()}'
                except ZeroDivisionError:
                    build['patch_coverage'] = 0.0
                    build['repository_name'] = f'{coveralls.org()}/{coveralls.repo()}'
                    continue
            except Exception:
                continue
        return builds
    
    def codecov_data(self,  codecov: CodeCovCoverage, helpers: Helpers, lang_ext: str):
        git_url = f'https://github.com/{codecov.org()}/{codecov.repo()}.git'
        builds = codecov.collect_build_data()
        for build in builds:
            try:
                for commit in Repository(git_url, single = build['commit_sha']).traverse_commits():
                    codecov_commit_files = codecov.fetch_source_file_names(commit.hash)
                    #print("files: ", codecov_commit_files)
                    executable_lines, executed_lines = 0 , 0
                    for m in commit.modified_files:
                        if m.filename.endswith(lang_ext) and helpers.index_finder(m.filename, codecov_commit_files) != -1:
                            coveral_file_path = helpers.index_finder(m.filename, codecov_commit_files)
                            coverage_array = codecov.file_line_coverage_array( commit.hash,
                                                codecov_commit_files[coveral_file_path])
                                
                            modified_lines  = [ line_number[0] for line_number in m.diff_parsed['added'] ]
                            for line in modified_lines:
                                for line_coverage_arr in coverage_array:
                                    if line == line_coverage_arr[0] and ( line_coverage_arr[1] == 0 or \
                                        line_coverage_arr[0] == 2):
                                            executed_lines += 1
                            #print("Commit hash: ", commit.hash, "File Changed:", m.filename)
                            executable_lines += len(coverage_array)
                try:
                    #print("Executed Lines: ", executed_lines, "Executable Lines: ", executable_lines)
                    build['patch_coverage'] = round((executed_lines/executable_lines)*100, 3)
                    build['repository_name'] = f'{codecov.org()}/{codecov.repo()}'
                except ZeroDivisionError:
                    build['patch_coverage'] = 0.0
                    build['repository_name'] = f'{codecov.org()}/{codecov.repo()}'
                    continue
            except Exception:
                continue
        return builds

if __name__ == '__main__':
    print(__name__)