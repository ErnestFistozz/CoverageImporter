from .codecov import CodeCovCoverage
from .coveralls import CoverallsCoverage
from pydriller import Repository
from .helpers import Helpers
from .patch_extracts import PatchExtracts
from crap_metric.commit_crap import CrapMetric

class CoverageImporter:

    def coveralls_data(self, coveralls: CoverallsCoverage, helpers: Helpers):
        git_url = f'https://github.com/{coveralls.org()}/{coveralls.repo()}.git'
        builds = coveralls.collect_builds_data()
        
        for build in builds:
            try:
                for commit in Repository(git_url, single = build['commit_sha']).traverse_commits():
                    coveralls_commit_files = coveralls.fetch_source_files(commit.hash)
                    executable_lines = executed_lines = 0 
                    patch_extracts = PatchExtracts()
                    crap_metric = CrapMetric()

                    if not isinstance(coveralls_commit_files, type(None)) and len(coveralls_commit_files) != 0:
                        for m in commit.modified_files:
                            if helpers.index_finder(m.filename, coveralls_commit_files) != -1:
                                coveral_file_path = helpers.index_finder(m.filename, coveralls_commit_files)
                                coverage_array = coveralls.source_coverage_array( commit.hash,
                                                coveralls_commit_files[coveral_file_path])
                                if not isinstance(coverage_array, type(None)) and len(coverage_array) != 0:
                                    modified_lines  = [ line_number[0] for line_number in m.diff_parsed['added'] ]
                                    executable_lines += len([1 for line_number in modified_lines  if isinstance(coverage_array[line_number - 1], int)])
                                    executed_lines += len([1 for line_number in modified_lines  if isinstance(coverage_array[line_number - 1], int) and coverage_array[line_number - 1] > 0])
                                else:
                                    continue
                        patch_files = patch_extracts.patch_files(commit, coveralls_commit_files)
                        patch_size = patch_extracts.patch_sizes(commit, coveralls_commit_files)
                        commit_crappiness = crap_metric.commit_crap_metric(commit, (executed_lines/executable_lines)*100)
                    else:
                        continue
                    dmm_commit_size = commit.dmm_unit_size
                    dmm_commit_complexity = commit.dmm_unit_complexity
                    dmm_commit_interface = commit.dmm_unit_interface
                    delta_maintainibility_model = round((dmm_commit_size + dmm_commit_complexity + dmm_commit_interface)/3 , 3)
                try:
                    build['patch_coverage'] = round((executed_lines/executable_lines)*100, 3)
                    build['repository_name'] = f'{coveralls.org()}/{coveralls.repo()}'
                except ZeroDivisionError:
                    build['patch_coverage'] = 0.0
                    build['repository_name'] = f'{coveralls.org()}/{coveralls.repo()}'
                finally:
                    build.update(patch_files)
                    build.update(patch_size)
            except Exception:
                continue
        return builds
    
    def codecov_data(self,  codecov: CodeCovCoverage, helpers: Helpers):
        git_url = f'https://github.com/{codecov.org()}/{codecov.repo()}.git'
        builds = codecov.collect_build_data()
        for build in builds:
            try:
                for commit in Repository(git_url, single = build['commit_sha']).traverse_commits():
                    codecov_commit_files = codecov.fetch_source_file_names(commit.hash)
                    executable_lines = executed_lines = 0 
                    overall_coverage = codecov.computed_overall_coverage(commit.hash)
                    patch_extracts = PatchExtracts()
                    crap_metric = CrapMetric()
                    if not isinstance(codecov_commit_files, type(None)) and len(codecov_commit_files) != 0:
                        for m in commit.modified_files:
                            if helpers.index_finder(m.filename, codecov_commit_files) != -1:
                                coveral_file_path = helpers.index_finder(m.filename, codecov_commit_files)
                                coverage_array = codecov.file_line_coverage_array( commit.hash,
                                                    codecov_commit_files[coveral_file_path])
                                if not isinstance(coverage_array, type(None)) and len(coverage_array) != 0:
                                    modified_lines  = [ line_number[0] for line_number in m.diff_parsed['added'] ]
                                    for line in modified_lines:
                                        for line_coverage_arr in coverage_array:
                                            if line == line_coverage_arr[0]:
                                                if  line_coverage_arr[1] == 0:
                                                    executed_lines += 1
                                                if line_coverage_arr[1] == 0 or line_coverage_arr[1] == 1 or line_coverage_arr[1] == 2:
                                                    executable_lines += 1
                                else:
                                    continue
                        patch_files = patch_extracts.patch_files(commit, codecov_commit_files)
                        patch_size = patch_extracts.patch_sizes(commit, codecov_commit_files)
                        commit_crappiness = crap_metric.commit_crap_metric(commit, (executed_lines/executable_lines)*100)
                    else:
                        continue
                    dmm_commit_size = commit.dmm_unit_size
                    dmm_commit_complexity = commit.dmm_unit_complexity
                    dmm_commit_interface = commit.dmm_unit_interface
                    delta_maintainibility_model = round((dmm_commit_size + dmm_commit_complexity + dmm_commit_interface)/3 , 3)
                try:
                    build['patch_coverage'] = round((executed_lines/executable_lines)*100, 3)
                    build['repository_name'] = f'{codecov.org()}/{codecov.repo()}'
                    build['computed_coverage'] = overall_coverage
                except ZeroDivisionError:
                    build['patch_coverage'] = 0.0
                    build['computed_coverage'] = overall_coverage
                    build['repository_name'] = f'{codecov.org()}/{codecov.repo()}'
                finally:
                    build.update(patch_files)
                    build.update(patch_size)
            except Exception:
                continue
        return builds

if __name__ == '__main__':
    print(__name__)